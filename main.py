import os
import sys
import json
import random
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

def generate_test_sample(num):
    # scan the schema directory
    if not os.path.exists('./json_data'):
        os.mkdir('./json_data')
    if not os.path.exists('./schemas'):
        os.mkdir('./schemas')
        schema_hashes = []
    else: # load existing schemas and convert them to hashable format
        schemas = os.listdir('./schemas')
        schema_hashes = [schema.split('.')[0] for schema in schemas]
    
    # generate schema and corresponding json data
    for i in tqdm(range(num), desc='Generating test samples'):
        schema = generate_schema()
        try:
            # check if the schema has been generated before
            tuple_schema = dict_to_tuple(schema)
            schema_hash = hash(tuple_schema)
            if schema_hash in schema_hashes:
                continue
            # if not, add the schema hash to the list
            schema_hashes.append(schema_hash)
            
            json_datas = []
            for j in range(50):
                json_data = generate_json_data(schema)
                json_datas.append(json_data)
            # save schema
            schema_path = os.path.join('./schemas', f'{schema_hash}.json')
            with open(schema_path, 'w') as f:
                json.dump(schema, f, indent=4)
            # save json data
            json_data_path = os.path.join('./json_data', f'{schema_hash}_json_data.json')
            with open(json_data_path, 'w') as f:
                json.dump(json_datas, f, indent=4)
        except:
            continue

def conduct_differential_testing():
    '''
    Func: load test cases and conduct differential testing
    '''
    # conduct differential testing
    failed_cases = []
    for schema_file in tqdm(os.listdir('./schemas'), desc='Conducting differential testing'):
        # load schema
        schema_path = os.path.join('./schemas', schema_file)
        with open(schema_path, 'r') as f:
            schema = json.load(f)
        # load json data
        json_data_path = os.path.join('./json_data', f'{schema_file.split(".")[0]}_json_data.json')
        with open(json_data_path, 'r') as f:
            json_datas = json.load(f)
        # test json data that suppose to pass the schema checker
        for json_data in json_datas: 
            result = differential_testing(schema, json_data)
            if result == False:
                failed_cases.append((schema, json_data))
                break # if one json data fails, then skip the rest
        # test json data that are supposed to fail the schema checker
        # randomly pick n schema

        other_schema_files = random.sample(os.listdir('./schemas'), len(json_datas))
        for other_schema_file in other_schema_files:
            # load their json data
            json_data_path = os.path.join('./json_data', f'{other_schema_file.split(".")[0]}_json_data.json')
            with open(json_data_path, 'r') as f:
                json_datas = json.load(f)
            # randomly pick 1 json data
            other_json_data = random.choice(json_datas)
            result = differential_testing(schema, other_json_data)
            if result == False:
                failed_cases.append((schema, other_json_data))
    
    # save failed cases
    with open('failed_cases.json', 'w') as f:
        json.dump(failed_cases, f, indent=4)

def clean_data():
    '''
    Func: clean data
    '''
    if os.path.exists('./json_data'):
        os.system('rm -rf ./json_data')
    if os.path.exists('./schemas'):
        os.system('rm -rf ./schemas')
    if os.path.exists('./failed_cases.json'):
        os.system('rm -rf ./failed_cases.json')

def main():
    clean_data()
    generate_test_sample(10000)
    conduct_differential_testing()

if __name__ == '__main__':
    main()