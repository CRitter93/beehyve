from ast import literal_eval

import pandas as pd
from behave import given, register_type, then, when
from behave_pandas import dataframe_to_table, table_to_dataframe

from beehyve import types
from beehyve.functions import add_var, get_var, run_func

DEFAULT_COLUMN_LEVEL = 1

register_type(Tuple=types.parse_tuple)
register_type(Dict=types.parse_dict)
register_type(Result=types.parse_func_result)
register_type(Module=types.parse_module)


@given("the following table is loaded into dataframe {name:w}")
def step_impl(context, name):
    add_var(
        context,
        name,
        table_to_dataframe(context.table, column_levels=DEFAULT_COLUMN_LEVEL),
    )


@given(
    "the CSV file {file_name} is loaded into dataframe {name:w} (read_csv kwargs: {kwargs:Dict})"
)
def step_impl(context, file_name, name, kwargs):
    add_var(context, name, pd.read_csv(file_name, **kwargs))


@given("the CSV file {file_name} is loaded into dataframe {name:w}")
def step_impl(context, file_name, name):
    add_var(context, name, pd.read_csv(file_name))


@given("the value {val} is loaded into variable {name:w}")
def step_impl(context, val, name):
    add_var(context, name, literal_eval(val))


@given("the following variables are loaded")
def step_impl(context):
    table = context.table

    if "var" not in table.headings and "val" not in table.headings:
        raise ValueError("table has to contain a 'val' and 'var' column")

    for row in table:
        add_var(context, row["var"], literal_eval(row["val"]))


@when(
    "the function {func_name:w} of module {module:Module} is called writing the results to {result_vars:Result}"
)
def step_impl(context, func_name, module, result_vars):
    run_func(context, func_name, module, result_vars)


@then("dataframe {name:w} is equal to")
def step_impl(context, name):
    pd.testing.assert_frame_equal(
        get_var(context, name),
        table_to_dataframe(context.table, column_levels=DEFAULT_COLUMN_LEVEL),
    )


@then("the string representation of dataframe {name:w} is equal to")
def step_impl(context, name):
    table_representation = dataframe_to_table(get_var(context, name))
    assert (
        table_representation == context.text
    ), f"dataframe {name} does not match the expected text\nactual:\n{table_representation}"


@then("dataframe {name1:w} is equal to dataframe {name2:w}")
def step_impl(context, name1, name2):
    pd.testing.assert_frame_equal(get_var(context, name1), get_var(context, name2))


@then("the value of variable {name:w} is {true_val}")
def step_impl(context, name, true_val):
    actual_val = get_var(context, name)
    assert actual_val == literal_eval(true_val), f"actual value is {actual_val}"


@then("the type of variable {name:w} is {true_type:w}")
def step_impl(context, name, true_type):
    actual_type = type(get_var(context, name)).__name__
    assert actual_type == true_type, f"actual type is {actual_type}"
