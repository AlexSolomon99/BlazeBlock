from flask import Blueprint, render_template, request, flash, current_app, redirect, url_for, session
from database_models import fire_data

from . import db

admin = Blueprint('admin', __name__)


@admin.route('/admin', methods = ['GET', 'POST'])
def admin_page():
    full_historical_data = fire_data.FireData.query.all()
    full_historical_data_list = [elem for elem in full_historical_data]

    if request.method == 'POST':
        if request.form.get('add_historical') == 'add_historical' :
            list_of_ids = fire_data.FireDataUtils.download_historical_data(num_years_past=1.0)
            flash(f"Number of entries added to the db: {len(list_of_ids)}")

    return render_template("admin.html", full_historical_data_list=full_historical_data_list)
