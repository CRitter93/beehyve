"""Collection of functions used to call arbitrary functions in step definitions."""

import inspect
from collections.abc import Iterable
from typing import Any, Callable, Mapping, Optional, Sequence, Tuple, Union

from behave.runner import Context

from beehyve.utils.variables import add_var, get_from_module, get_var, has_var


def execute_function(
    *,
    context: Context,
    func_name: str,
    module: str,
    args: Sequence[str],
    kwargs: Mapping[str, str],
    result_names: Tuple[str, ...] = (),
):
    """Import and run a function from a given module.

    Uses the given args and kwargs from the context as arguments.

    :param context: the current context
    :param func_name: the name of the function to execute
    :param module: the module where the function can be found,
        i.e., you should be able to import <func_name> from <module>
    :param args: variable names of the variables
        which should be used as arguments to the function
    :param kwargs: a mapping of function kwarg to variable name
        which should be passed to the function
    :param result_names: a tuple of variable names
        to which the result(s) of the function should be assigned
    """
    func = get_from_module(module, func_name)

    args_vals = _load_args_from_context(context, args)
    kwargs_vals = _load_kwargs_from_context(context, kwargs)

    results = func(*args_vals, **kwargs_vals)

    _assign_results(context, results, result_names)


def _load_args_from_context(context: Context, args: Sequence[str]) -> Sequence[Any]:
    args_vals = [get_var(context, arg) for arg in args]
    return args_vals


def _load_kwargs_from_context(context: Context, kwargs: Mapping[str, str]) -> Mapping[str, Any]:
    kwargs_vals = {keyword: get_var(context, kwarg) for keyword, kwarg in kwargs.items()}
    return kwargs_vals


def execute_function_from_context(
    *,
    context: Context,
    func_name: str,
    module: str,
    result_names: Tuple[str, ...] = (),
):
    """Import and run a function from a given module.

    It expects the variables in the context to have the exact same names
    as the arguments of the function signature.

    :param context: the current context
    :param func_name: the name of the function to execute
    :param module: the module where the function can be found,
        i.e., you should be able to import <func_name> from <module>
    :param result_names: a tuple of variable names
        to which the result(s) of the function should be assigned
    """
    func = get_from_module(module, func_name)

    signature = _get_func_signature(func)

    _check_func_signature(context, signature)

    args_vals, kwargs_vals = signature.get_argument_values_for_context(context)

    results = func(*args_vals, **kwargs_vals)

    _assign_results(context, results, result_names)


def _get_func_signature(func: Callable) -> "SignatureHandler":
    signature = inspect.signature(func)

    return SignatureHandler(signature)


def _check_func_signature(context: Context, signature: "SignatureHandler"):
    has_required_args = signature.context_has_required_args(context)
    has_required_varargs = signature.context_has_required_varargs(context)
    has_required_kwargs = signature.context_has_required_kwargs(context)
    has_required_varkw = signature.context_has_required_varkw(context)

    if not (has_required_args and has_required_varargs and has_required_kwargs and has_required_varkw):
        raise ValueError("Not all required arguments are in the context.")


def _assign_results(
    context: Context,
    results: Optional[Union[Any, Tuple[Any, ...]]],
    result_names: Tuple[str, ...],
):
    if results is None and len(result_names) == 0:
        return

    if not isinstance(results, tuple):
        results = (results,)

    if len(results) == len(result_names):
        for name, val in zip(result_names, results):
            add_var(context, name, val)

    elif len(result_names) == 1:
        add_var(context, result_names[0], results)

    else:
        raise ValueError(
            f"length mismatch of function returns ({len(results)}) " f"and given variable names ({len(result_names)})"
        )


class SignatureHandler:
    """Handler to deal with function signatures."""

    def __init__(self, signature: inspect.Signature):
        """Initialize a handler for the given signature.

        :param signature: a signature object
        """
        self._signature = signature

        self._args, self._varargs, self._kwargs, self._varkw = self._split_signature()

    def _split_signature(
        self,
    ) -> Tuple[
        Sequence[inspect.Parameter],
        Optional[inspect.Parameter],
        Sequence[inspect.Parameter],
        Optional[inspect.Parameter],
    ]:
        args = []
        varargs = None
        kwargs = []
        varkw = None

        for parameter in self._signature.parameters.values():
            if parameter.kind in (
                inspect.Parameter.POSITIONAL_ONLY,
                inspect.Parameter.POSITIONAL_OR_KEYWORD,
            ):
                args.append(parameter)
            elif parameter.kind == inspect.Parameter.VAR_POSITIONAL:
                varargs = parameter
            elif parameter.kind == inspect.Parameter.KEYWORD_ONLY:
                kwargs.append(parameter)
            elif parameter.kind == inspect.Parameter.VAR_KEYWORD:
                varkw = parameter
            else:
                raise KeyError(f"Unsupported parameter kind: {parameter.kind}")

        return args, varargs, kwargs, varkw

    def context_has_required_args(self, context: Context) -> bool:
        """Check whether the context contains all args from the signature that do not have a default value.

        :param context: the current context
        :return: a boolean representing the check
        """
        return all([self._arg_is_available(context, arg) for arg in self._args])

    def context_has_required_varargs(self, context: Context) -> bool:
        """Check whether the context contains the varargs from the signature.

        :param context: the current context
        :return: a boolean representing the check
        """
        return not self._varargs or self._arg_is_available(context, self._varargs)

    def context_has_required_kwargs(self, context: Context) -> bool:
        """Check whether the context contains all kwargs from the signature that do not have a default value.

        :param context: the current context
        :return: a boolean representing the check
        """
        return all([self._arg_is_available(context, kwarg) for kwarg in self._kwargs])

    def context_has_required_varkw(self, context: Context) -> bool:
        """Check whether the context contains the varkw from the signature.

        :param context: the current context
        :return: a boolean representing the check
        """
        return not self._varkw or self._arg_is_available(context, self._varkw)

    @staticmethod
    def _arg_is_available(context: Context, arg: inspect.Parameter) -> bool:
        return arg.default != inspect.Parameter.empty or has_var(context, arg.name)

    def get_argument_values_for_context(
        self,
        context: Context,
    ) -> Tuple[Sequence[Any], Mapping[str, Any]]:
        """Get all argument values corresponding to this signature from the context.

        :param context: the current context
        :return: args (positional args and varargs in correct order),
            kwargs (keyword only args and varkw as mapping)
        """
        args_vals = self._get_args_vals_from_context(context)
        varargs_vals = self._get_varargs_vals_from_context(context)
        kwargs_vals = self._get_kwargs_vals_from_context(context)
        varkw_vals = self._get_varkw_vals_from_context(context)

        varargs_vals = self._varargs_vals_to_tuple(varargs_vals)

        args_vals.extend(varargs_vals)
        kwargs_vals.update(varkw_vals)

        return args_vals, kwargs_vals

    def _get_args_vals_from_context(self, context: Context):
        return [get_var(context, arg.name) for arg in self._args if has_var(context, arg.name)]

    def _get_varargs_vals_from_context(self, context: Context):
        if self._varargs and has_var(context, self._varargs.name):
            return get_var(context, self._varargs.name)
        return tuple()

    def _get_kwargs_vals_from_context(self, context: Context):
        return {kwarg.name: get_var(context, kwarg.name) for kwarg in self._kwargs if has_var(context, kwarg.name)}

    def _get_varkw_vals_from_context(self, context: Context):
        if self._varkw and has_var(context, self._varkw.name):
            varkw_vals = get_var(context, self._varkw.name)
            if not isinstance(varkw_vals, dict):
                raise ValueError("varkw values have to be a dict")
            return varkw_vals
        return dict()

    @staticmethod
    def _varargs_vals_to_tuple(varargs_vals):
        if not isinstance(varargs_vals, tuple):
            if isinstance(varargs_vals, Iterable) and not isinstance(varargs_vals, str):
                varargs_vals = tuple(varargs_vals)
            else:
                varargs_vals = (varargs_vals,)

        return varargs_vals
