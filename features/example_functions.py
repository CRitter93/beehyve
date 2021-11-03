# noqa

import pandas as pd

SOME_CONSTANT = "abcdef"

ANOTHER_CONSTANT = "tuvxyz"


class SomeObject:
    @property
    def some_property(self):
        return 123456


class AnotherObject:
    @property
    def some_property(self):
        return 987654


def add_2_to_dataframe(df, col):
    df = df.copy()
    df[col] = df[col] + 2
    return df


def create_new_df(fill_val=0):
    return pd.DataFrame({col: [fill_val for _ in range(3)] for col in ("col_a", "col_b", "col_c")})


def join_args(*args):
    return ".".join(args)


def join_kwargs(**kwargs):
    return "-".join([f"{k}:{v}" for k, v in kwargs.items()])


def concat_cols(df, sep="-", *, cols=None, new_col_name="concatenated_cols"):
    if cols == None or not isinstance(cols, list):
        raise ValueError

    df = df.copy()

    df[new_col_name] = df[cols[0]]

    for col in cols[1:]:
        df[new_col_name] = df[new_col_name] + sep + df[col]

    return df


def join(a, b, *args, **kwargs):
    return "*".join([a, b, join_args(*args), join_kwargs(**kwargs)])


def join_multi(a, b, *args, d=None, e=None, f=None):
    return "*".join([a, b]), join_args(*args), join_kwargs(d=d, e=e, f=f)


def do_nothing():
    return


def join_wo_defaults(*args, d, e, **kwargs):
    return join(*args, d=d, e=e, **kwargs)


def do_nothing_w_input(*args, **kwargs):
    return


def get_some_constant():
    return SOME_CONSTANT


def return_abc():
    return "abc"


def get_some_property_from_some_object():
    return SomeObject().some_property
