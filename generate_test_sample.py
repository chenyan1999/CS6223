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
    type_list = ['string', 'number', 'integer', 'boolean', 'object', 'array', 'null']
    weight = [1, 1, 1, 1, 3, 3, 1]
    
    max_deepth = 5
    if level == 0:
        schema["$schema"] = random.choice(schema_version)
    # generate type
    schema["type"] = random.choices(type_list, weights=weight, k=1)[0]
    # generate properties
    if schema["type"] == 'string':
        if random.choice([True, False]):
            schema["minLength"] = random.randint(0, 100)
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
            schema["minimum"] = random.randint(0, 100)
            if random.choice([True, False]):
                schema["exclusiveMinimum"] = random.choice([True, False])
        if random.choice([True, False]):
            if "minimum" in schema:
                schema["maximum"] = random.randint(schema["minimum"], 100)
            else:
                schema["maximum"] = random.randint(0, 100)
            if random.choice([True, False]):
                schema["exclusiveMaximum"] = random.choice([True, False])
        if level == max_deepth:
            return schema
    elif schema["type"] == 'integer':
        if random.choice([True, False]):
            schema["minimum"] = random.randint(0, 50)
            if random.choice([True, False]):
                schema["exclusiveMinimum"] = random.choice([True, False])
        if random.choice([True, False]):
            if "minimum" in schema:
                schema["maximum"] = random.randint(schema["minimum"], 100)
            else:
                schema["maximum"] = random.randint(0, 100)
            if random.choice([True, False]):
                schema["exclusiveMaximum"] = random.choice([True, False])
        if random.choice([True, False]):
            schema["multipleOf"] = random.randint(1, 5)
        if level == max_deepth:
            return schema
    elif schema["type"] == 'boolean':
        return schema
    elif schema["type"] == 'array':
        if random.choice([True, False]):
            schema["minItems"] = random.randint(0, 10)
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
    elif schema["type"] == 'object':
        if random.choice([True, False]):
            schema["minProperties"] = random.randint(0, 5)
        if random.choice([True, False]):
            if "minProperties" in schema:
                schema["maxProperties"] = random.randint(schema["minProperties"], 10)
            else:
                schema["maxProperties"] = random.randint(0, 10)
        if "min_properties" in schema:
            min_properties = schema["minProperties"]
        else:
            min_properties = 1
        if "max_properties" in schema:
            max_properties = schema["maxProperties"]
        else:
            max_properties = 10
        for i in range(random.randint(min_properties, max_properties)):
            if level == max_deepth:
                return schema
            schema["property"] = {}
            schema["property"][f"key_{str(i)}"] = generate_schema(level+1)
        if random.choice([True, False]) and "property" in schema:
            try:
                schema["required"] = random.sample(list(schema["property"].keys()), random.randint(1, len(schema["property"])))
            except:
                print(schema["property"].keys())
                print(random.randint(1, len(schema["property"])))
                raise Exception
    
    return schema

def generate_json_data(schema):
    try:
        faker = JSF(schema)
        return faker.generate()
    except:
        print(schema)
        raise Exception