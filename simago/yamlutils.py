"""
Functions for finding, checking and loading of the YAML configuration files.
"""
import ast
import os

import yaml


def find_yamls(yaml_folder):
    """Find YAML files from a folder.

    Gather all the YAML files for the aggregated data in the folder.
    Return the list of paths to YAML files.

    Parameters
    ----------
    yaml_folder : str
        Name of folder where YAML files are stored.

    Returns
    -------
    yaml_filenames : list of str
        List of YAML filenames.
    """
    print("YAML folder: %s" % (yaml_folder))
    yaml_filenames = []
    for dirpath, dirs, filenames in os.walk(yaml_folder):
        for filename in filenames:
            if filename.endswith(".yml") or filename.endswith(".yaml"):
                yaml_filenames.append(filename)
    yaml_filenames = [yaml_folder + fname for fname in yaml_filenames]
    yaml_filenames = sorted(yaml_filenames)

    print("Found YAML files:")
    print(yaml_filenames)

    return yaml_filenames


def check_yaml(yaml_object):
    """Check YAML object.

    Using a number of assertions each YAML object, the dictionary derived
    from the YAML file, is checked if it is complete and if the defined
    variables are in the correct format.

    Parameters
    ----------
    yaml_object : dict
        Dictionary with the information from the YAML file.

    Returns
    -------
    yaml_object : dict
        Dictionary with the checked information from the YAML file.
    """
    fname = yaml_object['yaml_filename']

    assert 'property_name' in yaml_object.keys(), \
        fname + ', no property defined'
    assert isinstance(yaml_object['property_name'], str),\
        fname + ", incorrect name format"

    assert 'data_type' in yaml_object.keys(), fname + ', no data type defined'
    assert isinstance(yaml_object['data_type'], str),\
        fname + ", incorrect data type"
    assert yaml_object['data_type'] in [
        'categorical',
        'ordinal',
        'continuous'
    ], (
        fname + ", invalid data type"
    )

    if yaml_object['data_type'] in ['categorical', 'ordinal']:
        assert 'data_file' in yaml_object.keys(), fname +\
            ', no data file defined'
        assert isinstance(yaml_object['data_file'], str),\
            fname + ", incorrect data filename type"
        assert os.path.isfile(yaml_object['data_file']),\
            fname + ', data file does not exist'
        assert yaml_object['data_file'].endswith('.csv'),\
            fname + ', data file is not a CSV file'
    elif yaml_object['data_type'] == "continuous":
        assert 'pdf_parameters' in yaml_object.keys(),\
            fname + ', no parameters defined'
        assert isinstance(yaml_object['pdf_parameters'], list),\
            fname + ', parameters are not a list'

        assert 'pdf' in yaml_object.keys(),\
            fname + ', no pdf defined'
        assert isinstance(yaml_object['pdf'], str),\
            fname + ', pdf is not a string'

        assert 'pdf_file' in yaml_object.keys(),\
            fname + ', no pdf file defined'
        assert isinstance(yaml_object['pdf_file'], str),\
            fname + ', pdf filename is not a string'
        assert os.path.isfile(yaml_object['pdf_file']),\
            fname + ', pdf file does not exist'
        assert yaml_object['pdf_file'].endswith('.py'),\
            fname + ', pdf file is not a Python file'
        try:
            with open(yaml_object['pdf_file'], 'r') as f:
                source = f.read()
            ast.parse(source)
        except SyntaxError:
            print(fname + ', pdf file can not be executed')
            quit()

    if 'conditions' not in yaml_object.keys():
        yaml_object['conditions'] = None
    else:
        if yaml_object['conditions'] is not None:
            assert isinstance(yaml_object['conditions'], str),\
                fname + ', conditions not None or a string'
            assert os.path.isfile(yaml_object['conditions']),\
                fname + ', conditions file does not exist'
            assert yaml_object['conditions'].endswith('.csv'),\
                fname + ', conditions files is not a csv'

    return yaml_object


def load_yamls(yaml_filenames):
    """Load YAML files.

    Loads the YAML configuration files and converts them to dictionaries
    using ``yaml`` package. Checks if the imported YAML files contain
    the correct information using the function ``check_yaml``.

    Parameters
    ----------
    yaml_filenames : list of str
        List of YAML filenames.

    Returns
    -------
    yaml_objects : list of dict
        List of YAML objects.
    """
    yaml_objects = []
    for yaml_filename in yaml_filenames:
        with open(yaml_filename, 'r') as yaml_file:
            yaml_object = yaml.safe_load(yaml_file)
            assert isinstance(yaml_object, dict),\
                yaml_filename + ', improper YAML syntax'

        yaml_object['yaml_filename'] = yaml_filename
        yaml_objects.append(yaml_object)

    yaml_objects = [check_yaml(obj) for obj in yaml_objects]
    yaml_properties = [obj['property_name'] for obj in yaml_objects]
    assert len(yaml_properties) == len(set(yaml_properties)),\
        "Multiple YAMLs are defined for the same property"

    return yaml_objects
