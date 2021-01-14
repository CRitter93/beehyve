Feature: Testing exceptions

    Scenario: Exception on adding existing var
        Given the value 1 is loaded into variable a
        And an error is expected
        And the value 2 is loaded into variable a
        Then the exception ValueError was raised

    Scenario: context.vars is accessed without being set first
        Given an error is expected
        Then the value of variable a is None
        And the exception ValueError was raised

    Scenario: Function requirements for args and kwargs are not fulfilled
        Given an error is expected
        When the function concat_cols of module features.example_functions is called writing the results to df2
        Then the exception ValueError was raised

    Scenario: Function requirements for varargs and varkw are not fulfilled
        Given an error is expected
        When the function join_wo_defaults of module features.example_functions is called writing the results to joined_args
        Then the exception ValueError was raised

    Scenario: Function was called with malformed varkw (i.e., varkw is not a dict)
        Given the following variables are loaded
            | var    | val       |
            | kwargs | (1, 2, 3) |
        And an error is expected
        When the function join_kwargs of module features.example_functions is called writing the results to joined_kwargs
        Then the exception ValueError was raised

    Scenario: Function return does not match expected number of results
        Given an error is expected
        When the function do_nothing of module features.example_functions is called writing the results to (a, b)
        Then the exception ValueError was raised

    Scenario: Malformed variable table
        Given an error is expected
        And the following variables are loaded:
            | a   | b |
            | "a" | 1 |
            | "b" | 2 |
        Then the exception ValueError was raised

    Scenario: 'cols' missing in concat_cols
        Given the following table is loaded into dataframe df
            | str  | float | str  |
            | val1 | val2  | val3 |
            | 1    | 1.23  | text |
            | 5    | -4.5  | ABC  |
            | -3   | 6.78  | 123  |
        And an error is expected
        When the function concat_cols of module features.example_functions is called writing the results to df2
        Then the exception ValueError was raised