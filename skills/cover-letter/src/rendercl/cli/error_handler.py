import functools
from collections.abc import Callable

import rich.panel
import typer
from rich import print

from ..exception import RenderCLUserError


def handle_user_errors[T, **P](function: Callable[P, None]) -> Callable[P, None]:
    """Decorator that catches user errors and displays friendly messages without stack traces.

    Mirrors rendercv's own cli/error_handler.py: CLI commands should show clean
    error messages for expected user errors (invalid YAML, missing files) while
    letting genuinely unexpected errors (a bug) still raise with their real
    traceback.
    """

    @functools.wraps(function)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> None:
        try:
            return function(*args, **kwargs)
        except RenderCLUserError as e:
            if e.message:
                print(
                    rich.panel.Panel(
                        e.message,
                        title="[bold red]Error[/bold red]",
                        title_align="left",
                        border_style="bold red",
                    )
                )
            raise typer.Exit(code=1) from e

    return wrapper
