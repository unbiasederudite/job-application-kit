import pathlib
from dataclasses import dataclass

import rich.console
import rich.live
import rich.panel
import typer

from ...exception import RenderCLUserError


class ProgressPanel(rich.live.Live):
    """Live-updating terminal panel showing render progress with timing.

    Mirrors rendercv's own cli/render_command/progress_panel.py: one Live
    instance is opened for the whole CLI command (including the entire
    --watch session) and every step calls `.update()` on it, redrawing the
    same panel in place instead of printing a new line per render.
    """

    def __init__(self, quiet: bool = False):
        self.completed_steps: list[CompletedStep] = []
        super().__init__(
            rich.panel.Panel(
                "...",
                title="Rendering your cover letter...",
                title_align="left",
                border_style="bright_black",
            ),
            console=rich.console.Console(quiet=quiet),
            refresh_per_second=4,
        )

    def update_progress(self, time_took: str, message: str, paths: list[pathlib.Path]) -> None:
        self.completed_steps.append(CompletedStep(time_took, message, paths))
        self.print_progress_panel(title="Rendering your cover letter...")

    def finish_progress(self) -> None:
        self.print_progress_panel(title="Your cover letter is ready")
        self.completed_steps.clear()

    def print_progress_panel(self, title: str) -> None:
        lines: list[str] = []
        for step in self.completed_steps:
            paths_str = ""
            if step.paths:
                try:
                    paths = [path.relative_to(pathlib.Path.cwd()) for path in step.paths]
                except ValueError:
                    paths = step.paths
                paths_str = "; ".join(f"./{path}" for path in paths)

            timing = f"[bold green]{step.timing_ms + ' ms':<8}[/bold green]"
            message = step.message + (": " if paths_str else ".")
            paths_display = f"[purple]{paths_str}[/purple]" if paths_str else ""
            lines.append(f"[green]✓[/green] {timing} {message:<26} {paths_display}")

        content = "\n".join(lines) if lines else "Rendering..."

        self.update(
            rich.panel.Panel(content, title=title, title_align="left", border_style="bright_black")
        )

    def print_user_error(self, user_error: RenderCLUserError) -> None:
        self.clear()
        self.update(
            rich.panel.Panel(
                user_error.message or "An unknown error occurred.",
                title="[bold red]Error[/bold red]",
                title_align="left",
                border_style="bold red",
            )
        )
        raise typer.Exit(code=1)

    def clear(self) -> None:
        self.completed_steps.clear()
        self.update("")


@dataclass
class CompletedStep:
    timing_ms: str
    message: str
    paths: list[pathlib.Path]
