function clockUpdate() {
  let date = new Date();
  const clock = window.document.getElementsByClassName('footer-clock')[0];
  clock.css = {'color': '#fff', 'text-shadow': '0 0 6px #ff0'};
  function addZero(x) {
    if (x < 10) {
      return x = '0' + x;
    } else {
      return x;
    }
  }
  let y = addZero(date.getFullYear())
  let h = addZero(date.getHours());
  let m = addZero(date.getMinutes());
  let s = addZero(date.getSeconds());
  clock.textContent = (y + ' ' + h + ':' + m + ':' + s)
}