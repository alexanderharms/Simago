#!/usr/bin/env python3
import numpy as np
import pandas as pd
from scipy import stats

# Get total population number
censusdata = pd.read_csv('./data/ACS_17_5YR_DP05.csv').transpose()
censusdata = censusdata[censusdata.iloc[:, 0].str.contains('Estimate')]
censusdata.iloc[:, 1] = censusdata.iloc[:, 1].apply(pd.to_numeric)

total_pop = censusdata.loc['HC01_VC03', 1]

# Generate dataframe with a unique id per person
population_dataframe = pd.DataFrame({"person_id" :
                                     np.linspace(0, total_pop - 1, total_pop)})

population_dataframe['person_id'] = population_dataframe.person_id.apply(int)
# Load discrete probabilities
prob_agesexrace = pd.read_csv("./data-process/prob_agesexrace.csv")
prob_education = pd.read_csv("./data-process/prob_education.csv")

# Concatenate into one dataframe
prob_df = pd.concat([prob_agesexrace, prob_education])

# set_properties = set(prob_df.property.values)
set_properties = ["sex", "age", "race", "education"]


# In the column 'conditional' the condtional should be arranged 
# as a dictionary of each property and their constraints.
# So a group of males of 18 and 19 year old should have the 
# conditional {'sex' : ['male'], 'age' : [18, 19]}.
for prop in set_properties:
    # Add empty column for the property
    population_dataframe = population_dataframe.assign(**{prop : None})
    # Select probability dataframe from prob_df
    prob_selection = prob_df.query("property == @prop")
    print(prob_selection)
    for cond_sum_selection in set(prob_selection.cond_num.values):
        # Select a conditional
        prob_cond_selection = prob_selection.\
                query("cond_num == @cond_sum_selection")
        conditional = str(prob_cond_selection.conditional.values[0])
        # Make selection of population dataframe based on the conditionals
        # in the form of indices
        if conditional == 'nan':
            cond_population = population_dataframe.person_id.values
        else:
            cond_population = population_dataframe
            conditional = eval(conditional)
            for cond_property, cond_option in conditional.items():
                print(cond_property)
                print(cond_option)
                cond_population = cond_population[cond_population[cond_property] 
                                                  == str(cond_option)]
            #print(cond_population)
            cond_population = cond_population.person_id.values

        prob_cond_selection_option = prob_cond_selection.option.values
       
        prob_cond_selection_prob = prob_cond_selection.prob.values

        option_numbers = np.linspace(0, 
                len(prob_cond_selection_option) - 1,
                len(prob_cond_selection_option))
        sample_rv = stats.rv_discrete(name='sample_rv', 
                values=(option_numbers,
                        prob_cond_selection_prob))
        sample_num = sample_rv.rvs(size = len(cond_population))

        population_dataframe.loc[cond_population, prop] = \
                prob_cond_selection_option[sample_num]

    # Generate list of outcomes out of the options for the property
    # for the selection of the dataframe.

# Change numeric quantities to numeric
population_dataframe['age'] = pd.to_numeric(population_dataframe['age'])
print(population_dataframe.head())

print(population_dataframe.query("age >= 25 and race == 'white'").shape)

population_dataframe.to_csv(path_or_buf="data-process/population.csv",
        index = False)

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


