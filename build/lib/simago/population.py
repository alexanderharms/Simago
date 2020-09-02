import numpy as np
import pandas as pd

from .yamlutils import find_yamls, load_yamls
from .probability import ProbabilityClass
from .probability import check_comb_conditionals, order_probab_objects
from .discdist import draw_disc_values
from .contdist import draw_cont_values

class PopulationClass():
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

        # Initialize list of probability objects
        self.prob_objects = []

    def _generate_population(self):
        self.population = pd.DataFrame(
            {"person_id" : np.linspace(0, self.popsize - 1, self.popsize)})

        self.population['person_id'] = self.population['person_id'].apply(int)

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

    # def update(self, property_name="all", people_id="all"):
    def update(self, property_name="all"):
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
    def export(self, output, nowrite=False):
        # Replace the options with the labels
        population_w_labels = self.population.copy()

        for prob_obj in self.prob_objects:
            if prob_obj.data_type in ['categorical', 'ordinal']:
                prop = prob_obj.property_name
                population_w_labels[prop] = population_w_labels[prop]\
                        .apply(lambda idx: prob_obj.labels[int(idx)])

        print("------------------------")
        print("Generated population:")
        print(population_w_labels)

        print("------------------------")
        # Export population.population
        if nowrite:
            print("Population is not written to disk.")
            pass
        else:
            population_w_labels.to_csv(path_or_buf=output, index = False)
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
        probab_objects.append(ProbabilityClass(y_obj)) 

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
