#!/usr/bin/env python3

# I assume that the part of 'Race vs educational attainment' is for all 
# people over 18


censusdata = pd.read_csv('./data/ACS_17_5YR_S1501csv').transpose()
censusdata = censusdata[censusdata.iloc[:, 0].str.contains('Estimate')]
censusdata.iloc[:, 1] = censusdata.iloc[:, 1].apply(pd.to_numeric)
