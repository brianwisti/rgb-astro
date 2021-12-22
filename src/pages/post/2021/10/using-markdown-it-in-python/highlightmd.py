#!/usr/bin/python

from pathlib import Path

import typer
from markdown_it import MarkdownIt
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name


def highlight_code(code, name, attrs):
    """Highlight a block of code"""

    lexer = get_lexer_by_name(name)
    formatter = HtmlFormatter()

    return highlight(code, lexer, formatter)


def make_html(markdown):
    """Return HTML string rendered from markdown source."""

    md = MarkdownIt()

    return md.render(markdown)


def main(source_path: str):
    """Transforms markdown into HTML with markdown-it-py."""

    target_path = source_path.replace(".md.txt", ".html")

    with open(source_path, encoding="utf-8") as fp:
        markdown = fp.read()

    html = make_html(markdown)

    with open(target_path, "w", encoding="utf-8") as fp:
        fp.write(html)


if __name__ == "__main__":
    typer.run(main)
