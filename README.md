# BeeHyve

[![Test Status](https://github.com/CRitter93/beehyve/workflows/Tests/badge.svg)](https://github.com/CRitter93/beehyve/actions?query=workflow%3ATests)
[![Lint Status](https://github.com/CRitter93/beehyve/workflows/Lint/badge.svg)](https://github.com/CRitter93/beehyve/actions?query=workflow%3ALint)
[![isort Status](https://github.com/CRitter93/beehyve/workflows/isort/badge.svg)](https://github.com/CRitter93/beehyve/actions?query=workflow%3Aisort)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

---

__Hijacking behave to test data pipelines.__

---

## Installation

### Install from sources
To install the latest version from sources use:
```bash
git clone https://github.com/CRitter93/beehyve.git
cd beehyve
python setup.py install
```

## Usage
To use the steps defined by BeeHyve add an import script into your features/steps folder:

*import_behyve.py:*
```python
from beehyve.steps import *
```

The steps can than be used alongside others in the feature files.

## Examples
Example uses of the BeeHyve steps cna be found 
