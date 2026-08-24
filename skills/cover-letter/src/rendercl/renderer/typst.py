"""Fill the Typst template via Jinja2, then compile it to PDF with the `typst` package."""
import pathlib

import jinja2
import typst
from ruamel.yaml import YAML
from ruamel.yaml.error import YAMLError

from ..exception import RenderCLUserError
from . import path_resolver
from .templater import build_context, resolve_current_date

TEMPLATE_DIR = pathlib.Path(__file__).parent / "templates" / "typst"
TEMPLATE_NAME = "CoverLetter.j2.typ"

_yaml = YAML(typ="safe")


def load_yaml(path: pathlib.Path) -> dict:
    if not path.exists():
        raise RenderCLUserError(f"No such file: {path}")
    try:
        with path.open(encoding="utf-8") as f:
            return _yaml.load(f) or {}
    except YAMLError as e:
        raise RenderCLUserError(f"Invalid YAML in {path}: {e}") from e


def generate_typst(data: dict, typst_path: pathlib.Path) -> pathlib.Path:
    context = build_context(data)

    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(TEMPLATE_DIR),
        trim_blocks=True,
        keep_trailing_newline=True,
    )
    typst_source = env.get_template(TEMPLATE_NAME).render(**context)

    typst_path.parent.mkdir(parents=True, exist_ok=True)
    typst_path.write_text(typst_source, encoding="utf-8")
    return typst_path


def generate_pdf(typst_path: pathlib.Path, pdf_path: pathlib.Path) -> pathlib.Path:
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        typst.compile(str(typst_path), output=str(pdf_path))
    except typst.TypstError as e:
        raise RenderCLUserError(f"Typst compilation failed: {e}") from e
    return pdf_path


def resolve_output_paths(
    data: dict,
    cover_letter_yaml: pathlib.Path,
    output_folder: pathlib.Path | None = None,
) -> tuple[pathlib.Path, pathlib.Path]:
    """Resolve the `.typ` and `.pdf` output paths for `data`.

    Mirrors rendercv's own `--output-folder` behavior: point at a folder, not a
    filename, and the PDF/Typst files are auto-named from the letter's own
    `cl.sender.name` via `settings.render_command.pdf_path`/`typst_path`
    templates (default `OUTPUT_FOLDER/NAME_IN_SNAKE_CASE_CL.pdf`/`.typ`), the
    same placeholder system rendercv uses for `cv.yaml`.

    Precedence for `output_folder`, matching rendercv's CLI-overrides-YAML rule:
    the `--output-folder` CLI flag, if given, wins; otherwise `settings.render_
    command.output_folder` from the YAML itself; otherwise `rendercl_output/`,
    resolved next to the input file — same default name rendercv uses for its
    own `rendercv_output/` (see .gitignore).

    Returns:
        (typst_path, pdf_path)
    """
    render_command = (data.get("settings") or {}).get("render_command") or {}

    if output_folder is None:
        configured = render_command.get("output_folder")
        output_folder = (
            pathlib.Path(configured) if configured else pathlib.Path("rendercl_output")
        )

    name = (
        ((data.get("cl") or {}).get("sender") or {}).get("name") or "Cover_Letter"
    )
    date = resolve_current_date(data)
    base_dir = cover_letter_yaml.parent

    pdf_template = render_command.get("pdf_path") or "OUTPUT_FOLDER/NAME_IN_SNAKE_CASE_CL.pdf"
    typst_template = render_command.get("typst_path") or "OUTPUT_FOLDER/NAME_IN_SNAKE_CASE_CL.typ"

    output_pdf = path_resolver.resolve_path(
        pdf_template, name=name, date=date, output_folder=output_folder, base_dir=base_dir
    )
    typst_path = path_resolver.resolve_path(
        typst_template, name=name, date=date, output_folder=output_folder, base_dir=base_dir
    )

    return typst_path, output_pdf


def render_cover_letter(
    cover_letter_yaml: pathlib.Path,
    output_folder: pathlib.Path | None = None,
) -> pathlib.Path:
    """Render `cover_letter_yaml` to a PDF inside `output_folder`, also writing
    out the intermediate `.typ` file as a real, persistent output alongside it —
    matching rendercv's own default behavior of keeping both files.
    """
    data = load_yaml(cover_letter_yaml)
    typst_path, output_pdf = resolve_output_paths(data, cover_letter_yaml, output_folder)

    generate_typst(data, typst_path)
    generate_pdf(typst_path, output_pdf)

    return output_pdf
