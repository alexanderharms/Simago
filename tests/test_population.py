import numpy as np
import pandas as pd
import pytest

from simago.population import PopulationClass


def test_PopClass_init():
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


# def test_PopClass_update_disc_all():
#     # Test update for a discrete variable
#
# def test_PopClass_update_cont_all():
#     # Test update for a continuous variable
#
# def test_PopClass_update_disc_specific():
#     # Test update for a discrete variable
#
# def test_PopClass_update_cont_specific():
#     # Test update for a continuous variable
