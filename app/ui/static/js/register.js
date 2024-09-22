const form = document.getElementById('RegisterForm')

form.addEventListener('submit', function(event){
    event.preventDefault()

    const form_data = new FormData(form)

    fetch('/register_service',{
        method: 'POST',
        body: form_data
    }).then(res => res.json())
    .then(data => {
        console.log(data['loged'])
        if (data['loged'] == true){
            console.log('enviado com sucesso')
            window.location.href = '/'
        }
    })
    .catch(error => {
        console.error('Erro:', error);
    });
});