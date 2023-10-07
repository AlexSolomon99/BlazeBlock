from flask import Blueprint, render_template, request, flash, current_app, redirect, url_for, session

from . import db

map = Blueprint('map', __name__)


@map.route('/map', methods = ['GET', 'POST'])
def map_page():
    return render_template("map.html")
