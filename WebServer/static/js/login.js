function set_token(token) {
     document.cookie = "Authorisation=" + token;
}

function login() {
    var username = document.getElementById('login-username').value;
    var password = document.getElementById('login-password').value;

    fetch('/users/login', {
        method: 'POST',
        headers: {
            'Access': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({'username': username, 'password': password})
    }).then((response) => {
        if (response.ok) {
            var data = response.json();
            var token = data["data"]["token"];
            console.log(token);
        } else {
            alert("Неправильные данные входа");
        }
    })
}

function register() {
    var name = document.getElementById('register-name').value;
    var username = document.getElementById('register-username').value;
    var email = document.getElementById('register-email').value;
    var password = document.getElementById('register-password').value;

    fetch('/users/register', {
        method: 'POST',
        headers: {
            'Access': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({'name': name, 'email': email,
            'username': username, 'password': password})
    }).then((response) => {
        if (response.ok) {
            var data = response.json();
            var token = data["data"]["token"];
            console.log(token);
        } else {
            alert("Email or username already taken");
        }
    })
}
