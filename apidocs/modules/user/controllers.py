from flask import (
        Blueprint, render_template, request, url_for, redirect, flash, g
)

from apidocs.helpers.pagination import Pagination
from apidocs.modules.access_control.manager import login_required, admin_required
from apidocs.modules.audit_log.controllers import audit_log
from apidocs.modules.user.models import UserModel
from apidocs.db.mongodb import MongoDb
from apidocs.helpers.utils import status_list, show_status_text, profile_list, show_profile_text

bp = Blueprint('user_controller', __name__)
db_users = MongoDb('users')

### METHODS ###

def get_active_users():
    return get_users_by_status('A', 1)

def get_users_by_status(status, page_num):
    filter = { 'status' : status }
    sort = [( 'name' , 1 )]

    db_users.set_page_num(page_num)
    return db_users.get_all_by_filter(filter, sort), db_users.count_total(filter)

def get_user_by_id(id):
    return db_users.get_by_id(id)

def get_user(email):
    filter = { 'email' : email }

    return db_users.get_one_by_filter(filter)

def update_user(user):
    result = db_users.update(user)

    return result

def delete_user(user_id):
    result = db_users.delete(user_id)

    return result

def register_new_user(firstname, lastname, email, password):
    model = UserModel(firstname + ' ' + lastname, email, password, 'P', 'U')
    user = model.get_model()
    
    insert_user(user)
    
    return True

def insert_user(user):
    result = db_users.insert(user)
    
    return result    

def user_update_validation(user, new_password, confirm_new_password):
    error = None

    #Em caso de troca de senha, atualiza o password do usuário, se não, confirma a senha automaticamente
    if not new_password is None and len(new_password) > 0:
        user['password'] = new_password
    else:
        confirm_new_password = user['password']

    if user is None:
        error = 'Usuário não encontrado em nossa base de dados.'
    elif user['name'] is None or not user['name']:
        error = 'Nome não informado.'
    elif user['email'] is None or not user['email']:
        error = 'E-mail não informado.'
    elif not user_update_email_validation(user):
        error = 'E-mail informado já está cadastrado para outro usuário.'        
    elif user['password'] is None or not user['password']:
        error = 'Senha não informada.'
    elif user['password'] != confirm_new_password:
        error = 'As senhas informadas são diferentes.'
    elif user['status'] is None or not user['status']:
        error = 'Situação não informada.'
    elif user['profile'] is None or not user['profile']:
        error = 'Perfil não informado.'                

    return error

def user_update_email_validation(updated_user):
    original_user = get_user_by_id(updated_user['_id'])
    
    #Verifica se o e-mail informado é igual ao e-mail original do usuário, se não, verifica se o e-email novo está em uso
    if updated_user['email'] != original_user['email']:
        users_in_db = get_user(updated_user['email'])

        if users_in_db:
            return False
    
    return True

def user_change(user_id, status):
    user = get_user_by_id(user_id)
    error = None

    if status == "P" or status == "D": #Aprovar ou Reativar
        user['status'] = "A"
        
        error = user_update_validation(user, None, None)

        if error is None:
            update_user(user)

            flash("Usuário {} com sucesso!".format('aprovado' if status == 'P' else 'reativado'), "success")
            
            return True

    elif status == "A": #Salvar Alterações
        new_name = request.form['new_name']
        new_email = request.form['new_email']
        new_password = request.form['new_password']
        confirm_new_password = request.form['confirm_new_password']
        selected_status = request.form['new_status']
        selected_profile = request.form['new_profile']

        user['name'] = new_name
        user['email'] = new_email
        user['status'] = selected_status
        user['profile'] = selected_profile
        
        error = user_update_validation(user, new_password, confirm_new_password)

        if error is None:
            update_user(user)

            flash("Usuário atualizado com sucesso!", "success")        
            
            return True
    
    else:
        error = "Operação Inválida (erro)"

    flash(error, 'error')
    return False

def profile_change(user_id, password):
    fullname = request.form['fullname']
    new_password = request.form['password']
    confirm_password = request.form['confirmpassword']

    user = get_user_by_id(user_id)
    user['name'] = fullname
    user['password'] = password

    error = user_update_validation(user, new_password, confirm_password)

    if error is None:
        update_user(user)

        audit_log("PERFIL ATUALIZADO")

        flash('Perfil atualizado com sucesso!', 'success')
    else:
        flash(error, 'error')


def user_db_remove(user_id):
    try:
        result = delete_user(user_id)
        flash("Usuário foi excluído com sucesso!", 'success')
        return True
    except Exception as ex:
        flash("Ocorreu um erro ao excluir o usuário: {}".format(ex), 'error')
        return False

### ROUTES ###

@bp.route("/user/list/<string:status>", defaults={'page_num' : 1})
@bp.route("/user/list/<string:status>/<int:page_num>")
@login_required
@admin_required
def user_list(status, page_num):
    users, total_users = get_users_by_status(status, page_num)
    pagination = Pagination(total_users, page_num)
    return render_template('user/list.html', pagination=pagination, users=users, status=status, show_status_text=show_status_text, show_profile_text=show_profile_text)

@bp.route("/user/detail/<string:id>/<string:status>")
@login_required
@admin_required
def user_detail(id, status):
    user = get_user_by_id(id)
    return render_template('user/detail.html', user=user, status=status, status_list=status_list, show_status_text=show_status_text, profile_list=profile_list, show_profile_text=show_profile_text)

@bp.route("/user/detail/save", methods=('POST',))
@login_required
@admin_required
def user_detail_save():
    user_id = request.form['user_id']
    status = request.form['status']

    if user_change(user_id, status):
        return redirect(url_for('user_controller.user_list', status="A"))
    else:
        return redirect(url_for('user_controller.user_detail', id=user_id, status=status))

@bp.route("/user/delete", methods=('POST',))
@login_required
@admin_required
def user_delete():
    user_id = request.form['user_to_delete']

    user_db_remove(user_id)
    return redirect(url_for('user_controller.user_list', status="A"))

@bp.route("/profile", methods=('GET', 'POST'))
@login_required
def profile():
    user_id = g.user['_id']

    if request.method == 'POST':
        actual_password = g.user['password']
        profile_change(user_id, actual_password)

    user = get_user_by_id(user_id)

    return render_template('user/profile.html', user=user, show_status_text=show_status_text, show_profile_text=show_profile_text)