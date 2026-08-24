"""Generate a realistic sample cover letter YAML, the same way rendercv's own
schema/sample_generator.py builds a sample CV: load real example content and
re-dump it with the requested name, rather than templating comment-heavy
placeholder text.
"""
import io
import pathlib
from typing import overload

from ruamel.yaml import YAML

SAMPLE_CONTENT_PATH = pathlib.Path(__file__).parent / "sample_content.yaml"

_yaml = YAML()
_yaml.width = 9999
_yaml.indent(mapping=2, sequence=4, offset=2)


@overload
def create_sample_cover_letter_yaml(*, file_path: None, full_name: str) -> str: ...
@overload
def create_sample_cover_letter_yaml(
    *, file_path: pathlib.Path, full_name: str
) -> None: ...
def create_sample_cover_letter_yaml(
    *, file_path: pathlib.Path | None = None, full_name: str
) -> str | None:
    """Build sample cover letter content with `full_name` as the sender.

    Args:
        file_path: Optional path to write the YAML to.
        full_name: Person's full name, set as `cl.sender.name`.

    Returns:
        YAML string if file_path is None, otherwise None after writing the file.
    """
    with SAMPLE_CONTENT_PATH.open(encoding="utf-8") as f:
        data = _yaml.load(f)

    data["cl"]["sender"]["name"] = full_name

    with io.StringIO() as stream:
        _yaml.dump(data, stream)
        yaml_string = stream.getvalue()

    if file_path is not None:
        file_path.write_text(yaml_string, encoding="utf-8")
        return None
    return yaml_string
