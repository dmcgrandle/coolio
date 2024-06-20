/* script to animate the slider value changing */
const value = document.getElementById('speed_display_val');
const speed = document.getElementById('speed');
const frm = document.forms['array_form'];

speed.oninput = function () { value.innerHTML = Math.round(this.value) };
speed.addEventListener('mouseup', function() { frm.requestSubmit() });

