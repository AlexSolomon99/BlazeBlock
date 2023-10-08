from flask import Blueprint, render_template, request, flash, current_app, redirect, url_for, session
from webapp.database_models import fire_data

from . import db

alert = Blueprint('alert', __name__)

@alert.route ('/alert', methods=['GET', 'POST'])
def alert_page():
    if request.method == 'POST':
        email = request.form.get('email')
        lat_long_data = request.form.get('addresses')
    return render_template("alert.html")
