from ast import literal_eval
from behave import given, when, then, register_type
from behave_pandas import dataframe_to_table, table_to_dataframe
import importlib
import inspect
import pandas as pd
import parse
import re

DEFAULT_COLUMN_LEVEL = 1


@parse.with_pattern(r"\((\w+?, ?)+?\w*?\)")
def _parse_tuple(string):
    string = re.sub(r"(\w+)", r'"\1"', string) # add quotes
    t = literal_eval(string)
    if not isinstance(t, tuple):
        raise ValueError(f"the given value {string} cannot be interpreted as tuple")
    return t


@parse.with_pattern(r"\{(\w+?: \w+?, ?)*?(\w+?: \w+?)?\}")
def _parse_dict(string):
    string = re.sub(r"(\w+)", r'"\1"', string) # add quotes
    d = literal_eval(string)
    if not isinstance(d, dict):
        raise ValueError(f"the given value {string} cannot be interpreted as dict")
    return d


@parse.with_pattern(r"(\((\w+?, ?)+?\w*?\)|\w*?)")
def _parse_func_result(string):
    if re.match(r"^\w*?$", string):
        return (string, )
    else:
        return _parse_tuple(string)


@parse.with_pattern(r".+?(\..+?)+?")
def _parse_module(string):
    return string


register_type(Tuple=_parse_tuple)
register_type(Dict=_parse_dict)
register_type(Result=_parse_func_result)
register_type(Module=_parse_module)


def _add_var(context, name, val):
    if "vars" not in context:
        context.vars = {}

    if name in context.vars:
        raise ValueError(f"variable {name} cannot be overwritten")

    context.vars[name] = val


def _get_var(context, name):
    if "vars" not in context or name not in context.vars:
        raise ValueError(f"variable {name} has not been set")

    return context.vars[name]


def _has_var(context, name):
    return "vars" in context and name in context.vars


@given("the following table is loaded into dataframe {name:w}")
def step_impl(context, name):
    _add_var(
        context,
        name,
        table_to_dataframe(context.table, column_levels=DEFAULT_COLUMN_LEVEL),
    )


@given("the value {val} is loaded into variable {name:w}")
def step_impl(context, val, name):
    _add_var(context, name, literal_eval(val))


@given("the following variables are loaded")
def step_impl(context):
    table = context.table

    if "var" not in table.headings and "val" not in table.headings:
        raise ValueError("table has to contain a 'val' and 'var' column")

    for row in table:
        _add_var(context, row["var"], literal_eval(row["val"]))


def _check_func_arguments(context, func):
    """
    Checks whether all required arguments of a function are available in the context's variables.

    :return: None if the function cannot be called with the given variables,
        names of available args, varargs, kwargs, and varkw - otherwise.
    """
    spec = inspect.getfullargspec(func)

    args = spec.args
    varargs = spec.varargs
    kwargs = spec.kwonlyargs
    varkw = spec.varkw

    available_args = [arg for arg in args if _has_var(context, arg)]
    available_varargs = varargs if varargs and _has_var(context, varargs) else None
    available_kwargs = [kwarg for kwarg in kwargs if _has_var(context, kwarg)]
    available_varkw = varkw if varkw and _has_var(context, varkw) else None

    if spec.defaults and varargs is None:
        required_args = args[: -len(spec.defaults)]
    else:
        required_args = args
    has_required_args = all([arg in available_args for arg in required_args])
    has_required_varargs = varargs is None or available_varargs == varargs

    required_kwargs = [kwarg for kwarg in kwargs if kwarg not in spec.kwonlydefaults]
    has_required_kwargs = all([kwarg in available_kwargs for kwarg in required_kwargs])
    has_required_varkw = varkw is None or available_varkw == available_varkw

    if (
        has_required_args
        and has_required_varargs
        and has_required_kwargs
        and has_required_varkw
    ):
        return available_args, available_varargs, available_kwargs, available_varkw

    else:
        error_msg = []
        if not has_required_args:
            error_msg.append(
                f"required arguments are missing: {[arg for arg in required_args if arg not in available_args]}"
            )
        if not has_required_varargs:
            error_msg.append(f"required varargs is missing: {varargs}")
        if not has_required_kwargs:
            error_msg.append(
                f"required kwargs are missing: {[kwarg for kwarg in required_kwargs if kwarg not in available_kwargs]}"
            )
        if not has_required_varkw:
            error_msg.append(f"required varkw is missing: {varkw}")

        raise ValueError("\n".join(error_msg))


def _run_func(context, func_name, module, result_vars):
    module = importlib.import_module(module)
    func = getattr(module, func_name)

    args, varargs, kwargs, varkw = _check_func_arguments(context, func)

    args_vals = [_get_var(context, arg) for arg in args]
    varargs_vals = _get_var(context, varargs) if varargs else None
    kwargs_vals = {kwarg: _get_var(context, kwarg) for kwarg in kwargs}
    varkw_vals = _get_var(context, varkw) if varkw else {}

    if varargs:
        results = func(*args_vals, *varargs_vals, **kwargs_vals, **varkw_vals)

    else:
        results = func(
            **{arg: arg_val for arg, arg_val in zip(args, args_vals)},
            **kwargs_vals,
            **varkw_vals,
        )

    if not isinstance(results, tuple):
        results = (results,)

    if len(results) == len(result_vars):
        for name, val in zip(result_vars, results):
            _add_var(context, name, val)
    elif len(result_vars) == 1:
        _add_var(context, result_vars[0], results)
    else:
        raise ValueError(
            f"length mismatch of function returns ({len(results)}) and given variable names ({len(result_vars)})"
        )


@when(
    "the function {func_name:w} of module {module:Module} is called writing the results to {result_vars:Result}"
)
def step_impl(context, func_name, module, result_vars):
    _run_func(context, func_name, module, result_vars)


@then("dataframe {name:w} is equal to")
def step_impl(context, name):
    pd.testing.assert_frame_equal(
        _get_var(context, name),
        table_to_dataframe(context.table, column_levels=DEFAULT_COLUMN_LEVEL),
    )


@then("the string representation of dataframe {name:w} is equal to")
def step_impl(context, name):
    table_representation = dataframe_to_table(_get_var(context, name))
    assert (
        table_representation == context.text
    ), f"dataframe {name} does not match the expected text\nactual:\n{table_representation}"


@then("dataframe {name1:w} is equal to dataframe {name2:w}")
def step_impl(context, name1, name2):
    pd.testing.assert_frame_equal(_get_var(context, name1), _get_var(context, name2))


@then("the value of variable {name:w} is {true_val}")
def step_impl(context, name, true_val):
    actual_val = _get_var(context, name)
    assert actual_val == literal_eval(true_val), f"actual value is {actual_val}"


@then("the type of variable {name:w} is {true_type:w}")
def step_impl(context, name, true_type):
    actual_type = type(_get_var(context, name)).__name__
    assert actual_type == true_type, f"actual type is {actual_type}"
