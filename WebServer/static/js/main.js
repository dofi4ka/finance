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