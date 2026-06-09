import re

from html import unescape


TAG_PATTERN = re.compile(r"<[^>]*>")

WHITESPACE_PATTERN = re.compile(r"\s+")


def sanitize_text(
    value: str | None
):

    if value is None:

        return None

    cleaned = unescape(value)

    cleaned = TAG_PATTERN.sub(
        "",
        cleaned
    )

    cleaned = WHITESPACE_PATTERN.sub(
        " ",
        cleaned
    ).strip()

    return cleaned


def require_clean_text(
    value: str,
    field_name: str
):

    cleaned = sanitize_text(
        value
    )

    if not cleaned:

        raise ValueError(
            f"{field_name} is required"
        )

    return cleaned
