#!/usr/bin/env python4
import os
import argparse
from types import MethodType

import yaml

import numpy as np
from scipy import stats
import pandas as pd

def find_yamls(yaml_folder):
    # Gather all the YAML files for the aggregated data in the folder.
    # Return the list of paths to YAML files.
    yaml_filenames = []
    for dirpath, dirs, filenames in os.walk(yaml_folder):
        for filename in filenames:
            print(filename)
            if filename.endswith(".yml") or filename.endswith(".yaml"):
                yaml_filenames.append(filename)
    yaml_filenames = [yaml_folder + fname for fname in yaml_filenames]
    return yaml_filenames

def check_yaml(yaml_object):
    fname = yaml_object['yaml_filename']

    assert 'property_name' in yaml_object.keys(), fname + ', no property defined'
    assert isinstance(yaml_object['property_name'], str),\
            fname + ", incorrect name format"

    assert 'data_type' in yaml_object.keys(), fname + ', no data type defined'
    assert isinstance(yaml_object['data_type'], str),\
            fname + ", incorrect data type"
    assert yaml_object['data_type'] in\
            ['categorical', 'ordinal', 'continuous'],\
            fname + ", invalid data type"

    if yaml_object['data_type'] in ['categorical', 'ordinal']:
        assert 'data_file' in yaml_object.keys(), fname +\
                ', no data file defined'
        assert isinstance(yaml_object['data_file'], str),\
                fname + ", incorrect data filename type"
        assert os.path.isfile(yaml_object['data_file']),\
                fname + ', data file does not exist'
        assert yaml_object['data_file'].endswith('.csv'),\
                fname + ', data file is not a CSV file'
    elif yaml_object['data_type'] == "continuous":
        assert 'pdf_parameters' in yaml_object.keys(),\
                fname + ', no parameters defined'
        assert isinstance(yaml_object['pdf_parameters'], list),\
                fname + ', parameters are not a list'

        assert 'pdf' in yaml_object.keys(),\
                fname + ', no pdf defined'
        assert isinstance(yaml_object['pdf'], str),\
                fname + ', pdf is not a string'

        assert 'pdf_file' in yaml_object.keys(),\
                fname + ', no pdf file defined'
        assert isinstance(yaml_object['pdf_file'], str),\
                fname + ', pdf filename is not a string'
        assert os.path.isfile(yaml_object['pdf_file']),\
                fname + ', pdf file does not exist'
        assert yaml_object['pdf_file'].endswith('.py'),\
                fname + ', pdf file is not a Python file'
        try:
            exec(open(yaml_object['pdf_file'].read()))
        except:
            print(fname + ', pdf file can not be executed')
            quit()


    if 'conditionals' not in yaml_object.keys():
        yaml_object['conditionals'] = None
    else:
        if yaml_object['conditionals'] is not None:
            assert isinstance(yaml_object['conditionals'], str),\
                    fname + ', conditionals not None or a string'
            assert os.path.isfile(yaml_object['conditionals']),\
                    fname + ', conditionals file does not exist'
            assert yaml_object['conditionals'].endswith('.csv'),\
                    fname + ', conditionals files is not a csv'

    return yaml_object


def load_yamls(yaml_filenames):
    yaml_objects = []
    for yaml_filename in yaml_filenames:
        with open(yaml_filename, 'r') as yaml_file:
            try:
                yaml_object = yaml.safe_load(yaml_file)
                print(yaml_object)
            except yaml.YAMLError as exc:
                print(exc)

        yaml_object['yaml_filename'] = yaml_filename
        yaml_objects.append(yaml_object)

    yaml_objects = [check_yaml(obj) for obj in yaml_objects]
    yaml_properties = [obj['property_name'] for obj in yaml_objects]
    assert len(yaml_properties) == len(set(yaml_properties)),\
            "Multiple YAMLs are defined for the same property"

    return yaml_objects

class ProbabilityClass():
    def __init__(self, yaml_object):
        self.property_name = yaml_object['property_name']
        self.data_type = yaml_object['data_type']

        if self.data_type in ["categorical", "ordinal"]:
            self.read_data(yaml_object['data_file'])
            self.generate_probabilities()

        elif self.data_type == "continous":
            self.pdf_parameters = yaml_object['pdf_parameters']
            # Execute the pdf file to define the pdf function
            exec(open(yaml_object['pdf_file']).read())
            self.pdf = MethodType(eval(yaml_object['pdf']),
                                  None, self)
        if yaml_object['conditionals'] is None:
            self.conditionals = None
        else:
            self.read_conditionals(yaml_object['conditionals'])

    def read_data(self, data_file):
        # Only if self.data_type is categorical or ordinal
        # Read CSV
        data_frame = pd.read_csv(data_file)
        # Define list of labels; conversion between index and label name
        # Assign list to self.labels
        if "label" not in data_frame.columns.values:
            # Replace "option" column with an integer, add corresponding
            # label to self.labels
            pass
        else:
            options_labels = data_frame[['option', 'label']]\
                    .drop_duplicates(inplace=False)\
                    .reset_index(drop=True)
            self.labels = [None] * (options_labels.option.max() + 1)
            for idx in range(options_labels.shape[0]):
                self.labels[options_labels.at[idx, 'option']] =\
                        options_labels.at[idx, 'label']
        # Assign the data to self.data
        self.data = data_frame[['option', 'value', 'conditional_index']]
        return

    def read_conditionals(self, conditionals_file):
        # Read CSV
        # Assign data to self.conditionals
        self.conditionals = pd.read_csv(conditionals_file)
        return

    #def least_squares(self):
    #    # For ordinal variables defined as ranges
    #    return

    def generate_probabilities(self):
        # From the data generate the probabilities
        self.probabs = self.data.copy()
        sum_values = self.probabs[['value', 'conditional_index']]\
                .groupby('conditional_index')\
                .sum()\
                .rename(columns={'value': 'value_sum'})
        self.probabs = pd.merge(self.probabs, sum_values, 
                                on='conditional_index')
        self.probabs['value'] = self.probabs['value'] \
                / self.probabs['value_sum']
        self.probabs = self.probabs.drop('value_sum', axis=1)
        self.probabs = self.probabs.rename(columns={'value':'probab'})
        return

class PopulationClass():
    def __init__(self, popsize, rand_seed):
        # Set up random seed

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
                    self.population = draw_disc_values(prob_obj, self.population)
                elif prob_obj.data_type == 'continuous':
                    self.population = draw_cont_values(prob_obj, self.population)
        else:
            # Make a singular property name a list to homogenize the next code
            # section.
            if isinstance(property_name, 'str'):
                property_name = [property_name]
            for prob_obj in self.prob_objects:
                if prob_obj.property_name in property_name: 
                    if prob_obj.data_type in ['categorical', 'ordinal']:
                        self.population = draw_disc_values(prob_obj, self.population)
                    elif prob_obj.data_type == 'continuous':
                        self.population = draw_cont_values(prob_obj, self.population)

def draw_from_disc_distribution(probabs, size):
    sample_rv = stats.rv_discrete(name='sample_rv',
            values=(probabs.option, probabs.probab))
    sample_num = sample_rv.rvs(size = size)
    drawn_values = probabs.option.values[sample_num]
    # TODO: Convert drawn values to labels
    #drawn_values = prob_obj.labels[drawn_values]
    return drawn_values

def draw_from_cont_distribution(pdf, params, size):
    # Repeat pdf(params) to form a list of length size.
    drawn_values = []
    for k in range(size):
        drawn_values.append(pdf(params))
    return drawn_values

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

def draw_cont_values(prob_obj, population):
    if prob_obj.conditionals is None:
        population[prob_obj.property_name] =\
                draw_from_cont_distribution(prob_obj,
                                            prob_obj.probabs,
                                            population.shape[0])
    else:
        for cond_index in prob_obj.conditionals.conditional_index.unique():
            # For every conditional:
            # - Get the corr. segment of the population
            # - Draw the values
            # - Write the values in a list to the correct places

            population_cond = get_conditional_population(prob_obj,
                    population, cond_index)
            population_cond[prob_obj.property_name] =\
                    draw_from_cont_distribution(prob_obj.pdf,
                                                prob_obj.parameters[cond_index],
                                                population_cond.shape[0])
            # - Write the values in a list to the correct places
            # Use a left join for this
            if prob_obj.property_name not in population.columns.values:
                population = pd.merge(population, population_cond, 
                                      how="left", on="person_id")
            else:
                # If the column already exists, update the values in that column.
                # Couple of index tricks are necessary to arrange that.
                population = population.set_index('person_id')
                population_cond = population_cond.set_index('person_id')
                population_cond = population_cond[[prob_obj.property_name]]
                population.update(population_cond)
                population.reset_index(inplace=True, drop=False)
    return population


def draw_disc_values(prob_obj, population):
    if prob_obj.conditionals is None:
        population[prob_obj.property_name] =\
                draw_from_disc_distribution(prob_obj.probabs, 
                                            population.shape[0])
    # Iterate over the various conditionals.
    else:
        for cond_index in prob_obj.conditionals.conditional_index.unique():
            # For every conditional:
            # - Get the corresponding conditional from prob_obj.conditionals
            # - Get the corr. segment of the population
            # - Draw the values
            # - Write the values in a list to the correct places

            # - Get the corr. conditional probabilities from prob_obj.probabs
            probabs_df = prob_obj.probabs\
                    .query("conditional_index == @cond_index")
            # - Get the corr. segment of the population
            population_cond = get_conditional_population(prob_obj,
                    population, cond_index)

            # - Draw the values
            population_cond[prob_obj.property_name] =\
                    draw_from_disc_distribution(probabs_df,
                                                population_cond.shape[0])

            # - Write the values in a list to the correct places
            # Use a left join for this
            if prob_obj.property_name not in population.columns.values:
                population = pd.merge(population, population_cond, 
                                      how="left", on="person_id")
            else:
                # If the column already exists, update the values in that column.
                # Couple of index tricks are necessary to arrange that.
                population = population.set_index('person_id')
                population_cond = population_cond.set_index('person_id')
                population_cond = population_cond[[prob_obj.property_name]]
                population.update(population_cond)
                population.reset_index(inplace=True, drop=False)
    return population

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--popsize", type=int,
                        help="Size of the population")
    parser.add_argument("-o", "--output", type=str,
                        default="./population.csv",
                        help="Output file for the population")
    parser.add_argument("--rand_seed", type=int, default=100,
                        help="Seed for random number generation")
    parser.add_argument("--yaml_folder", type=str,
                        default="./data_yaml/",
                        help="Location of YAML files for the aggregated data.")
    args = parser.parse_args()

    print(args.popsize)
    print(args.rand_seed)

    # Gather YAML files for aggregated data
    yaml_filenames = find_yamls(args.yaml_folder)
    print(yaml_filenames)
    yaml_objects = load_yamls(yaml_filenames)

    # Based on the yaml_objects, create a list of ProbPopulation instances.
    probab_objects = []
    for y_obj in yaml_objects:
        probab_objects.append(ProbabilityClass(y_obj)) 

    for obj in probab_objects:
        print(obj.property_name)
        print(obj.probabs)

    # Generate an empty population
    population = PopulationClass(args.popsize, args.rand_seed)

    # Add variables to the population based on the ProbPopulation instances.
    for obj in probab_objects:
        population.add_property(obj)

    population.update()
    print(population.population)

    # Export population.population
    # population.population.to_csv(path_or_buf=args.output, index = False)
