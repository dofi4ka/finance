// Пример отправки POST запроса:
async function postData(url = "", data = {}) {
  // Default options are marked with *
  const response = await fetch(url, {
    method: "POST", // *GET, POST, PUT, DELETE, etc.
    mode: "cors", // no-cors, *cors, same-origin
    cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
    credentials: "same-origin", // include, *same-origin, omit
    headers: {
      "Content-Type": "application/json",
      // 'Content-Type': 'application/x-www-form-urlencoded',
      "Cookies": document.cookie
    },
    redirect: "follow", // manual, *follow, error
    referrerPolicy: "no-referrer", // no-referrer, *client
    body: JSON.stringify(data), // body data type must match "Content-Type" header
  });
  return await response.json(); // parses JSON response into native JavaScript objects
}

function set_token(token) {
     document.cookie = "Authorisation=" + token;
}

function login() {
    var username = document.getElementById('login-username').value;
    var password = document.getElementById('login-password').value;

    postData("/users/login", {username: username, password: password}).then((data) => {
        if (data["status"]) {
        set_token(data["data"]["token"]);
        window.location.replace("/");
        } else alert(data['message'])
    });
}

function register() {
    var name = document.getElementById('register-name').value;
    var surname = document.getElementById('register-surname').value;
    var username = document.getElementById('register-username').value;
    var email = document.getElementById('register-email').value;
    var password = document.getElementById('register-password').value;

    postData("/users/register", {name: name, surname: surname, username: username, email: email, password: password}).then((data) => {
        if (data["status"]) {
        set_token(data["data"]["token"]);
        window.location.replace("/");
        } else alert(data['message'])
    });
}
