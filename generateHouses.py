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

    x_0 = coord_0.x
    y_0 = coord_0.y
    x_1 = coord_1.x
    y_1 = coord_1.y

    x_dist = np.abs(x_1 - x_0)
    y_dist = np.abs(y_1 - y_0)

    price = price_0 * ((x_1 - x) / x_dist + (y_1 - y) / y_dist) \
            + price_1 * ((x_0 - x) / x_dist + (y_0 - y) / y_dist)
    return price

# Read in building data
buildings = gpd.read_file("./data-process/Residential buildings.geojson")
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
# The mortage is for 30 years, with a rate of 4 percent.
rate = 0.04
years = 30
house_prices['mort_payment'] = house_prices['buy_price']\
        .apply(calculateMonthlyPayment, args = (rate, years))

# Get the center of the zip code area.
zip_codes['geometry'] = zip_codes['geometry'].centroid

# Get the center of the buildings
buildings['geometry'] = buildings['geometry'].centroid

# Make the zip code columns numeric to assure the join will work
zip_codes['zip'] = zip_codes['zip'].apply(pd.to_numeric)
house_prices['Zip code'] = house_prices['Zip code'].apply(pd.to_numeric)

# Join zip geometry and zip prices 
zip_codes_prices = pd.merge(zip_codes[['zip', 'geometry']], 
    house_prices[['Zip code', 'mort_payment']],
    left_on='zip', right_on='Zip code', 
    how = 'inner')
zip_codes_prices = zip_codes_prices.drop('Zip code', axis = 1)

# Per building in the buildings data frame, find the two closest zip code 
# centroids to the building.
# Use the coordinates and the prices from the zip codes to calculate the price
# of the building.

# Insert monthly price column per building
buildings.insert(buildings.shape[1], 'monthly price', None)
multipoint = zip_codes_prices.geometry.unary_union
for index, building in buildings.iterrows():
    point = building.geometry
    # Nearest zip code row
    nearest_1 = zip_codes_prices[zip_codes_prices.geometry == \
            nearest_points(point, multipoint)[1]]
    geometry_1 = nearest_1.geometry.values[0]
    price_1 = nearest_1.mort_payment.values[0]
    print(geometry_1)
    print(price_1)
    
    # Second nearest zip code row
    new_zip_codes_prices = zip_codes_prices.drop(nearest_1.index, axis = 0)
    multipoint_2 = new_zip_codes_prices.geometry.unary_union

    nearest_2 = zip_codes_prices[zip_codes_prices.geometry == \
            nearest_points(point, multipoint_2)[1]]
    geometry_2 = nearest_2.geometry.values[0]
    price_2 = nearest_2.mort_payment.values[0]
    print(geometry_2)
    print(price_2)

    buildings.loc[index, 'monthly price'] = \
            interpolatePrices(point, geometry_1, geometry_2,
                    price_1, price_2)

buildings.to_file("./data-process/Buildings_mortgages.geojson", 
                  driver = "GeoJSON")
