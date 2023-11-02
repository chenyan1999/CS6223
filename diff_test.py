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
    jsonschema_exception = None
    jsonschema_exception_code = -1
    try:
        # raise exception if json_data does not match schema
        jsonschema.validate(json_data, schema)
    except: # record exception
        jsonschema_exception = sys.exc_info()[0].__name__
        if jsonschema_exception == 'ValidationError':
            # means that the json_data does not match schema
            jsonschema_exception_code = 0
        if jsonschema_exception == 'SchemaError':
            # means that the schema is invalid
            jsonschema_exception_code = 1

    fastjsonschema_exception = None
    fastjsonschema_exception_code = -1
    try:
        # raise exception if json_data does not match schema
        fastjsonschema.validate(schema, json_data)
    except: # record exception
        fastjsonschema_exception = sys.exc_info()[0].__name__
        if fastjsonschema_exception == 'JsonSchemaValueException':
            # means that the json_data does not match schema
            fastjsonschema_exception_code = 0
        if fastjsonschema_exception == 'JsonSchemaDefinitionException':
            # means that the schema is invalid
            fastjsonschema_exception_code = 1

    # if none of the two methods raise exception, then they return the same result
    if jsonschema_exception_code == -1 and fastjsonschema_exception_code == -1:
        return True
    else: # at least one of the two methods raise exception
        if jsonschema_exception_code == fastjsonschema_exception_code:
            return True
        else:
            return False