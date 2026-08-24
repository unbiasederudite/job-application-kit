#!/usr/bin/env python3
"""Report how many PDF rows each cv.yaml highlight and skills line takes up,
and the total page count. Read-only: never edits anything.

Usage:
    uv run python skills/curriculum-vitae/scripts/page_usage.py <path-to-pdf>

Every entry's `highlights` and every `cv.sections.skills` line (label +
details) is located in the rendered PDF by exact text match, and the number
of physical PDF rows it took is the row count. Rows come straight from the
PDF's own character positions.

Text is reduced to lowercase letters and digits only before comparing, so
whitespace, punctuation, quote style, dashes, and line-wrap hyphenation
never need special handling - there's nothing left in the comparison for
them to affect.
"""
import re
import sys
import unicodedata
from pathlib import Path

import pdfplumber
from ruamel.yaml import YAML


def normalize(text):
    text = re.sub(r"\(cid:\d+\)", "", text)  # unmapped glyph, not real text
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    return re.sub(r"[^a-zA-Z0-9]", "", text).lower()


def strip_markdown(text):
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)  # link -> link text
    return text.replace("**", "").replace("*", "")


DEFAULT_ONE_LINE_TEMPLATE = "**LABEL:** DETAILS"  # rendercv's own built-in default


def load_expected_items(cv_yaml_path: Path):
    yaml = YAML(typ="safe")
    data = yaml.load(cv_yaml_path.read_text(encoding="utf-8"))
    sections = (data.get("cv") or {}).get("sections") or {}

    templates = ((data.get("design") or {}).get("templates") or {})
    one_line_template = (
        (templates.get("one_line_entry") or {}).get("main_column") or DEFAULT_ONE_LINE_TEMPLATE
    )

    items = []
    for section_name, entries in sections.items():
        if section_name == "skills":
            for entry in entries or []:
                text = one_line_template.replace("LABEL", entry.get("label") or "").replace(
                    "DETAILS", entry.get("details") or ""
                )
                items.append({"kind": "skill", "text": text})
            continue
        for entry in entries or []:
            for highlight in entry.get("highlights") or []:
                items.append({"kind": "bullet", "text": highlight})

    for item in items:
        item["norm"] = normalize(strip_markdown(item["text"]))
    return items


def extract_rows(pdf_path: Path):
    """Return (rows, page_count). rows is a flat list of {page, text}, one
    per physical line, in reading order. Line grouping is pdfplumber's own
    extract_text_lines(), not a hand-rolled y-position rule."""
    rows = []
    with pdfplumber.open(pdf_path) as pdf:
        page_count = len(pdf.pages)
        for page_index, page in enumerate(pdf.pages, start=1):
            for line in page.extract_text_lines():
                if line["text"].strip():
                    rows.append({"page": page_index, "text": line["text"]})
    return rows, page_count


def match_items(rows, items):
    """For each item, find its starting row anywhere among rows not already
    claimed by another item (no assumption that cv.yaml's order matches the
    PDF's row order), then keep appending the following rows until they
    spell it out. A row's own wrapped continuation is always the next row
    in reading order, so growth itself stays a simple forward walk."""
    row_norms = [normalize(r["text"]) for r in rows]
    claimed = [False] * len(rows)
    results = []

    for item in items:
        target = item["norm"]
        start = next(
            (
                i
                for i in range(len(rows))
                if not claimed[i]
                and row_norms[i]
                and (target.startswith(row_norms[i]) or row_norms[i].startswith(target))
            ),
            None,
        )

        if start is None:
            results.append({**item, "found": False, "row_count": 0, "page": None})
            continue

        buf = row_norms[start]
        end = start
        while len(buf) < len(target) and end + 1 < len(rows):
            end += 1
            buf += row_norms[end]

        found = buf == target
        if found:
            for i in range(start, end + 1):
                claimed[i] = True

        results.append(
            {
                **item,
                "found": found,
                "row_count": end - start + 1,
                "page": rows[start]["page"],
            }
        )

    return results


def main():
    if len(sys.argv) != 2:
        print("Usage: uv run python skills/curriculum-vitae/scripts/page_usage.py <path-to-pdf>")
        sys.exit(1)

    pdf_path = Path(sys.argv[1])
    if not pdf_path.exists():
        print(f"PDF not found: {pdf_path}")
        sys.exit(1)

    cv_yaml_path = pdf_path.parent.parent / "cv.yaml"
    if not cv_yaml_path.exists():
        print(f"Could not find source cv.yaml at expected path: {cv_yaml_path}")
        sys.exit(1)

    items = load_expected_items(cv_yaml_path)
    rows, page_count = extract_rows(pdf_path)
    results = match_items(rows, items)

    print(f"Pages: {page_count}\n")
    for r in results:
        display_text = strip_markdown(r["text"])
        preview = display_text[:70] + ("..." if len(display_text) > 70 else "")
        if not r["found"]:
            print(f"[NOT FOUND] {r['kind']}: {preview}")
            continue
        print(f"{r['kind']}: {r['row_count']} row(s), page {r['page']} - {preview}")


if __name__ == "__main__":
    main()
