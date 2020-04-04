import numpy as np
import pandas as pd

from .discdist import draw_disc_values
from .contdist import draw_cont_values

class PopulationClass():
    def __init__(self, popsize, random_seed):
        # Set up random seed
        self.random_seed = random_seed

        # Generate empty population
        self.population = pd.DataFrame(
            {"person_id" : np.linspace(0, popsize - 1, popsize)})

        self.population['person_id'] = self.population['person_id'].apply(int)
        self.popsize = popsize

        # Initialize list of probability objects
        self.prob_objects = []

    def add_property(self, ProbPopulation):
        # Add ProbPopulation object to self.prob_objects list
        self.prob_objects.append(ProbPopulation)

    def remove_property(self, property_name):
        # Remove property
        for prob_obj in self.prob_objects:
            if prob_obj.property_name == property_name:
                self.prob_objects.remove(prob_obj)

    #def add_people(self, num_people):
    #    # Add people to the population by randomly drawing
    #    # TODO: Expand functionality for more control over new people
    #    self.popsize = new_popsize
    #    return

    #def remove_people(self, people_id):
    #    # Remove people by ID
    #    self.popsize = new_popsize
    #    return

    def update(self, property_name="all", people_id="all"):
        # Update people by randomly drawing new values
        # Based on self.population, the conditionals and the
        # probabilities from ProbPopulation, draw a value for this
        # property for all people in the population.
        # TODO: Expand functionality for more control over update
        if property_name == "all":
            for prob_obj in self.prob_objects:
                if prob_obj.data_type in ['categorical', 'ordinal']:
                    self.population = draw_disc_values(prob_obj, 
                                                       self.population, 
                                                       self.random_seed)
                elif prob_obj.data_type == 'continuous':
                    self.population = draw_cont_values(prob_obj,
                                                       self.population, 
                                                       self.random_seed)
        else:
            # Make a singular property name a list to homogenize the next code
            # section.
            if isinstance(property_name, 'str'):
                property_name = [property_name]
            for prob_obj in self.prob_objects:
                if prob_obj.property_name in property_name: 
                    if prob_obj.data_type in ['categorical', 'ordinal']:
                        self.population = draw_disc_values(prob_obj, 
                                                           self.population, 
                                                           self.random_seed)
                    elif prob_obj.data_type == 'continuous':
                        self.population = draw_cont_values(prob_obj,
                                                           self.population, 
                                                           self.random_seed)

def construct_query_string(property_name, option, relation):
    if relation == 'eq':
        relation_string = '=='
    elif relation == 'leq':
        relation_string = '<='
    elif relation == 'geq':
        relation_string = '>='
    elif relation == 'le':
        relation_string = '<'
    elif relation == 'gr':
        relation_string = '>'
    elif relation == 'neq':
        relation_string = '~='

    query_list = [property_name, relation_string, str(option)]
    query_string = ' '.join(query_list)
    return query_string

def get_conditional_population(prob_obj, population, cond_index):
    # - Get the corresponding conditional from prob_obj.conditionals
    conds = prob_obj.conditionals.query("conditional_index == @cond_index")
    # - Get the corr. segment of the population
    # There can be multiple conditionals.
    # Combine them all in one query string
    query_list = [] 
    for index, row in conds.iterrows():
        query_list.append(
                construct_query_string(
                    row['property_name'], row['option'], row['relation']))
    query_string = ' & '.join(query_list)
    population_cond = population.query(query_string)
    # We're only interested in the ID's of the people. 
    population_cond = population_cond[['person_id']]
    return population_cond