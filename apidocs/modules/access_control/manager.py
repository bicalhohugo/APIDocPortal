import functools
from flask import (
        Blueprint, redirect, url_for, g
)

bp = Blueprint('access_control_manager', __name__)

def is_logged_user():
    return g.user is not None

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not is_logged_user():
            return redirect(url_for('access_control_controller.access_control_login'))

        return view(**kwargs)

    return wrapped_view

def is_logged_user_an_editor():
    return g.user['profile'] in ["E", "A"]

def editor_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not is_logged_user():
            return redirect(url_for('access_control_controller.access_control_denied'))
        elif not is_logged_user_an_editor():
            return redirect(url_for('access_control_controller.access_control_denied'))

        return view(**kwargs)

    return wrapped_view	       

def is_logged_user_an_admin():
    return g.user['profile'] == "A"

def admin_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not is_logged_user():
            return redirect(url_for('access_control_controller.access_control_denied'))
        elif not is_logged_user_an_admin():
            return redirect(url_for('access_control_controller.access_control_denied'))

        return view(**kwargs)

    return wrapped_view
