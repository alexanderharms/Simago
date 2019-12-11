#!/usr/bin/env python3
import numpy as np
import pandas as pd

def genProb_NoCond(data_frame, prop_name):
    # column 0 option label
    # column 1 amounts
    # total population is equal to the sum of the two numbers
    option_vec = data_frame.iloc[:, 0]
    prob_vec = data_frame.iloc[:, 1] / data_frame.iloc[:, 1].sum()
    prob_df = pd.DataFrame({"property" : prop_name,
                            "cond_num" : 0, 
                            "conditional" : None,
                            "option" : option_vec,
                            "prob" : prob_vec})
    return prob_df

def genProb_NoCond_Range(data_frame, prop_name):
    # column 0 is minimum of range
    # column 1 is maximum of range
    # column 2 is the total population in each range
    # total population is equal to the sum of the two numbers
    solve_system = np.zeros((data_frame.shape[0],
        max(data_frame.iloc[:, 1]) - min(data_frame.iloc[:, 0]) + 1))

    for i in range(0, data_frame.shape[0]): 
        solve_system[i, data_frame.iloc[i, 0]:(data_frame.iloc[i, 1] + 1)] = 1

    solution = np.rint(np.linalg.lstsq(solve_system, data_frame.iloc[:, 2])[0])
    prob_df = pd.DataFrame(data = {"property" : prop_name,
                                   "cond_num" : 0,
                                   "conditional" : None,
                                   "option" : range(min(data_frame.iloc[:, 0]),
                                       max(data_frame.iloc[:, 1]) + 1),
                                   "prob" : solution / sum(solution)})
    return prob_df
