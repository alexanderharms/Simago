"""Tests corresponding to the simago/probability.py file."""
import pandas as pd
import pytest

# from simago.probability import (
#     ContinuousProbabilityClass,
#     DiscreteProbabilityClass,
#     check_comb_conditionals,
# )
from simago.probability import (
    DiscreteProbabilityClass,
    check_comb_conditionals,
)
from simago.yamlutils import load_yamls


# def test_order_probab():
# def test_check_comb_conditionals():
#     yaml_folder =
#     yaml_filenames = find_yamls(args.yaml_folder)
#     yaml_objects = load_yamls(yaml_filenames)
#
#     # Based on the yaml_objects, create a list of ProbabilityClass instances.
#     probab_objects = []
#     for y_obj in yaml_objects:
#         probab_objects.append(ProbabilityClass(y_obj))


def test_ProbClass_read_data():
    """
    Test reading a data file for a categorical variable.
    """
    test_yaml = "./tests/testdata/ProbabilityClass/sex.yml"
    yaml_object = load_yamls([test_yaml])

    prob_object = DiscreteProbabilityClass(yaml_object[0])
    test_data = pd.DataFrame(
        {
            "option": [0, 1],
            "value": [3805370719, 3742018211],
            "conditional_index": [0, 0],
        }
    )
    test_labels = ["male", "female"]
    # After initializing the ProbabilityClass, the data should be read.
    # The attribute prob_object.data should have three columns,
    #    'option', 'value' and 'conditional_index'
    assert prob_object.data.columns.tolist() == [
        "option",
        "value",
        "conditional_index",
    ]
    # Per conditional index, there should not be duplicates in either
    #    options or labels.
    # The attribute prob_object.labels should match the labels from the data
    #    per option.
    assert prob_object.data.equals(test_data)
    assert prob_object.labels == test_labels


# TODO: Test importing PDF function and PDF parameters for a continuous
# variable.


def test_ProbClass_gen_probabs():
    """
    Check that a correct ProbabilityClass is generated for a categorical
    variable.
    """
    test_yaml = "./tests/testdata/ProbabilityClass/sex.yml"
    yaml_object = load_yamls([test_yaml])

    prob_object = DiscreteProbabilityClass(yaml_object[0])
    test_probabs = pd.DataFrame(
        {
            "option": [0, 1],
            "probab": [0.504196981803083, 0.495803018196917],
            "conditional_index": [0, 0],
        }
    )
    assert prob_object.probabs.columns.tolist() == [
        "option",
        "probab",
        "conditional_index",
    ]
    assert prob_object.probabs.equals(test_probabs)


def test_ProbClass_read_conditionals():
    """
    Check that the conditionals files is properly imported.
    """
    test_yaml = "./tests/testdata/ProbabilityClass/age.yml"
    test_conditionals = pd.DataFrame(
        {
            "conditional_index": [0, 1],
            "property_name": ["sex", "sex"],
            "option": [0, 1],
            "relation": ["eq", "eq"],
        }
    )

    yaml_object = load_yamls([test_yaml])
    prob_object = DiscreteProbabilityClass(yaml_object[0])
    # The conditionals should have the columns:
    #   'conditional_index', 'property_name', 'option', 'relation'
    assert prob_object.conditionals.columns.tolist() == [
        "conditional_index",
        "property_name",
        "option",
        "relation",
    ]
    assert prob_object.conditionals.equals(test_conditionals)


# def test_check_data():
#    test_yaml = "./tests/testdata/ProbabilityClass/sex.yml"
#    yaml_object = load_yamls([test_yaml])
#
#    prob_object = ProbabilityClass(yaml_object[0])
#    # Data should be rejected if:
#    # - it does not have four columns:
#    #   'option', 'value', 'label', 'conditional_index'
#    # - the options do not match the labels everywhere.
#    # - within a conditional index the every duplicate option should
#    #   have the same value
#    # - there are duplicate conditional indices with different values for
#    #   option, value or label.


def test_check_comb_conditionals_undefinedprop():
    """
    Function check_comb_conditionals() returns an AssertionError when
    the conditionals of a new property reference an undefined property.
    """
    # Conditionals reference undefined property
    test_yaml = "./tests/testdata/ProbabilityClass/age.yml"

    yaml_object = load_yamls([test_yaml])
    prob_objects = [DiscreteProbabilityClass(yaml_object[0])]
    with pytest.raises(AssertionError):
        check_comb_conditionals(prob_objects)


# def test_check_comb_conditionals_amountparams():
#     # TODO: Check that a continuous variable has enough PDF parameters for
#     # the amount of conditionals.
#     return
#
# def test_check_comb_cond():
#     # TODO: There should be at least one property without conditionals
#
# def test_get_cond_pop():
#     # TODO: Test if the correct conditional population is retrieved.

# def test_order_probab_objects():
#     # TODO: Test if the ProbabilityClass objects are ordered correctly.

# TODO: Check that get_conditional_population gets the correct conditional
# population.
