import os
import yaml

def find_yamls(yaml_folder):
    # Gather all the YAML files for the aggregated data in the folder.
    # Return the list of paths to YAML files.
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
    fname = yaml_object['yaml_filename']

    assert 'property_name' in yaml_object.keys(), fname + ', no property defined'
    assert isinstance(yaml_object['property_name'], str),\
            fname + ", incorrect name format"

    assert 'data_type' in yaml_object.keys(), fname + ', no data type defined'
    assert isinstance(yaml_object['data_type'], str),\
            fname + ", incorrect data type"
    assert yaml_object['data_type'] in\
            ['categorical', 'ordinal', 'continuous'],\
            fname + ", invalid data type"

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
            exec(open(yaml_object['pdf_file']).read())
        except:
            print(fname + ', pdf file can not be executed')
            quit()

    if 'conditionals' not in yaml_object.keys():
        yaml_object['conditionals'] = None
    else:
        if yaml_object['conditionals'] is not None:
            assert isinstance(yaml_object['conditionals'], str),\
                    fname + ', conditionals not None or a string'
            assert os.path.isfile(yaml_object['conditionals']),\
                    fname + ', conditionals file does not exist'
            assert yaml_object['conditionals'].endswith('.csv'),\
                    fname + ', conditionals files is not a csv'

    return yaml_object

def load_yamls(yaml_filenames):
    yaml_objects = []
    for yaml_filename in yaml_filenames:
        with open(yaml_filename, 'r') as yaml_file:
            try:
                yaml_object = yaml.safe_load(yaml_file)
            except yaml.YAMLError as exc:
                print(exc)

        yaml_object['yaml_filename'] = yaml_filename
        yaml_objects.append(yaml_object)

    yaml_objects = [check_yaml(obj) for obj in yaml_objects]
    yaml_properties = [obj['property_name'] for obj in yaml_objects]
    assert len(yaml_properties) == len(set(yaml_properties)),\
            "Multiple YAMLs are defined for the same property"

    return yaml_objects
