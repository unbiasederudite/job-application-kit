import pathlib
from typing import Annotated

import typer

from ..app import app
from ..error_handler import handle_user_errors
from .progress_panel import ProgressPanel
from .run_rendercl import run_rendercl
from .watcher import run_function_if_file_changes


@app.command(
    name="render",
    help=(
        "Render a cover letter YAML into a PDF. Example: [yellow]rendercl render"
        " John_Doe_CL.yaml[/yellow]. Details: [cyan]rendercl render --help[/cyan]"
    ),
)
@handle_user_errors
def cli_command_render(
    cover_letter_yaml: Annotated[
        pathlib.Path, typer.Argument(help="The cover letter YAML input file.")
    ],
    output_folder: Annotated[
        pathlib.Path | None,
        typer.Option(
            "--output-folder",
            "-o",
            help=(
                "Base output folder. The PDF is auto-named <Sender_Name>_CL.pdf"
                " from the letter's own sender.name (default: rendercl_output/,"
                " next to the input file)."
            ),
        ),
    ] = None,
    watch: Annotated[
        bool,
        typer.Option(
            "--watch",
            "-w",
            help="Re-render automatically whenever the input YAML file changes.",
        ),
    ] = False,
):
    with ProgressPanel() as progress:
        if watch:
            run_function_if_file_changes(
                cover_letter_yaml,
                lambda: run_rendercl(cover_letter_yaml, progress, output_folder),
            )
        else:
            run_rendercl(cover_letter_yaml, progress, output_folder)
