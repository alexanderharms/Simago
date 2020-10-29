"""
Classes and functions surrounding the ProbabilityClass objects.
"""
import importlib

from abc import ABC

import numpy as np
import pandas as pd

from scipy import stats


class ProbabilityClass(ABC):
    """
    Abstract base class; inherited versions of this class contain attributes
    and methods surrounding the properties of the population and their
    stochastic behaviour.

    Attributes
    ----------
    property_name : string
    data_type : string
    conditionals : DataFrame

    """
    def __init__(self, yaml_object):
        self.property_name = yaml_object["property_name"]
        self.data_type = yaml_object["data_type"]

        if yaml_object["conditionals"] is None:
            self.conditionals = None
        else:
            self.read_conditionals(yaml_object["conditionals"])

    def read_conditionals(self, conditionals_file):
        """
        Reads and checks the conditionals file from a CSV file.

        Parameters
        ----------
        conditionals_file : string
            Filename for the CSV file.
        """
        # Read CSV
        # Assign data to self.conditionals
        self.conditionals = pd.read_csv(conditionals_file)
        assert sorted(self.conditionals.columns.tolist()) == sorted(
            [
                "conditional_index",
                "property_name",
                "option",
                "relation",
            ]
        ), (
            str(self.property_name) + ", "
            "Conditionals file does not contain the necessary columns"
        )


class DiscreteProbabilityClass(ProbabilityClass):
    """
    DiscreteProbabilityClass contains attributes and methods surrounding the
    properties with discrete probability distributions.
    """
    def __init__(self, yaml_object):
        super(DiscreteProbabilityClass, self).__init__(yaml_object)

        self.read_data(yaml_object["data_file"])
        self.generate_probabilities()

    def read_data(self, data_file):
        """Read in data for discrete probability distributions."""
        # Only if self.data_type is categorical or ordinal
        # Read CSV
        data_frame = pd.read_csv(data_file)
        assert sorted(data_frame.columns.tolist()) == sorted(
            [
                "option",
                "value",
                "label",
                "conditional_index",
            ]
        ), "Data file does not contain the necessary columns"
        # Define list of labels; conversion between index and label name
        # Assign list to self.labels
        options_labels = (
            data_frame[["option", "label"]]
            .drop_duplicates(inplace=False)
            .reset_index(drop=True)
        )
        self.labels = [None] * (options_labels.option.max() + 1)
        for idx in range(options_labels.shape[0]):
            self.labels[options_labels.at[idx, "option"]] = options_labels.at[
                idx, "label"
            ]
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
        self.data = (
            data_frame[["option", "value", "conditional_index"]]
            .drop_duplicates(inplace=False)
            .reset_index(drop=True)
        )

    def generate_probabilities(self):
        """Generate probabilities through normalization of the data."""
        # From the data generate the probabilities
        self.probabs = self.data.copy()
        sum_values = (
            self.probabs[["value", "conditional_index"]]
            .groupby("conditional_index")
            .sum()
            .rename(columns={"value": "value_sum"})
        )
        self.probabs = pd.merge(
            self.probabs, sum_values, on="conditional_index"
        )
        self.probabs["value"] = (
            self.probabs["value"] / self.probabs["value_sum"]
        )
        self.probabs = self.probabs.drop("value_sum", axis=1)
        self.probabs = self.probabs.rename(columns={"value": "probab"})

    def draw_values(self, pop_obj):
        """
        Draw values for discrete, i.e. categorical and ordinal, variables.

        Parameters
        ----------
        pop_obj : PopulationClass

        Returns
        -------
        DataFrame

        """
        population = pop_obj.population

        if self.conditionals is None:
            population[
                self.property_name
            ] = draw_from_disc_distribution(
                self.probabs, pop_obj.population.shape[0], pop_obj.random_seed
            )
        # Iterate over the various conditionals.
        else:
            for cond_index in self.conditionals.conditional_index.unique():
                # For every conditional:
                # - Get the corresponding conditional from
                #     self.conditionals
                # - Get the corr. segment of the population
                # - Draw the values
                # - Write the values in a list to the correct places

                # - Get the corr. conditional probabilities from self.probabs
                probabs_df = self.probabs.query(
                    "conditional_index == @cond_index"
                )
                # - Get the corr. segment of the population
                population_cond = pop_obj.get_conditional_population(
                    self.property_name, cond_index
                )

                # - Draw the values
                population_cond[
                    self.property_name
                ] = draw_from_disc_distribution(
                    probabs_df, population_cond.shape[0], pop_obj.random_seed
                )

                # - Write the values in a list to the correct places
                # Use a left join for this
                if self.property_name not in population.columns.values:
                    population = pd.merge(
                        population,
                        population_cond,
                        how="left",
                        on="person_id",
                    )
                else:
                    # If the column already exists, update the values in that
                    # column. A couple of index tricks are necessary to arrange
                    # that.
                    population = population.set_index("person_id")
                    population_cond = population_cond.set_index("person_id")
                    population_cond = population_cond[[self.property_name]]
                    population.update(population_cond)
                    population.reset_index(inplace=True, drop=False)
        return population


def draw_from_disc_distribution(probabs, size, random_seed):
    """
    Draw from a discrete distribution.

    Parameters
    ----------
    probabs : Pandas DataFrame
    size : int
        Number of values drawn from distribution.
    random_seed : int
        Seed for random number generation.

    Returns
    -------
    list
        List of drawn values.

    """

    sample_rv = stats.rv_discrete(
        name="sample_rv", values=(probabs.option, probabs.probab)
    )
    sample_num = sample_rv.rvs(size=size)
    drawn_values = probabs.option.values[sample_num]
    return drawn_values


class ContinuousProbabilityClass(ProbabilityClass):
    """
    ContinuousProbabilityClass contains attributes and methods surrounding the
    properties with continuous probability distributions.
    """
    def __init__(self, yaml_object):
        super(ContinuousProbabilityClass, self).__init__(yaml_object)

        self.pdf_parameters = yaml_object["pdf_parameters"]
        # Execute the pdf file to define the pdf function
        module_name = yaml_object["pdf_file"][2:-3].replace("/", ".")
        imported_pdfs = importlib.import_module(module_name)
        pdf_function = getattr(imported_pdfs, yaml_object["pdf"])
        self.pdf = pdf_function

    def draw_values(self, pop_obj):
        """
        Draw values for continuous variables.

        Parameters
        ----------
        pop_obj : PopulationClass

        Returns
        -------
        DataFrame

        """
        population = pop_obj.population

        if self.conditionals is None:
            population[self.property_name] = draw_from_cont_distribution(
                self.pdf,
                self.pdf_parameters[0],
                population.shape[0],
                pop_obj.random_seed,
            )
        else:
            for cond_index in self.conditionals.conditional_index.unique():
                # For every conditional:
                # - Get the corr. segment of the population
                # - Draw the values
                # - Write the values in a list to the correct places

                population_cond = pop_obj.get_conditional_population(
                    self.property_name, cond_index
                )
                population_cond[
                    self.property_name
                ] = draw_from_cont_distribution(
                    self.pdf,
                    self.pdf_parameters[cond_index],
                    population_cond.shape[0],
                    pop_obj.random_seed,
                )
                # - Write the values in a list to the correct places
                # Use a left join for this
                if self.property_name not in population.columns.values:
                    population = pd.merge(
                        population, population_cond, how="left", on="person_id"
                    )
                else:
                    # If the column already exists, update the values in that
                    # column.
                    # Couple of index tricks are necessary to arrange that.
                    population = population.set_index("person_id")
                    population_cond = population_cond.set_index("person_id")
                    population_cond = population_cond[[self.property_name]]
                    population.update(population_cond)
                    population.reset_index(inplace=True, drop=False)
        return population


def draw_from_cont_distribution(pdf, parameters, size, random_seed):
    """
    Draw from a continuous distribution.

    Parameters
    ----------
    pdf : function
        Probability distribution function.
    parameters : list
        List of parameters for the probability distribution function.
    size : int
        Number of values drawn from distribution.
    random_seed : int
        Seed for random number generation.

    Returns
    -------
    list
        List of values drawn from the probability distribution function.

    """

    dist_instance = pdf(parameters)
    drawn_values = dist_instance.rvs(size=size)
    return drawn_values


# def cumulative_properties(probab_objects):
#     properties = [None] * len(probab_objects)
#     for idx, obj in enumerate(probab_objects):
#         if idx == 0:
#             properties[idx] = [obj.property_name]
#         else:
#             properties[idx] = properties[idx - 1] + [obj.property_name]
#     return properties


def order_probab_objects(probab_objects):
    """
    Orders ProbabilityClass objects so all properties that do not depend on
    others are handled first.
    """
    # There should be at least one property without conditionals.
    cond_bool = [
        True if x.conditionals is None else False for x in probab_objects
    ]
    assert any(
        cond_bool
    ), "There should be at least one property without conditionals"

    # Start ordering the list of probab_objects with all the properties with
    # obj.conditionals is None.
    probab_none = [probab_objects[i] for i, x in enumerate(cond_bool) if x]
    # probab_none_prop = [obj.property_name for obj in probab_none]

    probab_cond = [probab_objects[i] for i, x in enumerate(cond_bool) if not x]
    # probab_cond_prop = [obj.property_name for obj in probab_cond]

    probab_objects = probab_none + probab_cond

    return probab_objects


def check_comb_conditionals(probab_objects):
    """
    Checks the ProbabilityClass objects for impossible situations, e.g.
    properties that are dependent on non-defined properties.
    """
    properties = []
    for obj in probab_objects:
        properties.append(obj.property_name)

    for obj in probab_objects:
        if obj.conditionals is not None:
            assert obj.conditionals.property_name.values.all() in properties, (
                obj.property_name
                + ", conditionals references undefined "
                + "properties"
            )
            if obj.data_type == "continuous":
                assert len(
                    np.unique(obj.conditionals.conditional_index)
                ) == len(obj.pdf_parameters), (
                    obj.property_name
                    + ", not enough PDF parameters for "
                    + "the amount of conditionals"
                )

    # There should be at least one property without conditionals.
    cond_bool = [
        True if x.conditionals is None else False for x in probab_objects
    ]
    assert any(cond_bool), (
        "At least one of the properties should be without" + " conditionals."
    )

    # # Start ordering the list of probab_objects with all the properties with
    # # obj.conditionals is None.
    # probab_none = [probab_objects[i] for i, x in enumerate(cond_bool) if x]
    # probab_none_prop = [obj.property_name for obj in probab_none]

    # probab_cond = [probab_objects[i] for i, x in
    #                enumerate(cond_bool) if not x]
    # probab_cond_prop = [obj.property_name for obj in probab_cond]

    #  # Create a graph of the dependencies.
    #  # Check if there are cycles in the graph. Assert that there are no
    #  # cycles.
    #  probab_graph = dict()
    #  for obj in probab_cond:
    #      probab_graph[obj.property_name] = \
    #              np.unique(obj.conditionals.property_name).tolist()

    #  for key in probab_graph.keys():
    #      # If all the values of probab_graph are have no conditionals,
    #      # the graph cannot be simplified further.
    #      probab_graph_values = probab_graph[key]
    #      while not all(item in probab_none_prop for item in
    #                    probab_graph_values):
    #          assert key not in probab_graph_values, \
    #              'Circular dependency, ' + key

    #          probab_graph_values = [probab_graph[k] for k in
    #                                 probab_graph_values if k not in
    #                                 probab_none_prop]
    #          probab_graph_values = [item for sublist in probab_graph_values
    #                  for item in sublist]
    return
