"""Convert a loaded cover letter dict into the context values the Typst template needs."""
import datetime

import phonenumbers

from ..exception import RenderCLUserError

_PHONE_NUMBER_FORMATS = {
    "national": phonenumbers.PhoneNumberFormat.NATIONAL,
    "international": phonenumbers.PhoneNumberFormat.INTERNATIONAL,
    "e164": phonenumbers.PhoneNumberFormat.E164,
}

_TYPST_ESCAPE = str.maketrans(
    {
        "\\": "\\\\",
        "#": "\\#",
        "@": "\\@",
        "$": "\\$",
        "<": "\\<",
    }
)

def escape_typst(text: str) -> str:
    return str(text).translate(_TYPST_ESCAPE)


def address_block(*fields: str) -> str:
    """Join header fields (each possibly multi-line, any possibly blank, each
    either plain text or already-built Typst markup such as a `#link(...)`
    call) into one Typst line-break-separated block, dropping blank lines."""
    lines = []
    for field in fields:
        if not field:
            continue
        lines.extend(line.strip() for line in str(field).strip().splitlines() if line.strip())
    return " \\\n".join(lines)


def escape_lines(text) -> str:
    """Escape a plain (non-link) header field line by line, for use as an
    address_block() field alongside already-built Typst markup."""
    if not text:
        return ""
    return "\n".join(
        escape_typst(line.strip()) for line in str(text).strip().splitlines() if line.strip()
    )


def typst_link(url: str, label: str) -> str:
    """A clickable Typst link, e.g. `#link("tel:+1-555-123-4567")[(555) 123-4567]`."""
    return f'#link("{url}")[{escape_typst(label)}]'


def resolve_current_date(data: dict) -> datetime.date:
    """Resolve settings.current_date: a blank value, the literal "today", or a
    YYYY-MM-DD date.

    Mirrors rendercv's own settings.current_date field exactly (typed
    `datetime.date | Literal["today"]`, default "today"). ruamel's safe
    loader auto-parses an unquoted `2026-08-18` into a real `datetime.date`
    already; a quoted string needs parsing here instead.
    """
    raw = (data.get("settings") or {}).get("current_date")

    if raw is None:
        return datetime.date.today()
    if isinstance(raw, datetime.date):
        return raw

    text = str(raw).strip()
    if not text or text.lower() == "today":
        return datetime.date.today()

    try:
        return datetime.date.fromisoformat(text)
    except ValueError:
        raise RenderCLUserError(
            f'Invalid settings.current_date {raw!r}: use YYYY-MM-DD, "today", or leave it blank.'
        ) from None


def format_date(date: datetime.date) -> str:
    """Textual form, e.g. "18 August 2026" — day-month-year with the month
    spelled out, the internationally unambiguous convention (not tied to any
    one country's convention, unlike US-style "August 18, 2026"). Built
    manually rather than via strftime to avoid its platform-specific
    no-leading-zero day codes (%-d on Linux/Mac, %#d on Windows)."""
    return f"{date.day} {date:%B} {date.year}"


def margins_literal(margins) -> str:
    """Render design.page.margins as a raw (unquoted) Typst value.

    Mirrors letterloom's own `margins` parameter exactly: `auto` (the default),
    a single length applied to all sides (e.g. `1in`), or a dictionary of
    per-side lengths (any of top/bottom/left/right/x/y/rest, same shorthand
    rules letterloom uses for page margins).
    """
    if margins is None:
        return "auto"
    if isinstance(margins, dict):
        pairs = ", ".join(f"{side}: {value}" for side, value in margins.items())
        return f"({pairs})"

    text = str(margins).strip()
    return "auto" if not text or text.lower() == "auto" else text


def _parse_phone(raw: str) -> phonenumbers.PhoneNumber:
    try:
        return phonenumbers.parse(raw, None)
    except phonenumbers.NumberParseException as e:
        raise RenderCLUserError(
            f"Invalid sender.phone {raw!r}: {e}. Include the country code, e.g. +1 555-123-4567."
        ) from None


def phone_link(raw: str, phone_number_format: str) -> str:
    """A clickable `tel:` link for sender.phone, displayed per design.phone_number_format.

    Mirrors rendercv's own `design.header.connections.phone_number_format`
    exactly (`national` — the default —, `international`, or `E164`) for the
    *displayed* text, using the same `phonenumbers` library rendercv uses.
    The `tel:` URI itself always uses RFC3966 (e.g. `tel:+1-555-123-4567`),
    independent of the display format, same as rendercv's own phone links.
    """
    key = (phone_number_format or "national").strip().lower()
    try:
        display_format = _PHONE_NUMBER_FORMATS[key]
    except KeyError:
        raise RenderCLUserError(
            f'Invalid design.phone_number_format {phone_number_format!r}: use'
            ' "national", "international", or "E164".'
        ) from None

    parsed = _parse_phone(raw)
    label = phonenumbers.format_number(parsed, display_format)
    url = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.RFC3966)
    return typst_link(url, label)


def email_link(email: str) -> str:
    """A clickable `mailto:` link for sender.email."""
    return typst_link(f"mailto:{email}", email)


def build_context(data: dict) -> dict:
    letter = data.get("cl") or {}
    design = data.get("design") or {}
    typography = design.get("typography") or {}
    page = design.get("page") or {}

    sender = letter.get("sender") or {}
    recipient = letter.get("recipient") or {}
    body_paragraphs = letter.get("body") or []

    from_name = escape_typst(sender.get("name") or "")

    phone = sender.get("phone")
    phone_field = phone_link(str(phone), design.get("phone_number_format")) if phone else None

    email = sender.get("email")
    email_field = email_link(str(email).strip()) if email else None

    recipient_name = recipient.get("name") or ""
    recipient_title = recipient.get("title") or ""
    if not recipient_name and not recipient_title:
        # Only stand in with a generic "Hiring Manager" when there's no way to
        # identify the recipient at all — a real name without a title (or vice
        # versa) is specific enough on its own and shouldn't get padded with it.
        recipient_title = "Hiring Manager"

    return {
        "from_name": from_name,
        "from_address_lines": address_block(
            escape_lines(sender.get("address")), phone_field, email_field
        ),
        "to_name": escape_typst(recipient_name),
        "to_address_lines": address_block(
            escape_lines(recipient_title),
            escape_lines(recipient.get("company")),
            escape_lines(recipient.get("address")),
        ),
        "date": escape_typst(format_date(resolve_current_date(data))),
        "salutation": escape_typst(letter.get("salutation") or "Dear Hiring Manager,"),
        "closing": escape_typst(letter.get("closing") or "Sincerely,"),
        "body": "\n\n".join(escape_typst(p) for p in body_paragraphs),
        # Typst string literal (quoted in the template) — needs escaping like any text.
        "font_family": escape_typst(typography.get("font_family") or "New Computer Modern"),
        # Typst dimension literal (e.g. `11pt`, bare, not quoted) — not text, don't escape.
        "font_size": str(typography.get("font_size") or "11pt"),
        # Typst string literal (quoted in the template) — needs escaping like any text.
        "paper_size": escape_typst(page.get("size") or "a4"),
        # Typst value (auto / length / dictionary, bare, not quoted) — not text, don't escape.
        "margins": margins_literal(page.get("margins")),
    }
