import numpy as np
import pandas as pd
import pytest

from simago.population import PopulationClass, construct_query_string
from simago.probability import (
    ContinuousProbabilityClass,
    DiscreteProbabilityClass,
)
from simago.yamlutils import find_yamls, load_yamls


def test_PopClass_init():
    """
    Test that PopulationClass is initialized properly.
    """
    popsize = 100
    random_seed = 100
    pop_class = PopulationClass(popsize, random_seed)

    test_population = pd.DataFrame(
        {"person_id": np.linspace(0, popsize - 1, popsize)}
    )
    test_population["person_id"] = test_population["person_id"].apply(int)

    assert pop_class.popsize == popsize
    assert pop_class.random_seed == random_seed
    assert pop_class.population.equals(test_population)


def test_PopClass_init_noseed():
    popsize = 100
    pop_class = PopulationClass(popsize)

    assert pop_class.random_seed is None


def test_PopClass_popsize_edge():
    """
    Test handling of edge cases for initializing a PopulationClass.
    """
    # Test if AssertionError is triggered if popsize is 0.
    popsize = 0
    random_seed = 100
    with pytest.raises(AssertionError):
        pop_class = PopulationClass(popsize, random_seed)

    popsize = 1
    pop_class = PopulationClass(popsize, random_seed)

    test_population = pd.DataFrame({"person_id": np.linspace(0, 0, 1)})
    test_population["person_id"] = test_population["person_id"].apply(int)

    assert pop_class.population.equals(test_population)


def test_PopClass_add_property():
    """
    Test adding a property with PopulationClass.add_property.
    - Test for regular ProbabilityClass.
    - Check that property is a ProbabilityClass
    - Check that property is not already defined for the PopulationClass.
    """
    # Define test population
    popsize = 100
    random_seed = 100
    pop_class = PopulationClass(popsize, random_seed)
    # Check if pop_class.prob_objects is an empty dictionary at the start
    assert isinstance(pop_class.prob_objects, dict) and not \
        bool(pop_class.prob_objects)

    # Define test ProbabilityClass objects
    test_prob_objects = {}
    yaml_folder = "./tests/testdata/PopulationClass/"
    yaml_filenames = find_yamls(yaml_folder)
    yaml_objects = load_yamls(yaml_filenames)
    probab_objects = []
    for y_obj in yaml_objects:
        if y_obj["data_type"] in ["categorical", "ordinal"]:
            probab_objects.append(DiscreteProbabilityClass(y_obj))
        elif y_obj["data_type"] in ["continuous"]:
            probab_objects.append(ContinuousProbabilityClass(y_obj))
    for probab_object in probab_objects:
        pop_class.add_property(probab_object)
        test_prob_objects[probab_object.property_name] = \
            probab_object
    # Test behaviour for correct input
    assert pop_class.prob_objects == test_prob_objects
    # Test if prob_object is not a ProbabilityClass object
    pop_class.add_property("new_variable")
    assert pop_class.prob_objects == test_prob_objects
    # Test if prob_object already exists
    pop_class.add_property(probab_objects[0])
    assert pop_class.prob_objects == test_prob_objects


# TODO: Test removing a property with PopulationClass.remove_property.
# Test with a correct property_name.
# Assert property_name is a string.
# Check if property_name is defined within the PopulationClass.

# def test_PopClass_update_disc_all():
#     # TODO: Test update for a discrete variable
#
# def test_PopClass_update_cont_all():
#     # TODO: Test update for a continuous variable
#
# def test_PopClass_update_disc_specific():
#     # TODO: Test update for a discrete variable
#
# def test_PopClass_update_cont_specific():
#     # TODO: Test update for a continuous variable

# TODO: Test the function generate_population.


def test_construct_query_string():
    option = 0
    property_name = "sex"
    relation_list = ["eq", "leq", "geq", "le", "gr", "neq"]

    test_list = [
        "sex == 0",
        "sex <= 0",
        "sex >= 0",
        "sex < 0",
        "sex > 0",
        "sex ~= 0",
    ]
    query_list = [None] * len(relation_list)
    for k, rel in enumerate(relation_list):
        query_list[k] = construct_query_string(property_name, option, rel)

    assert query_list == test_list
