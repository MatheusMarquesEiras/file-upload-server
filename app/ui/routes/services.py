from flask import Blueprint, request, jsonify, current_app, session, send_file
from app.infra.actions import RegisterFile
from app.infra.actions import get_file_path_and_name
import uuid
import os

services_blueprint = Blueprint('service', __name__)

@services_blueprint.route('/upload', methods=['POST'])
def upload():
    if 'files' not in request.files:
        return jsonify({'success': False, 'error': 'Nenhum arquivo selecionado'}), 400

    files = request.files.getlist('files')

    if not files or files[0].filename == '':
        return jsonify({'success': False, 'error': 'Nenhum arquivo foi selecionado'}), 400

    for file in files:
        if file:
            file_name, file_extension = os.path.splitext(file.filename)
            file_uuid = uuid.uuid4()
            file_uuid_str = str(file_uuid) + file_extension
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], str(session['uuid']), file_uuid_str))
            registerFile = RegisterFile(filename=file_name, fileUuid=file_uuid, fileExtension=file_extension, userUuid=str(session['uuid']))
            registerFile.register()
    
    return jsonify({'success': True}), 200

@services_blueprint.route('/download/<int:file_uuid>')
def download(file_uuid):
    path, name = get_file_path_and_name(file_uuid=file_uuid)
    
    return send_file(path, as_attachment=True, download_name=name)