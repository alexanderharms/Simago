#!/usr/bin/env python3
import argparse

import numpy as np
import pandas as pd
from scipy import stats

from scripts.population import generateEmptyPeople
from scripts.population import addProperties

# Assign options to properties based on the probabilities given in de prob data frames.
# How do I handle contradictive/simultaneous conditionals?

# How do I handle discrete vs. continuous random variables?

# Assignment of salary should be performed in tandem with assigning households.
# The salaries of the persons in a household should add up to the household income.
# In a household people shoud earn enough to be able to afford housing.

# Generate households
# Max 4 adults
# 2 adults with max 3 kids
# 1 adult,1 bedroom
# 2 adults, 1(0.9) or 2 (0.1) bedrooms
# 1 kid, 1 bedroom,
# n kids, n (0.8) or n-1 (0.2) bedrooms
# Assign each person with a household ID.

def uniform_distribution(values, pop_size):
    # Draw pop_size amount samples from uniform 
    # distribution
    lower_bound = values[0]
    upper_bound = values[1]
    samples = np.random.uniform(low = lower_bound,
            high = upper_bound,
            size = pop_size)

    return samples


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--popsize", type=int, 
                        help="Size of the population")
    args = parser.parse_args()

    censusdata = pd.read_csv('./data/ACS_17_5YR_DP05.csv').transpose()
    censusdata = censusdata[censusdata.iloc[:, 0].str.contains('Estimate')]
    censusdata.iloc[:, 1] = censusdata.iloc[:, 1].apply(pd.to_numeric)

    total_pop = censusdata.loc['HC01_VC03', 1]
    print(total_pop)

    # Load discrete probabilities
    prob_agesexrace = pd.read_csv("./data-process/probabilities/prob_agesexrace.csv")
    prob_education = pd.read_csv("./data-process/probabilities/prob_education.csv")
    prob_personalincome = pd.read_csv("./data-process/probabilities/" + 
            "prob_personalincome.csv")

    # Concatenate into one dataframe
    prob_df = pd.concat([prob_agesexrace, prob_education,
        prob_personalincome], axis = 0)

    # set_properties = set(prob_df.property.values)
    set_properties = ["sex", "age", "race", "education", "personal_income"] 
    num_properties = ["age", "personal_income"]
    population = generateEmptyPeople(args.popsize)
    population = addProperties(population, set_properties, 
                               prob_df, num_properties)

    print(population)
    population.to_csv(path_or_buf="data-process/population.csv",
            index = False)
    
    

