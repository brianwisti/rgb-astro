#!/usr/bin/env python

"""Minimal demonstration of turning Markdown into HTML with markdown-it-py."""

from markdown_it import MarkdownIt


def main():
    """Return HTML rendered from predefined Markdown."""

    markdown = "Hello, **world**"
    md = MarkdownIt()  # pylint: disable=invalid-name
    print(md.render(markdown))


if __name__ == "__main__":
    main()
