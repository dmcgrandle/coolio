# Coolio

Coolio is a Raspberry Pi Python fan and temperature controller using a Flask webserver.  I developed it to control the temperature in our electronics room, which is the room under the stairs - we call it the Harry Potter room.

---
### Components/Libraries/opensource used:
- [Flask-APScheduler](https://pypi.org/project/Flask-APScheduler/) is used to run background tasks to asynchronously perform functions like reading temperature sensors and not be blocking to the webserver answering requests.  I considered redis, but that seemed excessive for the relatively simple tasks this project needs.
- [Python Statemachine](https://python-statemachine.readthedocs.io/) is used in automations to tie together the temperature readings of the sensors with the operation of fans
- [Flask-WTForms](https://flask-wtf.readthedocs.io/en/1.2.x/) is used to render forms and [Jinja2](https://pypi.org/project/Jinja2/) as well to assist with dynamically creating HTML at runtime.
- [Flask SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/) is used to save state to a local SQLite database.  Again, nothing particularly robust needed here for a db.

For controlling the Pi and attached fans and sensors, the following libraries are used:
- [RPi.GPIO](https://pypi.org/project/RPi.GPIO/) is used to turn pins on and off, though I am considering switching to [gpiozero](https://pypi.org/project/gpiozero).
- [rpi_hardware_pwm](https://github.com/Pioreactor/rpi_hardware_pwm) to control the PWM fans because RPi.GPIO uses software and kicks up the CPU (making more heat).
- [vcgencmd](https://pypi.org/project/vcgencmd/) for the internal temperature sensor on the Pi.

See the wiki for diagrams on the protoboard I use, circuit diagrams and connections to the Pi.

The Python code was originally inspired from Miguel Grinberg's [Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world).

- See the Wiki for details.