import pathlib
import time
from collections.abc import Callable
from typing import TypeVar

from ...exception import RenderCLUserError
from ...renderer.typst import generate_pdf, generate_typst, load_yaml, resolve_output_paths
from .progress_panel import ProgressPanel

T = TypeVar("T")


def timed_step(
    message: str, progress_panel: ProgressPanel, func: Callable[..., T], *args, **kwargs
) -> T:
    """Execute function, measure timing, and update the progress panel with the result."""
    start = time.perf_counter()
    result = func(*args, **kwargs)
    end = time.perf_counter()
    timing_ms = f"{(end - start) * 1000:.0f}"

    paths = [result] if isinstance(result, pathlib.Path) else []
    if paths:
        progress_panel.update_progress(time_took=timing_ms, message=message, paths=paths)

    return result


def run_rendercl(
    cover_letter_yaml: pathlib.Path,
    progress: ProgressPanel,
    output_folder: pathlib.Path | None = None,
) -> None:
    """Run the full render pipeline with per-step timing in `progress`.

    Mirrors rendercv's own cli/render_command/run_rendercv.py: each step
    (load, Typst, PDF) is timed and pushed into the same live panel, and a
    RenderCLUserError anywhere in the pipeline is shown as a clean error
    panel instead of a traceback.
    """
    try:
        data = timed_step("Validated the input file", progress, load_yaml, cover_letter_yaml)
        typst_path, pdf_path = resolve_output_paths(data, cover_letter_yaml, output_folder)

        timed_step("Generated Typst", progress, generate_typst, data, typst_path)
        timed_step("Generated PDF", progress, generate_pdf, typst_path, pdf_path)

        progress.finish_progress()
    except RenderCLUserError as e:
        progress.print_user_error(e)
