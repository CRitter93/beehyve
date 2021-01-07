import pandas as pd


def add_to_dataframe(df, col, val=1):
    df = df.copy()
    df[col] = df[col] + val
    return df


def create_new_df(fill_val=0):
    return pd.DataFrame(
        {col: [fill_val for _ in xrange(5)] for col in ("col_a", "col_b", "col_c")}
    )
