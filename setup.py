import os

from setuptools import find_packages, setup

# Package metadata
# ----------------

NAME = "beehyve"
DESCRIPTION = (
    "A utility library facilitating the use of behave for testing data pipelines."
)
URL = ""
EMAIL = "christian.ritter.93@gmail.com"
AUTHOR = "Christian Ritter"
REQUIRES_PYTHON = ">=3.7"
VERSION = None

# What packages are required for this module to be executed?
REQUIRED = [
    "behave>=1.2",
    "pandas>=1",
    "behave-pandas>=0.4",
    "parse>=1",
]

# Package setup
# -------------

# Load the package's __version__.py module as a dictionary

here = os.path.abspath(os.path.dirname(__file__))

about = {}
if not VERSION:
    with open(os.path.join(here, NAME, "__version__.py")) as f:
        exec(f.read(), about)
else:
    about["__version__"] = VERSION

setup(
    name=NAME,
    version=about["__version__"],
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=("tests", "docs")),
    install_requires=REQUIRED,
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    setup_requires=["wheel"],
)
