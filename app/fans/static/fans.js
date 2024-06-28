/* script to animate the slider value changing */
const values = Array.from(document.getElementsByClassName('speed_display_val'));
const speeds = Array.from(document.getElementsByClassName('speed'));

speeds.forEach((speed, i) => {
  speed.oninput = (e) => { values[i].textContent = Math.round(e.target.value) };
  speed.onmouseup = (e) => { speed.form.requestSubmit() };
});

