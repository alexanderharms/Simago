"""
Converts data about the sex of the population from www.populationpyramid.net
to the simago format.
"""
import pandas as pd


data_frame = pd.read_csv("./data/WORLD-2017-adapted.csv")
male_value = data_frame['M'].sum()
female_value = data_frame['F'].sum()

data_export = pd.DataFrame(
        data={"option": [0, 1],
              "value": [male_value, female_value],
              "label": ["male", "female"],
              "condition_index": 0})
print(data_export)

data_export.to_csv("./data/example/sex.csv", index=False)
