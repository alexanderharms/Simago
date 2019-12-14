#!/usr/bin/env python3

import geopandas as gpd

zip_codes = gpd.read_file("Boundaries - ZIP Codes.geojson")
print(zip_codes.zip.values)
