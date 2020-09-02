# Simago: Population simulation

This package can be used to generate random populations, sets of microdata, based
on (publicly availabled) aggregated data.  

These populations can then for example be used for experimentation in the field
of machine learning or simulation studies.

## Usage
To generate a population the 'generate_population' from 'simago.population' has
to be called. This function creates a population in the form of tablfe with a
row for every person and a column for each property of this person. The values
for these properties are randomly drawn from probability distributions defined
by the supplied data. This is done by supplying a settings file, a data file and
possibly a conditionals file. In the
[simago-examples](www.github.com/alexanderharms/simago-examples) repository an example is
described of how to use the package.

## How to contribute
In order to contribute either leave a message in the Issues section or open a pull request. The documentation is currently made in Sphinx 1.8.5 and the unit testing is performed using pytest 6.0.1.
