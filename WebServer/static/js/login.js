function set_token(token) {
     document.cookie = "Authorisation=" + token;
}

function login() {
    var username = document.getElementById('login-username').value;
    var password = document.getElementById('login-password').value;

    var url = new URL("/users/login");
    url.searchParams.append('username', username);
    url.searchParams.append('password', password);

    r = fetch(url);
    if (r.ok) {
        console.log(r.json())
    } else {
        alert("Invalid password or username");
    }
}

function register() {
    var name = document.getElementById('register-name').value;
    var username = document.getElementById('register-username').value;
    var email = document.getElementById('register-email').value;
    var password = document.getElementById('register-password').value;

    var url = new URL("/users/register");
    url.searchParams.append('name', name);
    url.searchParams.append('username', username);
    url.searchParams.append('email', email);
    url.searchParams.append('password', password);

    r = fetch(url);
    if (r.ok) {
        console.log(r.json())
        // ...
    } else {
        alert("Email or username already taken");
    }
}
