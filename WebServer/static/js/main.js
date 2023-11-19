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
var selected = 0;
function select(n) {
    selected = n;
    document.getElementById('selector')
    .setAttribute("style", `left: ${n * 20}%;`);

    var pages = document.getElementsByClassName('page');
    for (var i = 0; i < pages.length; i++) {
       pages.item(i).setAttribute("style", `left: ${(i-n) * 100}%;`);;
    }
}
function close_all() {
    var opened = document.getElementsByClassName('opened');
    while (opened.length > 0) {
       opened.item(0).classList.remove('opened');
    }
}
function toggle_menu(menuId) {
    document.getElementById('screen-blur').classList.toggle('opened');
    document.getElementById(menuId).classList.toggle('opened');
}

document.addEventListener('touchstart', handleTouchStart, false);
document.addEventListener('touchmove', handleTouchMove, false);
var xDown = null;
var yDown = null;
function getTouches(evt) {
  return evt.touches || evt.originalEvent.touches;
}
function handleTouchStart(evt) {
    const firstTouch = getTouches(evt)[0];
    xDown = firstTouch.clientX;
    yDown = firstTouch.clientY;
};
function handleTouchMove(evt) {
    if ( ! xDown || ! yDown ) {
        return;
    }
    var xUp = evt.touches[0].clientX;
    var yUp = evt.touches[0].clientY;
    var xDiff = xDown - xUp;
    var yDiff = yDown - yUp;
    if ( Math.abs( xDiff ) > Math.abs( yDiff ) ) {
        if ( xDiff > 0 ) {
            if (selected < 4) {
               select(selected+1)
            }
        } else {
            if (selected > 0) {
               select(selected-1)
            }
        }
    }
    xDown = null;
    yDown = null;
};

function income() {
    var amount = document.getElementById('income-bottom-panel-amount').value;
    var category = document.getElementById('income-bottom-panel-category').value;

    postData("/transactions/add", {amount: amount, category: category}).then((data) => {
        if (data["status"]) {
            window.location.reload();
        } else alert(data['message'])
    });
}

function expense() {
    var amount = -parseInt(document.getElementById('income-bottom-panel-amount').value);
    var category = document.getElementById('income-bottom-panel-category').value;

    postData("/transactions/add", {amount: amount, category: category}).then((data) => {
        if (data["status"]) {
            window.location.reload();
        } else alert(data['message'])
    });
}