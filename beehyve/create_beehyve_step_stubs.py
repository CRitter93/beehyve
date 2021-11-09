"""Script to create "stubs" of step definitions.

To be usedwith the *Cucumber (Gherkin) Full Support* Extension
(https://marketplace.visualstudio.com/items?itemName=alexkrechik.cucumberautocomplete).

As the extension just uses regex parsing, the steps need to be defined in a single line
in a pure text file (i.e., does not detect python imports).

This script will load all steps of **beehyve** and create a dummy file.
"""

from typing import List, Sequence

import click
from behave.matchers import ParseMatcher
from behave.step_registry import registry

from beehyve.steps.all_steps import *  # noqa: F401,F403


@click.command()
@click.option("-o", "--output", help="output file path of the stub file", default="beehyve_stubs")
def main(output: str) -> None:
    """Create a stub file for all beehyve steps."""
    step_definition_lines = []

    step_definition_lines.extend(_convert_givens_to_stub())
    step_definition_lines.extend(_convert_whens_to_stub())
    step_definition_lines.extend(_convert_thens_to_stub())
    step_definition_lines.extend(_convert_steps_to_stub())

    _write_to_file(step_definition_lines, output)


def _convert_givens_to_stub() -> List[str]:
    givens = registry.steps["given"]
    given_lines = []
    for given in givens:
        given_lines.append(_convert_given_to_stub(given))
    return given_lines


def _convert_given_to_stub(given: ParseMatcher) -> str:
    return f"@given('{given.pattern}')"


def _convert_whens_to_stub() -> List[str]:
    whens = registry.steps["when"]
    when_lines = []
    for when in whens:
        when_lines.append(_convert_when_to_stub(when))
    return when_lines


def _convert_when_to_stub(when: ParseMatcher) -> str:
    return f"@when('{when.pattern}')"


def _convert_thens_to_stub() -> List[str]:
    thens = registry.steps["then"]
    then_lines = []
    for then in thens:
        then_lines.append(_convert_then_to_stub(then))
    return then_lines


def _convert_then_to_stub(then: ParseMatcher) -> str:
    return f"@then('{then.pattern}')"


def _convert_steps_to_stub() -> List[str]:
    steps = registry.steps["step"]
    step_lines = []
    for step in steps:
        step_lines.append(_convert_given_to_stub(step))
        step_lines.append(_convert_when_to_stub(step))
        step_lines.append(_convert_then_to_stub(step))
    return step_lines


def _write_to_file(lines: Sequence[str], file_name: str) -> None:
    lines_with_newline = [line + "\n" for line in lines]
    with open(file_name, "w") as f:
        f.writelines(lines_with_newline)


if __name__ == "__main__":
    main("test_stubs")
