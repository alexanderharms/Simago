#!/usr/bin/env python
import argparse

import numpy as np

from simago.yamlutils import find_yamls, load_yamls
from simago.population import PopulationClass
from simago.probability import ProbabilityClass, check_conditionals

def cumulative_properties(probab_objects):
    properties = [None] * len(probab_objects)
    for idx, obj in enumerate(probab_objects):
        if idx == 0:
            properties[idx] = [obj.property_name]
        else: 
            properties[idx] = properties[idx - 1] + [obj.property_name]
    return properties

def order_probab_objects(probab_objects):
    # There should be at least one property without conditionals.
    cond_bool = [True if x.conditionals is None else False 
                 for x in probab_objects]
    assert any(cond_bool), 'At least one of the properties should be without'\
            + ' conditionals.'
    # Start ordering the list of probab_objects with all the properties with
    # obj.conditionals is None.
    probab_none = [probab_objects[i] for i, x in enumerate(cond_bool) if x]
    probab_none_prop = [obj.property_name for obj in probab_none]

    probab_cond = [probab_objects[i] for i, x in enumerate(cond_bool) if not x]
    probab_cond_prop = [obj.property_name for obj in probab_cond]

    # Create a graph of the dependencies.
    # Check if there are cycles in the graph. Assert that there are no cycles.
    # After that follow the graph from these properties to order the list of 
    # probab objects.
    probab_graph = dict()
    for obj in probab_cond:
        probab_graph[obj.property_name] = \
                np.unique(obj.conditionals.property_name).tolist()

    for key in probab_graph.keys():
        # If all the values of probab_graph are have no conditionals, the graph
        # cannot be simplified further.
        probab_graph_values = probab_graph[key]
        while not all(item in probab_none_prop for item in probab_graph_values):
            assert key not in probab_graph_values, 'Circular dependency, ' + key
            
            probab_graph_values = [probab_graph[k] for k in probab_graph_values 
                    if k not in probab_none_prop]
            probab_graph_values = [item for sublist in probab_graph_values 
                    for item in sublist]

    cumul_props = cumulative_properties(probab_objects)
    
    return probab_objects

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
    
    probab_objects = order_probab_objects(probab_objects)

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
