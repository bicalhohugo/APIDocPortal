from flask import (
        Blueprint, render_template, redirect, url_for, flash, g, request
)
from apidocs.modules.access_control.manager import login_required, is_logged_user
from apidocs.helpers.utils import get_session_object, write_session_object, remove_all_session_info
from apidocs.modules.user.controllers import get_user, get_user_by_id
from apidocs.modules.audit_log.controllers import audit_log

bp = Blueprint('access_control_controller', __name__)

### METHODS ### 

def check_user_password(password_db, password_form):
    return password_form == password_db

def send_password_to(email):
    #TODO: implementar
    return True

def login():
    try:
        email = request.form['email']
        password = request.form['password']

        error = None
        user = get_user(email)

        if user is None:
            error = 'Usuário não existente e/ou não ativo.'
        elif not check_user_password(user['password'], password):
            error = 'As credenciais informadas são inválidas.'
        elif user['status'] != "A":
            error = 'Usuário aguardando aprovação e/ou desativado.'

        if error is None:
            remove_all_session_info()
            write_session_object('user_id', str(user['_id']))

            audit_log("LOGIN")

            return True
        
        else:
            flash(error, 'error')

            return False
    except Exception as ex:
        flash(f'Erro desconhecido ao efetuar o login: {ex}', 'info')        

def send_password():
    try:
        email = request.form['email']

        error = None
        user = get_user(email)

        if user is None:
            error = 'Usuário não existente e/ou não ativo.'

        if error is None:
            send_password_to(email)

            flash(f'E-mail enviado para {email} com sucesso! Verifique sua caixa de entrada, que enviamos um e-mail com as instruções para efetuar o reset da sua senha.', 'info')
            return True
        
        else:
            flash(error, 'error')

            return False
    except Exception as ex:
        flash(f'Erro desconhecido ao enviar a senha: {ex}', 'error')

def logout():
    try:
        audit_log("LOGOUT")
        remove_all_session_info()
        return True
    except Exception as ex:
        flash(f'Erro desconhecido ao efetuar o logout: {ex}', 'info')

@bp.before_app_request
def load_logged_in_user():
    user_id = get_session_object('user_id')

    if user_id:
        g.user = get_user_by_id(user_id)
    else:
        g.user = None
        
#### ROUTES ###

@bp.route("/login")
def access_control_login():
    #TODO: IMPLEMENTAR CRIPTOGRAFIA NAS SENHAS
    if is_logged_user():
        return redirect(url_for('base_controller.index'))
    else:
        return render_template('access_control/login.html')

@bp.route("/confirm_login", methods=('POST',))
def access_control_confirm_login():
    if login():
        return redirect(url_for('base_controller.index'))
    else:
        return redirect(url_for('access_control_controller.access_control_login'))

@bp.route("/denied")
def access_control_denied():
    return render_template('access_control/denied.html')

@bp.route("/forgot_password")
def access_control_forgot_password():
    return render_template('access_control/forgot-password.html')

@bp.route("/send_password", methods=('POST',))
def access_control_send_password():
    if send_password():
        return redirect(url_for('access_control_controller.access_control_login'))
    else:
        return redirect(url_for('access_control_controller.access_control_forgot_password'))

@bp.route("/logout")
@login_required
def access_control_logout():
    if logout():
        return redirect(url_for('access_control_controller.access_control_login'))
    else:
        return redirect(url_for('base_controller.index'))