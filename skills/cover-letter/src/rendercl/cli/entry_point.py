"""Entry point for the rendercl CLI (the target `pyproject.toml`'s [project.scripts] points to)."""

from .app import app


def entry_point() -> None:
    app()
