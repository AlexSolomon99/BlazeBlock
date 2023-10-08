from flask import Blueprint, render_template, request, flash, current_app, redirect, url_for, session
from webapp.database_models import fire_data

from . import db

views = Blueprint('views', __name__)

def print_flashes():
    if "flashes" in session:
        if session['flashes']:
            
            errorflashes = session['flashes']['errors']
            successflashes = session['flashes']['success']

            for errorflash in errorflashes:
                flash(errorflash,category='error')
            for successflash in successflashes:
                flash(successflash,category='success')


def clear_flashes():
    if "flashes" in session:
        session['flashes']={
            'errors':[],
            'success':[]
        }

@views.route('/', methods = ['GET', 'POST'])
def home_page():
    return render_template("home.html")

@views.route('/report', methods = ['GET', 'POST'])
def report_page():
    if request.method == 'POST':
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')

        report_addition_id = fire_data.FireDataUtils().add_db_entry_from_report(latitude=latitude,
                                                                                longitude=longitude)
        
        return redirect(url_for('views.home_page'))

    return render_template("report.html")


@views.route ('/login', methods=['GET', 'POST'])
def login():
    return render_template("login.html")
