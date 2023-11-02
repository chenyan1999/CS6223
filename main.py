import os
import json
from jsf import JSF
from tqdm import tqdm
import fastjsonschema
from generate_test_sample import generate_schema, generate_json_data
from diff_test import differential_testing

def dict_to_tuple(d):
    if isinstance(d, dict):
        # 将字典的键值对转换为元组，并对键进行排序以确保顺序一致性
        items = sorted((key, dict_to_tuple(value)) for key, value in d.items())
        return tuple(items)
    elif isinstance(d, (list, tuple)):
        # 处理可能包含嵌套字典的列表或元组
        return tuple(dict_to_tuple(item) for item in d)
    else:
        return None

def tuple_to_dict(t):
    if isinstance(t, tuple):
        # 如果是元组，还原为字典
        result_dict = {}
        for item in t:
            key, value = item
            result_dict[key] = tuple_to_dict(value)
        return result_dict
    elif isinstance(t, (list, tuple)):
        # 处理可能包含嵌套字典的列表或元组
        return [tuple_to_dict(item) for item in t]
    else:
        return None  # 不可变类型，直接返回

def generate_test_sample():
    if os.path.exists('test_set.json'):
        with open('test_set.json', 'r') as f:
            dataset = json.load(f)
    else:
        dataset = {}
    for i in tqdm(range(100), desc='Generating test schema and json data'):
        schema = generate_schema()
        tuple_schema = dict_to_tuple(schema)
        if tuple_schema in dataset:
            continue
        dataset[tuple_schema] = []
        faker = JSF(schema)
        try:
            faker.generate()
        except:
            continue
        for j in range(50):
            json_data = faker.generate()
            dataset[tuple_schema].append(json_data)
    with open('test_set.json', 'w') as f:
        json.dump(dataset, f, indent=4)

def conduct_differential_testing(dataset):
    '''
    Func: load test cases and conduct differential testing
    '''
    # load json schema and corresponding json data
    # in a dict format: {schema: [json_data1, json_data2, ...]}

    # conduct differential testing
    failed_cases = []
    for schema in dataset:
        # test json data that suppose to pass the schema checker
        for json_data in dataset[schema]: 
            result = differential_testing(schema, json_data)
            if result == False:
                failed_cases.append((schema, json_data))
        # test json data that are supposed to fail the schema checker
        # randomly pick n schema
        other_schemas = random.sample(dataset.keys(), len(dataset[schema]))
        for other_schema in other_schemas:
            # randomly pick 1 json data
            other_json_data = random.choice(dataset[other_schema])
            result = differential_testing(schema, other_json_data)
            if result == False:
                failed_cases.append((schema, other_json_data))
    
    # save failed cases
    with open('failed_cases.json', 'w') as f:
        json.dump(failed_cases, f, indent=4)

def main():
    generate_test_sample()
    # conduct_differential_testing()

if __name__ == '__main__':
    main()