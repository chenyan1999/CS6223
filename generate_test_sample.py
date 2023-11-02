import re
import random
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
    schema_version = ['http://json-schema.org/draft-04/schema#', 'http://json-schema.org/draft-06/schema#', 'http://json-schema.org/draft-07/schema#']
    type_list = ['string', 'number', 'integer', 'boolean', 'object','null']
    leaf_type_list = ['string', 'number', 'integer', 'boolean', 'null']
    init_weight = [1, 1, 1, 1, 10, 0.5]
    mid_layer_weight = [1, 1, 1, 1, 1, 0.5]
    
    max_deepth = 4
    if level == 0:
        schema["$schema"] = random.choice(schema_version)
    # generate type
    if level == 0:
        schema["type"] = random.choices(type_list, weights=init_weight, k=1)[0]
    elif level != max_deepth:
        schema["type"] = random.choices(type_list, weights=mid_layer_weight, k=1)[0]
    else:
        schema["type"] = random.choices(leaf_type_list, k=1)[0]
    # generate properties
    if schema["type"] == 'string':
        if random.choice([True, False]):
            schema["format"] = random.choice(['float','date-time', 'time', 'date', 'email', 'hostname', 'ipv4', 'ipv6', 'uri', 'uri-reference', 'uri-template', 'json-pointer', 'relative-json-pointer'])
        return schema
        if random.choice([True, False]):
            schema["minLength"] = random.randint(1, 100)
        if random.choice([True, False]):
            if "minLength" in schema:
                schema["maxLength"] = random.randint(schema["minLength"], 200)
            else:
                schema["maxLength"] = random.randint(0, 200)
        if random.choice([True, False]):
            schema["pattern"] = get_random_regex()
        if level == max_deepth:
            return schema
    elif schema["type"] == 'number':
        if random.choice([True, False]):
            random_number = random.randint(0, 50)
            if random.choice([True, False]):
                schema["minimum"] = random.choice([random_number, float(random_number)])
            else:
                schema["exclusiveMinimum"] = random.choice([random_number, float(random_number)])
        if random.choice([True, False]):
            if "minimum" in schema:
                random_number = random.randint(schema["minimum"], 100)
            elif "exclusiveMinimum" in schema:
                random_number = random.randint(schema["exclusiveMinimum"], 100)
            else:
                random_number = random.randint(0, 100)
            if random.choice([True, False]):
                schema["maximum"] = random.choice([random_number, float(random_number)])
            else:
                schema["exclusiveMaximum"] = random.choice([random_number, float(random_number)])
        if random.choice([True, False]):
            schema["multipleOf"] = random.uniform(1.0, 5.0)
        if level == max_deepth:
            return schema
    elif schema["type"] == 'integer':
        if random.choice([True, False]):
            random_number = random.randint(0, 50)
            if random.choice([True, False]):
                schema["minimum"] = random.choice([random_number, float(random_number)])
            else:
                schema["exclusiveMinimum"] = random.choice([random_number, float(random_number)])
        if random.choice([True, False]):
            if "minimum" in schema:
                random_number = random.randint(schema["minimum"], 100)
            elif "exclusiveMinimum" in schema:
                random_number = random.randint(schema["exclusiveMinimum"], 100)
            else:
                random_number = random.randint(0, 100)
            if random.choice([True, False]):
                schema["maximum"] = random.choice([random_number, float(random_number)])
            else:
                schema["exclusiveMaximum"] = random.choice([random_number, float(random_number)])
        if random.choice([True, False]):
            random_number = random.randint(1, 5)
            schema["multipleOf"] = random.choice([random_number, float(random_number)])
        if level == max_deepth:
            return schema
    elif schema["type"] == 'boolean':
        return schema
    elif schema["type"] == 'array':
        if random.choice([True, False]):
            schema["minItems"] = random.randint(0, 6)
        if random.choice([True, False]):
            if "minItems" in schema:
                schema["maxItems"] = random.randint(schema["minItems"], 20)
            else:
                schema["maxItems"] = random.randint(0, 20)
        if random.choice([True, False]):
            schema["uniqueItems"] = random.choice([True, False])
        if random.choice([True, False]):
            if level == max_deepth:
                return schema
            schema["items"] = generate_schema(level+1)
    elif schema["type"] == "object":
        if random.choice([True, False]):
            schema["minProperties"] = random.randint(1, 3)
        if random.choice([True, False]):
            if "minProperties" in schema:
                schema["maxProperties"] = random.randint(schema["minProperties"], 6)
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
        schema["properties"] = {}
        for i in range(property_num):
            schema["properties"][f"key_{str(i)}"] = generate_schema(level+1)
        if random.choice([True, False]) and "properties" in schema:
            schema["required"] = random.sample(list(schema["properties"].keys()), random.randint(1, len(schema["properties"])))
    return schema

def generate_json_data(schema):
    faker = JSF(schema)
    return faker.generate()