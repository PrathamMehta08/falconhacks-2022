import inspect, utils, hashlib

class MandatoryArg:
    pass

#get the argument from a function and return a dict
def get_args(func):
    defaults = {}
    arg_spec = inspect.getfullargspec(func)

    for arg in arg_spec.args:
        defaults[arg] = MandatoryArg()
    i = len(defaults) - 1
    for default in arg_spec.defaults[::-1]:
        key = arg_spec.args[i]
        defaults[key] = default
        i -= 1
    return defaults

#parse query arguments and raise an error if one is missing
def parse_args(defaults, args):
    returned = {}
    for key in defaults:
        arg = args.get(key)
        if arg == None:
            if type(defaults[key]) is MandatoryArg:
                raise ValueError("Missing argument: "+key)
            returned[key] = defaults[key]
        else:
            try:
                returned[key] = float(args[key])
            except ValueError:
                returned[key] = args[key]
    return returned

def hash_string(string):
    return hashlib.sha256(string.encode()).hexdigest()