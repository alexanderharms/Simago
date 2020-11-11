"""Tests corresponding to the simago/probability.py file."""
import pandas as pd
import pytest

from simago.probability import (
    ContinuousProbabilityClass,
    DiscreteProbabilityClass,
    check_comb_conditions,
)
from simago.yamlutils import load_yamls


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
            "condition_index": [0, 0],
        }
    )
    test_labels = ["male", "female"]
    # After initializing the ProbabilityClass, the data should be read.
    # The attribute prob_object.data should have three columns,
    #    'option', 'value' and 'condition_index'
    assert prob_object.data.columns.tolist() == [
        "option",
        "value",
        "condition_index",
    ]
    # Per condition index, there should not be duplicates in either
    #    options or labels.
    # The attribute prob_object.labels should match the labels from the data
    #    per option.
    assert prob_object.data.equals(test_data)
    assert prob_object.labels == test_labels


def test_ContProbClass_import_pdf():
    """
    If a ContinuousProbabilityClass object is intialized, it must be
    checked that the defined PDF returns a frozen rv_continuous object.
    """
    test_yaml = "./tests/testdata/ProbabilityClass/pdf_no_rv.yml"

    yaml_object = load_yamls([test_yaml])
    with pytest.raises(AssertionError):
        prob_objects = [ContinuousProbabilityClass(yaml_object[0])]
        del prob_objects

    test_yaml = "./tests/testdata/ProbabilityClass/pdf_no_frozen_rv.yml"

    yaml_object = load_yamls([test_yaml])
    with pytest.raises(AssertionError):
        prob_objects = [ContinuousProbabilityClass(yaml_object[0])]
        del prob_objects


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
            "condition_index": [0, 0],
        }
    )
    assert prob_object.probabs.columns.tolist() == [
        "option",
        "probab",
        "condition_index",
    ]
    assert prob_object.probabs.equals(test_probabs)


def test_ProbClass_read_conditions():
    """
    Check that the conditions files is properly imported.
    """
    test_yaml = "./tests/testdata/ProbabilityClass/age.yml"
    test_conditions = pd.DataFrame(
        {
            "condition_index": [0, 1],
            "property_name": ["sex", "sex"],
            "option": [0, 1],
            "relation": ["eq", "eq"],
        }
    )

    yaml_object = load_yamls([test_yaml])
    prob_object = DiscreteProbabilityClass(yaml_object[0])
    # The conditions should have the columns:
    #   'condition_index', 'property_name', 'option', 'relation'
    assert prob_object.conditions.columns.tolist() == [
        "condition_index",
        "property_name",
        "option",
        "relation",
    ]
    assert prob_object.conditions.equals(test_conditions)


def test_check_comb_conditions_undefinedprop():
    """
    Function check_comb_conditions() returns an AssertionError when
    the conditions of a new property reference an undefined property.
    """
    # Conditionals reference undefined property
    test_yaml = "./tests/testdata/ProbabilityClass/age.yml"

    yaml_object = load_yamls([test_yaml])
    prob_objects = [DiscreteProbabilityClass(yaml_object[0])]
    with pytest.raises(AssertionError):
        check_comb_conditions(prob_objects)

# def test_check_data():
#    test_yaml = "./tests/testdata/ProbabilityClass/sex.yml"
#    yaml_object = load_yamls([test_yaml])
#
#    prob_object = ProbabilityClass(yaml_object[0])
#    # Data should be rejected if:
#    # - it does not have four columns:
#    #   'option', 'value', 'label', 'condition_index'
#    # - the options do not match the labels everywhere.
#    # - within a condition index the every duplicate option should
#    #   have the same value
#    # - there are duplicate condition indices with different values for
#    #   option, value or label.

# def test_check_comb_conditions_amountparams():
#     # TODO: Check that a continuous variable has enough PDF parameters for
#     # the amount of conditions.
#     return
#
# def test_check_comb_cond():
#     # TODO: There should be at least one property without conditions
#
# def test_get_cond_pop():
#     # TODO: Test if the correct conditional population is retrieved.

# def test_order_probab_objects():
#     # TODO: Test if the ProbabilityClass objects are ordered correctly.
