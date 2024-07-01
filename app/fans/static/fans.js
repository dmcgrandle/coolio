/* script to animate the slider value changing and detect mouseup events */
const values = Array.from(document.getElementsByClassName('speed_display_val'));
const speeds = Array.from(document.getElementsByClassName('speed'));
const swtches = Array.from(document.getElementsByClassName('swtch')); //Note: switch is a reserved word in JS

speeds.forEach((speed, i) => {
  speed.oninput = (e) => { values[i].textContent = Math.round(e.target.value) + '%' };
  speed.onmouseup = () => { speed.form.requestSubmit() }; // speed.form.elements['submit']
});
swtches.forEach((swtch) => {
  swtch.onclick = () => { swtch.form.requestSubmit() };
});

