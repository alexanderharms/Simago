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

def addDiscreteProperties(options, probs, pop_size):
    option_numbers = np.linspace(0, 
            len(options) - 1,
            len(options))
    sample_rv = stats.rv_discrete(name='sample_rv', 
            values=(option_numbers, probs))
    sample_num = sample_rv.rvs(size = pop_size)

    return options[sample_num]

def uniform_distribution(values, pop_size):
    # Draw pop_size amount samples from uniform 
    # distribution
    lower_bound = values[0]
    upper_bound = values[1]
    samples = np.random.uniform(low = lower_bound,
            high = upper_bound,
            size = pop_size)

    return samples

def addContinuousProperties(values, distribution, pop_size):
    # For the generation of continous properties, 
    # the distribution should be defined as a Python function,
    # and the values for the function (mean, variance etc)
    # should be in the list 'values'. 
    possibles = globals().copy()
    possibles.update(locals())
    distribution_func = possibles.get(distribution)
    if not distribution_func:
         raise NotImplementedError("Distribution %s not implemented" %
                 distribution)
    samples = distribution_func(values, pop_size)
    return samples

def addProperties(population_dataframe, set_properties, 
                  prob_df, num_properties):
    # In the column 'conditional' the condtional should be arranged 
    # as a dictionary of each property and their constraints.
    # So a group of males of 18 and 19 year old should have the 
    # conditional {'sex' : ['male'], 'age' : [18, 19]}.
    for prop in set_properties:
        print(prop)
        # Add empty column for the property
        population_dataframe = population_dataframe.assign(**{prop : None})
        # Select probability dataframe from prob_df
        prob_selection = prob_df.query("property == @prop")
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
                    cond_population = \
                            cond_population[
                                    cond_population[cond_property].apply(str) 
                                    == str(cond_option)]
                cond_population = cond_population.person_id.values

            if prob_cond_selection['option'].shape[0] > 1 \
                    or prob_cond_selection['prob'] is 1:
                # Discrete distribution
                population_dataframe.loc[cond_population, prop] = \
                        addDiscreteProperties(
                                prob_cond_selection.option.values,
                                prob_cond_selection.prob.values,
                                len(cond_population))
            else:
                # Continuous distribution
                population_dataframe.loc[cond_population, prop] = \
                        addContinuousProperties(
                                eval(prob_cond_selection.option.values[0]),
                                prob_cond_selection.prob.values[0],
                                len(cond_population))

        # Generate list of outcomes out of the options for the property
        # for the selection of the dataframe.

        # Change numeric quantities to numeric
        if prop in num_properties:
            population_dataframe[prop] = \
                    pd.to_numeric(population_dataframe[prop])
    return population_dataframe
