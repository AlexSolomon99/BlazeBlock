from . import db
from nasa_api.api_main_requester import get_sat_df
from flask_login import UserMixin
from flask import flash
import pandas as pd
from datetime import datetime, timedelta


class FireData(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(50))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    brightness = db.Column(db.Float)
    scan = db.Column(db.Float)
    track = db.Column(db.Float)
    acq_date = db.Column(db.String(50))
    acq_time = db.Column(db.String(50))
    satellite = db.Column(db.String(50))
    confidence = db.Column(db.Float)
    instrument = db.Column(db.String(50))
    version = db.Column(db.String(50))
    bright_t31 = db.Column(db.Float)
    frp = db.Column(db.Float)
    daynight = db.Column(db.String(10))


class FireDataUtils():

    def __init__(self) -> None:
        pass


    def import_df_to_db(df_to_import):
        list_of_added_ids = []
        for _, row in df_to_import.iterrows():
            try:
                new_fire_data = FireData(
                    source="sat",
                    latitude = row["latitude"],
                    longitude = row["longitude"],
                    brightness = row["brightness"],
                    scan = row["scan"],
                    track = row["track"],
                    acq_date = row["acq_date"],
                    acq_time = row["acq_time"],
                    satellite = row["satellite"],
                    confidence = row["confidence"],
                    instrument = row["instrument"],
                    version = row["version"],
                    bright_t31 = row["bright_t31"],
                    frp = row["frp"],
                    daynight = row["daynight"]
                )

                db.session.add(new_fire_data)
                db.session.commit()
                list_of_added_ids.append(new_fire_data.id)

            except Exception as e:
                flash(f"There was an error trying to add sat data to the db: {e}", category='error')
                continue

        return list_of_added_ids
    

    def download_historical_data():
        downloaded_df = get_sat_df()
