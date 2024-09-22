// upload.js

// Função para mostrar mensagens ao usuário
function showMessage(text) {
    const messageContainer = document.getElementById('messageContainer');
    messageContainer.textContent = text;
}

// Função para limpar mensagens
function clearMessage() {
    const messageContainer = document.getElementById('messageContainer');
    messageContainer.textContent = '';
}

// Função para enviar os arquivos automaticamente
function uploadFiles(files) {
    const formData = new FormData();

    // Adiciona todos os arquivos ao FormData
    for (let i = 0; i < files.length; i++) {
        formData.append('files', files[i]);
    }

    // Exibe uma mensagem de carregamento
    showMessage('Enviando arquivos...');

    // Envia os arquivos usando fetch
    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        clearMessage(); // Limpa a mensagem de carregamento
        if (data.success) {
            showMessage('Upload realizado com sucesso!');
        } else {
            showMessage('Erro no upload: ' + data.error);
        }
    })
    .catch(error => {
        clearMessage(); // Limpa a mensagem de carregamento
        console.error('Erro no upload:', error);
        showMessage('Ocorreu um erro ao fazer o upload.');
    });
}

// Escuta o evento change no input de arquivo
document.getElementById('fileUpload').addEventListener('change', function(event) {
    const files = event.target.files;

    if (files.length === 0) {
        showMessage('Nenhum arquivo selecionado.');
        return;
    }

    // Envia os arquivos automaticamente
    uploadFiles(files);
});
