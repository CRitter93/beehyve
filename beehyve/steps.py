from ast import literal_eval
from typing import Any, Dict, Tuple

import pandas as pd
from behave import given, register_type, then, when
from behave.runner import Context
from behave_pandas import table_to_dataframe

from beehyve import types
from beehyve.functions import add_var, get_var, raises_error, run_func

DEFAULT_COLUMN_LEVEL = 1

register_type(Tuple=types.parse_tuple)
register_type(Dict=types.parse_dict)
register_type(Result=types.parse_func_result)
register_type(Module=types.parse_module)


@given("the following table is loaded into dataframe {name:w}")
@raises_error
def step_load_table_into_df(context: Context, name: str) -> None:
    """Loads and parses a behave table into a :class:`pandas.DataFrame`
    using `behave_pandas <https://pypi.org/project/behave-pandas/>`_.

    :param context: the current context
    :type context: :class:`behave.runner.Context`
    :param name: the name of the variable to which the dataframe should be assigned
    :type name: str
    """
    add_var(
        context,
        name,
        table_to_dataframe(context.table, column_levels=DEFAULT_COLUMN_LEVEL),
    )


@given(
    "the CSV file {file_name} is loaded into dataframe {name:w} (read_csv kwargs: {kwargs:Dict})"
)
@raises_error
def step_load_csv_into_df_with_kwargs(
    context: Context, file_name: str, name: str, kwargs: Dict[str, str]
) -> None:
    """Loads a CSV into a :class:`pandas.DataFrame` with additional kwargs.

    :param context: the current context
    :type context: :class:`behave.runner.Context`
    :param file_name: the name of the CSV file to load
    :type file_name: str
    :param name: the name of the variable to which the dataframe should be assigned
    :type name: str
    :param kwargs: a dict containing kwargs to be passed to :func:`pandas.read_csv`
    :type kwargs: Dict[str, str]
    """
    add_var(context, name, pd.read_csv(file_name, **kwargs))


@given("the CSV file {file_name} is loaded into dataframe {name:w}")
@raises_error
def step_load_csv_into_df(context: Context, file_name: str, name: str) -> None:
    """Loads a CSV into a :class:`pandas.DataFrame`.

    :param context: the current context
    :type context: :class:`behave.runner.Context`
    :param file_name: the name of the CSV file to load
    :type file_name: str
    :param name: the name of the variable to which the dataframe should be assigned
    :type name: str
    """
    add_var(context, name, pd.read_csv(file_name))


@given("the value {val} is loaded into variable {name:w}")
@raises_error
def step_load_value_into_variable(context: Context, val: Any, name: str) -> None:
    """Loads a value into a variable.

    :param context: the current context
    :type context: :class:`behave.runner.Context`
    :param val: a value to be loaded
    :type val: Any
    :param name: the name of the variable to which the value should be assigned
    :type name: str
    """
    add_var(context, name, literal_eval(val))


@given("the following variables are loaded")
@raises_error
def step_load_table_into_variables(context: Context) -> None:
    """Loads a table of values into variables.

    :param context: the current context
    :type context: :class:`behave.runner.Context`
    :raises ValueError: if the given table does not contain the necessary columns 'val' and 'var'
    """
    table = context.table

    if "var" not in table.headings and "val" not in table.headings:
        raise ValueError(
            "table has to contain a 'val' and 'var' column"
        )  # pragma: no cover

    for row in table:
        add_var(context, row["var"], literal_eval(row["val"]))


@when(
    "the function {func_name:w} of module {module:Module} is called writing the results to {result_vars:Result}"
)
@raises_error
def step_run_function(
    context: Context, func_name: str, module: str, result_vars: Tuple[str]
) -> None:
    """Executes an arbitrary python function using the variables in the context.
    For more details see :func:`run_func`.

    :param context: the current context
    :type context: :class:`behave.runner.Context`
    :param func_name: the name of the function to execute
    :type func_name: str
    :param module: the module where the function can be found,
        i.e., you should be able to import <func_name> from <module>
    :type module: str
    :param result_vars: a tuple of variable names
        to which the result(s) of the function should be assigned
    :type result_vars: Tuple[str]
    """
    run_func(context, func_name, module, result_vars)


@when("the function {func_name:w} of module {module:Module} is called")
@raises_error
def step_run_function_wo_return(context: Context, func_name: str, module: str) -> None:
    """Executes an arbitrary python function using the variables in the context.
    For more details see :func:`run_func`.

    :param context: the current context
    :type context: :class:`behave.runner.Context`
    :param func_name: the name of the function to execute
    :type func_name: str
    :param module: the module where the function can be found,
        i.e., you should be able to import <func_name> from <module>
    :type module: str
    """
    run_func(context, func_name, module, ())


@then("dataframe {name:w} is equal to")
def step_df_equal_to_table(context: Context, name: str) -> None:
    """Checks whether a dataframe is equal to the given table
    using :func:`pandas.testing.assert_frame_equal`.

    :param context: the current context
    :type context: :class:`behave.runner.Context`
    :param name: the name of the variable in which the dataframe is stored
    :type name: str
    """
    pd.testing.assert_frame_equal(
        get_var(context, name),
        table_to_dataframe(context.table, column_levels=DEFAULT_COLUMN_LEVEL),
    )


@then("dataframe {name1:w} is equal to dataframe {name2:w}")
def step_df_equal_to_df(context: Context, name1: str, name2: str) -> None:
    """Checks whether two dataframes are equal
    using :func:`pandas.testing.assert_frame_equal`.

    :param context: the current context
    :type context: :class:`behave.runner.Context`
    :param name1: the name of the variable in which the first dataframe is stored
    :type name1: str
    :param name2: the name of the variable in which the second dataframe is stored
    :type name2: str
    """
    pd.testing.assert_frame_equal(get_var(context, name1), get_var(context, name2))


@then("the value of variable {name:w} is {true_val}")
@raises_error
def step_variable_equal_to_value(context: Context, name: str, true_val: str) -> None:
    """Checks whether a variable is equal to a value.

    :param context: the current context
    :type context: :class:`behave.runner.Context`
    :param name: the name of the variable to check
    :type name: str
    :param true_val: the expected value
    :type true_val: str
    """
    actual_val = get_var(context, name)
    assert actual_val == literal_eval(true_val), f"actual value is {actual_val}"


@then("the type of variable {name:w} is {true_type:w}")
@raises_error
def step_variable_type_equal_to(context: Context, name: str, true_type: str) -> None:
    """Checks whether the type of a variable matches a given type.

    :param context: the current context
    :type context: :class:`behave.runner.Context`
    :param name: the name of the variable to check
    :type name: str
    :param true_type: the expected type
    :type true_type: str
    """
    actual_type = type(get_var(context, name)).__name__
    assert actual_type == true_type, f"actual type is {actual_type}"


@given("an error is expected")
def step_error_expected(context: Context):
    """Sets up expecting an error in following steps.
    Do not use without :func:`step_exception_raised`!

    :param context: the current context
    :type context: :class:`behave.runner.Context`
    """
    context.error_expected = True


@then("the exception {exception:w} was raised")
def step_exception_raised(context: Context, exception: str):
    """Checks whether a specific exception was raised in previous steps.
    Do not use without :func:`step_error_expected`!

    :param context: the current context
    :type context: :class:`behave.runner.Context`
    :param exception: the type of the expected exception
    :type exception: str
    :raises RuntimeError: if :func:`step_error_expected` was not executed as previous step
    """
    if not context.error_expected:
        raise RuntimeError(
            "this step should only be used when 'Given an error is expected' step is executed before"
        )  # pragma: no cover

    assert context.exception_type, "No exception has been thrown"
    assert (
        context.exception_type == exception
    ), f"Actual exception {context.exception_type} does not match expected exception {exception}"
