import re
from ast import literal_eval
from typing import Any, Callable, Dict, Mapping, Sequence, Tuple

import parse


@parse.with_pattern(r"\((.+?, ?)+?.*?\)")
def parse_tuple(string: str) -> Tuple[Any, ...]:
    """Parse a tuple from a given string.

    Uses :py:func:`literal_eval` to parse the values.
    """
    tup = literal_eval(string)
    if not isinstance(tup, tuple):
        raise ValueError(f"the given value {string} cannot be interpreted as tuple")  # pragma: no cover
    return tup


@parse.with_pattern(r"\{([\"'].+?[\"']: .+?, ?)*?([\"'].+?[\"']: .+?)?\}")
def parse_dict(string: str) -> Dict[str, Any]:
    """Parse a dict from a given string.

    Uses :py:func:`literal_eval` to parse the values.
    """
    dic = literal_eval(string)
    if not isinstance(dic, dict):
        raise ValueError(f"the given value {string} cannot be interpreted as dict")  # pragma: no cover
    return dic


@parse.with_pattern(r"(\((\w+?, ?)+?\w*?\)|\w*?)")
def parse_func_result(string: str) -> Tuple[str, ...]:
    """Parse a tuple of strings from a given string.
    If only a single string is passed it is added to a tuple.
    Uses :func:`parse_tuple` to do the actual parsing.
    """
    if re.match(r"^\w*?$", string):
        return (string,)
    else:
        # add quotes so that it can be evaluated as string
        # e.g., (df1, df2) --> ("df1", "df2")
        string = re.sub(r"(\w+)", r'"\1"', string)
        return parse_tuple(string)


@parse.with_pattern(r"\w+?(\.\w+?)*?")
def parse_module(string: str) -> str:
    """Used to type a module name (i.e., dot-separated module path) in behave."""
    return string


@parse.with_pattern(r"(\w+?, ?)*?(\w+?)?")
def parse_args(string: str) -> Sequence[str]:
    """Parse arguments given as comma separated list."""
    if string == "":
        return list()

    args = string.replace(" ", "").split(",")

    if args[-1] == "":
        args = args[:-1]

    return args


@parse.with_pattern(r"(\w+? ?= ?\w+?, ?)*?(\w+? ?= ?\w+?)?")
def parse_kwargs(string: str) -> Mapping[str, str]:
    """Parse keyword arguments given as comma separated list of assignments,
    e.g., :code:`a=var_1, b=var_2, d=var_3`
    """
    if string == "":
        return dict

    kwargs_strings = string.replace(" ", "").split(",")

    if kwargs_strings[-1] == "":
        kwargs_strings = kwargs_strings[:-1]

    kwargs_pairs = [kwargs_string.split("=") for kwargs_string in kwargs_strings]

    kwargs = {kwargs_name: kwargs_variable for kwargs_name, kwargs_variable in kwargs_pairs}

    return kwargs


@parse.with_pattern(r"(/?\w+?/)*\w+?\.(csv|CSV)")
def parse_csv_file_path(string: str) -> str:
    """Parse a file path of a csv file."""
    return string


def create_limited_kwarg_parser(
    allowed_kwargs: Sequence[str],
) -> Callable[[str], Mapping[str, Any]]:
    kwarg_names_regex = "|".join(allowed_kwargs)
    pattern = fr"(({kwarg_names_regex}) ?= ?.+?, ?)*?(({kwarg_names_regex}) ?= ?.+?)?"

    @parse.with_pattern(pattern)
    def _parse_limited_kwargs(string: str) -> Mapping[str, Any]:
        mapping = parse_kwargs(string)

        mapping = {key: literal_eval(val) for key, val in mapping.items()}

        return mapping

    return _parse_limited_kwargs
