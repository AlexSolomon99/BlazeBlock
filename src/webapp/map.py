from flask import Blueprint, render_template, request, flash, current_app, redirect, url_for, session, jsonify
from datetime import datetime, timedelta
from .database_models import fire_data
from . import db
import json
import geojson



map = Blueprint('map', __name__)


@map.route('/map', methods = ['GET', 'POST'])
def map_page():

    current_date = datetime.now()
    yesterday_date = current_date - timedelta(days=1)
    yesterday_str = yesterday_date.strftime(r"%Y-%m-%d")
    date_str = current_date.strftime(r"%Y-%m-%d")

    date_1_f = yesterday_date.strftime(r"%m/%d/%Y")
    date_2_f = current_date.strftime(r"%m/%d/%Y")

    selected_map = 1

    requested_data_dict = fire_data.FireDataUtils().return_individual_data(time_thr_1=yesterday_str, 
                                                                            time_thr_2=date_str)

    if request.method == 'POST':

        date_range = request.form.get('date-range')
        selected_map = request.form.get('select-map')

        date_1, date_2 = date_range.split(" - ")
        date_1_f = date_1
        date_2_f = date_2
        date_1 = date_1.split("/")
        date_2 = date_2.split("/")

        if int(selected_map) == 1:
            requested_data_dict = fire_data.FireDataUtils().return_individual_data(time_thr_1=f"{date_1[2]}-{date_1[0]}-{date_1[1]}", 
                                                                                   time_thr_2=f"{date_2[2]}-{date_2[0]}-{date_2[1]}")
        
        elif int(selected_map) == 2:
            requested_data_dict = fire_data.FireDataUtils().aggregate_data_over_time(time_thr_1=f"{date_1[2]}-{date_1[0]}-{date_1[1]}", 
                                                                                     time_thr_2=f"{date_2[2]}-{date_2[0]}-{date_2[1]}")
            return render_template("map.html",selected_map = json.dumps(selected_map), requested_data_dict=geojson.dumps(requested_data_dict, sort_keys = True))
            
        if request.form.get('redirect_uas') == 'redirect_uas':
            return redirect(url_for("alert.alert_page"))

    return render_template("map.html",selected_map = json.dumps(selected_map), requested_data_dict=json.dumps(requested_data_dict), date_1=date_1_f, date_2=date_2_f)
