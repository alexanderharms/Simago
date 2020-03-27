#!/usr/bin/env python3

import numpy as np
import pandas as pd
from scripts.probabilities import buildProbDf

# Test probabilties for income
# We test with a uniform distribution
#median_income = 40000
#width = 80000
#upper_bound = median_income + 0.5 * width
#lower_bound = median_income - 0.5 * width
#prob_income = buildProbDf("personal_income", 
#        [[lower_bound, upper_bound]], 'uniform_distribution')

median_income = 34420
mean_income = 1.5 * 34420
mu = np.log(median_income)
sigma = np.sqrt(2 * np.log(np.exp(-1 * mu) * mean_income))
prob_income = buildProbDf("personal_income", 
        [[mu, sigma]], 'lognorm_distribution')

prob_income.to_csv("./data-process/probabilities/prob_personalincome.csv",
        index = False)
