"""
`__main__.py` is the file that gets executed when the rendercl package itself is
invoked directly from the command line with `python -m rendercl`. That's why we
have it here so the CLI can be invoked that way, mirroring rendercv's own
`__main__.py`.
"""

from .cli.entry_point import entry_point

if __name__ == "__main__":
    entry_point()
