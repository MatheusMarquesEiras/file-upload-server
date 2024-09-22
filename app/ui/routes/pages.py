from flask import Blueprint, render_template, session, redirect, url_for
from app.infra.actions import get_user_files, get_username

pages_blueprint = Blueprint('page', __name__)

@pages_blueprint.before_app_request
def ensire_login():
    if 'loged_in' not in session:
        session['loged_in'] = False
        session['uuid'] = None

@pages_blueprint.route('/')
def main_page():
    if not session['loged_in']:
        return redirect(url_for('page.login_page'))
    print(session['uuid'])
    return render_template('index.html', name=get_username(session['uuid']))

@pages_blueprint.route('/upload_page')
def upload_page():
    if not session['loged_in']:
        return redirect(url_for('page.login_page'))

    return render_template('upload.html')

@pages_blueprint.route('/download_page')
def download_page():
    if not session['loged_in']:
        return redirect(url_for('page.login_page'))

    return render_template("download.html", files=get_user_files(session['uuid']))

@pages_blueprint.route('/login')
def login_page():
    return render_template('login.html')

@pages_blueprint.route('/register.html')
def register_page():
    return render_template('register.html')

