#!/usr/bin/env python3

# I assume that the part of 'Race vs educational attainment' is for all 
# people over 25
import sys
import math
import numpy as np
import pandas as pd
import scipy.optimize as opt
import matplotlib.pyplot as plt

#def genProb_Cond_Range(data_frame, prop_name):
#    # column 0 is minimum of range
#    # column 1 is maximum of range
#    # column 2 is the total population in each range
#    # total population is equal to the sum of the two numbers
#    solve_system = np.zeros((data_frame.shape[0],
#        max(data_frame.iloc[:, 1]) - min(data_frame.iloc[:, 0]) + 1)
#
#    for i in range(0, data_frame.shape[0]):
#        solve_system[i, data_frame.iloc[i, 0]:(data_frame.iloc[i, 1] + 1)] = 1
#
#    solution = np.rint(np.linalg.lstsq(solve_system, data_frame.iloc[:, 2]))
#    prob_df = pd.DataFrame(data = {"property" : prop_name,
#                                   "cond_num" : 0,
#                                   "conditional" : None,
#                                   "option" : range(min(data_frame.iloc[:, 0]),
#                                       max(data_frame.iloc[:, 1]) + 1),
#                                   "prob" : solution / sum(solution)})
#    return prob_df

def construct_group_dataframe(group_degree, grade_conv, group_age,
                              race, race_vector):
    # Set up a diagonal matrix with group_1_degree as columns
    group_matrix = np.diag(np.ones(len(group_degree)))
    # Construct dictionary for DataFrame
    group_df_dict = {}
    for k in range(0, len(group_degree)):
        group_df_dict[group_degree[k]] = group_matrix[:, k]

    # Put it in a data frame with group_1_degree as labels
    group_df = pd.DataFrame(data = group_df_dict) 

    # Change it to an extended degree matrix using grade_conv
    for key in grade_conv:
        if key in group_df.columns.values:
            # Take key column
            df_col = group_df[[key]]
            # Add the same column as a column with the names in value
            for value in grade_conv[key]:
               group_df[[value]] = df_col
            # Delete the key column
            group_df.drop(key, axis = 1, inplace = True)

    # Expand dataframe to add race
    if race == None:
        # The column is for all races
        for col in group_df.columns.values:
            df_col = group_df[[col]]
            for r in race_vector:
                r_col = r + '-' + col
                group_df[[r_col]] = df_col
            group_df.drop(col, axis = 1, inplace = True)
    else:
        # The data is specified for a certain race/background, so 
        # all the other columns for the other races should be all 
        # zeros. 
        for col in group_df.columns.values:
            df_col = group_df[[col]]
            r_col = race + '-' + col
            group_df[[r_col]] = df_col
            print(df_col)
            race_vector_without = race_vector.copy()
            race_vector_without.remove(race)
            for r in race_vector_without:
                r_col = r + '-' + col
                group_df[[r_col]] = 0
            group_df.drop(col, axis = 1, inplace = True)

    # Expand dataframe into the ages
    # The whole dataframe should replicated for all the ages in the 
    # age vector, all the other ages from the series of 18 to 99 should
    # be a zero vector.
    for col in group_df.columns.values:
        df_col = group_df[[col]]
        for age in range(18, 100):
            age_col = str(age) + '-' + col
            if age in group_age:
                group_df[[age_col]] = df_col
            else:
                # Apparently the other assignment way didnt work here
                group_df = group_df.assign(**{age_col : 0.0})
        group_df.drop(col, axis = 1, inplace = True)

    return group_df

def generate_group(censusdata, age, degree, num, 
                   grade_conv, race_vector, race = None):
    age = np.linspace(age[0], age[1], age[1]-age[0]+1).astype(int)
    group_df = construct_group_dataframe(degree, grade_conv,
                                         age, None, race_vector)
    
    num_male = ['HC03_EST_VC' + x for x in num]
    num_female = ['HC05_EST_VC' + x for x in num]
    group_male = censusdata.loc[num_male, 1]
    group_female = censusdata.loc[num_female, 1]
    return group_df, group_male, group_female

censusdata = pd.read_csv('./data/ACS_17_5YR_S1501.csv').transpose()
censusdata = censusdata[censusdata.iloc[:, 0].str.contains('Estimate')]
censusdata.iloc[:, 1] = censusdata.iloc[:, 1].apply(pd.to_numeric)

print(censusdata)

# Group 1 is from 18 to 24
# less_hs = less_9, 9_12
# hs 
# some_col_asdeg = some_col, asdeg
# bach_higher = bach, graduate
grade_conv = {'less_hs' : ['less_9', '9_12'],
              'some_col_asdeg' : ['some_col', 'asdeg'],
              'bach_higher' : ['bach', 'graduate'],
              'hs_higher' : ['hs', 'some_col', 'asdeg', 'bach', 
                             'graduate']}

race_vector = ['white', 'african_american', 'american_indian',
               'asian', 'native_hawaiian', 'some_other_race',
               'two_or_more_races']

# ----------------------------------------------------------------------------
group_1_age = [18, 24]
group_1_degree = ['less_hs', 'hs', 'some_col_asdeg', 'bach_higher']
group_1_num = ['03', '04', '05', '06']

group_1_df, group_1_male, group_1_female =\
        generate_group(censusdata, group_1_age, group_1_degree,
                       group_1_num, grade_conv, race_vector)
# ----------------------------------------------------------------------------
group_2_age = [25, 34]
group_2_degree = ['hs_higher', 'bach_higher']
group_2_num = ['21', '22']

group_2_df, group_2_male, group_2_female =\
        generate_group(censusdata, group_2_age, group_2_degree,
                       group_2_num, grade_conv, race_vector)
# ----------------------------------------------------------------------------
group_3_age = [35, 44]
group_3_degree = ['hs_higher', 'bach_higher']
group_3_num = ['25', '26']

group_3_df, group_3_male, group_3_female =\
        generate_group(censusdata, group_3_age, group_3_degree,
                       group_3_num, grade_conv, race_vector)
# ----------------------------------------------------------------------------
group_4_age = [45, 64]
group_4_degree = ['hs_higher', 'bach_higher']
group_4_num = ['29', '30']

group_4_df, group_4_male, group_4_female =\
        generate_group(censusdata, group_4_age, group_4_degree,
                       group_4_num, grade_conv, race_vector)
# ----------------------------------------------------------------------------
group_5_age = [65, 99]
group_5_degree = ['hs_higher', 'bach_higher']
group_5_num = ['33', '34']

group_5_df, group_5_male, group_5_female =\
        generate_group(censusdata, group_5_age, group_5_degree,
                       group_5_num, grade_conv, race_vector)
# ----------------------------------------------------------------------------
group_tot_age = [25, 99]
group_tot_degree = ['less_9', '9_12', 'hs', 'some_col', 'asdeg', 'bach',
                    'graduate']
group_tot_num = ['09', '10', '11', '12', '13', '14', '15']

group_tot_df, group_tot_male, group_tot_female =\
        generate_group(censusdata, group_tot_age, group_tot_degree,
                       group_tot_num, grade_conv, race_vector)
# Education per race. ----------------------
group_race_age = [25, 99]
group_race_degree = ['hs_higher', 'bach_higher']
group_race_num = [['38', '39'], ['46', '47'], ['50', '51'],
                  ['54', '55'], ['58', '59'], ['62', '63',],
                  ['66', '67']]

group_race_df = [None] * len(group_race_num)
group_race_male = [None] * len(group_race_num)
group_race_female = [None] * len(group_race_num)
for i, race_num in enumerate(group_race_num):
    group_race_df[i], group_race_male[i], group_race_female[i] =\
            generate_group(censusdata, group_race_age, group_race_degree,
                           race_num, grade_conv, race_vector,
                           race = race_vector[i])




race_df = pd.concat(group_race_df, sort = True, axis = 0)
race_df.fillna(value = 0.0, inplace = True)

race_male = pd.concat(group_race_male, axis = 0)
race_female = pd.concat(group_race_female, axis = 0)
print(race_df) 

print(race_df.columns.values)

print(race_male)
# Concatenate generated dataframes -------------------------------------------
df_concat = pd.concat([group_tot_df, group_1_df, group_2_df,
                       group_3_df, group_4_df, group_5_df],
                       sort = True,
                       axis = 0)

df_concat.fillna(value = 0.0, inplace = True)

male_concat = pd.concat([group_tot_male, group_1_male, group_2_male,
                         group_3_male, group_4_male, group_5_male],
                         axis = 0)

female_concat = pd.concat([group_tot_female, group_1_female, 
                           group_2_female, group_3_female, 
                           group_4_female, group_5_female],
                           axis = 0)

def minimize_func(x, A, b):
    y = np.dot(A, x) - b
    return np.dot(y, y)

# Take the sum of all the male values, divided over all the columns, as the
# initial values.
# init_cond = [np.sum(male_concat.values) / df_concat.shape[1]] * df_concat.shape[1]
# Take the maximum value of the group values as the upper bound of one column.
#bnds_max = np.max([np.max(male_concat.values), np.max(female_concat.values)])
#bnds = tuple((0.0, bnds_max) for _ in range(df_concat.shape[1]))
init_cond = [2e6 * 0.5 / df_concat.shape[1]] \
        * df_concat.shape[1]
bnds = tuple((0.0, 1e6) for _ in range(df_concat.shape[1]))
# Solve for Male
male_solution = opt.minimize(fun = minimize_func,
                             x0 = init_cond,
                             args = (df_concat, male_concat),
                             bounds = bnds,
                             options = {'maxfun' : 1e6,
                                        'maxiter' : 1e6})

print(male_solution)
male_solution = np.rint(male_solution['x'])
with np.printoptions(threshold=sys.maxsize):
    print(male_solution)
print(male_solution)

#init_cond_race = [np.max(race_male) * 0.5 / race_df.shape[1]] \
#        * race_df.shape[1]
#bnds_race = tuple((0.0, 1e6) for _ in range(race_df.shape[1]))
#
#male_race_solution = opt.minimize(fun = minimize_func,
#                                  x0 = init_cond_race,
#                                  args = (race_df, race_male),
#                                  bounds = bnds_race,
#                                  options ={'maxfun' : 1e6,
#                                            'maxiter' : 1e6})
#male_race_solution = np.rint(male_race_solution['x'])
#with np.printoptions(threshold=sys.maxsize):
#    print(male_race_solution)
#print(male_race_solution)
# Solve for Female

female_solution = opt.minimize(fun = minimize_func,
                               x0 = init_cond,
                               args = (df_concat, female_concat),
                               bounds = bnds,
                               options = {'maxfun' : 1e6,
                                          'maxiter' : 1e6})

print(female_solution)
female_solution = np.rint(female_solution['x'])
with np.printoptions(threshold=sys.maxsize):
    print(female_solution)
#female_race_solution = opt.minimize(fun = minimize_func,
#                                    x0 = init_cond_race,
#                                    args = (race_df, race_female),
#                                    bounds = bnds_race,
#                                    options ={'maxfun' : 1e6,
#                                              'maxiter' : 1e6})
#female_race_solution = np.rint(female_race_solution['x'])
#with np.printoptions(threshold=sys.maxsize):
#    print(female_race_solution)

print(sum(male_solution))
print(sum(female_solution))

# Build probability dataframe --------------------------------------------
column_names = df_concat.columns.values
cond_num_count = 0
prob_education = pd.DataFrame(columns = ["property", "cond_num", "conditional",
                                         "option", "prob"])
for age in range(18, 100):
    for race in race_vector:
        # Find all columns with 'age-race' in its name.
        age_race = str(age) + '-' + race
        age_race_index = [i for i, item in enumerate(column_names) if age_race
                          in item]
        age_race_names = column_names[age_race_index]

        # Using the index of the columns get the corresponding
        # values form the 'solution' vectors.
        male_prob = male_solution[age_race_index]
        female_prob = female_solution[age_race_index]

        # Normalize these values
        male_prob = male_prob / sum(male_prob)
        female_prob = female_prob / sum(female_prob)

        # Strip the column names from 'age-race-', the column names
        # should now form an ideal 'option' vector with te corresponding
        # normalized values as the probabilties.
        option_vec = [x.split('-')[2] for x in age_race_names]
        new_entry_male = {"property" : "education",
                          "cond_num" : cond_num_count,
                          "conditional" : [{"sex" : "male",
                                           "age" : age,
                                           "race" : race}] * len(option_vec),
                          "option" : option_vec,
                          "prob" : male_prob.tolist()}
    
        new_entry_female = {"property" : "education",
                            "cond_num" : cond_num_count + 1,
                            "conditional" : [{"sex" : "female",
                                             "age" : age,
                                             "race" : race}] * len(option_vec),
                            "option" : option_vec,
                            "prob" : female_prob.tolist()}
        new_df_male = pd.DataFrame(data = new_entry_male)
        new_df_female = pd.DataFrame(data = new_entry_female)
        prob_education = pd.concat([prob_education, new_df_male, new_df_female],
                axis = 0)
        cond_num_count += 2
print(prob_education)
prob_education.to_csv(path_or_buf='data-process/probabilities/prob_education.csv',
        index = False)
