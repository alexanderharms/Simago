from simago.probability import construct_query_string
from simago.yamlutils import load_yamls

def test_construct_query_string():
    option = 0
    property_name = 'sex'
    relation_list = ['eq', 'leq', 'geq', 'le', 'gr', 'neq']

    test_list = ['sex == 0', 'sex <= 0', 'sex >= 0', 
                 'sex < 0', 'sex > 0', 'sex ~= 0']
    query_list = [None] * len(relation_list)
    for k, rel in enumerate(relation_list):
        query_list[k] = construct_query_string(property_name, option,rel)

    assert query_list == test_list

# def test_order_probab():
# def test_check_conditionals():
#     yaml_folder = 
#     yaml_filenames = find_yamls(args.yaml_folder)
#     yaml_objects = load_yamls(yaml_filenames)
# 
#     # Based on the yaml_objects, create a list of ProbabilityClass instances.
#     probab_objects = []
#     for y_obj in yaml_objects:
#         probab_objects.append(ProbabilityClass(y_obj)) 


# def test_ProbClass_read_data():
#     test_yaml = "./tests/testdata/ProbabilityClass/sex.yml"
#     yaml_objects = load_yamls([test_yaml])
# 
#     probab_objects = []
#     for y_obj in yaml_objects:
#         probab_objects.append(ProbabilityClass(y_obj)) 
# 
# def test_ProbClass_read_conditionals():
#     test_yaml = "./tests/testdata/ProbabilityClass/sex.yml"
#     yaml_objects = load_yamls([test_yaml])
# 
#     probab_objects = []
#     for y_obj in yaml_objects:
#         probab_objects.append(ProbabilityClass(y_obj)) 
# 
# def test_ProbClass_gen_probss():
#     test_yaml = "./tests/testdata/ProbabilityClass/sex.yml"
#     yaml_objects = load_yamls([test_yaml])
# 
#     probab_objects = []
#     for y_obj in yaml_objects:
#         probab_objects.append(ProbabilityClass(y_obj)) 
# 
# def test_ProbClass_init():
