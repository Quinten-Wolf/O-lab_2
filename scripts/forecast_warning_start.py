from eratos.creds import AccessTokenCreds
from eratos.adapter import Adapter
import eratos.climate as eratosClimate
import eratos.helpers as helpers
import os
import yaml
from yaml.loader import SafeLoader
import json
import pprint
import datetime
import shapely
from shapely import wkt, geometry
from datetime import timezone
from keplergl import KeplerGl
import geopandas as gpd
import numpy as np
import datetime
import json
import pandas as pd
import numpy as np
from datetime import  timezone
from datetime import date
import geopandas as gpd
from shapely.geometry import box
from shapely import wkt
import datetime
import os

creds_path = r"C:\Users\Quinten\Documents\Eratos_tok\mycreds.json"
# Opening JSON file
f = open(creds_path)
  
# returns JSON object as 
# a dictionary
creds = json.load(f)

ecreds = AccessTokenCreds(
  creds['key'],
  creds['secret']
)
eadapter = Adapter(ecreds)


# Points in Australia,  Federation Square, Melbourne and Sydney Opera House.
point_name = ['Federation Square, Melbourne','Sydney Opera House']

#'POINT(151.215177 -33.857169)'
def get_forecast_data_for_points(ern: str, point_list):

    # Parse the date range using the iso8601 format
    e_data = eadapter.Resource(ern=ern)
    #access the gridded data via the gridded data adapter:
    gridded_e_data = e_data.data().gapi() 
         # Load Point strings as Shapely Points
    wkt_list = []
    for point in (point_list):
        loc_shape = wkt.loads(point)
        if type(loc_shape) is not geometry.Point:
            raise ValueError('value inside point_list should be a WKT point')
        loc= [loc_shape.y, loc_shape.x]
        wkt_list.append(loc)


    data_query_array = gridded_e_data.get_point_slices(gridded_e_data.get_key_variables()[0], 'SPP', pts=wkt_list, starts=[0], ends=[-1],strides =  [1])
    
    times = []
    for unix_time in gridded_e_data.get_subset_as_array('time'):

        date = datetime.datetime.fromtimestamp(unix_time)

        # Format the datetime object as an ISO 8601 string
        date_8601 = date.isoformat()
        times.append(date_8601)

    return data_query_array,times

point_list = ['POINT(144.968654  -37.817960)']
ern = 'ern:e-pn.io:resource:eratos.blocks.bom.adfd.dailymaxtempforecastau6km'
ern_temp_hourly = 'ern:e-pn.io:resource:eratos.blocks.bom.adfd.hourlytempforecastau6km'
ern_rainfall_3hourly = 'ern:e-pn.io:resource:eratos.blocks.bom.adfd.3hourlymeanprecipforecastau6km'
data_query_array,times = get_forecast_data_for_points(ern_rainfall_3hourly,point_list)

print(data_query_array,times)

y_axis = data_query_array
x_axis = times

# Timeseries visualisation, flat horizontal at the given threshold

# Thresholding, adding tollerance
# 9hours in a row, hourly temperature, 9 values, 3 hourly, 3 values