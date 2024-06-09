from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    temps = [
        {'name': 'Outside HP Room', 'tempF': '65'},
        {'name': 'Back of Cabinet', 'tempF': '80'},
        {'name': 'By Dreamwall', 'tempF': '72'},
    ]
    return render_template('index.html', temps=temps)