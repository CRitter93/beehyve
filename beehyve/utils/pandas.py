"""Collection of functions for pandas dataframes."""

from typing import Sequence

import pandas as pd

IGNORE_DF_DTYPE_KWARGS = {
    "check_dtype": False,
    "check_column_type": False,
    "check_index_type": False,
    "check_categorical": False,
    "check_freq": False,
}

IGNORE_SERIES_DTYPE_KWARGS = {
    "check_dtype": False,
    "check_series_type": False,
    "check_index_type": False,
    "check_categorical": False,
    "check_freq": False,
}


def compare_dataframes(
    df1: pd.DataFrame,
    df2: pd.DataFrame,
    *,
    common_columns_only: bool = False,
    ignore_index: bool = False,
    ignore_dtypes: bool = False,
    atol: float = 1e-8,
    rtol: float = 1e-5,
    check_exact: bool = False,
):
    """Compare two given dataframes.

    Uses :py:func:`pd.testing.assert_frame_equal` to determine whether two dataframes are equal.

    Ignores the order of columns in the dataframe.

    :param df1: a dataframe
    :param df2: another dataframe
    :param common_columns_only: whether or not to only compare columns present in both dataframes.
        If False, the assertion will fail if the dataframes have different columns.
        Defaults to False
    :param ignore_index: whether or not to ignore the index of the dataframes
        (using :py:meth:`pd.DataFrame.reset_index`), defaults to False
    :param ignore_dtypes: whether or not to ignore the dtypes when checking the dataframes, defaults to False
    :param atol: absolute tolerance when comparing numerical values, defaults to 1e-8
    :param rtol: relative tolerance when comparing numerical values, defaults to 1e-5
    :param check_exact: whether or not to check for exact values, defaults to False
    """
    assert_kwargs = {}

    if ignore_index:
        df1 = df1.reset_index(drop=True)
        df2 = df2.reset_index(drop=True)

    columns_to_compare = _get_common_columns(df1.columns, df2.columns)

    if not common_columns_only:
        if len(columns_to_compare) != len(df1.columns) or len(columns_to_compare) != len(df2.columns):
            raise AssertionError(f"Columns of dataframes do not match. Got {df1.columns} and {df2.columns}")

    df1 = df1[columns_to_compare]
    df2 = df2[columns_to_compare]

    if ignore_dtypes:
        assert_kwargs.update(IGNORE_DF_DTYPE_KWARGS)

    pd.testing.assert_frame_equal(df1, df2, atol=atol, rtol=rtol, check_exact=check_exact, **assert_kwargs)


def _get_common_columns(columns1: Sequence[str], columns2: Sequence[str]) -> Sequence[str]:
    return [col for col in columns1 if col in columns2]


def compare_series(
    series1: pd.Series,
    series2: pd.Series,
    *,
    ignore_index: bool = False,
    ignore_dtypes: bool = False,
    ignore_names: bool = False,
    atol: float = 1e-8,
    rtol: float = 1e-5,
    check_exact: bool = False,
):
    """Compare two given series.

    Uses :py:func:`pd.testing.assert_series_equal` to determine whether two series are equal.

    :param df1: a series
    :param df2: another series
    :param ignore_index: whether or not to ignore the index of the series
        (using :py:meth:`pd.Series.reset_index`), defaults to False
    :param ignore_dtypes: whether or not to ignore the dtypes when checking the series, defaults to False
    :param ignore_names: whether to ignore the Series and Index names attribute, defaults to False
    :param atol: absolute tolerance when comparing numerical values, defaults to 1e-8
    :param rtol: relative tolerance when comparing numerical values, defaults to 1e-5
    :param check_exact: whether or not to check for exact values, defaults to False
    """
    assert_kwargs = {}

    if ignore_index:
        series1 = series1.reset_index(drop=True)
        series2 = series2.reset_index(drop=True)

    if ignore_dtypes:
        assert_kwargs.update(IGNORE_SERIES_DTYPE_KWARGS)

    if ignore_names:
        assert_kwargs["check_names"] = False

    pd.testing.assert_series_equal(series1, series2, atol=atol, rtol=rtol, check_exact=check_exact, **assert_kwargs)
