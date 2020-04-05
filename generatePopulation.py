#!/usr/bin/env python
import argparse

import numpy as np

from simago.yamlutils import find_yamls, load_yamls
from simago.population import PopulationClass
from simago.probability import ProbabilityClass, check_conditionals

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--popsize", type=int,
                        help="Size of the population")
    parser.add_argument("-o", "--output", type=str,
                        default="./output/population.csv",
                        help="Output file for the population")
    parser.add_argument("--nowrite", action="store_true",
                        help="Do not write the population to file.")
    parser.add_argument("--rand_seed", type=int, default=None,
                        help="Seed for random number generation")
    parser.add_argument("--yaml_folder", type=str,
                        default="./data-yaml/",
                        help="Location of YAML files for the aggregated data.")
    args = parser.parse_args()

    print("Population size: %d" % (args.popsize))
    if args.rand_seed is None:
        print("No random seed defined")
    else:
        print("Random seed: %d" % (args.rand_seed))
    np.random.seed(args.rand_seed)

    print("------------------------")
    # Gather YAML files for aggregated data
    yaml_filenames = find_yamls(args.yaml_folder)
    yaml_filenames = sorted(yaml_filenames)
    print("YAML folder: %s" % (args.yaml_folder))
    print("Found YAML files:")
    print(yaml_filenames)
    yaml_objects = load_yamls(yaml_filenames)

    # Based on the yaml_objects, create a list of ProbPopulation instances.
    probab_objects = []
    for y_obj in yaml_objects:
        probab_objects.append(ProbabilityClass(y_obj)) 

    print("------------------------")
    print("Defined properties:")
    for obj in probab_objects:
        print(obj.property_name)

    check_conditionals(probab_objects)

    # Generate an empty population
    population = PopulationClass(args.popsize, args.rand_seed)

    # Add variables to the population based on the ProbPopulation instances.
    for obj in probab_objects:
        population.add_property(obj)

    population.update()
    print("------------------------")
    print("Generated population:")
    print(population.population)

    print("------------------------")
    # Export population.population
    if args.nowrite:
        print("Population is not written to disk.")
        pass
    else:
        population.population.to_csv(path_or_buf=args.output, index = False)
        print("Population is written to %s" % (args.output))
