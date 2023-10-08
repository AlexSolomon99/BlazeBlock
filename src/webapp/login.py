from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from . import db

login = Blueprint('login', __name__)


@login.route ('/login', methods=['GET', 'POST'])
def login():
    
    return render_template("login.html")