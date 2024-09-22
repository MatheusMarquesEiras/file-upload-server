from flask import Blueprint, request, flash, session, jsonify
from app.infra.actions import Login, Register
import uuid

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/login_service', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    LoginUser = Login(user=username, password=password)
    if LoginUser.login():
        session['loged_in'] = True
        session['uuid'] = LoginUser.get_uuid()
        
        return jsonify({'loged': True})
    
    flash('Não foi possiovel realizar o login')
    return jsonify({'loged': False})

@auth_blueprint.route('/register_service', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']

    RegisterUser = Register(userUuid=uuid.uuid4(), user=username, password=password)
    if RegisterUser.register():
        session['loged_in'] = True
        session['uuid'] = RegisterUser.get_uuid()

        return jsonify({'loged': True})
    
    flash('Não foi possiovel realizar o registro')
    return jsonify({'loged': False})

@auth_blueprint.route('/logout_service', methods=['POST'])
def logout():
    session.pop('loged_in', None)
    session.pop('uuid', None)

    return jsonify({'logout': True})