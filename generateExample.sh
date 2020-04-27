#!/usr/bin/env bash
POPSIZE=1000
YAML='./data-yaml/example/'
OUTPUT='./output/population.csv'
SEED=100

python3 generatePopulation.py -p $POPSIZE --yaml_folder $YAML\
	-o $OUTPUT --rand_seed $SEED

