import re
import random
import numpy as np
from jsf import JSF
from rbloom import Bloom
from random_regex import RegexGenerator

def get_random_regex():
    def assert_all_match(examples, regex):
        re_com = re.compile(regex)
        for ex in examples:
            assert re_com.fullmatch(ex) is not None
    
    regex_generator = RegexGenerator(bloom_cls=Bloom).generate()
    try:
        for instance in regex_generator:
            regex = instance['regex']
            complexity = instance['complexity']
            length = instance['length']
            examples = instance['examples']
            re.compile(regex)
            assert len(regex) == length
            assert len(examples) == complexity
            assert_all_match(examples, regex)
            return regex
    except:
        return get_random_regex()

def generate_schema(level=0):
    '''
    Func: generate random json schema
    '''
    schema = {}
    schema_version = ['http://json-schema.org/draft-04/schema#','http://json-schema.org/draft-06/schema#', 'http://json-schema.org/draft-07/schema#', 'https://json-schema.org/draft/2020-12/schema']
    type_list = ['string', 'number', 'integer', 'boolean', 'object', 'array', 'null']
    leaf_type_list = ['string', 'number', 'integer', 'boolean', 'null']
    init_weight = [1, 1, 1, 1, 10, 2, 0.5]
    mid_layer_weight = [1, 1, 1, 1, 1, 1, 0.5]
    
    max_deepth = 4
    if level == 0:
        schema["$schema"] = random.choice(schema_version)
        schema['$id'] = "id"
        if random.choice([True, False]):
            schema["contentMediaType"] = "application/json"
        if random.choice([True, False]):
            schema['title'] = "title"
        if random.choice([True, False]):
            schema['description'] = "description"
    # generate type
    if level == 0:
        schema["type"] = random.choices(type_list, weights=init_weight, k=1)[0]
    elif level != max_deepth:
        schema["type"] = random.choices(type_list, weights=mid_layer_weight, k=1)[0]
    else:
        schema["type"] = random.choices(leaf_type_list, k=1)[0]
    # generate properties
    if schema["type"] == 'string':
        if random.choice([True, False]):  # 50% chance to add format
            schema["format"] = random.choice(['float','date-time', 'time', 'date', 'email', 'hostname', 'ipv4', 'ipv6', 'uri', 'uri-reference', 'uri-template', 'json-pointer', 'relative-json-pointer'])
            if random.choice([True, False]): # 50% chance to add formatMinimum
                schema["formatMinimum"] = random.randint(0, 100)
            if random.choice([True, False]): # 50% chance to add formatMaximum
                if "formatMinimum" in schema:
                    schema["formatMaximum"] = random.randint(schema["formatMinimum"]+1, 200)
                else:
                    schema["formatMaximum"] = random.randint(0, 200)
            return schema
        if random.choice([True, False]): # 50% chance to add minLength
            schema["minLength"] = random.randint(1, 100)
        if random.choice([True, False]): # 50% chance to add maxLength
            if "minLength" in schema:
                schema["maxLength"] = random.randint(schema["minLength"]+1, 200)
            else:
                schema["maxLength"] = random.randint(0, 200)
        if random.choice([True, False]): # 50% chance to add pattern
            schema["pattern"] = get_random_regex()
        if random.choice([True, False]): # 50% chance to add contentEncoding
            schema["contentEncoding"] = random.choice(['7-bit', '8-bit', 'binary', 'quoted-printable', 'base-16', 'base-32', 'base-64'])
        if level == max_deepth:
            return schema
    elif schema["type"] == 'number':
        if random.choice([True, False]): # 50% chance to add minimum or exclusiveMinimum
            random_number = random.uniform(-1e10, 1e10)
            if random.choice([True, False]):
                schema["minimum"] = random_number
            else:
                schema["exclusiveMinimum"] = random_number
        if random.choice([True, False]): # 50% chance to add maximum or exclusiveMaximum
            if "minimum" in schema:
                random_number = random.uniform(schema["minimum"]+1, 1e10)
            elif "exclusiveMinimum" in schema:
                random_number = random.uniform(schema["exclusiveMinimum"]+1, 1e10)
            else:
                random_number = np.random.normal()
            if random.choice([True, False]):
                schema["maximum"] = random_number
            else:
                schema["exclusiveMaximum"] = random_number
        if random.choice([True, False]): # 50% chance to add enum
            if "minimum" in schema:
                min_number = schema["minimum"]
            elif "exclusiveMinimum" in schema:
                min_number = schema["exclusiveMinimum"]
            else:
                min_number = 0
            if "maximum" in schema:
                max_number = schema["maximum"]
            elif "exclusiveMaximum" in schema:
                max_number = schema["exclusiveMaximum"]
            else:
                max_number = 100
            # 从 min_number 到 max_number 之间随机选取10个数
            schema["enum"] = random.sample([random.uniform(min_number, max_number) for _ in range(10)], 10)
        if level == max_deepth:
            return schema
    elif schema["type"] == 'integer':
        if random.choice([True, False]): # 50% chance to add minimum or exclusiveMinimum
            random_number = random.randrange(int(-1e10), int(1e10))
            if random.choice([True, False]):
                schema["minimum"] = random.choice([random_number, float(random_number)])
            else:
                schema["exclusiveMinimum"] = random.choice([random_number, float(random_number)])
        if random.choice([True, False]): # 50% chance to add maximum or exclusiveMaximum
            if "minimum" in schema:
                random_number = random.randint(int(schema["minimum"]+1), int(1e10))
            elif "exclusiveMinimum" in schema:
                random_number = random.randint(int(schema["exclusiveMinimum"]+1), int(1e10))
            else:
                random_number = random.randrange(int(-1e10), int(1e10))
            if random.choice([True, False]):
                schema["maximum"] = random.choice([random_number, float(random_number)])
            else:
                schema["exclusiveMaximum"] = random.choice([random_number, float(random_number)])
        if random.choice([True, False]): # 50% chance to add multipleOf
            random_number = random.randint(1, 10)
            schema["multipleOf"] = random.choice([random_number, float(random_number)])
        if level == max_deepth:
            return schema
    elif schema["type"] == 'boolean':
        if random.choice([True, False]): # 50% chance to add enum
            schema["enum"] = [True, False]
        return schema
    elif schema["type"] == 'array':
        if level == max_deepth:
            return schema
        if random.choice([True, False]): # 50% chance to add minItems
            schema["minItems"] = random.randint(0, 6)
        if random.choice([True, False]): # 50% chance to add maxItems
            if "minItems" in schema:
                schema["maxItems"] = random.randint(schema["minItems"]+1, 20)
            else:
                schema["maxItems"] = random.randint(0, 20)
        # if random.choice([True, False]): # 50% chance to add uniqueItems
        #     schema["uniqueItems"] = random.choice([True, False])
        if level == max_deepth:
            return schema
        schema["items"] = generate_schema(level+1)
        return schema
    elif schema["type"] == "object":
        if level == max_deepth:
            return schema
        if random.choice([True, False]): # 50% chance to add minProperties
            schema["minProperties"] = random.randint(1, 3)
        if random.choice([True, False]): # 50% chance to add maxProperties
            if "minProperties" in schema:
                schema["maxProperties"] = random.randint(schema["minProperties"]+1, 6)
            else:
                schema["maxProperties"] = random.randint(1, 6)
        if "min_properties" in schema.keys(): 
            min_properties = schema["minProperties"]
        else:
            min_properties = 1
        if "max_properties" in schema.keys():
            max_properties = schema["maxProperties"]
        else:
            max_properties = 6
        property_num = random.randint(min_properties, max_properties)
        if random.choice([True, False]): # 50% chance to add properties
            schema["properties"] = {}
            for i in range(property_num): # add properties
                schema["properties"][f"key_{str(i)}"] = generate_schema(level+1)
            if random.choice([True, False]) and "properties" in schema: # 50% chance to add required
                schema["required"] = random.sample(list(schema["properties"].keys()), random.randint(1, len(schema["properties"])))
        elif random.choice([True, False]): # 25% chance to add oneof
            schema["oneOf"] = [{}, {}]
            for i in range(2):
                schema["oneOf"][i]["properties"] = {}
                for j in range(property_num):
                    schema["oneOf"][i]["properties"][f"key_{str(j)}"] = generate_schema(level+1)
        else:
            schema["anyOf"] = [{}, {}]
            for i in range(2):
                schema["anyOf"][i]["properties"] = {}
                for j in range(property_num):
                    schema["anyOf"][i]["properties"][f"key_{str(j)}"] = generate_schema(level+1)
        if random.choice([True, False]): # 50% chance to add additionalProperties
            schema["additionalProperties"] = random.choice([True, False, generate_schema(level+1)])
    return schema

def generate_json_data(schema):
    faker = JSF(schema)
    return faker.generate()