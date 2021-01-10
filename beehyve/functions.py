import importlib
import inspect


def add_var(context, name, val):
    if "vars" not in context:
        context.vars = {}

    if name in context.vars:
        raise ValueError(f"variable {name} cannot be overwritten")

    context.vars[name] = val


def get_var(context, name):
    if "vars" not in context or name not in context.vars:
        raise ValueError(f"variable {name} has not been set")

    return context.vars[name]


def has_var(context, name):
    return "vars" in context and name in context.vars


def _check_func_arguments(context, func):
    """
    Checks whether all required arguments of a function are available in the context's variables.

    :return: None if the function cannot be called with the given variables,
        names of available args, varargs, kwargs, and varkw - otherwise.
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

    required_kwargs = [kwarg for kwarg in kwargs if kwarg not in spec.kwonlydefaults]
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


def _get_argument_values(context, args, varargs, kwargs, varkw):
    args_vals = [get_var(context, arg) for arg in args]
    varargs_vals = get_var(context, varargs) if varargs else None
    kwargs_vals = {kwarg: get_var(context, kwarg) for kwarg in kwargs}
    varkw_vals = get_var(context, varkw) if varkw else {}

    return args_vals, varargs_vals, kwargs_vals, varkw_vals


def _assign_results(context, results, result_vars):
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


def run_func(context, func_name, module, result_vars):
    module = importlib.import_module(module)
    func = getattr(module, func_name)

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
