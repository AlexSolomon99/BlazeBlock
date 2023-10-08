from flask import Blueprint, render_template, request, flash, current_app, redirect, url_for, session
from webapp.database_models import fire_data

from . import db

uas = Blueprint('uas', __name__)

@uas.route ('/uas', methods=['GET', 'POST'])
def user_alert():
    return render_template("uas.html")
