#!/usr/bin/python

import frontmatter
import rich
import typer
from markdown_it import MarkdownIt
from mdit_py_plugins import container, deflist
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name


def highlight_code(code, name, attrs):
    """Highlight a block of code"""

    if attrs:
        rich.print(f"Ignoring {attrs=}")

    lexer = get_lexer_by_name(name)
    formatter = HtmlFormatter()

    return highlight(code, lexer, formatter)


def make_html(markdown):
    """Return HTML string rendered from markdown source."""

    md = MarkdownIt(
        "js-default",
        {
            "linkify": True,
            "html": True,
            "typographer": True,
            "highlight": highlight_code,
        },
    )
    md.use(deflist.deflist_plugin)
    md.use(container.container_plugin, name="note")

    return md.render(markdown)


def main(source_path: str):
    """Transforms markdown into HTML with markdown-it-py."""

    target_path = source_path.replace(".md.txt", ".html")
    post = frontmatter.load(source_path)
    post.content = make_html(post.content)
    post.metadata["format"] = "md"

    with open(target_path, "w", encoding="utf-8") as fp:
        fp.write(frontmatter.dumps(post))


if __name__ == "__main__":
    typer.run(main)
