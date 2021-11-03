"""Collection of functions to handle variables in the behave context."""

import importlib
import os
from typing import Any, Optional

from behave.runner import Context


def add_var(context: Context, name: str, val: Any):
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
    return os.getenv(name)


def set_env(name: str, value: str):
    os.environ[name] = value


def get_from_module(module_name: str, object_name: Optional[str] = None) -> Any:
    module = importlib.import_module(module_name)
    if object_name:
        return getattr(module, object_name)
    return module
