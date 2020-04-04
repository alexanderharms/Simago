import importlib
import pandas as pd

class ProbabilityClass():
    # TODO: Method to convert generated options back to the labels
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

    def read_conditionals(self, conditionals_file):
        # Read CSV
        # Assign data to self.conditionals
        self.conditionals = pd.read_csv(conditionals_file)

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
