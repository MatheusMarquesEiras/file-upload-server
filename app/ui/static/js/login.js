const form = document.getElementById('LoginForm');

form.addEventListener('submit', function(event){
    event.preventDefault();

    const form_data = new FormData(form);

    fetch('/login_service',{
        method: 'POST',
        body: form_data
    }).then(res => res.json())
    .then(data => {
        if (data['loged'] == true){
            console.log('enviado com sucesso')
            window.location.href = '/'
        }
    })
    .catch(error => {
        console.error('Erro:', error);
    });
});