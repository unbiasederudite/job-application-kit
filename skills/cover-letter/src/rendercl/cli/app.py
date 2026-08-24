import typer

app = typer.Typer(
    rich_markup_mode="rich",
    context_settings={"help_option_names": ["-h", "--help"]},
    help="rendercl renders a cover_letter.yaml into a PDF via a Typst letterloom template.",
)

# Import command modules so they register themselves on `app` (mirrors rendercv's
# cli/app.py pattern, minus its PyPI-facing auto-discovery/version-check machinery,
# which doesn't apply to an internal, unpublished tool).
from .new_command import new_command  # NOQA: E402, F401
from .render_command import render_command  # NOQA: E402, F401
