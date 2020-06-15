import yaml
import pytest
from simago.yamlutils import find_yamls
from simago.yamlutils import load_yamls
from simago.yamlutils import check_yaml

def test_find_yamls():
    folder_name = "./tests/testdata/find_yamls/"
    yaml_filenames = find_yamls(folder_name)
    test_filenames = ['./tests/testdata/find_yamls/a.yml', 
                      './tests/testdata/find_yamls/b.yaml']

    assert yaml_filenames == test_filenames

# def test_load_yamls_YAMLError():
#     # If YAML does not contain valid YAML content, 
#     # raise yaml.YAMLError
#     # Create YAML with invalid content
#     yaml_filenames = ["./tests/testdata/invalid_yaml/invalid.yaml"]
#     with pytest.raises(yaml.YAMLError):
#         yaml_objects = load_yamls(yaml_filenames)

def test_load_yamls_multi_prop():
    # If multiple YAML files are defined for the same property, trigger an
    # AssertionError.
    testfolder = "./tests/testdata/load_yamls-multiple_properties/"
    yaml_filenames = find_yamls(testfolder)
    with pytest.raises(AssertionError):
        yaml_objects = load_yamls(yaml_filenames)

def test_check_yaml():
    testfiles = ["./tests/testdata/check_yaml/no_property_name.yml",
            "./tests/testdata/check_yaml/incorrect_property_name_type.yml",
            "./tests/testdata/check_yaml/no_data_type.yml",
            "./tests/testdata/check_yaml/incorrect_data_type.yml",
            "./tests/testdata/check_yaml/invalid_data_type.yml"]
    for testfile in testfiles:
        testfile = [testfile]
        with pytest.raises(AssertionError):
            yaml_objects = load_yamls(testfile)
    
# 
# def test_check_yaml():






