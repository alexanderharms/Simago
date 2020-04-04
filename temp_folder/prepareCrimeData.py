#!/usr/bin/env python3
import pandas as pd

# Read in crime data
crimes = pd.read_csv('./Data/Chicago_Crimes_2012_to_2017.csv')
crimes = crimes.query('Arrest == True')
crimes.write_csv("./Data-process/Crimes-Arrested.csv")
