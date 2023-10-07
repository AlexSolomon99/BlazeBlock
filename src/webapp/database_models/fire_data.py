from webapp import db
from webapp.nasa_api.api_main_requester import get_sat_df
from webapp.nasa_api import additional_functions_api
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


    def import_df_to_db(self, df_to_import):
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
    

    def download_historical_data(self, num_years_past=5.0):
        threshold_date = datetime.strptime("2023-02-01", r"%Y-%m-%d")
        satellite_to_download = r"MODIS_SP"

        list_of_map_keys = ["9bfc8b15391d7e01d3861470367bf190", 
                            "9e87aa69d9afa85bd633db1031309c03",
                            "bc871aa73ded57f050717f0b5f07b8b2"
                            ]

        init_date = datetime.now()

        current_analysis_date = init_date - timedelta(days=int(365*num_years_past))
        diff_date = init_date - current_analysis_date

        master_df_list = []
        mapkey_idx = 0
        num_of_tries = 0
        max_tries = 10

        while diff_date > timedelta(seconds=0):
            current_analysis_date_str = additional_functions_api.convert_datetime_to_day_string(current_analysis_date)

            downloaded_df = get_sat_df(DAYS_RANGE=10,
                                       FIRMS_MAPKEY=list_of_map_keys[mapkey_idx],
                                       DATE_STR=current_analysis_date_str, 
                                       SATELLITE=satellite_to_download)
            if downloaded_df is None:
                mapkey_idx += 1
                mapkey_idx = min(mapkey_idx, len(list_of_map_keys)-1)
                if mapkey_idx == len(list_of_map_keys):
                    num_of_tries += 1
                    if num_of_tries > max_tries:
                        break
                continue

            if len(downloaded_df) != 0:
                master_df_list.append(downloaded_df)

            current_analysis_date = current_analysis_date + timedelta(days=10)
            if current_analysis_date > threshold_date:
                satellite_to_download = r"MODIS_NRT"

            diff_date = init_date - current_analysis_date

        concatenated_master_df = pd.concat(master_df_list)
        list_of_added_ids = self.import_df_to_db(df_to_import=concatenated_master_df)

        return list_of_added_ids

