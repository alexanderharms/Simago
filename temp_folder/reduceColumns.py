#!/usr/bin/env python3

import geopandas as gpd

buildings = gpd.read_file("Residential buildings.geojson")
# no_of_unit is number of residential units. 
# Only residential buildings are needed so no_of_unit > 0
buildings = buildings.query("bldg_statu == 'ACTIVE'")
buildings = buildings[['geometry', 'x_coord', 'y_coord', 'no_stories',
    'shape_area', 'year_built', 'suf_dir1', 'bldg_id', 'cdb_city_i', 
    'stories', 'bldg_name1', 'bldg_name2', 'pre_dir1', 'st_name1', 
    'f_add1', 't_add1', 'no_of_unit', 'shape_len']]
buildings.to_file("Residential buildings.geojson", driver = "GeoJSON")