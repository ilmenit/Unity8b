import inspect
import wrapt

@wrapt.decorator
def trace(wrapped, instance, args, kwargs):
    '''
    My custom tracing decorator that doesn't change function signature and works well with defaults and *args
    '''
    function_name = wrapped.__name__
    if instance.__class__ is not type(None):
        class_name = instance.__class__.__name__ + '.'
        arg_index = 1
    else:
        class_name = ''
        arg_index = 0

    argument_names = inspect.getfullargspec(wrapped).args
    defaults = inspect.getfullargspec(wrapped).defaults
    if defaults is None:
        len_defaults = 0
    else:
        len_defaults = len(defaults)
    arguments_count = max(len(args),len_defaults)
    arguments = ''
    for i in range(arguments_count):
        if i != 0:
            arguments += ','

        if (arg_index+i < len(argument_names)):
            name = argument_names[arg_index+i] + '='
        else:
            name = ''
        if i<len(args):
            value = args[i]
        else:
            value = defaults[i]
        arguments += str(name) + str(value)
    print( class_name + function_name + '(' + arguments + ')' )
    return wrapped(*args, **kwargs)
