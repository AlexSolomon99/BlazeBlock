from flask import Blueprint, render_template, request, flash, current_app, redirect, url_for, session
from .database_models import fire_data

from . import db

map = Blueprint('map', __name__)


@map.route('/map', methods = ['GET', 'POST'])
def map_page():
    full_historical_data = fire_data.FireData.query.all()
    full_historical_data_list = [elem for elem in full_historical_data]

    return render_template("map.html")
