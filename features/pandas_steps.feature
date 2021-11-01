Feature: Example Feature

    Scenario: Load table into pandas Dataframe
        Given the following table is loaded into dataframe df1
            | int64 | float64 | str  |
            | val1  | val2    | val3 |
            | 1     | 1.23    | text |
            | 5     | -4.5    | ABC  |
            | -3    | 6.78    | 123  |
        Then dataframe df1 is equal to
            | int64 | float64 | str  |
            | val1  | val2    | val3 |
            | 1     | 1.23    | text |
            | 5     | -4.5    | ABC  |
            | -3    | 6.78    | 123  |

    Scenario: Load table into pandas Dataframe (alternative step)
        Given dataframe df1 <-
            | int64 | float64 | str  |
            | val1  | val2    | val3 |
            | 1     | 1.23    | text |
            | 5     | -4.5    | ABC  |
            | -3    | 6.78    | 123  |
        Then dataframe df1 equals
            | int64 | float64 | str  |
            | val1  | val2    | val3 |
            | 1     | 1.23    | text |
            | 5     | -4.5    | ABC  |
            | -3    | 6.78    | 123  |

    Scenario: Load CSV into pandas Dataframe
        Given the CSV file features/example_table.csv is loaded into dataframe df1
        Then dataframe df1 is equal to
            | int64 | float64 | str  |
            | val1  | val2    | val3 |
            | 1     | 1.23    | text |
            | 5     | -4.5    | ABC  |
            | -3    | 6.78    | 123  |

    Scenario: Load CSV into pandas Dataframe (alternative step)
        Given dataframe df1 <- read(features/example_table.csv)
        Then dataframe df1 is equal to
            | int64 | float64 | str  |
            | val1  | val2    | val3 |
            | 1     | 1.23    | text |
            | 5     | -4.5    | ABC  |
            | -3    | 6.78    | 123  |

    Scenario: Load CSV into pandas Dataframe with kwargs
        Given the CSV file features/example_table_malformed.csv is loaded into dataframe df1 (read_csv kwargs: {"delimiter": ";", "skiprows": 1})
        Then dataframe df1 is equal to
            | int64 | float64 | str  |
            | val1  | val2    | val3 |
            | 1     | 1.23    | text |
            | 5     | -4.5    | ABC  |
            | -3    | 6.78    | 123  |

    Scenario: Load CSV into pandas Dataframe with kwargs (alternative step)
        Given dataframe df1 <- read(features/example_table_malformed.csv, kwargs={"delimiter": ";", "skiprows": 1})
        Then dataframe df1 is equal to
            | int64 | float64 | str  |
            | val1  | val2    | val3 |
            | 1     | 1.23    | text |
            | 5     | -4.5    | ABC  |
            | -3    | 6.78    | 123  |

    Scenario: Compare two dataframes
        Given the following table is loaded into dataframe df1
            | int  | float | str  |
            | val1 | val2  | val3 |
            | 1    | 1.23  | text |
            | 5    | -4.5  | ABC  |
            | -3   | 6.78  | 123  |
        And the following table is loaded into dataframe df2
            | int  | float | str  |
            | val1 | val2  | val3 |
            | 1    | 1.23  | text |
            | 5    | -4.5  | ABC  |
            | -3   | 6.78  | 123  |
        Then dataframe df1 is equal to dataframe df2

    Scenario: Compare two dataframes (alternative step)
        Given dataframe df1 <-
            | int  | float | str  |
            | val1 | val2  | val3 |
            | 1    | 1.23  | text |
            | 5    | -4.5  | ABC  |
            | -3   | 6.78  | 123  |
        And dataframe df2 <-
            | int  | float | str  |
            | val1 | val2  | val3 |
            | 1    | 1.23  | text |
            | 5    | -4.5  | ABC  |
            | -3   | 6.78  | 123  |
        Then dataframe df1 equals df2

    Scenario: Compare two dataframes with kwargs
        Given the following table is loaded into dataframe df1
            | int  | float | str  |
            | val1 | val2  | val3 |
            | 1    | 1.23  | text |
            | 5    | -4.5  | ABC  |
            | -3   | 6.78  | 123  |
        And the following table is loaded into dataframe df2
            | int  | float | str  |
            | val1 | val2  | val3 |
            | 1    | 1.23  | text |
            | 5    | -4.5  | ABC  |
            | -3   | 6.78  | 123  |
        Then dataframe df1 is equal to dataframe df2 (kwargs: ignore_index=True, common_columns_only=True, ignore_dtypes=True, atol=1e-8, rtol=1e-5, check_exact=True)

    Scenario: Compare two dataframes with kwargs (alternative step)
        Given dataframe df1 <-
            | int  | float | str  |
            | val1 | val2  | val3 |
            | 1    | 1.23  | text |
            | 5    | -4.5  | ABC  |
            | -3   | 6.78  | 123  |
        And dataframe df2 <-
            | int  | float | str  |
            | val1 | val2  | val3 |
            | 1    | 1.23  | text |
            | 5    | -4.5  | ABC  |
            | -3   | 6.78  | 123  |
        Then dataframe df1 equals df2 (ignore_index=True, common_columns_only=True, ignore_dtypes=True, atol=1e-8, rtol=1e-5, check_exact=True)

    Scenario: Compare pandas dataframe to table with kwargs
        Given the following table is loaded into dataframe df1
            | int64 | float64 | str  |
            | val1  | val2    | val3 |
            | 1     | 1.23    | text |
            | 5     | -4.5    | ABC  |
            | -3    | 6.78    | 123  |
        Then dataframe df1 is equal to (kwargs: ignore_index=True, common_columns_only=True, ignore_dtypes=True, atol=1e-8, rtol=1e-5, check_exact=True)
            | int64 | float64 | str  |
            | val1  | val2    | val3 |
            | 1     | 1.23    | text |
            | 5     | -4.5    | ABC  |
            | -3    | 6.78    | 123  |

    Scenario: Compare pandas dataframe to table with kwargs (alternative step)
        Given dataframe df1 <-
            | int64 | float64 | str  |
            | val1  | val2    | val3 |
            | 1     | 1.23    | text |
            | 5     | -4.5    | ABC  |
            | -3    | 6.78    | 123  |
        Then dataframe df1 equals (ignore_index=True, common_columns_only=True, ignore_dtypes=True, atol=1e-8, rtol=1e-5, check_exact=True)
            | int64 | float64 | str  |
            | val1  | val2    | val3 |
            | 1     | 1.23    | text |
            | 5     | -4.5    | ABC  |
            | -3    | 6.78    | 123  |

    Scenario: Compare series with table
        Given the following table is loaded into series series1
            | int  |
            | val1 |
            | 1    |
            | 5    |
            | -3   |
        Then series series1 is equal to
            | int  |
            | val1 |
            | 1    |
            | 5    |
            | -3   |

    Scenario: Compare series with table (alternative step)
        Given series series1 <-
            | int  |
            | val1 |
            | 1    |
            | 5    |
            | -3   |
        Then series series1 equals
            | int  |
            | val1 |
            | 1    |
            | 5    |
            | -3   |

    Scenario: Compare two series
        Given the following table is loaded into series series1
            | int  |
            | val1 |
            | 1    |
            | 5    |
            | -3   |
        And the following table is loaded into series series2
            | int  |
            | val1 |
            | 1    |
            | 5    |
            | -3   |
        Then series series1 is equal to series series2

    Scenario: Compare two series (alternative step)
        Given series series1 <-
            | int  |
            | val1 |
            | 1    |
            | 5    |
            | -3   |
        And series series2 <-
            | int  |
            | val1 |
            | 1    |
            | 5    |
            | -3   |
        Then series series1 equals series2

    Scenario: Compare two series with kwargs
        Given the following table is loaded into series series1
            | int  |
            | val1 |
            | 1    |
            | 5    |
            | -3   |
        And the following table is loaded into series series2
            | int  |
            | val1 |
            | 1    |
            | 5    |
            | -3   |
        Then series series1 is equal to series series2 (kwargs: ignore_index=True, ignore_dtypes=True, ignore_names=True, atol=1e-8, rtol=1e-5, check_exact=True)

    Scenario: Compare two series with kwargs (alternative step)
        Given series series1 <-
            | int  |
            | val1 |
            | 1    |
            | 5    |
            | -3   |
        And series series2 <-
            | int  |
            | val1 |
            | 1    |
            | 5    |
            | -3   |
        Then series series1 equals series2 (ignore_index=True, ignore_dtypes=True, ignore_names=True, atol=1e-8, rtol=1e-5, check_exact=True)

    Scenario: Compare pandas series to table with kwargs
        Given the following table is loaded into series series1
            | int  |
            | val1 |
            | 1    |
            | 5    |
            | -3   |
        Then series series1 is equal to (kwargs: ignore_index=True, ignore_dtypes=True, ignore_names=True, atol=1e-8, rtol=1e-5, check_exact=True)
            | int  |
            | val1 |
            | 1    |
            | 5    |
            | -3   |

    Scenario: Compare pandas series to table with kwargs (alternative step)
        Given series series1 <-
            | int  |
            | val1 |
            | 1    |
            | 5    |
            | -3   |
        Then series series1 equals (ignore_index=True, ignore_dtypes=True, ignore_names=True, atol=1e-8, rtol=1e-5, check_exact=True)
            | int  |
            | val1 |
            | 1    |
            | 5    |
            | -3   |