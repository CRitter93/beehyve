"""Collection of functions to handle variables in the behave context."""

import importlib
import os
from typing import Any, Optional

from behave.runner import Context


def add_var(context: Context, name: str, val: Any) -> None:
    """Add a variable to the context, making it available in future steps.

    :param context: the current context
    :param name: the name of the new variable
    :param val: the value that should be assigned to the variable
    """
    if "vars" not in context:
        context.vars = {}

    if name in context.vars:
        raise KeyError(f"variable {name} cannot be overwritten")

    context.vars[name] = val


def get_var(context: Context, name: str) -> Any:
    """Get a value from a variable stored in the context.

    :param context: the current context
    :param name: the name of the variable to get
    :return: the value of the variable
    """
    if "vars" not in context or name not in context.vars:
        raise KeyError(f"variable {name} has not been set")

    return context.vars[name]


def has_var(context: Context, name: str) -> bool:
    """Check whether the context has a value assigned to a given variable name.

    :param context: the current context
    :param name: the variable name to check
    :return: True if the variable is present in the context, False otherwise
    """
    return "vars" in context and name in context.vars


def get_env(name: str) -> str:
    """Get the value from the given environment variable.

    :param name: the name of the environment variable
    :return: the value assigned to the given environment variable
    """
    env_value = os.getenv(name)
    if env_value is None:
        raise AssertionError(f"No value set for environment variable {name}")
    return env_value


def set_env(name: str, value: str) -> None:
    """Set the value of an environment variable.

    :param name: the name of the variable to set
    :param value: the value to assign to the environment variable
    """
    os.environ[name] = value


def get_from_module(module_name: str, attribute_name: Optional[str] = None) -> Any:
    """Get a module or an attribute from a module.

    :param module_name: a module to import
    :param attribute_name: an attribute to get from the module, defaults to None
    :return: the given attribute from the module or the whole module if no attribute is given
    """
    module = importlib.import_module(module_name)
    if attribute_name:
        return getattr(module, attribute_name)
    return module
