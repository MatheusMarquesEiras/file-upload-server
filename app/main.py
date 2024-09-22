from flask import Flask, render_template, request, redirect, url_for, jsonify
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    # Verifica se o campo de arquivos está presente
    if 'files' not in request.files:
        return jsonify({'success': False, 'error': 'Nenhum arquivo selecionado'}), 400

    # Pega os arquivos enviados
    files = request.files.getlist('files')

    # Verifica se os arquivos estão vazios
    if not files or files[0].filename == '':
        return jsonify({'success': False, 'error': 'Nenhum arquivo foi selecionado'}), 400

    # Salva os arquivos
    for file in files:
        if file:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    
    return jsonify({'success': True}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=3333)