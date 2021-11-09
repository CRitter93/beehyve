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
    "behave>=1",
    "pandas>=1",
    "behave-pandas>=0.4",
    "parse>=1.19",
    "pytest>=6.2.5",
]
EXTRAS = {
    "dev": [
        "black>=20.8b0",
        "coverage>=5.5",
        "isort>=5.9.3",
        "flake8>=3.9.2",
        "flake8-docstrings>=1.6.0",
        "pep8-naming>=0.10.0",
        "mccabe>=0.6.1",
        "pydocstyle>=6.1.1",
        "mypy>=0.910",
        "bandit>=1.7.0",
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
    entry_points={
        "console_scripts": [
            "create-beehyve-stubs=beehyve.create_beehyve_step_stubs:main",
        ],
    },
)
