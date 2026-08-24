import contextlib
import pathlib
import time
from collections.abc import Callable

import typer
import watchdog.events
import watchdog.observers


class EventHandler(watchdog.events.FileSystemEventHandler):
    """Trigger a callback when the watched file is modified.

    Args:
        function: Callback to invoke on modification.
        watched_file: Absolute path string of the file to monitor.
    """

    def __init__(self, function: Callable[[], None], watched_file: str) -> None:
        super().__init__()
        self.function = function
        self.watched_file = watched_file

    def on_modified(
        self,
        event: watchdog.events.DirModifiedEvent | watchdog.events.FileModifiedEvent,
    ) -> None:
        if event.src_path != self.watched_file:
            return
        with contextlib.suppress(typer.Exit):
            self.function()


def run_function_if_file_changes(file_path: pathlib.Path, function: Callable[[], None]) -> None:
    """Watch one file and re-run function when it's modified.

    Why:
        Watch mode lets users edit the cover letter YAML and see the
        re-rendered PDF without re-running `rendercl render` by hand each time.

    Args:
        file_path: File path to watch.
        function: Zero-argument callback to invoke on file change.
    """
    watched_file = str(file_path.absolute())

    # Watch the parent directory (file-level watching is unreliable across platforms)
    event_handler = EventHandler(function, watched_file)

    observer = watchdog.observers.Observer()
    observer.schedule(event_handler, str(file_path.absolute().parent), recursive=False)
    observer.start()

    # Run immediately for the first render:
    with contextlib.suppress(typer.Exit):
        function()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
