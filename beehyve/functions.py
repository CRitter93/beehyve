import importlib
import inspect
from collections.abc import Iterable
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from behave.runner import Context


def add_var(context: Context, name: str, val: Any) -> None:
    """Adds a variable to the context, making it available in future steps.

    :param context: the current context
    :type context: :class:`behave.runner.Context`
    :param name: the name of the new variable
    :type name: str
    :param val: the value that should be assigned to the variable
    :type val: Any
    :raises ValueError: if the variable name is already in use
    """
    if "vars" not in context:
        context.vars = {}

    if name in context.vars:
        raise ValueError(f"variable {name} cannot be overwritten")

    context.vars[name] = val


def get_var(context: Context, name: str) -> Any:
    """Gets a value from a variable stored in the context.

    :param context: the current context
    :type context: :class:`behave.runner.Context`
    :param name: the name of the variable to get
    :type name: str
    :raises ValueError: if the variable is not available in the context
    :return: the value of the variable
    :rtype: Any
    """
    if "vars" not in context or name not in context.vars:
        raise ValueError(f"variable {name} has not been set")

    return context.vars[name]


def has_var(context: Context, name: str) -> bool:
    """Checks whether the context has a value assigned to a given variable name.

    :param context: the current context
    :type context: :class:`behave.runner.Context`
    :param name: the variable name to check
    :type name: str
    :return: True if the variable is present in the context, False otherwise
    :rtype: bool
    """
    return "vars" in context and name in context.vars


def _check_func_arguments(
    context: Context, func: Callable
) -> Tuple[List[str], Optional[str], List[str], Optional[str]]:
    """Checks whether all required arguments of a function are available
     in the context's variables.

    :param context: the current context
    :type context: :class:`behave.runner.Context`
    :param func: the function to check
    :type func: Callable
    :raises ValueError: if the function cannot be called with the available variables
    :return:  the names of available args, varargs, kwargs, and varkw
    :rtype: Tuple[List[str], Optional[str], List[str], Optional[str]]
    """
    spec = inspect.getfullargspec(func)

    args = spec.args
    varargs = spec.varargs
    kwargs = spec.kwonlyargs
    varkw = spec.varkw

    available_args = [arg for arg in args if has_var(context, arg)]
    available_varargs = varargs if varargs and has_var(context, varargs) else None
    available_kwargs = [kwarg for kwarg in kwargs if has_var(context, kwarg)]
    available_varkw = varkw if varkw and has_var(context, varkw) else None

    if spec.defaults and varargs is None:
        required_args = args[: -len(spec.defaults)]
    else:
        required_args = args
    has_required_args = all([arg in available_args for arg in required_args])
    has_required_varargs = varargs is None or available_varargs == varargs

    if spec.kwonlydefaults:
        required_kwargs = [
            kwarg for kwarg in kwargs if kwarg not in spec.kwonlydefaults
        ]
    else:
        required_kwargs = []
    has_required_kwargs = all([kwarg in available_kwargs for kwarg in required_kwargs])
    has_required_varkw = varkw is None or available_varkw == available_varkw

    if (
        has_required_args
        and has_required_varargs
        and has_required_kwargs
        and has_required_varkw
    ):
        return available_args, available_varargs, available_kwargs, available_varkw

    else:
        error_msg = []
        if not has_required_args:
            error_msg.append(
                f"required arguments are missing: {[arg for arg in required_args if arg not in available_args]}"
            )
        if not has_required_varargs:
            error_msg.append(f"required varargs is missing: {varargs}")
        if not has_required_kwargs:
            error_msg.append(
                f"required kwargs are missing: {[kwarg for kwarg in required_kwargs if kwarg not in available_kwargs]}"
            )
        if not has_required_varkw:
            error_msg.append(f"required varkw is missing: {varkw}")

        raise ValueError("\n".join(error_msg))


def _get_argument_values(
    context: Context,
    args: List[str],
    varargs: Optional[str],
    kwargs: List[str],
    varkw: Optional[str],
) -> Tuple[List[Any], Tuple[Any, ...], Dict[str, Any], Dict[str, Any]]:
    """Returns the values of the available arguments from the context.

    :param context: the current context
    :type context: :class:`behave.runner.Context`
    :param args: a list of args
    :type args: List[str]
    :param varargs: a variable name containing a tuple of varargs or None
    :type varargs: Optional[str]
    :param kwargs: a list of kwargs
    :type kwargs: List[str]
    :param varkw: a variable name containing a dict of varkw or None
    :type varkw: Optional[str]
    :raises ValueError: if the value of the varkw variable is not a dict
    :return: the values of the variables of args and varargs, a dict of kwargs,
        and the dict stored in the varkw variable
    :rtype: Tuple[List[Any], Tuple[Any, ...], Dict[str, Any], Dict[str, Any]]
    """
    args_vals = [get_var(context, arg) for arg in args]
    varargs_vals = get_var(context, varargs) if varargs else ()
    kwargs_vals = {kwarg: get_var(context, kwarg) for kwarg in kwargs}
    varkw_vals = get_var(context, varkw) if varkw else {}

    if not isinstance(varargs_vals, tuple):
        if isinstance(varargs_vals, Iterable):
            varargs_vals = tuple(varargs_vals)
        else:
            varargs_vals = (varargs_vals,)

    if not isinstance(varkw_vals, dict):
        raise ValueError("varkw values have to be a dict")

    return args_vals, varargs_vals, kwargs_vals, varkw_vals


def _assign_results(
    context: Context,
    results: Optional[Union[Any, Tuple[Any, ...]]],
    result_vars: Tuple[str, ...],
) -> None:
    """Assignes the results of a function (i.e., a single value or a tuple of values)
    to a given set of variables.

    If the number of variable names matches the number of values,
    the values are assigned respectively.
    If there is only one variable name, all results are assigned to that variable.

    :param context: the current context
    :type context: :class:`behave.runner.Context`
    :param results: the results of the function
    :type results: Optional[Union[Any, Tuple[Any, ...]]]
    :param result_vars: the names of variables to assign the results to
    :type result_vars: Tuple[str, ...]
    :raises ValueError: if the length of results and result_vars do not match
        and result_vars contains more than one value
    """
    if results is None:
        if len(result_vars) == 0:
            return

    if not isinstance(results, tuple):
        results = (results,)

    if len(results) == len(result_vars):
        for name, val in zip(result_vars, results):
            add_var(context, name, val)
    elif len(result_vars) == 1:
        add_var(context, result_vars[0], results)
    else:
        raise ValueError(
            f"length mismatch of function returns ({len(results)}) and given variable names ({len(result_vars)})"
        )


def run_func(
    context: Context,
    func_name: str,
    module: str,
    result_vars: Tuple[str, ...],
) -> None:
    """Imports and runs a function from a given module
     using the variables of the context as arguments.

    :param context: the current context
    :type context: :class:`behave.runner.Context`
    :param func_name: the name of the function to execute
    :type func_name: str
    :param module: the module where the function can be found,
        i.e., you should be able to import <func_name> from <module>
    :type module: str
    :param result_vars: a tuple of variable names
        to which the result(s) of the function should be assigned
    :type result_vars: Tuple[str]
    """
    module_type = importlib.import_module(module)
    func = getattr(module_type, func_name)

    args, varargs, kwargs, varkw = _check_func_arguments(context, func)

    args_vals, varargs_vals, kwargs_vals, varkw_vals = _get_argument_values(
        context, args, varargs, kwargs, varkw
    )

    if varargs:
        results = func(*args_vals, *varargs_vals, **kwargs_vals, **varkw_vals)

    else:
        results = func(
            **{arg: arg_val for arg, arg_val in zip(args, args_vals)},
            **kwargs_vals,
            **varkw_vals,
        )

    _assign_results(context, results, result_vars)
