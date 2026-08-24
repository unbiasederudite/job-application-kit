"""Resolve OUTPUT_FOLDER/NAME/date placeholders in a settings path template.

Mirrors rendercv's own renderer/path_resolver.py and its file_path_placeholders,
just against the letter's sender name and resolved settings.current_date instead
of a CV's name/date.
"""
import datetime
import pathlib


def name_placeholders(name: str) -> dict[str, str]:
    return {
        "NAME": name,
        "NAME_IN_SNAKE_CASE": name.replace(" ", "_"),
        "NAME_IN_LOWER_SNAKE_CASE": name.replace(" ", "_").lower(),
        "NAME_IN_UPPER_SNAKE_CASE": name.replace(" ", "_").upper(),
        "NAME_IN_KEBAB_CASE": name.replace(" ", "-"),
        "NAME_IN_LOWER_KEBAB_CASE": name.replace(" ", "-").lower(),
        "NAME_IN_UPPER_KEBAB_CASE": name.replace(" ", "-").upper(),
    }


def date_placeholders(date: datetime.date) -> dict[str, str]:
    return {
        "MONTH_NAME": f"{date:%B}",
        "MONTH_ABBREVIATION": f"{date:%b}",
        "MONTH": str(date.month),
        "MONTH_IN_TWO_DIGITS": f"{date.month:02d}",
        "DAY": str(date.day),
        "DAY_IN_TWO_DIGITS": f"{date.day:02d}",
        "YEAR": str(date.year),
        "YEAR_IN_TWO_DIGITS": str(date.year)[-2:],
    }


def resolve_path(
    template: str,
    *,
    name: str,
    date: datetime.date,
    output_folder: pathlib.Path,
    base_dir: pathlib.Path,
) -> pathlib.Path:
    """Substitute OUTPUT_FOLDER and name/date placeholders in a path template.

    `output_folder` is resolved relative to `base_dir` (the input YAML's own
    directory) unless it's already absolute — same rule rendercv applies to
    its own `PlannedPathRelativeToInput` fields.
    """
    placeholders = {**name_placeholders(name), **date_placeholders(date)}
    resolved_output_folder = (
        output_folder if output_folder.is_absolute() else base_dir / output_folder
    )

    # Longest keys first so "NAME_IN_SNAKE_CASE" is matched before the shorter
    # "NAME" substring inside it.
    ordered_keys = sorted(placeholders, key=len, reverse=True)

    parts: list[str] = []
    for part in pathlib.Path(template).parts:
        if part == "OUTPUT_FOLDER":
            parts.extend(resolved_output_folder.parts)
            continue
        for key in ordered_keys:
            part = part.replace(key, placeholders[key])
        parts.append(part)

    resolved = pathlib.Path(*parts)
    resolved.parent.mkdir(parents=True, exist_ok=True)
    return resolved
