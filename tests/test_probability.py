from simago.probability import construct_query_string

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

# def test_ProbClass_init():


