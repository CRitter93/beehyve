import re
from ast import literal_eval

import parse


@parse.with_pattern(r"\(([\"']?.+?[\"']?, ?)+?[\"']?.*?[\"']?\)")
def parse_tuple(string):
    t = literal_eval(string)
    if not isinstance(t, tuple):
        raise ValueError(f"the given value {string} cannot be interpreted as tuple")
    return t


@parse.with_pattern(
    r"\{([\"'].+?[\"']: [\"']?.+?[\"']?, ?)*?([\"'].+?[\"']: [\"']?.+?[\"']?)?\}"
)
def parse_dict(string):
    d = literal_eval(string)
    if not isinstance(d, dict):
        raise ValueError(f"the given value {string} cannot be interpreted as dict")
    return d


@parse.with_pattern(r"(\((\w+?, ?)+?\w*?\)|\w*?)")
def parse_func_result(string):
    if re.match(r"^\w*?$", string):
        return (string,)
    else:
        # add quotes so that it can be evaluated as string
        # e.g., (df1, df2) --> ("df1", "df2")
        string = re.sub(r"(\w+)", r'"\1"', string)
        return parse_tuple(string)


@parse.with_pattern(r".+?(\..+?)+?")
def parse_module(string):
    return string
