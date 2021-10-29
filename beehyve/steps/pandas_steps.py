from typing import Dict

import pandas as pd
from behave import given, register_type, then
from behave.runner import Context
from behave_pandas import table_to_dataframe

from beehyve.steps import types
from beehyve.utils.variables import add_var, get_var

DEFAULT_COLUMN_LEVEL = 1

register_type(Tuple=types.parse_tuple)
register_type(Dict=types.parse_dict)
register_type(Result=types.parse_func_result)
register_type(Module=types.parse_module)


@given("the following table is loaded into dataframe {name:w}")
def step_load_table_into_df(context: Context, name: str):
    """Loads and parses a behave table into a :class:`pandas.DataFrame`
    using `behave_pandas <https://pypi.org/project/behave-pandas/>`_.

    :param context: the current context
    :param name: the name of the variable to which the dataframe should be assigned
    """
    add_var(
        context,
        name,
        table_to_dataframe(context.table, column_levels=DEFAULT_COLUMN_LEVEL),
    )


@given(
    "the CSV file {file_name} is loaded into dataframe {name:w} (read_csv kwargs: {kwargs:Dict})"
)
def step_load_csv_into_df_with_kwargs(
    context: Context, file_name: str, name: str, kwargs: Dict[str, str]
):
    """Loads a CSV into a :class:`pandas.DataFrame` with additional kwargs.

    :param context: the current context
    :param file_name: the name of the CSV file to load
    :param name: the name of the variable to which the dataframe should be assigned
    :param kwargs: a dict containing kwargs to be passed to :func:`pandas.read_csv`
    """
    add_var(context, name, pd.read_csv(file_name, **kwargs))


@given("the CSV file {file_name} is loaded into dataframe {name:w}")
def step_load_csv_into_df(context: Context, file_name: str, name: str):
    """Loads a CSV into a :class:`pandas.DataFrame`.

    :param context: the current context
    :param file_name: the name of the CSV file to load
    :param name: the name of the variable to which the dataframe should be assigned
    """
    add_var(context, name, pd.read_csv(file_name))


@then("dataframe {name:w} is equal to")
def step_df_equal_to_table(context: Context, name: str):
    """Checks whether a dataframe is equal to the given table
    using :func:`pandas.testing.assert_frame_equal`.

    :param context: the current context
    :param name: the name of the variable in which the dataframe is stored
    """
    pd.testing.assert_frame_equal(
        get_var(context, name),
        table_to_dataframe(context.table, column_levels=DEFAULT_COLUMN_LEVEL),
    )


@then("dataframe {name1:w} is equal to dataframe {name2:w}")
def step_df_equal_to_df(context: Context, name1: str, name2: str):
    """Checks whether two dataframes are equal
    using :func:`pandas.testing.assert_frame_equal`.

    :param context: the current context
    :param name1: the name of the variable in which the first dataframe is stored
    :param name2: the name of the variable in which the second dataframe is stored
    """
    pd.testing.assert_frame_equal(get_var(context, name1), get_var(context, name2))
