import inspect
import os
import sys

def format_arg_value(arg_val):
    """ Return a string representing a (name, value) pair.
    >>> format_arg_value(('x', (1, 2, 3)))
    'x=(1, 2, 3)'
    """
    arg, val = arg_val
    return "%s=%r" % (arg, val)

def trace(fn, write=sys.stdout.write):
    """ Echo calls to a function.

    Returns a decorated version of the input function which "echoes" calls
    made to it by writing out the function's name and the arguments it was
    called with.
    """
    import functools
    # Unpack function's arg count, arg names, arg defaults
    code = fn.__code__
    argcount = code.co_argcount
    argnames = code.co_varnames[:argcount]
    fn_defaults = fn.__defaults__ or list()
    argdefs = dict(zip(argnames[-len(fn_defaults):], fn_defaults))

    @functools.wraps(fn)
    def wrapped(*v, **k):
        # Collect function arguments by chaining together positional,
        # defaulted, extra positional and keyword arguments.
        positional = map(format_arg_value, zip(argnames, v))
        defaulted = [format_arg_value((a, argdefs[a]))
                     for a in argnames[len(v):] if a not in k]
        nameless = map(repr, v[argcount:])
        keyword = map(format_arg_value, k.items())
        args = list(positional) + list(defaulted) + list(nameless) + list(keyword)
        class_name = fn.__class__
        write( fn.__name__ + "(%s)\n" % ", ".join(args))
        return fn(*v, **k)
    return wrapped

def inspect_call_args(show_params=True):
    frame = inspect.currentframe().f_back
    args, _, _, values = inspect.getargvalues(frame)
    frame_info = inspect.getframeinfo(frame)
    print(os.path.basename(frame_info.filename) + '[' + str(frame_info.lineno) + ']:' + frame_info.function, end="(")
    index = 0
    for i in args:
        if show_params:
            if index != 0:
                print(',', end=" ")
            print('{:s}={:s}'.format(repr(i), repr(values[i])), end="")
        index += 1
    print(')')


