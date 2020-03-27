#!/usr/bin/env python3

import numpy as np
import pandas as pd
import scipy.optimize as opt

def convert_categories(df, conv_dict, col_name = 'option'):
    # Convert the 'option' column in the data frame.
    df[col_name] = df[col_name].apply(lambda x: conv_dict[x] 
            if x in list(conv_dict.keys()) else x)
    return df

def stringlistmultiply(list_1, list_2, sep = "-"):
    comb_list = []
    for string_1 in list_1:
        comb_list += [str(string_1) + str(sep) + str(x) 
                for x in list_2] 
    return comb_list

def solve_system(system, values):
    def minimize_func(x, A, b):
        y = np.dot(A, x) - b
        return np.dot(y, y)
    init_cond = [sum(values) / system.shape[1]] * system.shape[1]
    bnds = tuple((0.0, sum(values)) for _ in range(system.shape[1]))

    solution = opt.minimize(fun = minimize_func,
                            x0 = init_cond,
                            args = (system, values),
                            bounds = bnds,
                            options = {'maxfun' : 1e6,
                                       'maxiter' : 1e6})
    solution = np.rint(solution['x'])
    return solution
