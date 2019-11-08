#!/usr/bin/env python3
# Generate probabilities for a person to be of a certain age, sex or race.

import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt

# Filter dataset -------------------------------------------------------------
# Read in census data on sex, age and race
censusdata = pd.read_csv('./data/ACS_17_5YR_DP05.csv').transpose()
censusdata = censusdata[censusdata.iloc[:, 0].str.contains('Estimate')]
censusdata.iloc[:, 1] = censusdata.iloc[:, 1].apply(pd.to_numeric)

total_pop = censusdata.loc['HC01_VC03', 1]
# Sex ------------------------------------------------------------------------
male_female = censusdata.loc[['HC01_VC04', 'HC01_VC05'], :]
# Male is 0, Female is 1
prob_sex = male_female.iloc[:, 1].values / total_pop
prob_sex = pd.DataFrame({"property" : "sex",
                         "cond_num" : 0, 
                         "conditional" : None,
                         "option" : ["male", "female"],
                         "prob" : prob_sex})

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

# Construct a system of equations to more closely determine the age 
# distribution.
age_system = np.zeros((age_df.shape[0], 100))
pop_vector = age_df['population']

for i in range(0, age_df.shape[0]):
  age_system[i, age_df.min_age[i]:(age_df.max_age[i] + 1)] = 1

age_solution = np.rint(np.linalg.lstsq(age_system, pop_vector)[0])
prob_age = pd.DataFrame(data = {"property": "age",
                                "cond_num" : 0, 
                                "conditional" : None,
                                "option" : range(0, 100),
                                "prob": age_solution / total_pop})

# Race -----------------------------------------------------------------------
race_codes = ["HC01_VC54", "HC01_VC55", "HC01_VC56", "HC01_VC61",
              "HC01_VC69", "HC01_VC74", "HC01_VC75"]
race_list = ["white", "african_american", "american_indian",
             "asian", "native_hawaiian", "some_other_race",
             "two_or_more_races"]
prob_list = censusdata.loc[race_codes, 1].values / total_pop

prob_race = pd.DataFrame(data = {"property" : "race",
                                 "cond_num" : 0, 
                                 "conditional" : None,
                                 "option" : race_list,
                                 "prob" : prob_list})
# Concatenate probability dataframes -----------------------------------------
agesexrace_prob_df = pd.concat([prob_sex,
                     prob_age,
                     prob_race])

print(agesexrace_prob_df)

agesexrace_prob_df.to_csv(path_or_buf="./data-process/prob_agesexrace.csv", 
                          index = False)
