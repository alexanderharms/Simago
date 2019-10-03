#!/usr/bin/env python3

# I assume that the part of 'Race vs educational attainment' is for all 
# people over 18
import numpy as np
import pandas as pd
import scipy.optimize as opt

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
        pass

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
group_1_age = np.linspace(18, 24, 24-18+1).astype(int)
group_1_degree = ['less_hs', 'hs', 'some_col_asdeg', 'bach_higher']
group_1_num_male = ['HC03_EST_VC03', 'HC03_EST_VC04', 'HC03_EST_VC05',
                    'HC03_EST_VC06']
group_1_num_female = ['HC05_EST_VC03', 'HC05_EST_VC04', 'HC05_EST_VC05',
                      'HC05_EST_VC06']

group_1_df = construct_group_dataframe(group_1_degree, grade_conv,
                                       group_1_age, None, race_vector)

group_1_male = censusdata.loc[group_1_num_male, 1]
group_1_female = censusdata.loc[group_1_num_female, 1]

# ----------------------------------------------------------------------------
group_2_age = np.linspace(25, 34, 34-25+1).astype(int)
group_2_degree = ['hs_higher', 'bach_higher']
group_2_num_male = ['HC03_EST_VC21', 'HC03_EST_VC22']
group_2_num_female = ['HC05_EST_VC21', 'HC05_EST_VC22']

group_2_df = construct_group_dataframe(group_2_degree, grade_conv,
                                       group_2_age, None, race_vector)

group_2_male = censusdata.loc[group_2_num_male, 1]
group_2_female = censusdata.loc[group_2_num_female, 1]

# ----------------------------------------------------------------------------
group_3_age = np.linspace(35, 44, 44-35+1).astype(int)
group_3_degree = ['hs_higher', 'bach_higher']
group_3_num_male = ['HC03_EST_VC25', 'HC03_EST_VC26']
group_3_num_female = ['HC05_EST_VC25', 'HC05_EST_VC26']

group_3_df = construct_group_dataframe(group_3_degree, grade_conv,
                                       group_3_age, None, race_vector)

group_3_male = censusdata.loc[group_3_num_male, 1]
group_3_female = censusdata.loc[group_3_num_female, 1]

# ----------------------------------------------------------------------------
group_4_age = np.linspace(45, 64, 64-45+1).astype(int)
group_4_degree = ['hs_higher', 'bach_higher']
group_4_num_male = ['HC03_EST_VC29', 'HC03_EST_VC30']
group_4_num_female = ['HC05_EST_VC29', 'HC05_EST_VC30']

group_4_df = construct_group_dataframe(group_4_degree, grade_conv,
                                       group_4_age, None, race_vector)

group_4_male = censusdata.loc[group_4_num_male, 1]
group_4_female = censusdata.loc[group_4_num_female, 1]

# ----------------------------------------------------------------------------
group_5_age = np.linspace(65, 99, 99-65+1).astype(int)
group_5_degree = ['hs_higher', 'bach_higher']
group_5_num_male = ['HC03_EST_VC33', 'HC03_EST_VC34']
group_5_num_female = ['HC05_EST_VC33', 'HC05_EST_VC34']

group_5_df = construct_group_dataframe(group_5_degree, grade_conv,
                                       group_5_age, None, race_vector)

group_5_male = censusdata.loc[group_5_num_male, 1]
group_5_female = censusdata.loc[group_5_num_female, 1]

# ----------------------------------------------------------------------------
group_tot_age = np.linspace(25, 99, 99-25+1).astype(int)
group_tot_degree = ['less_9', '9_12', 'hs', 'some_col', 'asdeg', 'bach',
                    'graduate']
group_tot_num_male = ['HC03_EST_VC09', 'HC03_EST_VC10', 'HC03_EST_VC11',
                      'HC03_EST_VC12', 'HC03_EST_VC13', 'HC03_EST_VC14',
                      'HC03_EST_VC15']
group_tot_num_female = ['HC05_EST_VC09', 'HC05_EST_VC10', 'HC05_EST_VC11',
                        'HC05_EST_VC12', 'HC05_EST_VC13', 'HC05_EST_VC14',
                        'HC05_EST_VC15']

group_tot_df = construct_group_dataframe(group_tot_degree, grade_conv,
                                         group_tot_age, None, race_vector)

group_tot_male = censusdata.loc[group_tot_num_male, 1]
group_tot_female = censusdata.loc[group_tot_num_female, 1]

# Concatenate generated dataframes -------------------------------------------
df_concat = pd.concat([group_tot_df, group_1_df, group_2_df,
                       group_3_df, group_4_df, group_5_df],
                       sort = True,
                       axis = 0)

df_concat.fillna(value = 0.0, inplace = True)
print(df_concat)

male_concat = pd.concat([group_tot_male, group_1_male, group_2_male,
                         group_3_male, group_4_male, group_5_male],
                         axis = 0)

female_concat = pd.concat([group_tot_female, group_1_female, 
                           group_2_female, group_3_female, 
                           group_4_female, group_5_female],
                           axis = 0)
print(male_concat)
print(female_concat)

def minimize_func(x, A, b):
    y = np.dot(A, x) - b
    return np.dot(y, y)

init_cond = [2e6 * 0.5 / df_concat.shape[1]] * df_concat.shape[1]
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

# Solve for Female

female_solution = opt.minimize(fun = minimize_func,
                               x0 = init_cond,
                               args = (df_concat, female_concat),
                               bounds = bnds,
                               options = {'maxfun' : 1e6,
                                          'maxiter' : 1e6})

print(female_solution)
female_solution = np.rint(female_solution['x'])

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
                                           "race" : race}],
                          "option" : [option_vec],
                          "prob" : [male_prob.tolist()]}
    
        new_entry_female = {"property" : "education",
                            "cond_num" : cond_num_count + 1,
                            "conditional" : [{"sex" : "female",
                                             "age" : age,
                                             "race" : race}],
                            "option" : [option_vec],
                            "prob" : [female_prob.tolist()]}
        new_df_male = pd.DataFrame(data = new_entry_male)
        new_df_female = pd.DataFrame(data = new_entry_female)
        prob_education = pd.concat([prob_education, new_df_male, new_df_female],
                axis = 0)
        cond_num_count += 2

prob_education.to_csv(path_or_buf='data-process/prob_education.csv',
        index = False)
