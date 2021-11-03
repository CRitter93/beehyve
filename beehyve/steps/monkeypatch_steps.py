"""Collection of steps definitions for monkeypatching."""

from ast import literal_eval
from typing import Optional

from behave import given, register_type
from behave.runner import Context

from beehyve.steps import types
from beehyve.utils.monkeypatch import monkeypatch_attr, monkeypatch_env
from beehyve.utils.variables import get_from_module

register_type(Module=types.parse_module)


@given("the value of environment variable {name:w} is monkeypatched to {value}")
@given("env({name:w}) <-monkeypatch- {value}")
def step_monkeypatch_set_env(context: Context, name: str, value: str):
    """Apply monkeypatching to set an environment variable.

    See :py:func:`monkeypatch_env` for more detail.

    :param context: the current context
    :param name: name of the environment variable to set
    :param value: value to set for the environment variable
    """
    monkeypatch_env(context, name=name, value=value)


@given(
    "the attribute {attribute_name:w} of class {class_name:w} of module {module_name:Module} "
    "is monkeypatched to attribute {other_attribute_name:w} of module {other_module_name:Module}"
)
@given(
    "the attribute {attribute_name:w} of module {module_name:Module} "
    "is monkeypatched to attribute {other_attribute_name:w} of module {other_module_name:Module}"
)
@given(
    "{module_name:Module}.{class_name:w}[{attribute_name:w}] "
    "<-monkeypatch- {other_module_name:Module}.{other_attribute_name:w}"
)
def step_monkeypatch_set_attr_to_class(
    context: Context,
    module_name: str,
    attribute_name: str,
    other_module_name: str,
    other_attribute_name: str,
    class_name: str = None,
):
    """Apply monkeypatching to overwrite an attribute with a python class, constant, or function.

    See :py:func:`monkeypatch_attr` for more detail.

    :param context: the current context
    :param module_name: the name of the module containing the attribute to patch
    :param attribute_name: the name of the attribute to patch
    :param other_module_name: the name of the module containing the new attribute to assign
    :param other_attribute_name: the name of the new attribute to assign
    :param class_name: optional name of a class containing the attribute, defaults to None
    """
    value = get_from_module(other_module_name, other_attribute_name)

    monkeypatch_attr(
        context,
        module_name=module_name,
        class_name=class_name,
        attribute_name=attribute_name,
        value=value,
    )


@given(
    "the attribute {attribute_name:w} of class {class_name:w} of module {module_name:Module} "
    "is monkeypatched to {value}"
)
@given("{module_name:Module}.{class_name:w}[{attribute_name:w}] <-monkeypatch- {value}")
@given("the attribute {attribute_name:w} of module {module_name:Module} is monkeypatched to {value}")
def step_monkeypatch_set_attr_to_value(
    context: Context,
    module_name: str,
    attribute_name: str,
    value: str,
    class_name: Optional[str] = None,
):
    """Apply monkeypatching to overwrite an attribute with a value.

    See :py:func:`monkeypatch_attr` for more detail.

    The given value will be interpreted using :py:func:`ast.literal_eval`.

    :param context: the current context
    :param module_name: the name of the module containing the attribute to patch
    :param attribute_name: the name of the attribute to patch
    :param value: the value to assign
    :param class_name: optional name of a class containing the attribute, defaults to None
    """
    value = literal_eval(value)

    monkeypatch_attr(
        context,
        module_name=module_name,
        class_name=class_name,
        attribute_name=attribute_name,
        value=value,
    )
