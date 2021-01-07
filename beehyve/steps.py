from ast import literal_eval
from behave import given, when, then, register_type
from behave_pandas import dataframe_to_table, table_to_dataframe
import importlib
import pandas as pd
import parse
import re

DEFAULT_COLUMN_LEVEL = 1


@parse.with_pattern(r"\((.+?, ?)+?.*?\)")
def _parse_tuple(string):
    string = re.sub(r"(\w+)", r'"\1"', string)
    t = literal_eval(string)
    if not isinstance(t, tuple):
        raise ValueError(f"the given value {string} cannot be interpreted as tuple")
    return t


@parse.with_pattern(r"\{(.+?: .+?, ?)*?(.+?: .+?)?\}")
def _parse_dict(string):
    string = re.sub(r"(\w+)", r'"\1"', string)
    d = literal_eval(string)
    if not isinstance(d, dict):
        raise ValueError(f"the given value {string} cannot be interpreted as dict")
    return d


@parse.with_pattern(r".+?(\..+?)+?")
def _parse_module(string):
    return string


register_type(Tuple=_parse_tuple)
register_type(Dict=_parse_dict)
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


def _run_func(context, func, module, result_vars, args=None, kwargs=None):
    if args is None:
        args = ()
    if kwargs is None:
        kwargs = {}

    module = importlib.import_module(module)
    f = getattr(module, func)
    results = f(
        *(_get_var(context, name) for name in args),
        **{key: _get_var(context, name) for key, name in kwargs.items()},
    )

    if not isinstance(results, tuple):
        results = (results,)

    assert len(results) == len(
        result_vars
    ), f"length mismatch of function returns ({len(results)}) and given variable names ({len(result_vars)})"

    for name, val in zip(result_vars, results):
        _add_var(context, name, val)


@when(
    "the function {func:w} of module {module:Module} is called with args={args:Tuple} and kwargs={kwargs:Dict} writing the results to {result_vars:Tuple}"
)
def step_impl(context, func, module, args, kwargs, result_vars):
    _run_func(context, func, module, result_vars, args=args, kwargs=kwargs)


@when(
    "the function {func:w} of module {module:Module} is called with args={args:Tuple} writing the results to {result_vars:Tuple}"
)
def step_impl(context, func, module, args, result_vars):
    _run_func(context, func, module, result_vars, args=args)


@when(
    "the function {func:w} of module {module:Module} is called with kwargs={kwargs:Dict} writing the results to {result_vars:Tuple}"
)
def step_impl(context, func, module, kwargs, result_vars):
    _run_func(context, func, module, result_vars, kwargs=kwargs)


@when(
    "the function {func:w} of module {module:Module} is called writing the results to {result_vars:Tuple}"
)
def step_impl(context, func, module, result_vars):
    _run_func(context, func, module, result_vars)


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
