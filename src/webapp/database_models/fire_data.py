from webapp import db
from webapp.nasa_api.api_main_requester import get_sat_df
from webapp.nasa_api import additional_functions_api
from flask_login import UserMixin
from flask import flash
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

BASE_USER_CONFIDENCE = 0.3
LAT_DISTANCE_DIFF = 0.05
LONG_DISTANCE_DIFF = 0.05
NORTH_LAT = 48
SOUTH_LAT = 43.5
WEST_LONG = 20
EAST_LONG = 30


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

    def return_individual_data(self, time_thr_1: str, time_thr_2: str):
        list_of_str_times = self.get_list_of_date_strings(time_thr_1=time_thr_1, time_thr_2=time_thr_2)
        all_requested_data = FireData.query.filter(FireData.acq_date.in_(list_of_str_times))

        only_required_data = [elem for elem in all_requested_data]
        data_dict = {}
        for idx, elem in enumerate(only_required_data):
            data_dict[idx] = {
                "latitude": elem.latitude,
                "longitude": elem.longitude,
                "confidence": elem.confidence
            }

        return data_dict

    def aggregate_data_over_time(self, time_thr_1: str, time_thr_2: str):
        list_of_str_times = self.get_list_of_date_strings(time_thr_1=time_thr_1, time_thr_2=time_thr_2)

        grid_lat = np.arange(SOUTH_LAT, NORTH_LAT, LAT_DISTANCE_DIFF)
        grid_long = np.arange(WEST_LONG, EAST_LONG, LONG_DISTANCE_DIFF)

        # get data for te requested days
        all_requested_data = FireData.query.filter(FireData.acq_date.in_(list_of_str_times))
        only_required_data = [[elem.latitude, elem.longitude, elem.confidence] for elem in all_requested_data]
        req_data_df = pd.DataFrame(columns=["latitude", "longitude", "confidence"], data=only_required_data)

        data_dict = {
            "type": "FeatureCollection",
            "name": "Averaged_Data",
            "crs": {
                "type": "name",
                "properties": {
                "name": "urn:ogc:def:crs:OGC:1.3:CRS84"
                }
            }
        }
        features_list = []

        lat_idx, long_idx = 0, 0

        while lat_idx < len(grid_lat) - 1:
            while long_idx < len(grid_long) - 1:
                lat_low_bound, lat_high_bound = grid_lat[lat_idx], grid_lat[lat_idx + 1]
                long_low_bound, long_high_bound = grid_long[long_idx], grid_long[long_idx + 1]

                bounded_df = req_data_df.loc[(req_data_df["latitude"].between(lat_low_bound, lat_high_bound)) & 
                                             (req_data_df["longitude"].between(long_low_bound, long_high_bound))]
                confidence = bounded_df["confidence"].sum()

                feature_dict = {
                    "type": "Feature",
                    "properties": {
                    "confidence": confidence,
                    },
                    "geometry": {
                    "type": "Point",
                    "coordinates": [
                    grid_lat[lat_idx] + LAT_DISTANCE_DIFF/2,
                    grid_lat[long_idx] + LONG_DISTANCE_DIFF/2
                    ]
                    }
                }
                features_list.append(feature_dict)

                long_idx += 1
            
            long_idx = 0
            lat_idx += 1

        data_dict["features"] = features_list

        return data_dict


    @staticmethod
    def get_list_of_date_strings(time_thr_1: str, time_thr_2: str):
        date_thr_1 = additional_functions_api.convert_ymd_string_to_datetime(time_thr_1)
        date_thr_2 = additional_functions_api.convert_ymd_string_to_datetime(time_thr_2)

        list_of_str_times = []

        while date_thr_1 <= date_thr_2:
            current_str_tr = additional_functions_api.convert_datetime_to_day_string(date_thr_1)
            list_of_str_times.append(current_str_tr)
            date_thr_1 = date_thr_1 + timedelta(days=1)
        
        return list_of_str_times


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
    
    def add_db_entry_from_report(self, latitude, longitude, area=2):
        now = datetime.now()
        now_time_str = additional_functions_api.convert_datetime_to_day_string(now)

        try:
            new_fire_data = FireData(
                source="user",
                latitude = latitude,
                longitude = longitude,
                brightness = None,
                scan = area/3,
                track = area/3,
                acq_date = now_time_str,
                acq_time = 0,
                satellite = None,
                confidence = BASE_USER_CONFIDENCE,
                instrument = None,
                version = None,
                bright_t31 = None,
                frp = None,
                daynight = None
            )

            db.session.add(new_fire_data)
            db.session.commit()
            return new_fire_data.id

        except Exception as e:
            flash(f"There was an error trying to add sat data to the db: {e}", category='error')
            return None
    

    def download_historical_data(self, num_years_past=5.0):
        threshold_date = datetime.strptime("2023-02-01", r"%Y-%m-%d")
        satellite_to_download = r"MODIS_SP"

        list_of_map_keys = ["9bfc8b15391d7e01d3861470367bf190", 
                            "9e87aa69d9afa85bd633db1031309c03",
                            "bc871aa73ded57f050717f0b5f07b8b2",
                            "0328e100c0a04e0ec224434631da3dbb",
                            "2c4d62035ce638355f1eef936f50fb81"
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

