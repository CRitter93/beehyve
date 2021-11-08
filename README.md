# beehyve

[![Test Status](https://github.com/CRitter93/beehyve/workflows/Tests/badge.svg)](https://github.com/CRitter93/beehyve/actions?query=workflow%3ATests)
[![Lint Status](https://github.com/CRitter93/beehyve/workflows/Lint/badge.svg)](https://github.com/CRitter93/beehyve/actions?query=workflow%3ALint)
[![isort Status](https://github.com/CRitter93/beehyve/workflows/isort/badge.svg)](https://github.com/CRitter93/beehyve/actions?query=workflow%3Aisort)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![codecov](https://codecov.io/gh/CRitter93/beehyve/branch/main/graph/badge.svg?token=5QBV9RI4J6)](https://codecov.io/gh/CRitter93/beehyve)

---

Hijacking [behave](https://behave.readthedocs.io/en/stable/) to test data pipelines.

---

# Documentation

See documentation at [readthedocs](https://beehyve.readthedocs.io/en/latest/).

# Installation

## Install using PyPI
TBD

## Install from sources
To install the latest version from sources use:
```bash
git clone https://github.com/CRitter93/beehyve.git
cd beehyve
python setup.py install
```

## Install using pip
To install beehyve using pip run the following code:
```bash
python -m pip install git+https://github.com/CRitter93/beehyve.git#egg=beehyve
```

# Usage
To use the steps defined by beehyve add an import script into your features/steps folder:

*features/steps/import_behyve.py:*
```python
from beehyve.steps.all_steps import *  # noqa: F401,F403
```

The steps can than be used alongside others in the feature files.

To use the monkeypatch fixture, add the `before_tag` function to your environment in the features folder.


*features/environment.py*:
```python
# you don't have your own before_tag
from beehyve.utils.monkeypatch import before_tag

# you do have your own before_tag
from beehyve.utils import monkeypatch

def before_tag(context: Context, tag: str):
    
    # here goes your implementation
    
    else:
        monkeypatch.before_tag(context, tag)
```

# Examples
The most common usage of beehyve should be testing data transformations.
Testing these usually follows the same steps:
setup &rarr; execute transformation &rarr; compare with desired output.


This can be done easily with the *Given* &rarr; *When* &rarr; *Then* structure of behave.
So when running a test you should
1. Load all dataframes and variables in the *Given* step.
2. Execute the data transformation function in *When* (ideally there is only one function executed in each scenario).
3. Compare to a desired result in *Then*.

*Example:*
```gherkin
Scenario: Example
    # 1: load dataframe and variables
    Given the following table is loaded into dataframe df
        | int  | float | str  |
        | val1 | val2  | val3 |
        | 1    | 1.23  | text |
        | 5    | -4.5  | ABC  |
        | -3   | 6.78  | 123  |
    And the following variables are loaded
        | var | val    |
        | col | "val1" |

    # 2: execute function and store results in new variables
    When the function add_2_to_dataframe of module features.example_functions is called writing the results to df2

    # 3: compare function output to desired result
    Then dataframe df2 is equal to
        | int  | float | str  |
        | val1 | val2  | val3 |
        | 3    | 1.23  | text |
        | 7    | -4.5  | ABC  |
        | -1   | 6.78  | 123  |
```

More example uses of the beehyve steps can be found in the `.feature` files in [features](https://github.com/CRitter93/beehyve/tree/main/features).

# Step Documentation

## Variable Steps
The steps in [`beehyve/steps/variable_steps.py`](https://github.com/CRitter93/beehyve/tree/main/beehyve/steps/variable_steps.py) are used to add variables to a test context and test variables.

---

**Given**
```
the value {value} is loaded into variable {name:w}

- or -

{name:w} <- {value}
```

Load a value into a variable of the context.
Uses [`ast.literal_eval`](https://docs.python.org/3/library/ast.html#ast.literal_eval) to interpret the value.

Arguments:
* `name`: the name of the new variable, only characters, digits, and underscores are allowed (corresponds to python's regex `\w`)
* `value`: the value to assign to the variable

---

**Given**
```
the following variables are loaded
```

Load a table of variable names and values into the context all at once.

Arguments:
* *table*: the table needs to have two columns: `var` - the name of the new variable(s) and `val`: the value(s) to assign to the variable(s)

---

**Then**
```
the value of variable {name:w} is {expected_value}

- or -

{name:w} equals {expected_value}
```

Checks whether the value assigned to a variable equals a given expected value.
Uses [`ast.literal_eval`](https://docs.python.org/3/library/ast.html#ast.literal_eval) to interpret the expected value.

Arguments:
* `name`: the name of the variable to check, only characters, digits, and underscores are allowed (corresponds to python's regex `\w`)
* `expected_value`: the expected value

---

**Then**
```
the type of variable {name:w} is {expected_type:w}

- or -

type({name:w}) equals {expected_type:w}
```

Checks whether the type of the value assigned to a variable equals a given expected type.
Type is checked by it's name (i.e., `type(val).__name__`).

Arguments:
* `name`: the name of the variable to check, only characters, digits, and underscores are allowed (corresponds to python's regex `\w`)
* `expected_type`: the expected type

---

**Given/When/Then**
```
the variable {name:w} is unpacked into {new_names:Result}

- or -

{new_names:Result} <- {name:w}
```

Unpacks a collection of values from one variable into multiple new variables.
Example: if `list = [1, 2, 3]`, `a, b, c <- list` would result in `a = 1`, `b = 2`, and `c = 3`.

Arguments:
* `name`: the name of the variable to unpack, only characters, digits, and underscores are allowed (corresponds to python's regex `\w`)
* `new_names`: the new names to assign, a comma-separated list of names or a single name (s.a., `\w`)

---

**Given/When/Then**
```
the element {key} of variable {name:w} is stored in new variable {new_name:w}

- or -

{new_name:w} <- {name:w}[{key}]
```

Assign a single element of a collection to a new variable using a key / index.
The key is interpreted using [`ast.literal_eval`](https://docs.python.org/3/library/ast.html#ast.literal_eval).

Arguments:
* `name`: the name of the variable containing the element, only characters, digits, and underscores are allowed (corresponds to python's regex `\w`)
* `new_name`: the new name to assign the element to, only characters, digits, and underscores are allowed (corresponds to python's regex `\w`)
* `key`: the key / index of the element in the collection

---

**Given**
```
the value of environment variable {name:w} is set to {value}

- or -

env({name:w}) <- {value}
```

Sets an environment variable to a given value.

Arguments:
* `name`: the name of the environment variable, only characters, digits, and underscores are allowed (corresponds to python's regex `\w`)
* `value`: the value to assign to the environment variable

---

**Then**
```
the value of environment variable {name:w} is {expected_value}

- or -

env({name:w}) equals {expected_value}
```

Checks whether the value assigned to an environment variable equals a given expected value.

Arguments:
* `name`: the name of the environment variable to check, only characters, digits, and underscores are allowed (corresponds to python's regex `\w`)
* `expected_value`: the expected value

## Pandas Steps
The steps in [`beehyve/steps/pandas_steps.py`](https://github.com/CRitter93/beehyve/tree/main/beehyve/steps/pandas_steps.py) are used to add pandas dataframes to a test context and test dataframes.

---

**Given**
```
the following table is loaded into dataframe {name:w}

- or -

dataframe {name:w} <-
```

Loads a table into a dataframe in the context.
Uses [`behave_pandas`](https://pypi.org/project/behave-pandas/) for parsing, so the table has to match its syntax.

Arguments:
* `name`: the name of the variable used for the dataframe, only characters, digits, and underscores are allowed (corresponds to python's regex `\w`)
* *table*: the table represents the dataframe, should use the syntax defined by `behave_pandas`.

---

**Given**
```
the following table is loaded into series {name:w}

- or -

series {name:w} <-
```

Loads a table into a series in the context.
Uses [`behave_pandas`](https://pypi.org/project/behave-pandas/) for parsing, so the table has to match its syntax.

Arguments:
* `name`: the name of the variable used for the series, only characters, digits, and underscores are allowed (corresponds to python's regex `\w`)
* *table*: the table represents the series, should use the syntax defined by `behave_pandas`.

---

**Given**
```
the CSV file {file_name:CSVFile} is loaded into dataframe {name:w} (read_csv kwargs: {kwargs:Dict})

- or -

dataframe {name:w} <- read({file_name:CSVFile}, kwargs={kwargs:Dict})

- or -

the CSV file {file_name:CSVFile} is loaded into dataframe {name:w}

- or -

dataframe {name:w} <- read({file_name:CSVFile})
```

Loads a CSV file into a dataframe in the context.

Arguments:
* `name`: the name of the variable used for the dataframe, only characters, digits, and underscores are allowed (corresponds to python's regex `\w`)
* `file_name`: the name of the CSV file, a file path (only characters, digits, and underscores are allowed) ending with `.csv` or `.CSV`
* `kwargs`: Optional dict of keyword arguments passed to pandas' [`read_csv`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html) function, interpreted using [`ast.literal_eval`](https://docs.python.org/3/library/ast.html#ast.literal_eval).
Example: `{"delimiter" = ";", "skiprows": 1}`

---

**Then**
```
dataframe {name:w} is equal to (kwargs: {kwargs:FrameEqualsKWArgs})

- or -

dataframe {name:w} equals ({kwargs:FrameEqualsKWArgs})

- or -

dataframe {name:w} is equal to

- or -

dataframe {name:w} equals
```

Checks if a dataframe matches a dataframe given as table.
Uses [`behave_pandas`](https://pypi.org/project/behave-pandas/) for parsing, so the table has to match its syntax.

Arguments:
* `name`: the name of the variable used for the dataframe, only characters, digits, and underscores are allowed (corresponds to python's regex `\w`)
* *table*: *table*: the table represents the expected dataframe, should use the syntax defined by `behave_pandas`.
* `kwargs`: Optional keyword arguments to apply when checking. Comma-separated list of `keyword=value` pairs.
Available options are:
    * `common_columns_only` (bool): whether to check all columns or just the columns that both dataframes share, default=`False`
    * `ignore_index` (bool): whether to check the index or not, default=`False`
    * `ignore_dtypes` (bool): whether to check the dtypes or not, default=`False`
    * `atol` (float): an absolute tolerance to apply when comparing numerical values, default=`1e-8`
    * `rtol` (float): a relative tolerance to apply when comparing numerical values, default=`1e-5`
    * `check_exact` (bool): whether to check numerical values exactly or with a tolerance (see above), default=`False`

---

**Then**
```
dataframe {name1:w} is equal to dataframe {name2:w} (kwargs: {kwargs:FrameEqualsKWArgs})

- or -

dataframe {name1:w} equals {name2:w} ({kwargs:FrameEqualsKWArgs})

- or -

dataframe {name1:w} is equal to dataframe {name2:w}

- or -

dataframe {name1:w} equals {name2:w}
```

Checks if a dataframe matches another dataframe.

Arguments:
* `name1`: the name of the variable used for the actual dataframe, only characters, digits, and underscores are allowed (corresponds to python's regex `\w`)
* `name2`: the name of the variable used for the expected dataframe, only characters, digits, and underscores are allowed (corresponds to python's regex `\w`)
* `kwargs`: Optional keyword arguments to apply when checking. Comma-separated list of `keyword=value` pairs.
Available options are:
    * `common_columns_only` (bool): whether to check all columns or just the columns that both dataframes share, default=`False`
    * `ignore_index` (bool): whether to check the index, default=`False`
    * `ignore_dtypes` (bool): whether to check the dtypes, default=`False`
    * `atol` (float): an absolute tolerance to apply when comparing numerical values, default=`1e-8`
    * `rtol` (float): a relative tolerance to apply when comparing numerical values, default=`1e-5`
    * `check_exact` (bool): whether to check numerical values exactly or with a tolerance (see above), default=`False`

---

**Then**
```
series {name:w} is equal to (kwargs: {kwargs:SeriesEqualsKWArgs})

- or -

series {name:w} equals ({kwargs:SeriesEqualsKWArgs})

- or -

series {name:w} is equal to

- or -

series {name:w} equals
```

Checks if a series matches a series given as table.
Uses [`behave_pandas`](https://pypi.org/project/behave-pandas/) for parsing, so the table has to match its syntax.

Arguments:
* `name`: the name of the variable used for the series, only characters, digits, and underscores are allowed (corresponds to python's regex `\w`)
* *table*: *table*: the table represents the expected series, should use the syntax defined by `behave_pandas`.
* `kwargs`: Optional keyword arguments to apply when checking. Comma-separated list of `keyword=value` pairs.
Available options are:
    * `ignore_index` (bool): whether to check the index, default=`False`
    * `ignore_dtypes` (bool): whether to check the dtypes, default=`False`
    * `ignore_names` (bool): whether to ignore the series and index names attribute, default=`False`
    * `atol` (float): an absolute tolerance to apply when comparing numerical values, default=`1e-8`
    * `rtol` (float): a relative tolerance to apply when comparing numerical values, default=`1e-5`
    * `check_exact` (bool): whether to check numerical values exactly or with a tolerance (see above), default=`False`

---

**Then**
```
series {name1:w} is equal to series {name2:w} (kwargs: {kwargs:SeriesEqualsKWArgs})

- or -

series {name1:w} equals {name2:w} ({kwargs:SeriesEqualsKWArgs})

- or -

series {name1:w} is equal to series {name2:w}

- or -

series {name1:w} equals {name2:w}
```

Checks if a series matches another series.

Arguments:
* `name1`: the name of the variable used for the actual series, only characters, digits, and underscores are allowed (corresponds to python's regex `\w`)
* `name2`: the name of the variable used for the expected series, only characters, digits, and underscores are allowed (corresponds to python's regex `\w`)
* `kwargs`: Optional keyword arguments to apply when checking. Comma-separated list of `keyword=value` pairs.
Available options are:
    * `ignore_index` (bool): whether to check the index, default=`False`
    * `ignore_dtypes` (bool): whether to check the dtypes, default=`False`
    * `ignore_names` (bool): whether to ignore the series and index names attribute, default=`False`
    * `atol` (float): an absolute tolerance to apply when comparing numerical values, default=`1e-8`
    * `rtol` (float): a relative tolerance to apply when comparing numerical values, default=`1e-5`
    * `check_exact` (bool): whether to check numerical values exactly or with a tolerance (see above), default=`False`

## Function Steps

The steps in [`beehyve/steps/function_steps.py`](https://github.com/CRitter93/beehyve/tree/main/beehyve/steps/function_steps.py) are used to call functions using the variables in the context.

---

**When**
```
the function {func_name:w} of module {module:Module} is called writing the results to {result_names:Result}

- or -

{result_names:Result} <- {module:Module}.{func_name:w}()

- or -

the function {func_name:w} of module {module:Module} is called

- or -

{module:Module}.{func_name:w}() is called
```

Call a function using variables in the context.
The variables will automatically be matched with the signature of the function, e.g., if `def f(x, y)` the context needs to have variables `x` and `y` available.

Arguments:
* `func_name`: the name of the function to call
* `module`: the name of the module containing the function, will be imported using [`importlib.import_module`](https://docs.python.org/3/library/importlib.html#importlib.import_module)
* `result_names`: optional list of variable name(s) to assign the results to, a comma-separated list of names or a single name (s.a., `\w`)

---

**When**
```
the function {func_name:w} of module {module:Module} is called using arguments {args:Arguments} and keyword arguments {kwargs:KWArguments} writing the results to {result_names:Result}

- or -

{result_names:Result} <- {module:Module}.{func_name:w}({args:Arguments}{kwargs:KWArguments})

- or -

the function {func_name:w} of module {module:Module} is called using arguments {args:Arguments} and keyword arguments {kwargs:KWArguments}

- or -

{module:Module}.{func_name:w}({args:Arguments}{kwargs:KWArguments}) is called
```

Call a function using variables in the context.
The given variables will be used for the function.
The variables need to be available in the context.

Arguments:
* `func_name`: the name of the function to call
* `module`: the name of the module containing the function, will be imported using [`importlib.import_module`](https://docs.python.org/3/library/importlib.html#importlib.import_module)
* `args`: a list of variable names to be used as positional arguments, a comma-separated list of names or a single name (s.a., `\w`)
* `kwargs`: a list of keyword arguments where the key is the name of the function parameter and the value is a variable name, a comma-separated list of `param=variable` pairs
* `result_names`: optional list of variable name(s) to assign the results to, a comma-separated list of names or a single name (s.a., `\w`)

## Monkeypatching Steps

The steps in [`beehyve/steps/monkeypatch_steps.py`](https://github.com/CRitter93/beehyve/tree/main/beehyve/steps/monkeypatch_steps.py) are used to monkeypatch objects and attributes for specific test cases.

> Monkeypatching requires to use the tag `@monkeypatch` and the `before_tag` function defined in [`beehyve/utils/monkeypatch.py`](https://github.com/CRitter93/beehyve/tree/main/beehyve/utils/monkeypatch.py) (see [Usage](#usage)).

---

**Given**
```
the value of environment variable {name:w} is monkeypatched to {value}

- or -

env({name:w}) <-monkeypatch- {value}
```

Monkeypatch an existing environment variable to a given value.

Arguments:
* `name`: the name of the environment variable, only characters, digits, and underscores are allowed (corresponds to python's regex `\w`)
* `value`: the value to monkeypatch to the environment variable

---

**Given**
```
the attribute {attribute_name:w} of class {class_name:w} of module {module_name:Module} is monkeypatched to attribute {other_attribute_name:w} of module {other_module_name:Module}

- or -

the attribute {attribute_name:w} of module {module_name:Module} is monkeypatched to attribute {other_attribute_name:w} of module {other_module_name:Module}

- or -

{module_name:Module}.{class_name:w}[{attribute_name:w}] <-monkeypatch- {other_module_name:Module}.{other_attribute_name:w}

- or -

{module_name:w}[{attribute_name:w}] <-monkeypatch- {other_module_name:Module}.{other_attribute_name:w}
```

Monkeypatch an arbitrary attribute to another attribute.

Arguments:
* `attribute_name`: the name of the attribute to monkeypatch
* `module_name`: the name of the module containing the attribute, will be imported using [`importlib.import_module`](https://docs.python.org/3/library/importlib.html#importlib.import_module)
* `class_name`: optional name of a class containing the attribute to patch
* `other_module_name`: the name of the module containing the attribute to use instead, will be imported using [`importlib.import_module`](https://docs.python.org/3/library/importlib.html#importlib.import_module)
* `other_attribute_name`: the name of the attribute to use instead

---

**Given**
```
the attribute {attribute_name:w} of class {class_name:w} of module {module_name:Module} is monkeypatched to {value}

- or -

{module_name:Module}.{class_name:w}[{attribute_name:w}] <-monkeypatch- {value}

- or -

the attribute {attribute_name:w} of module {module_name:Module} is monkeypatched to {value}

- or -

{module_name:w}[{attribute_name:w}] <-monkeypatch- {value}
```

Monkeypatch an arbitrary attribute to a value.

Arguments:
* `attribute_name`: the name of the attribute to monkeypatch
* `module_name`: the name of the module containing the attribute, will be imported using [`importlib.import_module`](https://docs.python.org/3/library/importlib.html#importlib.import_module)
* `class_name`: optional name of a class containing the attribute to patch
* `value`: the value to monkeypatch the variable to. Uses [`ast.literal_eval`](https://docs.python.org/3/library/ast.html#ast.literal_eval) to interpret the value.


# Not-yet-frequently Asked Questions
## Why beehyve?
Because telling a data scientist to write tests is like poking a beehive with a stick.

## No really, why beehyve?
Beehyve tries to make testing data pipelines less of a pain by providing an easy way to test data transformation functions.
