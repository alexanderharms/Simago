#!/usr/bin/env python3
"""
Generate the example population with the expression:
``python gen_population.py -p 1000 --yaml-folder ./data-yaml/
    -o ./output/population.csv --rand_seed 100``
"""
import argparse

from simago.population import generate_population


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

    population = generate_population(args.popsize, args.yaml_folder,
                                     args.rand_seed)
    population.update()
    population.export(args.output, nowrite=args.nowrite)
