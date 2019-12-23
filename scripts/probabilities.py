#!/usr/bin/env python3
import numpy as np
import pandas as pd

def buildProbDf(prop_name, option_vec, prob_vec,
        cond_num = 0, conditional = None):
    prob_df = pd.DataFrame({"property" : prop_name,
                            "cond_num" : cond_num, 
                            "conditional" : conditional,
                            "option" : option_vec,
                            "prob" : prob_vec})
    return prob_df

def genProb_NoCond(data_frame, prop_name):
    # column 0 option label
    # column 1 amounts
    # normalize probabilities with the sum of the amount
    option_vec = data_frame.iloc[:, 0]
    prob_vec = data_frame.iloc[:, 1] / data_frame.iloc[:, 1].sum()
    prob_df = buildProbDf(prop_name, option_vec, prob_vec)
    return prob_df

def genProb_Cond(data_frame, prop_name):
    # column 0 option label
    # column 1 conditional
    # column 2 amounts
    # normalize probabilities with the sum of the amount
    # within each contional probability
    
    prob_df_list = []

    for cond_num, cond in enumerate(np.unique(data_frame.iloc[:, 1])):
        data_frame_cond = data_frame[data_frame.iloc[:, 1] == cond]
        option_vec = data_frame_cond.iloc[:, 0]
        prob_vec = data_frame_cond.iloc[:, 2] / \
                data_frame_cond.iloc[:, 2].sum()
        prob_df_list.append(
                buildProbDf(prop_name, option_vec, 
                    prob_vec, 
                    cond_num, 
                    data_frame_cond.iloc[:, 1]))

    prob_df = pd.concat(prob_df_list, axis = 0)

    return prob_df

def genProb_NoCond_Range(data_frame, prop_name):
    # column 0 is minimum of range
    # column 1 is maximum of range
    # column 2 is the total population in each range
    # normalize probabilities with the sum of all the values
    solve_system = np.zeros((data_frame.shape[0],
        max(data_frame.iloc[:, 1]) - min(data_frame.iloc[:, 0]) + 1))

    for i in range(0, data_frame.shape[0]): 
        solve_system[i, data_frame.iloc[i, 0]:(data_frame.iloc[i, 1] + 1)] = 1

    solution = np.rint(np.linalg.lstsq(solve_system, data_frame.iloc[:, 2])[0])

    option_vec = range(min(data_frame.iloc[:, 0]), 
            max(data_frame.iloc[:, 1]) + 1)
    prob_vec = solution / sum(solution)
            
    prob_df = buildProbDf(prop_name, option_vec, prob_vec)
    prob_df = prob_df.query("prob != 0")
    return prob_df
