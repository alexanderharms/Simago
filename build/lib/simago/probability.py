import importlib
import numpy as np
import pandas as pd

class ProbabilityClass():
    def __init__(self, yaml_object):
        self.property_name = yaml_object['property_name']
        self.data_type = yaml_object['data_type']

        if self.data_type in ["categorical", "ordinal"]:
            self.read_data(yaml_object['data_file'])
            self.generate_probabilities()

        elif self.data_type == "continuous":
            self.pdf_parameters = yaml_object['pdf_parameters']
            # Execute the pdf file to define the pdf function
            module_name = yaml_object['pdf_file'][2:-3].replace('/','.')
            imported_pdfs = importlib.import_module(module_name)
            pdf_function = getattr(imported_pdfs, yaml_object['pdf'])
            self.pdf = pdf_function

        if yaml_object['conditionals'] is None:
            self.conditionals = None
        else:
            self.read_conditionals(yaml_object['conditionals'])

    def read_data(self, data_file):
        # Only if self.data_type is categorical or ordinal
        # Read CSV
        data_frame = pd.read_csv(data_file)
        assert data_frame.columns.tolist() ==\
                ['option', 'value', 'label', 'conditional_index'],\
                'Data file does not contain the necessary columns'
        # Define list of labels; conversion between index and label name
        # Assign list to self.labels
        options_labels = data_frame[['option', 'label']]\
                .drop_duplicates(inplace=False)\
                .reset_index(drop=True)
        self.labels = [None] * (options_labels.option.max() + 1)
        for idx in range(options_labels.shape[0]):
            self.labels[options_labels.at[idx, 'option']] =\
                    options_labels.at[idx, 'label']
        # if "label" not in data_frame.columns.values:
        #     # Replace "option" column with an integer, add corresponding
        #     # label to self.labels
        #     pass
        # else:
        #     options_labels = data_frame[['option', 'label']]\
        #             .drop_duplicates(inplace=False)\
        #             .reset_index(drop=True)
        #     self.labels = [None] * (options_labels.option.max() + 1)
        #     for idx in range(options_labels.shape[0]):
        #         self.labels[options_labels.at[idx, 'option']] =\
        #                 options_labels.at[idx, 'label']

        # Assign the data to self.data
        self.data = data_frame[['option', 'value', 'conditional_index']]\
                .drop_duplicates(inplace=False)\
                .reset_index(drop=True)

    def read_conditionals(self, conditionals_file):
        # Read CSV
        # Assign data to self.conditionals
        self.conditionals = pd.read_csv(conditionals_file)
        assert self.conditionals.columns.tolist() ==\
                ['conditional_index', 'property_name', 'option', 'relation'],\
                str(self.property_name) + ', ' \
                'Conditionals file does not contain the necessary columns'

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

# def cumulative_properties(probab_objects):
#     properties = [None] * len(probab_objects)
#     for idx, obj in enumerate(probab_objects):
#         if idx == 0:
#             properties[idx] = [obj.property_name]
#         else: 
#             properties[idx] = properties[idx - 1] + [obj.property_name]
#     return properties

def order_probab_objects(probab_objects):
    # There should be at least one property without conditionals.
    cond_bool = [True if x.conditionals is None else False 
                 for x in probab_objects]
    assert any(cond_bool),\
            'There should be at least one property without conditionals'

    # Start ordering the list of probab_objects with all the properties with
    # obj.conditionals is None.
    probab_none = [probab_objects[i] for i, x in enumerate(cond_bool) if x]
    probab_none_prop = [obj.property_name for obj in probab_none]

    probab_cond = [probab_objects[i] for i, x in enumerate(cond_bool) if not x]
    probab_cond_prop = [obj.property_name for obj in probab_cond]
    
    probab_objects = probab_none + probab_cond
    
    return probab_objects

def check_comb_conditionals(probab_objects):
    properties = []
    for obj in probab_objects:
        properties.append(obj.property_name)

    for obj in probab_objects:
        if obj.conditionals is not None:
            assert obj.conditionals.property_name.values.all() in properties,\
                    obj.property_name + ', conditionals references undefined '\
                    + 'properties'
            if obj.data_type == "continuous":
                assert len(np.unique(obj.conditionals.conditional_index))\
                        == len(obj.pdf_parameters),\
                        obj.property_name + ', not enough PDF parameters for '\
                        + 'the amount of conditionals'

    # There should be at least one property without conditionals.
    cond_bool = [True if x.conditionals is None else False 
                 for x in probab_objects]
    assert any(cond_bool), 'At least one of the properties should be without'\
            + ' conditionals.'

#    # Start ordering the list of probab_objects with all the properties with
#    # obj.conditionals is None.
#    probab_none = [probab_objects[i] for i, x in enumerate(cond_bool) if x]
#    probab_none_prop = [obj.property_name for obj in probab_none]
#
#    probab_cond = [probab_objects[i] for i, x in enumerate(cond_bool) if not x]
#    probab_cond_prop = [obj.property_name for obj in probab_cond]

#     # Create a graph of the dependencies.
#     # Check if there are cycles in the graph. Assert that there are no cycles.
#     probab_graph = dict()
#     for obj in probab_cond:
#         probab_graph[obj.property_name] = \
#                 np.unique(obj.conditionals.property_name).tolist()
# 
#     for key in probab_graph.keys():
#         # If all the values of probab_graph are have no conditionals, the graph
#         # cannot be simplified further.
#         probab_graph_values = probab_graph[key]
#         while not all(item in probab_none_prop for item in probab_graph_values):
#             assert key not in probab_graph_values, 'Circular dependency, ' + key
#             
#             probab_graph_values = [probab_graph[k] for k in probab_graph_values 
#                     if k not in probab_none_prop]
#             probab_graph_values = [item for sublist in probab_graph_values 
#                     for item in sublist]
    return 

