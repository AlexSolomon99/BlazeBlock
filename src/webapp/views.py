from flask import Blueprint, render_template

from . import db

views = Blueprint('views', __name__)

@views.route ('/login', methods=['GET', 'POST'])
def login():
    return render_template("login.html")
