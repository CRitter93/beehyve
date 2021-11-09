"""Python file setting up the environment for testing in beehyve."""
# flake8: noqa

import os

from behave.runner import Context

from beehyve.utils import monkeypatch


def before_tag(context: Context, tag: str):
    if tag == "dummy_env":
        os.environ["ENV_A"] = "1"
        os.environ["ENV_B"] = "abc"
    else:
        monkeypatch.before_tag(context, tag)


def after_tag(_context: Context, tag: str):
    if tag == "dummy_env":
        del os.environ["ENV_A"]
        del os.environ["ENV_B"]
