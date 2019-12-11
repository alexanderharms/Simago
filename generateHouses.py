#!/usr/bin/env python3

# Select the rental vs. sold houses

# Connect the sale prices to the sold houses
# Connect the rental price/bedroom to the rental houses
# Assign a number of bedrooms to the rental houses
# Convert sales prices to mortgage payments
# Convert prices to yearly costs

# Connect houses to households based on household income
import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.ops import nearest_points
import random
from multiprocessing import Pool
from functools import partial

import matplotlib.pyplot as plt

def calculateMonthlyPayment(principal, rate, years):
    rate = rate / 12
    num_payments = years * 12
    payment = principal * (rate * (1 + rate)**num_payments) \
            / ((1 + rate)**num_payments - 1)
    return payment

def interpolatePrices(coord_house, coord_0, coord_1, 
        price_0, price_1):
    #x = coord_house[1]
    #y = coord_house[0]

    #x_0 = coord_0[1]
    #y_0 = coord_0[0]
    #x_1 = coord_1[1]
    #y_1 = coord_1[0]

    x = coord_house.x
    y = coord_house.y
    pos_house = np.sqrt(x**2 + y**2)

    x_0 = coord_0.x
    y_0 = coord_0.y
    pos_0 = np.sqrt(x_0**2 + y_0**2)
    x_1 = coord_1.x
    y_1 = coord_1.y
    pos_1 = np.sqrt(x_1**2 + y_1**2)

    x_dist = np.abs(x_1 - x_0)
    y_dist = np.abs(y_1 - y_0)

    def dist_func(pos_house, pos_0, pos_1, epsilon):
        abs_dist = abs((pos_house - pos_0)/(pos_1 - pos_0))
        f = 1 - np.exp(np.log(epsilon) * abs_dist)
        return f

    epsilon = 0.1
    price = price_0 + (price_1 - price_0) \
            * dist_func(pos_house, pos_0, pos_1, epsilon)
    #price = price_0 + (price_1 - price_0)/(pos_1 - pos_0) \
    #        * (pos_house - pos_0)
    return price

def parallelize_dataframe(df, func, args = [], n_cores=6):
    df_split = np.array_split(df, n_cores)
    pool = Pool(n_cores)
    if args:
        func = partial(func, args = args)
    df = pd.concat(pool.map(func, df_split))
    pool.close()
    pool.join()
    return df

def findZip(point, zip_codes):
    zip_code = zip_codes[zip_codes['geometry'] == point]
    return zip_code.zip.values[0]

def calcNearestZip(buildings, args):
    multipoint = args[0]
    zip_codes = args[1]

    buildings['nearest_zip_geom'] = buildings['geometry']\
            .apply(lambda point, multipoint: nearest_points(point,
                multipoint)[1], multipoint = multipoint)

    buildings['nearest_zip'] = buildings['nearest_zip_geom']\
            .apply(lambda point, zip_codes: findZip(point, zip_codes),
                    zip_codes = zip_codes)
    return buildings

def calcNewMultipoint(point, zip_codes):
    new_zip_codes = zip_codes[zip_codes['geometry'] != point]
    new_multipoint = new_zip_codes.geometry.unary_union
    return new_multipoint

def calcNextNearestZip(buildings, args):
    zip_codes = args[1]

    print("Calculating new multipoints")
    buildings['new_multipoint'] = buildings['nearest_zip_geom']\
            .apply(lambda point, zip_codes:
                    calcNewMultipoint(point, zip_codes), 
                    zip_codes = zip_codes)

    print("Calculating next nearest zip geometry")
    buildings['next_nearest_zip_geom'] = \
            buildings.apply(lambda row: 
                    nearest_points(row['geometry'], 
                                   row['new_multipoint'])[1], 
                    axis = 1)

    print("Finding next nearest zip code")
    buildings['next_nearest_zip'] = buildings['next_nearest_zip_geom']\
            .apply(lambda point, zip_codes: findZip(point, zip_codes),
                    zip_codes = zip_codes)

    #buildings.drop('new_multipoint', axis = 1, inplace = True)
    return buildings

def getPrice(x, zip_codes, price_column):
    zip_code = zip_codes[zip_codes['zip'] == x]
    return zip_code[price_column].values[0]

def getHousePrice(buildings, args):
    zip_codes = args[0]
    zip_column = args[1]
    price_column = args[2] # In zip codes
    new_price_column = args[3]

    buildings[new_price_column] = buildings[zip_column]\
            .apply(lambda x, zip_codes, price_column:
                    getPrice(x, zip_codes, price_column),
                    zip_codes = zip_codes, 
                    price_column = price_column)
    return buildings
    
def interpolateHousePrice(buildings):
    buildings['price'] = buildings\
            .apply(lambda row:
                    interpolatePrices(row['geometry'],
                        row['nearest_zip_geom'], row['next_nearest_zip_geom'],
                        row['nearest_zip_price'],
                        row['next_nearest_zip_price']),
                    axis = 1)
    return buildings
# Read in building data
buildings = gpd.read_file("./data-process/Residential buildings.geojson")
#buildings = buildings.iloc[0:100, :]
# Read in the zip code data
zip_codes = gpd.read_file("./data/Boundaries - ZIP Codes.geojson")
# Read in the house price data
house_prices = pd.read_csv("./data/ChicagoHousePrices.csv")

# Combine the house prices per zip code with the house prices

# Take an average of the listing and sale price to get more 
# zip codes with a value.
house_prices['buy_price'] = house_prices[['Listing price', 
    'Sale price']].mean(axis = 1)
# We assume all houses are sold not rented.

# Get the center of the zip code area.
zip_codes['geometry'] = zip_codes['geometry'].centroid

# Get the center of the buildings
buildings['geometry'] = buildings['geometry'].centroid

# Make the zip code columns numeric to assure the join will work
zip_codes['zip'] = zip_codes['zip'].apply(pd.to_numeric)
house_prices['Zip code'] = house_prices['Zip code'].apply(pd.to_numeric)

# Join zip geometry and zip prices 
zip_codes_prices = pd.merge(zip_codes[['zip', 'geometry']], 
    house_prices[['Zip code', 'buy_price']],
    left_on='zip', right_on='Zip code', 
    how = 'inner')
zip_codes_prices = zip_codes_prices.drop('Zip code', axis = 1)

# Per building in the buildings data frame, find the two closest zip code 
# centroids to the building.
# Use the coordinates and the prices from the zip codes to calculate the price
# of the building.

# Insert monthly price column per building
buildings.insert(buildings.shape[1], 'nearest_zip', None)
buildings.insert(buildings.shape[1], 'nearest_zip_geom', None)
buildings.insert(buildings.shape[1], 'nearest_zip_price', None)
buildings.insert(buildings.shape[1], 'next_nearest_zip', None)
buildings.insert(buildings.shape[1], 'next_nearest_zip_geom', None)
buildings.insert(buildings.shape[1], 'next_nearest_zip_price', None)
buildings.insert(buildings.shape[1], 'new_multipoint', None)
buildings.insert(buildings.shape[1], 'price', None)
buildings.insert(buildings.shape[1], 'monthly_cost', None)

multipoint = zip_codes.geometry.unary_union

print("starting")
args = [multipoint, zip_codes]
buildings = parallelize_dataframe(buildings, calcNearestZip, args = args)
buildings = parallelize_dataframe(buildings, calcNextNearestZip, args = args)
buildings.drop(['new_multipoint'], axis = 1, inplace = True)
#buildings.drop(['nearest_zip_geom', 'next_nearest_zip_geom'], 
#        axis = 1, inplace = True)
# Now we just need to get the prices
buildings['rent_buy'] = 'buy'
args = [zip_codes_prices, 'nearest_zip', 'buy_price', 'nearest_zip_price']
buildings = parallelize_dataframe(buildings, getHousePrice, args = args)
args = [zip_codes_prices, 'next_nearest_zip', 'buy_price', 'next_nearest_zip_price']
buildings = parallelize_dataframe(buildings, getHousePrice, args = args)
# After that we extrapolate the price
buildings = parallelize_dataframe(buildings, interpolateHousePrice)
#print(buildings[['geometry', 'nearest_zip_geom', 'next_nearest_zip_geom',
#    'nearest_zip_price', 'next_nearest_zip_price']].head())

# After that calculate the morgage payment/monthly costs
rate = 0.04
years = 30
buildings['monthly_cost'] = buildings['price']\
        .apply(calculateMonthlyPayment, args = (rate, years))

print("finished, start writing")

buildings = buildings.drop(['nearest_zip_geom', 'next_nearest_zip_geom',
    'nearest_zip_price', 'next_nearest_zip_price'], axis = 1)

print(buildings.head())
buildings.to_file("./data-process/Buildings_mortgages.geojson", 
                  driver = "GeoJSON")

print(buildings.describe())
buildings['x'] = buildings['geometry'].apply(lambda point: point.x)
buildings['y'] = buildings['geometry'].apply(lambda point: point.y)

fig, ax = plt.subplots()
s = ax.scatter(buildings.x, buildings.y,
        c = buildings.price.values,
        s = 20,
        marker = 'o')
cbar = plt.colorbar(mappable = s, ax = ax)
plt.show()

