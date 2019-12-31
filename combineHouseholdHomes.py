#!/usr/bin/env python3

# Housing costs are between 15 and 50 percent of household income

# 1 adult,1 bedroom
# 2 adults, 1(0.9) or 2 (0.1) bedrooms
# 1 kid, 1 bedroom,
# n kids, n (0.8) or n-1 (0.2) bedrooms

# Read population
# Read buildings
# Selection rules for assigining a house to a person:
#  Cost > alpha * Income; alpha in (0, 1)
#  Cost < beta * Income; beta in (0, 1), beta > alpha

# From this subset of buildings, randomly draw a building from that
import random

import numpy as np
import pandas as pd 
import geopandas as gpd

def calc_min_cost(income):
    alpha_prop = 0.2
    alpha_top = max_income
    gamma = 0
    I_max = (1 + gamma) * (1.0/alpha_prop) * alpha_top

    #k = - (1/I_max) * np.log(((gamma - 1) * alpha_top)/
    #        (alpha_prop - (alpha_top / I_max)) * I_max)
    #C_min = (alpha_prop - (alpha_top / income)) \
    #        * np.exp(-k*income) * income \
    #        + alpha_top
    if income <= I_max:
        C_min = alpha_prop * income
    else: 
        C_min = alpha_top
    return C_min

def calc_max_cost(income):
    beta_prop = 0.3
    beta_low = 0.6
    p = 0.1
    I_min = (1/beta_prop) * min_income

    a = -1 * np.log(1 - p)/I_min
    b = -1 * np.log(1 - p)/I_min

    C_max = (beta_low * (1 - np.exp(-a * income)) \
            + beta_prop * np.exp(-b * income)) * income
    return C_max

population = pd.read_csv("./data-process/population.csv")
buildings = gpd.read_file("./data-process/Buildings_mortgages.geojson")

alpha = 0.15
beta = 0.5

# Only people 18 and over can own property
population['age'] = pd.to_numeric(population['age'])
population = population.query("age >= 18")

population.insert(population.shape[1], 'building_id', None)
person_index = [x for x in range(0, population.shape[0])]
population = population.reset_index(drop = True)
# Shuffle list to prevent preferral treatment based on sequence of people
random.shuffle(person_index)

max_income = buildings['cost'].quantile(q=0.75)
min_income = buildings['cost'].quantile(q=0.30)

import matplotlib.pyplot as plt

income_vec = [x for x in range(1, int(1e5))]
min_cost = [calc_min_cost(x) for x in income_vec]
max_cost = [calc_max_cost(x) for x in income_vec]

plt.plot(income_vec, min_cost)
plt.axvline(x=(1/0.6) * min_income)
plt.axvline(x=(1/0.2) * max_income)
plt.plot(income_vec, max_cost)
plt.show()

print("Start calculating")
count = 0
for k in person_index:
    if ((count + 1) % 100 == 0):
        print(count)
    person = population.iloc[k, :]
    person_income = person['personal_income']
    min_cost_building = calc_min_cost(person_income)
    max_cost_building = calc_max_cost(person_income)
    suitable_buildings = buildings.query("cost > @min_cost_building" \
            + " and cost < @max_cost_building")
    if suitable_buildings.shape[0] > 0:
        suitable_buildings_ids = suitable_buildings['building_id'].values
        rand_index = random.randint(0, len(suitable_buildings_ids) - 1)
        building_id = suitable_buildings_ids[rand_index]
        population.loc[k, 'building_id'] = building_id
        buildings = buildings.query("building_id != @building_id")
    count += 1

print(population)
print(population[['building_id']])
population.to_csv("./data-process/population_buildings.csv", 
        index = False)
