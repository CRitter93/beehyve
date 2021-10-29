from ast import literal_eval
from typing import Any, Tuple

from behave import given, register_type, step, then
from behave.runner import Context

from beehyve.steps import types
from beehyve.utils.variables import add_var, get_var

register_type(Result=types.parse_func_result)


@given("the value {val} is loaded into variable {name:w}")
@given("{name:w} <- {val}")
def step_load_value_into_variable(context: Context, val: Any, name: str):
    """Loads a value into a variable.

    :param context: the current context
    :param val: a value to be loaded
    :param name: the name of the variable to which the value should be assigned
    """
    add_var(context, name, literal_eval(val))


@given("the following variables are loaded")
def step_load_table_into_variables(context: Context):
    """Loads a table of values into variables.

    :param context: the current context
    :raises ValueError: if the given table does not contain the necessary columns 'val' and 'var'
    """
    table = context.table

    if "var" not in table.headings and "val" not in table.headings:
        raise ValueError("table has to contain a 'val' and 'var' column")

    for row in table:
        add_var(context, row["var"], literal_eval(row["val"]))


@then("the value of variable {name:w} is {true_val}")
@then("{name:w} equals {true_val}")
def step_variable_equal_to_value(context: Context, name: str, true_val: str):
    """Checks whether a variable is equal to a value.

    :param context: the current context
    :param name: the name of the variable to check
    :param true_val: the expected value
    """
    actual_val = get_var(context, name)
    assert actual_val == literal_eval(true_val), f"actual value is {actual_val}"


@then("the type of variable {name:w} is {true_type:w}")
@then("type({name:w}) equals {true_type:w}")
def step_variable_type_equal_to(context: Context, name: str, true_type: str):
    """Checks whether the type of a variable matches a given type.

    :param context: the current context
    :param name: the name of the variable to check
    :param true_type: the expected type
    """
    actual_type = type(get_var(context, name)).__name__
    assert actual_type == true_type, f"actual type is {actual_type}"


@step("the variable {name:w} is unpacked into {new_names:Result}")
@step("{new_names:Result} <- {name:w}")
def step_variable_repacking(context: Context, name: str, new_names: Tuple[str]):
    """Unpacks a single iterable variable into new variable names, e.g., :code:`(a, b, c) = [1, 2, 3]`.

    :param context: the current context
    :param name: the name of the variable to unpack
    :param new_names: the new names to assign
    """
    val = get_var(context, name)
    if len(new_names) == 1:
        add_var(context, new_names[0], val)
    else:
        assert len(val) == len(
            new_names
        ), f"length mismatch {len(val)} != {len(new_names)}"

        for new_name, partial_val in zip(new_names, val):
            add_var(context, new_name, partial_val)


@step("the element {key} of variable {name:w} is stored in new variable {new_name:w}")
@step("{new_name:w} <- {name:w}[{key}]")
def step_get_element(context: Context, name: str, key: Any, new_name: str):
    """Assigns a single element from a variable to a new variable.

    :param context: the current context
    :param name: the variable containing the element
    :param key: the key of the element to access
    :param new_name: the new variable to store the element in
    """
    container_var = get_var(context, name)
    key = literal_eval(key)
    element = container_var[key]
    add_var(context, new_name, element)
