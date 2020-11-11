"""
Tests for the file simago/population.py.
"""
import os

import numpy as np
import pandas as pd
import pytest

from pandas._testing import assert_frame_equal

from simago.population import (
    PopulationClass,
    construct_query_string,
    generate_population,
)
from simago.probability import (
    ContinuousProbabilityClass,
    DiscreteProbabilityClass,
)
from simago.yamlutils import find_yamls, load_yamls


def test_PopClass_init():
    """
    PopulationClass is initialized properly for
    - Reasonable population size and defined random seed.
    - Reasonable population size and undefined random seed.
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

    popsize = 100
    pop_class = PopulationClass(popsize)

    assert pop_class.random_seed is None


def test_PopClass_popsize_edge():
    """
    Edge cases for initializing a PopulationClass should be handled
    properly.
    - Popsize is 0; AssertionError must be raised.
    - Popsize is 1; regular execution.
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


def test_PopClass_eq():
    """
    The PopulationClass.__eq__ method must correctly compare two objects.
    """
    popsize = 100
    random_seed = 100
    pop_class_1 = PopulationClass(popsize, random_seed)
    pop_class_2 = PopulationClass(popsize, random_seed)
    pop_class_3 = PopulationClass(popsize)
    pop_class_4 = PopulationClass(popsize)
    assert pop_class_1 == pop_class_2
    assert pop_class_2 != pop_class_3
    assert pop_class_3 == pop_class_4
    assert not pop_class_1 == "thisIsNotAPopulationClassThisIsAString"


def test_PopClass_add_property():
    """
    Adding a property with PopulationClass.add_property must work correcly if
    the input is correct, a ProbabilityClass is entered as a parameter and
    it does not yet exist.
    An AssertionError must be raised if
    - a non-ProbabilityClass object is entered.
    - the property is already defined.
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


def test_PopClass_remove_property():
    """
    Removing a property with PopulationClass.remove_property must work
    correcly if the name of an existing property is entered.
    An AssertionError must be raised if
    - the entered argument is not a string
    - the property is not defined.
    """
    # Define test population
    popsize = 100
    random_seed = 100
    pop_class = PopulationClass(popsize, random_seed)

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
    del test_prob_objects['age']
    # Test behaviour for correct input
    pop_class.remove_property('age')
    assert pop_class.prob_objects == test_prob_objects
    # Test if property is not in the ProbabilityClass object
    pop_class.remove_property('age')
    assert pop_class.prob_objects == test_prob_objects
    # Test if a non-string is entered
    pop_class.remove_property(0)
    assert pop_class.prob_objects == test_prob_objects


def test_PopClass_get_conditional_population():
    """
    The get_conditional_population() method should return the correct
    population when supplied with a certain conditions file.
    """
    # Define test population
    popsize = 100
    random_seed = 100
    pop_class = PopulationClass(popsize, random_seed)
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
    pop_class.update(property_name="all")

    population_cond = pop_class.get_conditional_population('age', cond_index=0)
    test_population_cond = pop_class.population.query("sex == 0")
    test_population_cond = test_population_cond[['person_id']]
    assert population_cond.equals(test_population_cond)

    population_cond = pop_class.get_conditional_population('age', cond_index=1)
    test_population_cond = pop_class.population.query("sex == 1")
    test_population_cond = test_population_cond[['person_id']]
    assert population_cond.equals(test_population_cond)


def test_PopClass_update():
    """
    When updating the PopulationClass a new column of each
    property should be added on the first time updating that
    property. Any subsequent times the columns should remain the same.

    The age column should be completely filled.
    """
    popsize = 10
    random_seed = 100
    pop_class = PopulationClass(popsize, random_seed)
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
    # No properties yet filled with drawn values
    assert sorted(pop_class.population.columns.values) == \
        ['person_id']
    pop_class.update(property_name="sex")
    assert sorted(pop_class.population.columns.values) == \
        ['person_id', 'sex']
    pop_class.update(property_name="sex")
    assert sorted(pop_class.population.columns.values) == \
        ['person_id', 'sex']
    pop_class.update(property_name="age")
    assert sorted(pop_class.population.columns.values) == \
        ['age', 'person_id', 'sex']
    pop_class.update(property_name="income")
    assert sorted(pop_class.population.columns.values) == \
        ['age', 'income', 'person_id', 'sex']
    # If all the variables are updated again, no additional columns should
    # be created.
    pop_class.update(property_name="all")
    assert sorted(pop_class.population.columns.values) == \
        ['age', 'income', 'person_id', 'sex']


def test_PopClass_export():
    """
    Test the export method.
    - Test the assertions that check the argument types.
    """
    test_output_filename = "./tests/testdata/PopulationClass/export.csv"
    if os.path.exists(test_output_filename):
        os.remove(test_output_filename)
    # Define test population
    popsize = 100
    random_seed = 100
    pop_class = PopulationClass(popsize, random_seed)
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
    pop_class.update(property_name="all")

    # Test the assertions that check the argument types.
    with pytest.raises(AssertionError):
        pop_class.export(output=0)
    with pytest.raises(AssertionError):
        pop_class.export(output=test_output_filename,
                         nowrite="notaboolean")

    pop_class.export(test_output_filename, nowrite=True)
    assert not os.path.exists(test_output_filename), \
        "Export with nowrite writes to file"
    pop_class.export(test_output_filename)
    pop_class_from_export = pd.read_csv(test_output_filename, sep=',')

    population_w_labels = pop_class.population.copy()
    for prob_obj in pop_class.prob_objects.values():
        if prob_obj.data_type in ["categorical", "ordinal"]:
            prop = prob_obj.property_name
            population_w_labels[prop] = population_w_labels[prop]\
                .apply(lambda idx: 'nodata' if np.isnan(idx)
                       else prob_obj.labels[int(idx)])
    assert_frame_equal(pop_class_from_export, population_w_labels), \
        "Population written to file is different than calculated"


def test_generate_population():
    """
    Test the function generate_population()
    Test for an integer random seed and for a random seed equal to None.
    """
    # Define test population
    popsize = 100
    random_seed = 100
    test_pop_class = PopulationClass(popsize, random_seed)
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
        test_pop_class.add_property(probab_object)

    pop_class = generate_population(popsize, yaml_folder,
                                    rand_seed=random_seed)
    assert test_pop_class == pop_class

    # Test for random_seed=None
    test_pop_class_no_seed = PopulationClass(popsize)
    for probab_object in probab_objects:
        test_pop_class_no_seed.add_property(probab_object)

    pop_class_no_seed = generate_population(popsize, yaml_folder)
    assert pop_class_no_seed == test_pop_class_no_seed


def test_construct_query_string():
    """
    Test if every relation is property translated to a query string.
    """
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
