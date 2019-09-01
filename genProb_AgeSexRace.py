#!/usr/bin/env python3
# Generate probabilities for a person to be of a certain age, sex or race.

import pandas as pd
import numpy as np
from scipy.stats import bernoulli
from scipy import stats
import matplotlib.pyplot as plt

# Filter dataset -------------------------------------------------------------
# Read in census data on sex, age and race
censusdata = pd.read_csv('./Data/ACS_17_5YR_DP05/ACS_17_5YR_DP05.csv').transpose()
censusdata = censusdata[censusdata.iloc[:, 0].str.contains('Estimate')]
censusdata.iloc[:, 1] = censusdata.iloc[:, 1].apply(pd.to_numeric)

# Sex ------------------------------------------------------------------------
total_pop = censusdata.loc['HC01_VC03', 1]
male_female = censusdata.loc[['HC01_VC04', 'HC01_VC05'], :]
# Male is 0, Female is 1
prob_sex = male_female.iloc[:, 1].values / total_pop
sim_pop = bernoulli.rvs(prob_sex[1], size=int(total_pop))

# Age -------------------------------------------------------------------------
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
age = pd.DataFrame(data = {"age": range(0, 100),
                           "population": age_solution})

prob_age = age.iloc[:, 1].values / total_pop

xk = np.arange(0, 100)
pk = prob_age

age_rv = stats.rv_discrete(name='age_rv', values=(xk, pk))
sim_pop = age_rv.rvs(size=int(total_pop))

tot_sim_pop = 0
for k in range(0, 5):
  tot_sim_pop += sum(sim_pop == k)
#print(tot_sim_pop)

plt.plot(xk, pk * total_pop)

# Race -----------------------------------------------------------------------

