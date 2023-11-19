function set_token(token) {
     document.cookie = "Authorisation=" + token;
}

function login() {
    var username = document.getElementById('login-username').value;
    var password = document.getElementById('login-password').value;

    var response = fetch('/users/login', {
        method: 'POST',
        mode: "no-cors",
        headers: {
            'Access': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({'username': username, 'password': password})
    });

    console.log(response)
}

