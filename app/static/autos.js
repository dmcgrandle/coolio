/* script to send post when 'enable' clicked */
const enables = Array.from(document.getElementsByClassName('enable')); 

enables.forEach((enable) => {
  enable.onclick = () => { enable.form.requestSubmit() };
});

