import requests
import pandas as pd
from flask import flash


def get_sat_df(NORTH_LAT = 48, SOUTH_LAT = 43.5, WEST_LONG = 20, EAST_LONG = 30,
               FIRMS_MAPKEY = "9bfc8b15391d7e01d3861470367bf190", SATELLITE = "MODIS_ST",
               DATE_STR = "2023-10-07", DAYS_RANGE = "1"):

    api_link = f"/api/area/csv/{FIRMS_MAPKEY}/{SATELLITE}/{WEST_LONG},{SOUTH_LAT},{EAST_LONG},{NORTH_LAT}/{DAYS_RANGE}/{DATE_STR}"
    firms_base_link = r"https://firms.modaps.eosdis.nasa.gov"
    request_link = firms_base_link + api_link

    print(api_link)

    try:
        response = requests.get(request_link)
    except Exception as e:
        flash(f"Something went wrong: {e}")
        return pd.DataFrame()

    bytes_content = response.content
    string_content = bytes_content.decode("utf-8")

    if "Invalid" in string_content:
        return None

    # split by row
    row_splitted_data = string_content.split("\n")
    value_splitted_data = []
    for elem in row_splitted_data:
        value_splitted_data.append(elem.split(","))

    columns = value_splitted_data[0].copy()
    data = value_splitted_data[1:].copy()

    if len(data) == 0:
        return pd.DataFrame()

    data_df = pd.DataFrame(columns=columns,
                           data=data)

    data_df = data_df.astype(dtype={"latitude": "float64",
                                    "longitude": "float64",
                                    "brightness": "float64",
                                    "scan": "float64",
                                    "track": "float64",
                                    "confidence": "float64",
                                    "bright_t31": "float64",
                                    "frp": "float64",
                                    })

    return data_df


