# -*- coding: utf-8 -*-
# the deco must can run at python 2.7
import sys
import inspect
from collections import namedtuple, OrderedDict

DefaultArgSpec = namedtuple('DefaultArgSpec', 'has_default default_value')



# def get_method_sig(method):
#     """ Given a function, it returns a string that pretty much looks how the
#     function signature would be written in python.
#
#     :param method: a python method
#     :return: A string similar describing the pythong method signature.
#     eg: "my_method(first_argArg, second_arg=42, third_arg='something')"
#     """
#
#     # The return value of ArgSpec is a bit weird, as the list of arguments and
#     # list of defaults are returned in separate array.
#     # eg: ArgSpec(args=['first_arg', 'second_arg', 'third_arg'],
#     # varargs=None, keywords=None, defaults=(42, 'something'))
#     argspec = inspect.getargspec(method)
#     arg_index = 0
#     args = []
#
#     # Use the args and defaults array returned by argspec and find out
#     # which arguments has default
#     for arg in argspec.args:
#         default_arg = _get_default_arg(argspec.args, argspec.defaults, arg_index)
#         if default_arg.has_default:
#             args.append("%s=%s" % (arg, default_arg.default_value))
#         else:
#             args.append(arg)
#         arg_index += 1
#     return "%s(%s)" % (method.__name__, ", ".join(args))


def _get_default_arg(args, defaults, arg_index):
    """ Method that determines if an argument has default value or not,
    and if yes what is the default value for the argument

    :param args: array of arguments, eg: ['first_arg', 'second_arg', 'third_arg']
    :param defaults: array of default values, eg: (42, 'something')
    :param arg_index: index of the argument in the argument array for which,
    this function checks if a default value exists or not. And if default value
    exists it would return the default value. Example argument: 1
    :return: Tuple of whether there is a default or not, and if yes the default
    value, eg: for index 2 i.e. for "second_arg" this function returns (True, 42)
    """
    if not defaults:
        return DefaultArgSpec(False, None)

    args_with_no_defaults = len(args) - len(defaults)

    if arg_index < args_with_no_defaults:
        return DefaultArgSpec(False, None)
    else:
        value = defaults[arg_index - args_with_no_defaults]
        if (type(value) is str):
            value = '"%s"' % value
        return DefaultArgSpec(True, value)


def get_params_map(argspec, args, kwargs):
    """return a func call frame outside  and before the func call ."""
    params = OrderedDict()
    arg_index = 0
    for arg in argspec.args:
        default_arg = _get_default_arg(argspec.args, argspec.defaults, arg_index)
        if default_arg.has_default:
            params.update({arg: default_arg.default_value})
        else:
            params.update({arg: None})
        arg_index += 1
    params.update(kwargs)
    for k, v in zip(args, params.keys()):
        params[v] = k
    return params


def get_func_params_2(f):
    def wrapper(*args, **kwargs):
        # TODO VICI DEBUG
        if not callable(f):
            raise TypeError('{!r} is not a callable object'.format(f))
        print(1, 'at func {} now.'.format(f.__name__))
        argspec = inspect.getargspec(f)
        print(2, argspec)
        print(3, 'got in args', args)
        print(4, 'got in kwargs', kwargs)
        a = get_params_map(argspec, args, kwargs)
        arg_str = ['{}={}'.format(k, v) for k, v in a.items()]
        print("5 %s(%s)" % (f.__name__, ", ".join(arg_str)))

        return f(*args, **kwargs)
    return wrapper


@get_func_params_2
def test_func_2(a, b, c=2, **kwargs):
    return a, b, c, kwargs


def get_func_params_3(f):
    def wrapper(*args, **kwargs):
        # TODO VICI DEBUG
        print('*'*20)
        print('[!]in wrpper')
        # func_args = inspect.getargspec(f)
        # print(0, func_args)
        func_signature = inspect.signature(f)
        print(1, func_signature)
        bound_args = func_signature.bind(*args, **kwargs)
        print(2, bound_args)
        bound_args.apply_defaults()
        print(3, dict(bound_args.arguments))

        return f(*args, **kwargs)
    return wrapper


@get_func_params_3
def test_func_3(a, b, c=2, **kwargs):
    return a, b, c, kwargs


if __name__ == '__main__':

    # print(get_method_sig(test_func_2))
    print(sys.version_info)
    if sys.version_info <= (3, ):
        print('in python version 2')
        print('*'*20)
        print('outside', test_func_2(1, 2))
        print('*'*20)
        print('outside', test_func_2(1, 2, 3))
        print('*'*20)
        print('outside', test_func_2(1, 2, c=3))
        print('*'*20)
        print('outside', test_func_2(a=1, b=2, d=3, c=6))
        print('*'*20)
    else:
        print('in python version 3 ')
        print('outside', test_func_3(1, 2, d=3))

