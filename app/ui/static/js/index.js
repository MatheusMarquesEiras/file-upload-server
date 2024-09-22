const logouButton = document.getElementById('logoutButton');

logouButton.addEventListener('click',() => {
    fetch('/logout_service', {
        method: 'POST',
        body: ""
    }).then(res => res.json())
    .then(data =>{
        if (data['logout'] == true){
            setTimeout(function(){
                window.location.href = '/'
            }, 50);
        }
    });
});