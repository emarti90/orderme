# Import General Packages
from jsonschema import Draft4Validator
from jsonschema.exceptions import best_match

def validate_input(input, schema, log):
    log.info('Validating input schema')
    result = False
    error = best_match(Draft4Validator(schema).iter_errors((input)))
    if error:
        log.info('input NOT VALID')
    else:
        log.info('input VALID')
        result = True
    return result
