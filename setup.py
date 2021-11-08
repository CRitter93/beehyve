"""Setup file for installing beehyve."""

from setuptools import find_packages, setup

from beehyve.__version__ import __version__ as version

# Package metadata
# ----------------

NAME = "beehyve"
DESCRIPTION = "A utility library facilitating the use of behave for testing data pipelines."
URL = ""
EMAIL = "christian.ritter.93@gmail.com"
AUTHOR = "Christian Ritter"
REQUIRES_PYTHON = ">=3.7"
VERSION = version

# What packages are required for this module to be executed?
REQUIRED = [
    "behave>=1.2,<1.3",
    "pandas>=1.3,<1.4",
    "behave-pandas>=0.4,<0.5",
    "parse>=1.19,<1.20",
    "pytest>=6.2.5,<6.3",
]
EXTRAS = {
    "dev": [
        "black>=20.8b0,<21",
        "coverage>=5.5,<6",
        "isort>=5.9.3,<6",
    ]
}

# Package setup
# -------------
setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=("tests", "docs")),
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    setup_requires=["wheel"],
)
