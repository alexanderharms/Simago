#!/usr/bin/env python3
# Generate probabilities for a person to be of a certain age, sex or race.

import pandas as pd
import numpy as np
from scripts.probabilities import genProb_NoCond
from scripts.probabilities import genProb_NoCond_Range
#import matplotlib.pyplot as plt

# Filter dataset -------------------------------------------------------------
# Read in census data on sex, age and race
censusdata = pd.read_csv('./data/ACS_17_5YR_DP05.csv').transpose()
censusdata = censusdata[censusdata.iloc[:, 0].str.contains('Estimate')]
censusdata.iloc[:, 1] = censusdata.iloc[:, 1].apply(pd.to_numeric)

# Sex ------------------------------------------------------------------------
# column 0 option label
# column 1 amounts
# total population is equal to the sum of the two numbers
male_female = censusdata.loc[['HC01_VC04', 'HC01_VC05'], :]
# Male is 0, Female is 1
prob_data = pd.DataFrame({"option" : ["male", "female"],
                          "value" : male_female.iloc[:, 1].values})
prob_sex = genProb_NoCond(prob_data, "sex")

## Age -------------------------------------------------------------------------
age_rows = ['HC01_VC09'] \
        + ['HC01_VC' + str(x) for x in range(10, 22)] \
        + ['HC01_VC' + str(x) for x in range(28, 33)]
age = censusdata.loc[age_rows, :]

age_df = pd.DataFrame(data = {"min_age": [0, 5, 10, 15, 20, 25, 35, 45,
                                          55, 60, 65, 75, 85, 16, 18, 21, 62,
                                          65],
                             "max_age": [4, 9, 14, 19, 24, 34, 44, 54, 59,
                                         64, 74, 84, 99, 99, 99, 99, 99, 99],
                             "population": age.iloc[:, 1]})

prob_age = genProb_NoCond_Range(age_df, "age")

# Race -----------------------------------------------------------------------
race_codes = ["HC01_VC54", "HC01_VC55", "HC01_VC56", "HC01_VC61",
              "HC01_VC69", "HC01_VC74", "HC01_VC75"]
race_list = ["white", "african_american", "american_indian",
             "asian", "native_hawaiian", "some_other_race",
             "two_or_more_races"]
prob_data = pd.DataFrame({"option" : race_list,
                          "value" : censusdata.loc[race_codes, 1].values})
prob_race = genProb_NoCond(prob_data, "race")
# Concatenate probability dataframes -----------------------------------------
agesexrace_prob_df = pd.concat([prob_sex,
                     prob_age,
                     prob_race])

print(agesexrace_prob_df)

agesexrace_prob_df.to_csv(
        path_or_buf="./data-process/probabilities/prob_agesexrace.csv", 
        index = False)
