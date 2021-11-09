Feature: Call functions using BeeHyve

    Scenario: Call function without arguments
        When the function create_new_df of module features.example_functions is called writing the results to df
        Then dataframe df is equal to
            | int64 | int64 | int64 |
            | col_a | col_b | col_c |
            | 0     | 0     | 0     |
            | 0     | 0     | 0     |
            | 0     | 0     | 0     |

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
        When the function add_2_to_dataframe of module features.example_functions is called writing the results to df2
        Then dataframe df2 is equal to
            | int  | float | str  |
            | val1 | val2  | val3 |
            | 3    | 1.23  | text |
            | 7    | -4.5  | ABC  |
            | -1   | 6.78  | 123  |

    Scenario: Call function with args (alternative step)
        Given the following table is loaded into dataframe df
            | int  | float | str  |
            | val1 | val2  | val3 |
            | 1    | 1.23  | text |
            | 5    | -4.5  | ABC  |
            | -3   | 6.78  | 123  |
        And the following variables are loaded
            | var | val    |
            | col | "val1" |
        When df2 <- features.example_functions.add_2_to_dataframe()
        Then dataframe df2 is equal to
            | int  | float | str  |
            | val1 | val2  | val3 |
            | 3    | 1.23  | text |
            | 7    | -4.5  | ABC  |
            | -1   | 6.78  | 123  |

    Scenario: Call function with varargs
        Given the following variables are loaded
            | var  | val             |
            | args | ("a", "b", "c") |
        When the function join_args of module features.example_functions is called writing the results to joined_args
        Then the value of variable joined_args is "a.b.c"
        And the type of variable joined_args is str

    Scenario: Call function with varargs of type list
        Given the following variables are loaded
            | var  | val             |
            | args | ["a", "b", "c"] |
        When the function join_args of module features.example_functions is called writing the results to joined_args
        Then the value of variable joined_args is "a.b.c"
        And the type of variable joined_args is str

    Scenario: Call function with varargs being a single value
        Given the following variables are loaded
            | var  | val |
            | args | "a" |
        When the function join_args of module features.example_functions is called writing the results to joined_args
        Then the value of variable joined_args is "a"
        And the type of variable joined_args is str

    Scenario: Call function with kwargs
        Given the following variables are loaded
            | var      | val |
            | fill_val | 42  |
        When the function create_new_df of module features.example_functions is called writing the results to df
        Then dataframe df is equal to
            | int64 | int64 | int64 |
            | col_a | col_b | col_c |
            | 42    | 42    | 42    |
            | 42    | 42    | 42    |
            | 42    | 42    | 42    |

    Scenario: Call function with varkw
        Given the following variables are loaded
            | var    | val                      |
            | kwargs | {"a": 1, "b": 2, "c": 3} |
        When the function join_kwargs of module features.example_functions is called writing the results to joined_kwargs
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
            | var  | val              |
            | cols | ["val1", "val3"] |
        When the function concat_cols of module features.example_functions is called writing the results to df2
        Then dataframe df2 is equal to
            | str  | float | str  | str               |
            | val1 | val2  | val3 | concatenated_cols |
            | 1    | 1.23  | text | 1-text            |
            | 5    | -4.5  | ABC  | 5-ABC             |
            | -3   | 6.78  | 123  | -3-123            |

    Scenario: Call function with args, varargs, and varkw
        Given the following variables are loaded
            | var    | val                      |
            | a      | "x"                      |
            | b      | "y"                      |
            | args   | ["a", "b", "c"]          |
            | kwargs | {"d": 1, "e": 2, "f": 3} |
        When the function join of module features.example_functions is called writing the results to joined_args
        Then the value of variable joined_args is "x*y*a.b.c*d:1-e:2-f:3"
        And the type of variable joined_args is str

    Scenario: Call function with tuple output
        Given the following variables are loaded
            | var  | val             |
            | a    | "x"             |
            | b    | "y"             |
            | args | ["a", "b", "c"] |
            | d    | 1               |
            | e    | 2               |
            | f    | 3               |
        When the function join_multi of module features.example_functions is called writing the results to result_tuple
        Then the value of variable result_tuple is ("x*y", "a.b.c", "d:1-e:2-f:3")
        And the type of variable result_tuple is tuple

    Scenario: Call function with multiple outputs
        Given the following variables are loaded
            | var  | val             |
            | a    | "x"             |
            | b    | "y"             |
            | args | ["a", "b", "c"] |
            | d    | 1               |
            | e    | 2               |
            | f    | 3               |
        When the function join_multi of module features.example_functions is called writing the results to (args_out, varargs_out, kwargs_out)
        Then the value of variable args_out is "x*y"
        And the type of variable args_out is str
        And the value of variable varargs_out is "a.b.c"
        And the type of variable varargs_out is str
        And the value of variable kwargs_out is "d:1-e:2-f:3"
        And the type of variable kwargs_out is str

    Scenario: Call function without output
        When the function do_nothing of module features.example_functions is called

    Scenario: Call function without output (alternative step)
        When features.example_functions.do_nothing() is called

    Scenario: Call function with manual args and kwargs
        Given the following variables are loaded
            | var   | val |
            | not_a | "x" |
            | not_b | "y" |
            | a     | "a" |
            | b     | "b" |
            | c     | "c" |
            | g     | 1   |
            | h     | 2   |
            | i     | 3   |
        When the function join of module features.example_functions is called using arguments not_a,not_b, a, b, c and keyword arguments d=g,e= h, f = i writing the results to joined_args
        Then the value of variable joined_args is "x*y*a.b.c*d:1-e:2-f:3"
        And the type of variable joined_args is str

    Scenario: Call function with manual args and kwargs
        Given the following variables are loaded
            | var   | val |
            | not_a | "x" |
            | not_b | "y" |
            | a     | "a" |
            | b     | "b" |
            | c     | "c" |
            | g     | 1   |
            | h     | 2   |
            | i     | 3   |
        When the function join of module features.example_functions is called using arguments not_a,not_b, a, b, c and keyword arguments d=g,e= h, f = i writing the results to joined_args
        Then the value of variable joined_args is "x*y*a.b.c*d:1-e:2-f:3"
        And the type of variable joined_args is str

    Scenario: Call function with manual args and kwargs (alternative step)
        Given the following variables are loaded
            | var   | val |
            | not_a | "x" |
            | not_b | "y" |
            | a     | "a" |
            | b     | "b" |
            | c     | "c" |
            | g     | 1   |
            | h     | 2   |
            | i     | 3   |
        When joined_args <- features.example_functions.join(not_a, not_b, a, b, c, d=g, e=h, f=i)
        Then the value of variable joined_args is "x*y*a.b.c*d:1-e:2-f:3"
        And the type of variable joined_args is str

    Scenario: Call function with manual args and kwargs without output assignment
        Given the following variables are loaded
            | var   | val |
            | not_a | "x" |
            | not_b | "y" |
            | a     | "a" |
            | b     | "b" |
            | c     | "c" |
            | g     | 1   |
            | h     | 2   |
            | i     | 3   |
        When the function do_nothing_w_input of module features.example_functions is called using arguments not_a,not_b, a, b, c and keyword arguments d=g,e= h, f = i

    Scenario: Call function with manual args and kwargs without output assignment (alternative step)
        Given the following variables are loaded
            | var   | val |
            | not_a | "x" |
            | not_b | "y" |
            | a     | "a" |
            | b     | "b" |
            | c     | "c" |
            | g     | 1   |
            | h     | 2   |
            | i     | 3   |
        When features.example_functions.do_nothing_w_input(not_a, not_b, a, b, c, d=g, e=h, f=i) is called