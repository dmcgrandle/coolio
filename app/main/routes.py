from flask import render_template, flash, redirect, url_for, request
import sqlalchemy as sa
from app.main import bp
from app import db

@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html')
