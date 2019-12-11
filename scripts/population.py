#!/usr/bin/env python3
import numpy as np
import pandas as pd
from scipy import stats

### Generate list of 'empty people'
# Generate a data frame with only the person id's
def generateEmptyPeople(total_pop):
    # Generate dataframe with a unique id per person
    population_dataframe = pd.DataFrame({"person_id" :
                                         np.linspace(0, total_pop - 1, 
                                                     total_pop)})

    population_dataframe['person_id'] = population_dataframe.person_id.apply(int)
    return population_dataframe

def addProperties(population_dataframe, properties, 
                  prob_df, num_properties):
    # In the column 'conditional' the condtional should be arranged 
    # as a dictionary of each property and their constraints.
    # So a group of males of 18 and 19 year old should have the 
    # conditional {'sex' : ['male'], 'age' : [18, 19]}.
    for prop in set_properties:
        # Add empty column for the property
        population_dataframe = population_dataframe.assign(**{prop : None})
        # Select probability dataframe from prob_df
        prob_selection = prob_df.query("property == @prop")
        #print(prob_selection)
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
                    #print(cond_property)
                    #print(cond_option)
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
        if prop in num_properties:
            population_dataframe[prop] = \
                    pd.to_numeric(population_dataframe[prop])
    return population_dataframe
