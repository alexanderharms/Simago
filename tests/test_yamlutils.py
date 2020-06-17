import yaml
import pytest
from simago.yamlutils import find_yamls, load_yamls, check_yaml

def test_find_yamls():
    folder_name = "./tests/testdata/find_yamls/"
    yaml_filenames = find_yamls(folder_name)
    test_filenames = ['./tests/testdata/find_yamls/a.yml', 
                      './tests/testdata/find_yamls/b.yaml']

    assert yaml_filenames == test_filenames

def test_load_yamls_YAMLError():
    # If YAML does not contain valid YAML content, 
    # raise yaml.YAMLError
    # Create YAML with invalid content
    yaml_filenames = ["./tests/testdata/load_yamls-invalid_yaml/invalid.yaml"]
    with pytest.raises(AssertionError):
        yaml_objects = load_yamls(yaml_filenames)

def test_load_yamls_multi_prop():
    # If multiple YAML files are defined for the same property, trigger an
    # AssertionError.
    testfolder = "./tests/testdata/load_yamls-multiple_properties/"
    yaml_filenames = find_yamls(testfolder)
    with pytest.raises(AssertionError):
        yaml_objects = load_yamls(yaml_filenames)

def test_check_yaml():
    testfiles_folder = "./tests/testdata/check_yaml/"
    testfiles = ["no_property_name.yml",
                 "incorrect_property_name_type.yml",
                 "no_data_type.yml",
                 "incorrect_data_type.yml",
                 "invalid_data_type.yml",
                 "no_data_file_defined.yml",
                 "incorrect_data_file.yml",
                 "no_data_file_exists.yml",
                 "data_not_csv.yml",
                 "incorrect_conditionals_type.yml",
                 "cond_not_exist.yml",
                 "cond_not_csv.yml",
                 "no_parameters_defined.yml",
                 "parameters_not_list.yml",
                 "no_pdf_defined.yml",
                 "no_pdf_file_defined.yml",
                 "incorrect_pdf_file.yml",
                 "pdf_file_not_exist.yml",
                 "pdf_file_not_python.yml"]

    for testfile in testfiles:
        testfile = testfiles_folder + testfile
        testfile = [testfile]
        with pytest.raises(AssertionError):
            yaml_objects = load_yamls(testfile)
    
