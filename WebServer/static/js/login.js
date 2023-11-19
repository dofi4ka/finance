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

    postData("/users/register", { name: name, username: username, email: email, password: password }).then((data) => {
  console.log(data);
});
}
