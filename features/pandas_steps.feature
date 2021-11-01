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
