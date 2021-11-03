"""Collection of functions used for monkeypatching."""

from typing import Any, Generator, Optional

from behave import fixture, use_fixture
from behave.runner import Context
from pytest import MonkeyPatch

from beehyve.utils.variables import get_from_module


@fixture
def use_monkeypatching(context: Context) -> Generator[MonkeyPatch, None, None]:
    """Behave fixture setting up monkeypatching.

    Uses :py:class:`MonkeyPatch` from pytest.

    :param context: the current context
    :yield: a MonkeyPatch object to use
    """
    context.monkeypatch = MonkeyPatch()
    yield context.monkeypatch

    context.monkeypatch.undo()


def before_tag(context: Context, tag: str):
    """Implementation of behave's `before_tag` function for using monkeypatching.

    Scenarios relying on monkeypatching can be tagged using :code:`@monkeypatch`.

    :param context: the current context
    :param tag: the tag to process, only implemented for :code:`tag == "monkeypatch"`
    """
    if tag == "monkeypatch":
        use_fixture(use_monkeypatching, context)


def monkeypatch_env(context: Context, *, name: str, value: str):
    """Use monkeypatching to overwrite an environment variable.

    :param context: the current context
    :param name: the environment variable to overwrite
    :param value: the value to set for the variable
    """
    _verify_fixture(context)

    context.monkeypatch.setenv(name, value)


def monkeypatch_attr(
    context: Context,
    *,
    module_name: str,
    object_name: Optional[str] = None,
    attribute_name: str,
    value: Any,
):
    """Use monkeypatching to overwrite any attribute from an object.

    :param context: the current context
    :param module_name: the name of the module containing the object
        or attribute, if no object_name is given
    :param object_name: name of the object containing the attribute to overwrite
        or `None` if the attribute is part of a module, defaults to None
    :param attribute_name: the name of the attribute to overwrite
    :param value: the value to use for the attribute
    """
    _verify_fixture(context)

    obj = get_from_module(module_name, object_name)

    context.monkeypatch.setattr(obj, attribute_name, value)


def _verify_fixture(context: Context):
    if "monkeypatch" not in context:
        raise KeyError("When using monkeypatching, a fixture needs to be used.")
