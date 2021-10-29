from typing import Any

from behave.runner import Context


def add_var(context: Context, name: str, val: Any):
    """Adds a variable to the context, making it available in future steps.

    :param context: the current context
    :param name: the name of the new variable
    :param val: the value that should be assigned to the variable
    :raises KeyError: if the variable name is already in use
    """
    if "vars" not in context:
        context.vars = {}

    if name in context.vars:
        raise KeyError(f"variable {name} cannot be overwritten")

    context.vars[name] = val


def get_var(context: Context, name: str) -> Any:
    """Gets a value from a variable stored in the context.

    :param context: the current context
    :param name: the name of the variable to get
    :raises KeyError: if the variable is not available in the context
    :return: the value of the variable
    """
    if "vars" not in context or name not in context.vars:
        raise KeyError(f"variable {name} has not been set")

    return context.vars[name]


def has_var(context: Context, name: str) -> bool:
    """Checks whether the context has a value assigned to a given variable name.

    :param context: the current context
    :param name: the variable name to check
    :return: True if the variable is present in the context, False otherwise
    """
    return "vars" in context and name in context.vars
