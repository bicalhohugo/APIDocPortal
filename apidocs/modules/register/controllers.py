from flask import (
        Blueprint, render_template, redirect, url_for, request, flash
)
from apidocs.modules.user.controllers import get_user, register_new_user

bp = Blueprint('register_controller', __name__)

### METHODS ###

def register():
    try:
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        password = request.form['password']
        password_confirm = request.form['passwordconfirm']

        user = get_user(email)

        error = None

        if firstname is None or not firstname:
            error = 'Nome não informado.'
        elif lastname is None or not lastname:
            error = 'Sobrenome não informado.'        
        elif email is None or not email:
            error = 'E-mail não informado.'
        elif not user is None and user.count() > 0:
            error = 'E-mail já cadastrado em nossa base.'
        elif password is None or not password:
            error = 'Senha não informada.'
        elif password != password_confirm:
            error = 'As senhas informadas são diferentes.'

        if error is None:
            register_new_user(firstname, lastname, email, password)

            flash('Seu registro foi concluído em nosso sistema! Para nos acessar, aguarde a sua aprovação. Em caso de dúvidas, envie um e-mail para IT Arquitetura (it_arquitetura@nextel.com.br).','info')
                
            return True
        
        else:
            flash(error, 'error')

            return False

    except Exception as ex:
        flash(f"Ocorreu um erro ao criar o cadastro: {ex}", 'error')
        return False

### ROUTES ###

@bp.route("/register")
def new_user_register():
    return render_template('register/register.html')

@bp.route("/confirm_register", methods=('POST',))
def confirm_new_user_register():
    if register():
        return redirect(url_for('access_control_controller.access_control_login'))
    else:
        return redirect(url_for('register_controller.new_user_register'))    