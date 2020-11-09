"""
Converts data about age from www.populationpyramid.net to the
simago format.
"""
import numpy as np
import pandas as pd


# The data for ages above 99 years is removed.
data_frame = pd.read_csv("./data/WORLD-2017-adapted.csv")

age_list = [x for x in range(data_frame['Age1'].min(),
                             data_frame['Age2'].max() + 1)]
data_export = pd.DataFrame(
        data={"option": age_list,
              "label": age_list},
        columns=['option', 'value', 'label', 'condition_index'])

data_export_male = data_export.copy()
data_export_male['condition_index'] = 0
data_export_female = data_export.copy()
data_export_female['condition_index'] = 1

for idx, row in data_frame.iterrows():
    # Per row, select the value for the males or females.
    male_value = row['M']
    female_value = row['F']
    age_row_list = [x for x in range(row['Age1'], row['Age2'] + 1)]
    male_value /= len(age_row_list)
    female_value /= len(age_row_list)

    male_age_bool = [True if x in age_row_list else False for x in
                     data_export_male['option'].values]
    female_age_bool = [True if x in age_row_list else False for x in
                       data_export_female['option'].values]

    data_export_male.loc[np.where(male_age_bool)[0], 'value'] =\
        male_value
    data_export_female.loc[np.where(female_age_bool)[0], 'value'] =\
        female_value

data_export = pd.concat([data_export_male, data_export_female], axis=0)
data_export.to_csv("./data/example/age.csv", index=False)
