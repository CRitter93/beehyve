from typing import Mapping, Sequence, Tuple

from behave import register_type, when
from behave.runner import Context

from beehyve.steps import types
from beehyve.utils.functions import execute_function, execute_function_from_context

register_type(Result=types.parse_func_result)
register_type(Module=types.parse_module)
register_type(Arguments=types.parse_args)
register_type(KWArguments=types.parse_kwargs)


@when(
    "the function {func_name:w} of module {module:Module} is called "
    "writing the results to {result_names:Result}"
)
@when("{result_names:Result} <- {module:Module}.{func_name:w}()")
def step_execute_function_from_context(
    context: Context, func_name: str, module: str, result_names: Tuple[str, ...]
):
    """Executes an arbitrary python function using the variables in the context.
    For more details see :py:func:`execute_function_from_context`.

    :param context: the current context
    :param func_name: the name of the function to execute
    :param module: the module where the function can be found,
        i.e., you should be able to import <func_name> from <module>
    :param result_names: a tuple of variable names
        to which the result(s) of the function should be assigned
    """
    execute_function_from_context(
        context=context, func_name=func_name, module=module, result_names=result_names
    )


@when("the function {func_name:w} of module {module:Module} is called")
@when("{module:Module}.{func_name:w}() is called")
def step_execute_function_wo_return_from_context(
    context: Context, func_name: str, module: str
):
    """Executes an arbitrary python function that has not return
    using the variables in the context.
    For more details see :py:func:`execute_function_from_context`.

    :param context: the current context
    :param func_name: the name of the function to execute
    :param module: the module where the function can be found,
        i.e., you should be able to import <func_name> from <module>
    """
    execute_function_from_context(context=context, func_name=func_name, module=module)


@when(
    "the function {func_name:w} of module {module:Module} is called "
    "using arguments {args:Arguments} and keyword arguments {kwargs:KWArguments} "
    "writing the results to {result_names:Result}"
)
@when(
    "{result_names:Result} <- {module:Module}.{func_name:w}({args:Arguments}{kwargs:KWArguments})"
)
def step_execute_function_with_given_variables(
    context: Context,
    func_name: str,
    module: str,
    result_names: Tuple[str, ...],
    args: Sequence[str],
    kwargs: Mapping[str, str],
):
    """Executes an arbitrary python function
    using the given variables names as args and kwargs.
    For more details see :py:func:`execute_function`.

    :param context: the current context
    :param func_name: the name of the function to execute
    :param module: the module where the function can be found,
        i.e., you should be able to import <func_name> from <module>
    :param result_names: a tuple of variable names
        to which the result(s) of the function should be assigned
    :param args: variable names of the variables
        which should be used as arguments to the function
    :param kwargs: a mapping of function kwarg to variable name
        which should be passed to the function
    """
    execute_function(
        context=context,
        func_name=func_name,
        module=module,
        result_names=result_names,
        args=args,
        kwargs=kwargs,
    )


@when(
    "the function {func_name:w} of module {module:Module} is called "
    "using arguments {args:Arguments} and keyword arguments {kwargs:KWArguments}"
)
@when("{module:Module}.{func_name:w}({args:Arguments}{kwargs:KWArguments}) is called")
def step_execute_function_with_given_variables_wo_return(
    context: Context,
    func_name: str,
    module: str,
    args: Sequence[str],
    kwargs: Mapping[str, str],
):
    """Executes an arbitrary python function that has not return
    using the given variables names as args and kwargs.
    For more details see :py:func:`execute_function`.

    :param context: the current context
    :param func_name: the name of the function to execute
    :param module: the module where the function can be found,
        i.e., you should be able to import <func_name> from <module>
    :param args: variable names of the variables
        which should be used as arguments to the function
    :param kwargs: a mapping of function kwarg to variable name
        which should be passed to the function
    """
    execute_function(
        context=context,
        func_name=func_name,
        module=module,
        args=args,
        kwargs=kwargs,
    )
