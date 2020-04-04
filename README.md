# Simago: Population simulation

This package can be used to generate random populations, sets of microdata, based
on (publicly availabled) aggregated data.  

These populations can then for example be used for experimentation in the field
of machine learning or simulation studies.

<!-- To demonstrate the use of this package, a population is generated based on
aggregated data from the city of Chicago. -->

## Usage
``` 
python generatePopulation.py -p POP_SIZE
```
Options:
- -p: Size of the population.
- --yaml_folder: Folder for the settings-files (YAML-files).
- -o: Location for the output file of the generated population.
- --rand_seed: Random seed for the generated population.
- --nowrite: Flag to not write the population to file.

The core of the package is the generatePopulation script. In this script
first a population of 'empty' people, people with only an ID number without any
added information, is generated. After that values for properties, for example
'age' or 'income', are randomly drawn and added based on the supplied data. The 
resulting population consists of a table where each row represents a person and 
each column a property. This table can then be written to a CSV file.

For the generation of a population two or three files are needed:
- 'The YAML file': A YAML file with the settings for each property.
- 'The data file': A CSV file with the aggregated data per property. This data will be converted
  into a probability distribution. Per subset of the population a different
  conditional probability distribution can be defined.
- Optional: 'The conditionals file': A CSV file with the rules to select the population subsets for the
  conditional probability distributions.

Properties can exist in three types: 'categorical', 'ordinal' and 'continuous'.
For categorical and ordinal properties a discrete probability distribution is
constructed based on the data file. For the continuous properties a probability
distribution function must be defined in a separate Python file. The difference
between categorical and ordinal properties is that the options for the ordinal
properties are assumed to contain a certain order, for example in the cases of
'age' and 'education'.

### Example:
In the package a simple example is included. By running the Bash file
'generate_example.sh' this example population is generated.

<!--
## Data for the Chicago-based population
Data sources:
* US Census American Community Survey of 2013-2017.
* Chicago Data Portal: Building Footprints & Boundaries ZIP codes, 
	retrieved in July 2019.
* Trulia: median Sales & Listing prices per ZIP code; median rent price/bedroom, 
	retrieved on September 1st 2019.
-->
