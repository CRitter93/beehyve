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
    monkeypatch_env(context, name=name, value=value)


@given(
    "the attribute {attribute_name:w} of object {object_name:w} of module {module_name:Module} "
    "is monkeypatched to object {other_object_name:w} of module {other_module_name:Module}"
)
@given(
    "the attribute {attribute_name:w} of module {module_name:Module} "
    "is monkeypatched to object {other_object_name:w} of module {other_module_name:Module}"
)
@given(
    "{module_name:Module}.{object_name:w}[{attribute_name:w}] <-monkeypatch- {other_module_name:Module}.{other_object_name:w}"
)
def step_monkeypatch_set_attr_to_object(
    context: Context,
    module_name: str,
    attribute_name: str,
    other_module_name: str,
    other_object_name: str,
    object_name: str = None,
):
    value = get_from_module(other_module_name, other_object_name)

    monkeypatch_attr(
        context,
        module_name=module_name,
        object_name=object_name,
        attribute_name=attribute_name,
        value=value,
    )


@given(
    "the attribute {attribute_name:w} of object {object_name:w} of module {module_name:Module} is monkeypatched to {value}"
)
@given("{module_name:Module}.{object_name:w}[{attribute_name:w}] <-monkeypatch- {value}")
@given("the attribute {attribute_name:w} of module {module_name:Module} is monkeypatched to {value}")
def step_monkeypatch_set_attr_to_value(
    context: Context,
    module_name: str,
    attribute_name: str,
    value: str,
    object_name: Optional[str] = None,
):
    value = literal_eval(value)

    monkeypatch_attr(
        context,
        module_name=module_name,
        object_name=object_name,
        attribute_name=attribute_name,
        value=value,
    )
