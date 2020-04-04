from scipy import stats
import pandas as pd

from .probability import get_conditional_population

def draw_disc_values(prob_obj, population, random_seed):
    if prob_obj.conditionals is None:
        population[prob_obj.property_name] =\
                draw_from_disc_distribution(prob_obj.probabs, 
                                            population.shape[0],
                                            random_seed)
    # Iterate over the various conditionals.
    else:
        for cond_index in prob_obj.conditionals.conditional_index.unique():
            # For every conditional:
            # - Get the corresponding conditional from prob_obj.conditionals
            # - Get the corr. segment of the population
            # - Draw the values
            # - Write the values in a list to the correct places

            # - Get the corr. conditional probabilities from prob_obj.probabs
            probabs_df = prob_obj.probabs\
                    .query("conditional_index == @cond_index")
            # - Get the corr. segment of the population
            population_cond = get_conditional_population(prob_obj,
                    population, cond_index)

            # - Draw the values
            population_cond[prob_obj.property_name] =\
                    draw_from_disc_distribution(probabs_df,
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

def draw_from_disc_distribution(probabs, size, random_seed):
    sample_rv = stats.rv_discrete(name='sample_rv',
            values=(probabs.option, probabs.probab))
    sample_num = sample_rv.rvs(size = size)
    drawn_values = probabs.option.values[sample_num]
    # TODO: Convert drawn values to labels
    #drawn_values = prob_obj.labels[drawn_values]
    return drawn_values

