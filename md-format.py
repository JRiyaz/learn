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
import subprocess
import textwrap

import mdformat

LINE_LENGTH = 120

LIST_RE = re.compile(r"^\s*(?:[-+*]|\d+\.)\s")
TABLE_RE = re.compile(r"^\s*\|")
HEADER_RE = re.compile(r"^\s*#")
QUOTE_RE = re.compile(r"^\s*>")
HTML_RE = re.compile(r"^\s*<")
HRULE_RE = re.compile(r"^\s*([-*_])(?:\s*\1){2,}\s*$")


def is_ignored(path: pathlib.Path) -> bool:
    """Return whether Git would ignore a path according to repository rules."""

    try:
        repo_root = pathlib.Path(
            subprocess.check_output(
                ["git", "rev-parse", "--show-toplevel"],
                cwd=path.parent,
                text=True,
                stderr=subprocess.DEVNULL,
            ).strip()
        )
        relative_path = path.resolve().relative_to(repo_root.resolve())
        result = subprocess.run(
            ["git", "check-ignore", "--no-index", "--quiet", "--", str(relative_path)],
            cwd=repo_root,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return result.returncode == 0
    except (OSError, subprocess.CalledProcessError, ValueError):
        return False


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
    parser.add_argument("paths", nargs="*", default=["."], help="Markdown files or directories")

    args = parser.parse_args()

    for path in args.paths:
        root = pathlib.Path(path)

        if root.is_file():
            if root.suffix.lower() == ".md" and not is_ignored(root):
                format_file(root)
            continue

        for md in root.rglob("*.md"):
            if not is_ignored(md):
                format_file(md)


if __name__ == "__main__":
    main()
