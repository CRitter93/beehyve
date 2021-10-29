import re
from ast import literal_eval
from typing import Any, Dict, Mapping, Sequence, Tuple

import parse


@parse.with_pattern(r"\((.+?, ?)+?.*?\)")
def parse_tuple(string: str) -> Tuple[Any, ...]:
    """Parse a tuple from a given string.

    :param string: the string representation of a tuple
    :return: a tuple parsed from the given string
    """
    tup = literal_eval(string)
    if not isinstance(tup, tuple):
        raise ValueError(
            f"the given value {string} cannot be interpreted as tuple"
        )  # pragma: no cover
    return tup


@parse.with_pattern(r"\{([\"'].+?[\"']: .+?, ?)*?([\"'].+?[\"']: .+?)?\}")
def parse_dict(string: str) -> Dict[str, Any]:
    """Parse a dict from a given string.

    :param string: the string representation of the dict
    :return: a dict parsed from the given string
    """
    dic = literal_eval(string)
    if not isinstance(dic, dict):
        raise ValueError(
            f"the given value {string} cannot be interpreted as dict"
        )  # pragma: no cover
    return dic


@parse.with_pattern(r"(\((\w+?, ?)+?\w*?\)|\w*?)")
def parse_func_result(string: str) -> Tuple[str, ...]:
    """Parse a tuple of strings from a given string.
    If only a single string is passed it is added to a tuple.
    Uses :func:`parse_tuple` to do the actual parsing.

    :param string: the string representation of the tuple or a single name
    :return: a tuple containing result names (strings)
    """
    if re.match(r"^\w*?$", string):
        return (string,)
    else:
        # add quotes so that it can be evaluated as string
        # e.g., (df1, df2) --> ("df1", "df2")
        string = re.sub(r"(\w+)", r'"\1"', string)
        return parse_tuple(string)


@parse.with_pattern(r".+?(\..+?)+?")
def parse_module(string: str) -> str:
    """Used to type a module name (i.e., dot-separated module path) in behave.

    :param string: a string representing a module to be imported
    :return: the input string
    """
    return string


@parse.with_pattern(r"(\w+?, ?)*?(\w+?)?")
def parse_args(string: str) -> Sequence[str]:
    if string == "":
        return list()

    args = string.replace(" ", "").split(",")

    if args[-1] == "":
        args = args[:-1]

    return args


@parse.with_pattern(r"(\w+? ?= ?\w+?, ?)*?(\w+? ?= ?\w+?)?")
def parse_kwargs(string: str) -> Mapping[str, str]:
    if string == "":
        return dict

    kwargs_strings = string.replace(" ", "").split(",")

    if kwargs_strings[-1] == "":
        kwargs_strings = kwargs_strings[:-1]

    kwargs_pairs = [kwargs_string.split("=") for kwargs_string in kwargs_strings]

    kwargs = {
        kwargs_name: kwargs_variable for kwargs_name, kwargs_variable in kwargs_pairs
    }

    return kwargs
