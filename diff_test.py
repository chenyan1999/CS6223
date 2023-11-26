import sys
import jsonschema
import fastjsonschema

def differential_testing(schema, json_data):
    '''
    Func: conduct differential testing between jsonschema.validate and fastjsonschema.validate
    Args:
        schema: json schema
        json_data: json data
    Return:
        True if two methods return the same result, otherwise False
    '''
    try:
        # raise exception if json_data does not match schema
        jsonschema.validate(json_data, schema)
        jsonschema_pass = True
    except: # record exception
        jsonschema_pass = False

    try:
        # raise exception if json_data does not match schema
        fastjsonschema.validate(schema, json_data)
        fastjsonschema_pass = True
    except: # record exception
        fastjsonschema_pass = False

    # if none of the two methods raise exception, then they return the same result
    if jsonschema_pass == fastjsonschema_pass:
        return True
    else:
        return False