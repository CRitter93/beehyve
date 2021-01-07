Feature: Call functions using BeeHyve

    Scenario: Call function without arguments
        When the function create_new_df of module beehyve.example_functions is called writing the results to (df,)
        Then dataframe df is equal to
            | int   | int    | int   |
            | col_a | col_b  | col_c |
            | 0     | 0      | 0     |
            | 0     | 0      | 0     |
            | 0     | 0      | 0     |

    Scenario: Call function with args
        Given the following table is loaded into dataframe df
            | int  | float | str  |
            | val1 | val2  | val3 |
            | 1    | 1.23  | text |
            | 5    | -4.5  | ABC  |
            | -3   | 6.78  | 123  |
        And the following variables are loaded
            | var | val    |
            | col | "val1" |
        When the function add_2_to_dataframe of module beehyve.example_functions is called writing the results to (df2,)
        Then dataframe df2 is equal to
            | int  | float | str  |
            | val1 | val2  | val3 |
            | 3    | 1.23  | text |
            | 7    | -4.5  | ABC  |
            | -1   | 6.78  | 123  |

    Scenario: Call function with varargs
        Given the following variables are loaded
            | var  | val             |
            | args | ["a", "b", "c"] |
        When the function join_args of module beehyve.example_functions is called writing the results to (joined_args,)
        Then the value of variable joined_args is "a.b.c"
        And the type of variable joined_args is str

    Scenario: Call function with kwargs
        Given the following variables are loaded
            | var      | val |
            | fill_val | 42  |
        When the function create_new_df of module beehyve.example_functions is called writing the results to (df,)
        Then dataframe df is equal to
            | int   | int    | int   |
            | col_a | col_b  | col_c |
            | 42    | 42     | 42    |
            | 42    | 42     | 42    |
            | 42    | 42     | 42    |

    Scenario: Call function with varkw
        Given the following variables are loaded
            | var    | val                      |
            | kwargs | {"a": 1, "b": 2, "c": 3} |
        When the function join_kwargs of module beehyve.example_functions is called writing the results to (joined_kwargs,)
        Then the value of variable joined_kwargs is "a:1-b:2-c:3"
        And the type of variable joined_kwargs is str

    Scenario: Call function with args, arg defaults, and kwargs
        Given the following table is loaded into dataframe df
            | str  | float | str  |
            | val1 | val2  | val3 |
            | 1    | 1.23  | text |
            | 5    | -4.5  | ABC  |
            | -3   | 6.78  | 123  |
        And the following variables are loaded
            | var      | val              |
            | cols     | ["val1", "val3"] |
        When the function concat_cols of module beehyve.example_functions is called writing the results to (df2,)
        Then dataframe df2 is equal to
            | str  | float | str  | str               |
            | val1 | val2  | val3 | concatenated_cols |
            | 1    | 1.23  | text | 1-text            |
            | 5    | -4.5  | ABC  | 5-ABC             |
            | -3   | 6.78  | 123  | -3-123            |

    Scenario: Call function with args and varargs
        Given the following variables are loaded
            | var    | val                      |
            | a      | "x"                      |
            | b      | "y"                      |
            | args   | ["a", "b", "c"]          |
            | kwargs | {"d": 1, "e": 2, "f": 3} |
        When the function join of module beehyve.example_functions is called writing the results to (joined_args,)
        Then the value of variable joined_args is "x*y*a.b.c*d:1-e:2-f:3"
        And the type of variable joined_args is str
