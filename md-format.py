#!/usr/bin/env python3
"""
Format Markdown files.

1. Runs mdformat
2. Reflows normal paragraphs to LINE_LENGTH

Usage:
    python format_md.py .
    python format_md.py docs/
    python format_md.py README.md
"""

from __future__ import annotations

import argparse
import pathlib
import re
import textwrap

import mdformat

LINE_LENGTH = 120

LIST_RE = re.compile(r"^\s*(?:[-+*]|\d+\.)\s")
TABLE_RE = re.compile(r"^\s*\|")
HEADER_RE = re.compile(r"^\s*#")
QUOTE_RE = re.compile(r"^\s*>")
HTML_RE = re.compile(r"^\s*<")
HRULE_RE = re.compile(r"^\s*([-*_])(?:\s*\1){2,}\s*$")


def wrap_paragraph(lines: list[str]) -> list[str]:
    """Wrap a normal paragraph."""

    if not lines:
        return []

    text = " ".join(line.strip() for line in lines)

    return textwrap.fill(
        text,
        width=LINE_LENGTH,
        break_long_words=False,
        break_on_hyphens=False,
    ).splitlines()


def format_file(path: pathlib.Path) -> None:
    """Format a single markdown file."""

    original = path.read_text(encoding="utf-8")

    # ------------------------------------------------------------------
    # Step 1 : mdformat
    # ------------------------------------------------------------------

    try:
        formatted = mdformat.text(original)
    except Exception as exc:
        print(f"Failed to format {path}: {exc}")
        return

    lines = formatted.splitlines()

    output: list[str] = []
    paragraph: list[str] = []

    in_yaml = False
    in_code = False

    def flush():
        nonlocal paragraph
        if paragraph:
            output.extend(wrap_paragraph(paragraph))
            paragraph = []

    for i, line in enumerate(lines):
        stripped = line.strip()

        # ---------------- YAML Front Matter ----------------

        if i == 0 and stripped == "---":
            flush()
            in_yaml = True
            output.append(line)
            continue

        if in_yaml:
            output.append(line)
            if stripped == "---":
                in_yaml = False
            continue

        # ---------------- Code Fence ----------------

        if stripped.startswith("```") or stripped.startswith("~~~"):
            flush()
            in_code = not in_code
            output.append(line)
            continue

        if in_code:
            output.append(line)
            continue

        # ---------------- Blank Line ----------------

        if stripped == "":
            flush()
            output.append("")
            continue

        # ---------------- Preserve Markdown Blocks ----------------

        if (
            HEADER_RE.match(line)
            or LIST_RE.match(line)
            or TABLE_RE.match(line)
            or QUOTE_RE.match(line)
            or HTML_RE.match(line)
            or HRULE_RE.match(line)
        ):
            flush()
            output.append(line)
            continue

        # ---------------- Normal Paragraph ----------------

        paragraph.append(line)

    flush()

    result = "\n".join(output) + "\n"

    if result != original:
        path.write_text(result, encoding="utf-8")
        print(f"Formatted {path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Format Markdown files using mdformat and wrap paragraphs.")
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Markdown file or directory",
    )

    args = parser.parse_args()

    root = pathlib.Path(args.path)

    if root.is_file():
        if root.suffix.lower() == ".md":
            format_file(root)
        return

    for md in root.rglob("*.md"):
        format_file(md)


if __name__ == "__main__":
    main()
