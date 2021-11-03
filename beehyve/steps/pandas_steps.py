"""Collection of step definitions for loading and comparing pandas DataFrames and Series."""

from typing import Any, Dict, Mapping

import pandas as pd
from behave import given, register_type, then
from behave.runner import Context
from behave_pandas import table_to_dataframe

from beehyve.steps import types
from beehyve.utils.pandas import compare_dataframes, compare_series
from beehyve.utils.variables import add_var, get_var

DEFAULT_COLUMN_LEVEL = 1

register_type(Dict=types.parse_dict)
register_type(CSVFile=types.parse_csv_file_path)

register_type(
    FrameEqualsKWArgs=types.create_limited_kwarg_parser(
        ["ignore_index", "common_columns_only", "ignore_dtypes", "atol", "rtol", "check_exact"]
    )
)

register_type(
    SeriesEqualsKWArgs=types.create_limited_kwarg_parser(
        ["ignore_index", "ignore_dtypes", "ignore_names", "atol", "rtol", "check_exact"]
    )
)


@given("the following table is loaded into dataframe {name:w}")
@given("dataframe {name:w} <-")
def step_load_table_into_df(context: Context, name: str):
    """Load and parse a behave table into a :class:`pandas.DataFrame`.

    Uses `behave_pandas <https://pypi.org/project/behave-pandas/>`_.

    :param context: the current context
    :param name: the name of the variable to which the dataframe should be assigned
    """
    add_var(context, name, table_to_dataframe(context.table, column_levels=DEFAULT_COLUMN_LEVEL))


@given("the following table is loaded into series {name:w}")
@given("series {name:w} <-")
def step_load_table_into_series(context: Context, name: str):
    """Load and parse a behave table into a :class:`pandas.Series`.

    Uses `behave_pandas <https://pypi.org/project/behave-pandas/>`_.

    :param context: the current context
    :param name: the name of the variable to which the series should be assigned
    """
    add_var(context, name, table_to_dataframe(context.table, column_levels=DEFAULT_COLUMN_LEVEL).squeeze())


@given("the CSV file {file_name:CSVFile} is loaded into dataframe {name:w} (read_csv kwargs: {kwargs:Dict})")
@given("dataframe {name:w} <- read({file_name:CSVFile}, kwargs={kwargs:Dict})")
def step_load_csv_into_df_with_kwargs(context: Context, file_name: str, name: str, kwargs: Dict[str, str]):
    """Load a CSV into a :class:`pandas.DataFrame` with additional kwargs.

    :param context: the current context
    :param file_name: the name of the CSV file to load
    :param name: the name of the variable to which the dataframe should be assigned
    :param kwargs: a dict containing kwargs to be passed to :func:`pandas.read_csv`
    """
    df = pd.read_csv(file_name, **kwargs)
    add_var(context, name, df)


@given("the CSV file {file_name:CSVFile} is loaded into dataframe {name:w}")
@given("dataframe {name:w} <- read({file_name:CSVFile})")
def step_load_csv_into_df(context: Context, file_name: str, name: str):
    """Load a CSV into a :class:`pandas.DataFrame`.

    :param context: the current context
    :param file_name: the name of the CSV file to load
    :param name: the name of the variable to which the dataframe should be assigned
    """
    df = pd.read_csv(file_name)
    add_var(context, name, df)


@then("dataframe {name:w} is equal to")
@then("dataframe {name:w} equals")
def step_df_equal_to_table(context: Context, name: str):
    """Check whether a dataframe is equal to the given table.

    Uses :py:func:`compare_dataframes`.

    :param context: the current context
    :param name: the name of the variable in which the dataframe is stored
    """
    df1 = get_var(context, name)
    df2 = table_to_dataframe(context.table, column_levels=DEFAULT_COLUMN_LEVEL)
    compare_dataframes(df1, df2)


@then("dataframe {name1:w} is equal to dataframe {name2:w}")
@then("dataframe {name1:w} equals {name2:w}")
def step_df_equal_to_df(context: Context, name1: str, name2: str):
    """Check whether two dataframes are equal.

    Uses :py:func:`compare_dataframes`.

    :param context: the current context
    :param name1: the name of the variable in which the first dataframe is stored
    :param name2: the name of the variable in which the second dataframe is stored
    """
    df1 = get_var(context, name1)
    df2 = get_var(context, name2)
    compare_dataframes(df1, df2)


@then("dataframe {name:w} is equal to (kwargs: {kwargs:FrameEqualsKWArgs})")
@then("dataframe {name:w} equals ({kwargs:FrameEqualsKWArgs})")
def step_df_equal_to_table_w_kwargs(context: Context, name: str, kwargs: Mapping[str, Any]):
    """Check whether a dataframe is equal to the given table.

    Uses :py:func:`compare_dataframes`.

    :param context: the current context
    :param name: the name of the variable in which the dataframe is stored
    :param kwargs: a mapping of keyword argments to be passed to :py:func:`compare_dataframes`
    """
    df1 = get_var(context, name)
    df2 = table_to_dataframe(context.table, column_levels=DEFAULT_COLUMN_LEVEL)
    compare_dataframes(df1, df2, **kwargs)


@then("dataframe {name1:w} is equal to dataframe {name2:w} (kwargs: {kwargs:FrameEqualsKWArgs})")
@then("dataframe {name1:w} equals {name2:w} ({kwargs:FrameEqualsKWArgs})")
def step_df_equal_to_df_w_kwargs(context: Context, name1: str, name2: str, kwargs: Mapping[str, Any]):
    """Check whether two dataframes are equal.

    Uses :py:func:`compare_dataframes`.

    :param context: the current context
    :param name1: the name of the variable in which the first dataframe is stored
    :param name2: the name of the variable in which the second dataframe is stored
    :param kwargs: a mapping of keyword argments to be passed to :py:func:`compare_dataframes`
    """
    df1 = get_var(context, name1)
    df2 = get_var(context, name2)
    compare_dataframes(df1, df2, **kwargs)


@then("series {name:w} is equal to")
@then("series {name:w} equals")
def step_series_equal_to_table(context: Context, name: str):
    """Check whether a series is equal to the given table.

    Uses :py:func:`compare_series`.

    :param context: the current context
    :param name: the name of the variable in which the series is stored
    """
    series1 = get_var(context, name)
    series2 = table_to_dataframe(context.table, column_levels=DEFAULT_COLUMN_LEVEL).squeeze()
    compare_series(series1, series2)


@then("series {name1:w} is equal to series {name2:w}")
@then("series {name1:w} equals {name2:w}")
def step_series_equal_to_series(context: Context, name1: str, name2: str):
    """Check whether two series are equal.

    Uses :py:func:`compare_series`.

    :param context: the current context
    :param name1: the name of the variable in which the first series is stored
    :param name2: the name of the variable in which the second series is stored
    """
    series1 = get_var(context, name1)
    series2 = get_var(context, name2)
    compare_series(series1, series2)


@then("series {name:w} is equal to (kwargs: {kwargs:SeriesEqualsKWArgs})")
@then("series {name:w} equals ({kwargs:SeriesEqualsKWArgs})")
def step_series_equal_to_table_w_kwargs(context: Context, name: str, kwargs: Mapping[str, Any]):
    """Check whether a series is equal to the given table.

    Uses :py:func:`compare_series`.

    :param context: the current context
    :param name: the name of the variable in which the series is stored
    :param kwargs: a mapping of keyword argments to be passed to :py:func:`compare_series`
    """
    series1 = get_var(context, name)
    series2 = table_to_dataframe(context.table, column_levels=DEFAULT_COLUMN_LEVEL).squeeze()
    compare_series(series1, series2, **kwargs)


@then("series {name1:w} is equal to series {name2:w} (kwargs: {kwargs:SeriesEqualsKWArgs})")
@then("series {name1:w} equals {name2:w} ({kwargs:SeriesEqualsKWArgs})")
def step_series_equal_to_series_w_kwargs(context: Context, name1: str, name2: str, kwargs: Mapping[str, Any]):
    """Check whether two series are equal.

    Uses :py:func:`compare_series`.

    :param context: the current context
    :param name1: the name of the variable in which the first series is stored
    :param name2: the name of the variable in which the second series is stored
    :param kwargs: a mapping of keyword argments to be passed to :py:func:`compare_series`
    """
    series1 = get_var(context, name1)
    series2 = get_var(context, name2)
    compare_series(series1, series2, **kwargs)
