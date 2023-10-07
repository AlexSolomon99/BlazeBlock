from flask import Blueprint, render_template, request, flash, current_app, redirect, url_for, session
from .database_models import fire_data

from . import db

map = Blueprint('map', __name__)


@map.route('/map', methods = ['GET', 'POST'])
def map_page():
    if request.method == 'POST':
        if request.form.get('add_historical') == 'add_historical' :
            list_of_ids = fire_data.FireDataUtils().download_historical_data(num_years_past=5.0)
            
            flash(f"Number of entries added to the db: {len(list_of_ids)}")

    return render_template("map.html")
