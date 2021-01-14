# beehyve

[![Test Status](https://github.com/CRitter93/beehyve/workflows/Tests/badge.svg)](https://github.com/CRitter93/beehyve/actions?query=workflow%3ATests)
[![Lint Status](https://github.com/CRitter93/beehyve/workflows/Lint/badge.svg)](https://github.com/CRitter93/beehyve/actions?query=workflow%3ALint)
[![isort Status](https://github.com/CRitter93/beehyve/workflows/isort/badge.svg)](https://github.com/CRitter93/beehyve/actions?query=workflow%3Aisort)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![codecov](https://codecov.io/gh/CRitter93/beehyve/branch/main/graph/badge.svg?token=5QBV9RI4J6)](https://codecov.io/gh/CRitter93/beehyve)

---

__Hijacking [behave](https://behave.readthedocs.io/en/stable/) to test data pipelines.__

---

## Installation

### Install using PyPI
TBD

### Install from sources
To install the latest version from sources use:
```bash
git clone https://github.com/CRitter93/beehyve.git
cd beehyve
python setup.py install
```

### Install using pip
To install beehyve using pip run the following code:
```bash
python -m pip install git+https://github.com/CRitter93/beehyve.git#egg=beehyve
```

## Usage
To use the steps defined by beehyve add an import script into your features/steps folder:

*import_behyve.py:*
```python
from beehyve.steps import *
```

The steps can than be used alongside others in the feature files.

## Examples
The most common usage of beehyve should be testing data transformations.
Testing these usually follows the same steps: setup &rarr; execute transformation &rarr; compare with desired output.
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

More example uses of the beehyve steps can be found in [basic_steps.feature](https://github.com/CRitter93/beehyve/blob/initial_commit/features/basic_steps.feature) and [call_functions.feature](https://github.com/CRitter93/beehyve/blob/initial_commit/features/call_functions.feature).

## Not-yet-frequently Asked Questions
### Why beehyve?
Because telling a data scientist to write tests is like poking a beehive with a stick.

### No really, why beehyve?
Beehyve tries to make testing data pipelines less of a pain by providing an easy way to test data transformation functions.
