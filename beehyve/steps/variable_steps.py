"""Collection of step definitions for loading and checking variables."""

from ast import literal_eval
from typing import Any, Tuple

from behave import given, register_type, step, then
from behave.runner import Context

from beehyve.steps import types
from beehyve.utils.variables import add_var, get_env, get_var, set_env

register_type(Result=types.parse_func_result)


@given("the value {value} is loaded into variable {name:w}")
@given("{name:w} <- {value}")
def step_load_value_into_variable(context: Context, value: Any, name: str) -> None:
    """Load a value into a variable.

    :param context: the current context
    :param val: a value to be loaded
    :param name: the name of the variable to which the value should be assigned
    """
    add_var(context, name, literal_eval(value))


@given("the following variables are loaded")
def step_load_table_into_variables(context: Context) -> None:
    """Load a table of values into variables.

    :param context: the current context
    :raises ValueError: if the given table does not contain the necessary columns 'val' and 'var'
    """
    table = context.table

    if "var" not in table.headings and "val" not in table.headings:
        raise ValueError("table has to contain a 'val' and 'var' column")

    for row in table:
        add_var(context, row["var"], literal_eval(row["val"]))


@then("the value of variable {name:w} is {expected_value}")
@then("{name:w} equals {expected_value}")
def step_variable_equal_to_value(context: Context, name: str, expected_value: str) -> None:
    """Check whether a variable is equal to a value.

    :param context: the current context
    :param name: the name of the variable to check
    :param expected_value: the expected value, interpreted using :py:func:`ast.literal_eval`
    """
    actual_val = get_var(context, name)
    assert actual_val == literal_eval(expected_value), f"actual value is {actual_val}"


@then("the type of variable {name:w} is {expected_type:w}")
@then("type({name:w}) equals {expected_type:w}")
def step_variable_type_equal_to(context: Context, name: str, expected_type: str) -> None:
    """Check whether the type of a variable matches a given type.

    :param context: the current context
    :param name: the name of the variable to check
    :param expected_type: the expected type
    """
    actual_type = type(get_var(context, name)).__name__
    assert actual_type == expected_type, f"actual type is {actual_type}, not {expected_type}"


@step("the variable {name:w} is unpacked into {new_names:Result}")
@step("{new_names:Result} <- {name:w}")
def step_variable_repacking(context: Context, name: str, new_names: Tuple[str]) -> None:
    """Unpack a single iterable variable into new variable names, e.g., :code:`(a, b, c) = [1, 2, 3]`.

    :param context: the current context
    :param name: the name of the variable to unpack
    :param new_names: the new names to assign
    """
    val = get_var(context, name)
    if len(new_names) == 1:
        add_var(context, new_names[0], val)
    else:
        assert len(val) == len(new_names), f"length mismatch {len(val)} != {len(new_names)}"

        for new_name, partial_val in zip(new_names, val):
            add_var(context, new_name, partial_val)


@step("the element {key} of variable {name:w} is stored in new variable {new_name:w}")
@step("{new_name:w} <- {name:w}[{key}]")
def step_get_element(context: Context, name: str, key: str, new_name: str) -> None:
    """Assign a single element from a variable to a new variable.

    :param context: the current context
    :param name: the variable containing the element
    :param key: the key of the element to access, will be interpreted using :py:func:`ast.literal_eval`
    :param new_name: the new variable to store the element in
    """
    container_var = get_var(context, name)
    key = literal_eval(key)
    element = container_var[key]
    add_var(context, new_name, element)


@given("the value of environment variable {name:w} is set to {value}")
@given("env({name:w}) <- {value}")
def step_set_env(_context: Context, name: str, value: str) -> None:
    """Set the given environment variable to the given value.

    See :py:func:`set_env` for more detail.

    :param _context: the current context
    :param name: the name of the environment variable to set
    :param value: the value to assign to the environment variable
    """
    set_env(name, value)


@then("the value of environment variable {name:w} is {expected_value}")
@then("env({name:w}) equals {expected_value}")
def step_get_env(_context: Context, name: str, expected_value: str) -> None:
    """Check whether the given environment variable has the expected value.

    :param _context: the current context
    :param name: the name of the environment variable to check
    :param expected_value: the expected value of the environment variable
    """
    actual_value = get_env(name)
    assert (
        actual_value == expected_value
    ), f"Value of environment variable does not match expected value, {actual_value} != {expected_value}"
