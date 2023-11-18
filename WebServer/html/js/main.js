function select(n) {
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