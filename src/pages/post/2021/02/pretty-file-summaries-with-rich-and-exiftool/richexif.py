#!/usr/bin/env python


import logging
from bs4 import BeautifulSoup
import exiftool
import pyperclip
from rich.console import Console
from rich.logging import RichHandler
from rich.table import Table
from rich.tree import Tree
import typer


console = Console(record=True, width=80)
# logging_handler = RichHandler(console=console)
logging_handler = RichHandler()
logging.basicConfig(
    level=logging.DEBUG,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[logging_handler],
)

DISPLAYS = {
    "dict": lambda f, m: file_dict(f, m),
    "table": lambda f, m: file_table(f, m),
    "tree": lambda f, m: file_tree(f, m),
}


def extract_html(html_source):
    """Return just the output fragment of Rich-formatted HTML."""

    soup = BeautifulSoup(html_source, "lxml")
    pre_block = soup.pre
    del pre_block["style"]
    pre_block["class"] = "rich"

    return str(pre_block)


def file_dict(_, metadata):
    """Return the metadata for printing."""
    return metadata


def file_table(filename, metadata):
    """Return a Rich Table showing the metadata for a file."""

    table = Table("Field", "Value", title=filename)

    for key, value in metadata.items():
        table.add_row(key, str(value))

    return table


def file_tree(filename, metadata):
    tree = Tree(f"[bold]{filename}")
    branches = {}
    tagged_values = [(k.split(":"), v) for k, v in metadata.items()]

    for tags, value in tagged_values:
        root_tag = tags[0]

        if root_tag not in branches:
            branches[root_tag] = tree.add(f"[bold]{root_tag}")

        if len(tags) == 2:
            branches[root_tag].add(f"[italic]{tags[1]}:[/italic] {value}")
        else:
            branches[tags[0]].add(str(value))

    return tree


def filter_metadata(metadata, filter):
    """Return a copy of the metadata where fields contain the substring `filter`."""
    return {k: v for k, v in metadata.items() if filter in k}


def get_metadata(filename):
    """Return a dictionary of file metadata."""

    with exiftool.ExifTool() as et:
        return et.get_metadata(filename)


def validate_display(value):
    """Return value if valid, or panic if it isn't."""

    if value not in DISPLAYS:
        raise typer.BadParameter(f"Format must be one of: {DISPLAYS.keys()}")

    return value


def main(
    filename: str,
    display: str = typer.Option(
        "table",
        help="How to display the metadata",
        callback=validate_display,
    ),
    filter: str = typer.Option(None, help="Substring to restrict displayed fields"),
):
    """Display nicely-formatted file metadata."""

    logging.debug("filename: %s", filename)
    metadata = get_metadata(filename)

    if filter:
        metadata = filter_metadata(metadata, filter)

    logging.debug("display arg: %s", display)
    displayer = DISPLAYS[display]
    output = displayer(filename, metadata)
    console.print(output)

    output = console.export_html(inline_styles=True)
    html = extract_html(output)

    # I've tweaked my WSL setup so I need to be explicit here.
    pyperclip.set_clipboard("xclip")
    pyperclip.copy(html)


if __name__ == "__main__":
    typer.run(main)
