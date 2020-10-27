import numpy as np
import pandas as pd

from .probability import (
    ContinuousProbabilityClass,
    DiscreteProbabilityClass,
    ProbabilityClass,
    check_comb_conditionals,
    order_probab_objects,
)
from .yamlutils import find_yamls, load_yamls


class PopulationClass:
    """
    Class for the population.


    Attributes
    ----------
    random_seed : int
        Seed for random number generation.
    popsize : int
        Size of the population.
    prob_objects : list
        List of ProbabilityClass objects.
    population : Pandas DataFrame
        DataFrame containing the generated population.

    Methods
    -------
    add_property(ProbPopulation)
        Adds property to PopulationClass.
    remove_property(property_name)
        Removes property from PopulationClass.
    update(property_name="all")
        Updates property.
    export(output, nowrite=False)
        Prints and writes population to file.

    """

    def __init__(self, popsize, random_seed=None):
        """
        Parameters
        ----------
        popsize : int
            Size of population.
        random_seed : int
            Seed for random number generation.

        """

        # Set up random seed
        self.random_seed = random_seed

        # Generate empty population
        assert popsize >= 1, "Population size must be 1 or greater."
        self.popsize = popsize
        self._generate_population()

        # Initialize dictionary of probability objects
        self.prob_objects = {}

    def _generate_population(self):
        self.population = pd.DataFrame(
            {"person_id": np.linspace(0, self.popsize - 1, self.popsize)}
        )

        self.population["person_id"] = self.population["person_id"].apply(int)

    def add_property(self, ProbClass):
        """
        Adds a ProbabilityClass object to the PopulationClass object.

        Parameters
        ----------
        ProbClass : ProbabilityClass object
            ProbabilityClass object for the property.
        """
        if not isinstance(ProbClass, ProbabilityClass):
            # Check that property is a ProbabilityClass
            print("Added property is not an instance of ProbabilityClass")
        elif ProbClass.property_name in self.prob_objects.keys():
            # Check that property is not already defined for the
            # PopulationClass.
            print("Property is already defined in the PopulationClass"
                  + " instance.")
        else:
            # Add ProbPopulation object to self.prob_objects list
            self.prob_objects[ProbClass.property_name] = ProbClass

    def remove_property(self, property_name):
        # Remove property
        if property_name in self.prob_objects.keys():
            del self.prob_objects[property_name]
        else:
            print("Property is not defined in the PopulationClass instance.")

    # def update(self, property_name="all", people_id="all"):
    def update(self, property_name="all"):
        # Update people by randomly drawing new values
        # Based on self.population, the conditionals and the
        # probabilities from ProbPopulation, draw a value for this
        # property for all people in the population.
        # TODO: Expand functionality for more control over update
        if property_name == "all":
            for prob_obj in self.prob_objects.values():
                self.population = prob_obj.draw_values(self)
        else:
            # Make a singular property name a list to homogenize the next code
            # section.
            if isinstance(property_name, "str"):
                property_name = [property_name]
            for prob_obj in self.prob_objects.values():
                self.populuation = prob_obj.draw_values(self)

    def get_conditional_population(self, property_name, cond_index):
        prob_obj = self.prob_objects[property_name]
        # - Get the corresponding conditional from prob_obj.conditionals
        conds = prob_obj.conditionals.query("conditional_index == @cond_index")
        # - Get the corr. segment of the population
        # There can be multiple conditionals.
        # Combine them all in one query string
        query_list = []
        for index, row in conds.iterrows():
            query_list.append(
                construct_query_string(
                    row["property_name"], row["option"], row["relation"]
                )
            )
        query_string = " & ".join(query_list)
        population_cond = self.population.query(query_string)
        # We're only interested in the ID's of the people.
        population_cond = population_cond[["person_id"]]
        return population_cond

    def export(self, output, nowrite=False):
        # Replace the options with the labels
        population_w_labels = self.population.copy()

        for prob_obj in self.prob_objects.values():
            if prob_obj.data_type in ["categorical", "ordinal"]:
                prop = prob_obj.property_name
                population_w_labels[prop] = population_w_labels[prop].apply(
                    lambda idx: prob_obj.labels[int(idx)]
                )

        print("------------------------")
        print("Generated population:")
        print(population_w_labels)

        print("------------------------")
        # Export population.population
        if nowrite:
            print("Population is not written to disk.")
            pass
        else:
            population_w_labels.to_csv(path_or_buf=output, index=False)
            print("Population is written to %s" % (output))


def generate_population(popsize, yaml_folder, rand_seed=None):
    """
    Generate population.

    Parameters
    ----------
    popsize : int
        Size of population.
    yaml_folder : string
        Folder with settings YAML files.
    random_seed : int
        Seed for random number generation.

    Returns
    -------
    PopulationClass object

    """
    print("Population size: %d" % (popsize))
    if rand_seed is None:
        print("No random seed defined")
    else:
        print("Random seed: %d" % (rand_seed))
    np.random.seed(rand_seed)

    print("------------------------")
    # Gather YAML files for aggregated data
    yaml_filenames = find_yamls(yaml_folder)
    yaml_objects = load_yamls(yaml_filenames)

    # Based on the yaml_objects, create a list of ProbabilityClass instances.
    probab_objects = []
    for y_obj in yaml_objects:
        if y_obj["data_type"] in ["categorical", "ordinal"]:
            probab_objects.append(DiscreteProbabilityClass(y_obj))
        elif y_obj["data_type"] in ["continuous"]:
            probab_objects.append(ContinuousProbabilityClass(y_obj))

    print("------------------------")
    print("Defined properties:")
    print([obj.property_name for obj in probab_objects])

    check_comb_conditionals(probab_objects)

    probab_objects = order_probab_objects(probab_objects)

    # Generate an empty population
    population = PopulationClass(popsize, rand_seed)

    # Add variables to the population based on the ProbabilityClass instances.
    for obj in probab_objects:
        population.add_property(obj)

    return population


def construct_query_string(property_name, option, relation):
    if relation == "eq":
        relation_string = "=="
    elif relation == "leq":
        relation_string = "<="
    elif relation == "geq":
        relation_string = ">="
    elif relation == "le":
        relation_string = "<"
    elif relation == "gr":
        relation_string = ">"
    elif relation == "neq":
        relation_string = "~="

    query_list = [property_name, relation_string, str(option)]
    query_string = " ".join(query_list)
    return query_string
