import pandas as pd

from simago.probability import get_conditional_population

def draw_cont_values(prob_obj, population, random_seed):
    """
    Draw values for continuous variable.

    Parameters
    ----------
    prob_obj : ProbabilityClass
        ProbabilityClass object for the continuous variable.
    population : Pandas DataFrame
        DataFrame with a population to add the continuous variable to.
    random_seed : int
        Seed for random number generation.

    Returns
    -------
    PopulationClass object
        PopulationClass object with drawn values for the continuous variable.

    """

    if prob_obj.conditionals is None:
        population[prob_obj.property_name] =\
                draw_from_cont_distribution(prob_obj.pdf,
                                            prob_obj.pdf_parameters[0],
                                            population.shape[0],
                                            random_seed)
    else:
        for cond_index in prob_obj.conditionals.conditional_index.unique():
            # For every conditional:
            # - Get the corr. segment of the population
            # - Draw the values
            # - Write the values in a list to the correct places

            population_cond = get_conditional_population(prob_obj,
                    population, cond_index)
            population_cond[prob_obj.property_name] =\
                    draw_from_cont_distribution(prob_obj.pdf,
                                                prob_obj\
                                                    .pdf_parameters[cond_index],
                                                population_cond.shape[0],
                                                random_seed)
            # - Write the values in a list to the correct places
            # Use a left join for this
            if prob_obj.property_name not in population.columns.values:
                population = pd.merge(population, population_cond, 
                                      how="left", on="person_id")
            else:
                # If the column already exists, update the values in that column.
                # Couple of index tricks are necessary to arrange that.
                population = population.set_index('person_id')
                population_cond = population_cond.set_index('person_id')
                population_cond = population_cond[[prob_obj.property_name]]
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
