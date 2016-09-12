import inspect
import wrapt
import os
import sys

def inspect_call_args(show_params=True):
    '''
    Printing call arguments without using decorators.
    Preferred because in case of nested calls with decorator stack trace gets ugly
    '''
    frame = inspect.currentframe().f_back.f_back
    #frame = inspect.currentframe().f_back
    args, _, _, values = inspect.getargvalues(frame)
    frame_info = inspect.getframeinfo(frame)
    if 'self' in frame.f_locals:
        name = repr(frame.f_locals['self'].__class__.__name__) + '.'
        arg_index = 1
    else:
        name=''
        arg_index = 0
    print(os.path.basename(frame_info.filename) + '[' + str(frame_info.lineno) + ']:' + name + frame_info.function, end="(")

    printed = 0
    for i in range(arg_index,len(args)):
        argument = args[i]
        if show_params:
            if printed != 0:
                print(',', end=" ")
            print('{:s}={:s}'.format(repr(argument), repr(values[argument])), end="")
        printed += 1
    print(')')
    sys.stdout.flush()

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
