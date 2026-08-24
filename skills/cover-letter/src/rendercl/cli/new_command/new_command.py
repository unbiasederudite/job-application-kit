import pathlib
from typing import Annotated

import rich.panel
import typer
from rich import print

from ...schema.sample_generator import create_sample_cover_letter_yaml
from ..app import app
from ..error_handler import handle_user_errors


@app.command(
    name="new",
    help=(
        'Scaffold a new cover letter YAML. Example: [yellow]rendercl new "John'
        ' Doe"[/yellow]. Details: [cyan]rendercl new --help[/cyan]'
    ),
)
@handle_user_errors
def cli_command_new(
    full_name: Annotated[str, typer.Argument(help="Your full name")],
):
    destination = pathlib.Path(f"{full_name.replace(' ', '_')}_CL.yaml")

    if destination.exists():
        input_file_created = False
    else:
        create_sample_cover_letter_yaml(file_path=destination, full_name=full_name)
        input_file_created = True

    # Mirrors rendercv's own "Get started" panel from cli/new_command/new_command.py
    # (minus its separate "Useful Links" welcome panel).
    lines: list[str] = []

    if input_file_created:
        lines.append(
            f"[green]✓[/green] Created your YAML input file: [purple]./{destination}[/purple]"
        )
    else:
        lines.append(
            f"Your YAML input file already exists: [purple]./{destination}[/purple]"
        )

    lines.append("")
    lines.append("Next steps:")
    lines.append("  1. Fill in the recipient and body paragraphs")
    lines.append(f"  2. Run: [cyan]rendercl render {destination}[/cyan]")

    print(
        rich.panel.Panel(
            "\n".join(lines),
            title="Get started",
            title_align="left",
            border_style="bright_black",
        )
    )
