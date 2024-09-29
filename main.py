from app.ui.routes import auth_blueprint, pages_blueprint, services_blueprint
from app.infra.actions import init_data_base
from flask import Flask
import secrets
import os

app = Flask(__name__, template_folder='./app/ui/templates', static_folder='./app/ui/static')

app.register_blueprint(auth_blueprint)
app.register_blueprint(pages_blueprint)
app.register_blueprint(services_blueprint)

app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['UPLOAD_FOLDER'] = './uploads/'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

init_data_base()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=3333)