---
caption: Hoku hopes for scraps
category: Tools
cover_image: cover.jpg
date: 2021-02-06
description: Want to see something cool?
draft: false
format: md
layout: layout:PublishedArticle
slug: pretty-file-summaries-with-rich-and-exiftool
tags:
- files
- python
- perlish
- rich
- exiftool
title: Pretty File Summaries with Rich and ExifTool
updated: 2021-06-02
uuid: 7261cb27-26ca-4eb3-adfa-01f3c3d9ebf6
---

A while back I [shared][] how I use [ExifTool][exiftool] to get extensive metadata for any
file.  I want to make that info dump pretty with [Rich][rich], a text formatting
library for [Python][python].

"But Brian,"" I hear you cry.  "ExifTool is [Perl][perl]. Why would I want to use both
Perl and Python?"

Because it’s fun, obviously.

You want a "real" reason?  Okay fine.  I haven’t found anything that can get
the depth of file information I get from ExifTool.  I haven’t found a
formatting library that’s as pleasant to use as Rich — maybe [TTY Toolkit][tty-toolkit]?

Besides — ExifTool is a standalone command line tool.  We don’t need to write
any Perl to *use* it.  Heck, we don’t even need to figure out the system calls.
[Sven Marnach][sven-marnach] is way ahead of us with the extremely helpful [pyexiftool][].

Rich and pyexiftool make Python an easy choice for this task.

## Setting up

If you want to play along at home, make sure you have the dependencies.

    $ brew install exiftool
    $ pip install pyexiftool rich typer

[Typer][typer] simplifies turning this random idea into a useful command line tool.

:::note

If you’re already a fan of Perl, consider [`cpanm`][cpanm] instead of [Homebrew][homebrew].

``` text
$ cpanm Image::ExifTool
```

Now you can use [Image::ExifTool][image-exiftool] in your own Perl projects.

:::

## Some scaffolding

Even though I’m the only user, I still need to figure out how I plan to use it.
At minimum?  I hand my script a filename.  It hands me metadata.

    richexif FILENAME [OPTIONS]

I can hook some [minimal][] Typer argument handling around that flow.

```python
#!/usr/bin/env python

import logging

from rich.logging import RichHandler
import typer

logging.basicConfig(
    level=logging.DEBUG,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler()]
)


def main(filename: str):
    """Display nicely-formatted file metadata."""
    logging.debug("filename: %s", filename)
```

Can I run it?

    chmod 755 richexif.py
    ./richexif.py hoku-hopes-for-snacksjpg.jpg

I can!  What happens if I use it wrong?

    $ ./richexif.py
    Usage: richexif.py [OPTIONS] FILENAME
    Try 'richexif.py --help' for help.

    Error: Missing argument 'FILENAME'.

I get an error message telling me what `richexif.py` needs to do its thing.
Nice.

I confirmed that Typer handles the CLI bits, and Rich handles the formatting.
Now for pyexiftool.

Oh and I’ll skip logging output from here on.  Rich’s [logging handler][logging] output
is a joy to look at, but really that stuff is for me.  For you it’ll just add
noise.

## Some metadata

I need exiftool, of course.  Plus a Rich [Console][console] object, masterminding the
display details for my terminal.

```python
import exiftool
from rich.console import Console

console = Console()
```

exiftool’s [`get_metadata`][get-metadata] grabs everything ExifTool sees about a file.  It
also provides methods for ExifTool [tags][], but I won’t mess with them today.
Tags — the official name for our metadata keys — are most useful when you
already know what you’re looking for.  We’re just checking stuff out.

For now, a little abstraction layer over pyexiftool’s `ExifTool`.

```python
def get_metadata(filename):
    """Return a dictionary of file metadata."""
    with exiftool.ExifTool() as et:
        return et.get_metadata(filename)
```

`main` gets the metadata and asks `console` to print it.

```python
def main(filename: str):
    """Display nicely-formatted file metadata."""
    metadata = get_metadata(filename)
    console.print(metadata)
```

And here’s what that looks like.

<pre class="rich"><span style="font-weight: bold">&#123;</span>
    <span style="color: #008000">'SourceFile'</span>: <span style="color: #008000">'hoku-hopes-for-snacks.jpg'</span>,
    <span style="color: #008000">'ExifTool:ExifToolVersion'</span>: <span style="color: #000080; font-weight: bold">12.15</span>,
    <span style="color: #008000">'File:FileName'</span>: <span style="color: #008000">'hoku-hopes-for-snacks.jpg'</span>,
    <span style="color: #008000">'File:Directory'</span>: <span style="color: #008000">'.'</span>,
    <span style="color: #008000">'File:FileSize'</span>: <span style="color: #000080; font-weight: bold">918330</span>,
    <span style="color: #008000">'File:FileModifyDate'</span>: <span style="color: #008000">'2021:02:06 00:54:29-08:00'</span>,
    <span style="color: #008000">'File:FileAccessDate'</span>: <span style="color: #008000">'2021:02:06 11:30:33-08:00'</span>,
    <span style="color: #008000">'File:FileInodeChangeDate'</span>: <span style="color: #008000">'2021:02:06 11:30:33-08:00'</span>,
    <span style="color: #008000">'File:FilePermissions'</span>: <span style="color: #000080; font-weight: bold">775</span>,
    <span style="color: #008000">'File:FileType'</span>: <span style="color: #008000">'JPEG'</span>,
    <em>…skipping 62 lines…</em>
    <span style="color: #008000">'Composite:ScaleFactor35efl'</span>: <span style="color: #000080; font-weight: bold">6.04651162790698</span>,
    <span style="color: #008000">'Composite:ShutterSpeed'</span>: <span style="color: #000080; font-weight: bold">0.05</span>,
    <span style="color: #008000">'Composite:GPSLatitude'</span>: <span style="color: #000080; font-weight: bold">47.5750857997222</span>,
    <span style="color: #008000">'Composite:GPSLongitude'</span>: <span style="color: #000080; font-weight: bold">-122.386441</span>,
    <span style="color: #008000">'Composite:CircleOfConfusion'</span>: <span style="color: #008000">'0.00496918925785101'</span>,
    <span style="color: #008000">'Composite:FOV'</span>: <span style="color: #000080; font-weight: bold">69.3903656740024</span>,
    <span style="color: #008000">'Composite:FocalLength35efl'</span>: <span style="color: #000080; font-weight: bold">26</span>,
    <span style="color: #008000">'Composite:GPSPosition'</span>: <span style="color: #008000">'47.5750857997222 -122.386441'</span>,
    <span style="color: #008000">'Composite:HyperfocalDistance'</span>: <span style="color: #000080; font-weight: bold">2.48061927751922</span>,
    <span style="color: #008000">'Composite:LightValue'</span>: <span style="color: #000080; font-weight: bold">3.81378119121704</span>
<span style="font-weight: bold">}</span>
</pre>

Holy crap that’s a lot.  Some of it could be considered sensitive information —
unless you read my [`now`][now] page.  But it’s all there!  Even in the snipped
version you can learn a lot.  Hello from my Windows partition in West Seattle
during February of 2021!

:::tip

Uncomfortable sharing that much with every photo you upload?  You can scrub
those tags right out.  [With ExifTool][with-exiftool], of course.

:::

But back to the other gripe about all this metadata.  It’s way too much for me
to take in all at once.  I need some kind of filter!

### Filtering the firehose

```python
def filter_metadata(metadata, filter):
    """Return a copy of the metadata where fields contain the substring `filter`."""
    return {k: v for k, v in metadata.items() if filter in k}
```

There’s no kind of transformation here.  If a field constains the exact
substring described in `filter`, use it.

Adding a Typer [Option][option] lets us ask for a filter from the command line.

```python
def main(
    filename: str,
    filter: Optional[str] = typer.Option(
        None, help="Substring to restrict displayed fields"
    ),
):
    """Display nicely-formatted file metadata."""
    metadata = get_metadata(filename)

    if filter:
        metadata = filter_metadata(metadata, filter)

    console.print(metadata)
```

If use `--filter`, we should only get matching tags.  Leaving out the filter
gets us everything.

Try it out!

    $ ./richexif.py hoku-hopes-for-snacks.jpg --filter=Image

Now that I’m not overwhelmed by the quantity of output, I’m a little
underwhelmed by the quality.

<pre class="rich"><span style="font-weight: bold">&#123;</span>
    <span style="color: #008000">'File:ImageWidth'</span>: <span style="color: #000080; font-weight: bold">3672</span>,
    <span style="color: #008000">'File:ImageHeight'</span>: <span style="color: #000080; font-weight: bold">2066</span>,
    <span style="color: #008000">'EXIF:ImageWidth'</span>: <span style="color: #000080; font-weight: bold">4032</span>,
    <span style="color: #008000">'EXIF:ImageHeight'</span>: <span style="color: #000080; font-weight: bold">2268</span>,
    <span style="color: #008000">'EXIF:ExifImageWidth'</span>: <span style="color: #000080; font-weight: bold">4032</span>,
    <span style="color: #008000">'EXIF:ExifImageHeight'</span>: <span style="color: #000080; font-weight: bold">2268</span>,
    <span style="color: #008000">'EXIF:ImageUniqueID'</span>: <span style="color: #008000">'J12LLKL00SM'</span>,
    <span style="color: #008000">'EXIF:ThumbnailImage'</span>: <span style="color: #008000">'(Binary data 6788 bytes, use -b option to extract)'</span>,
    <span style="color: #008000">'Composite:ImageSize'</span>: <span style="color: #008000">'3672 2066'</span>
<span style="font-weight: bold">}</span></pre>

It’s nice.  Don’t get me wrong.  But all we’ve added to default `exiftool`
behavior is some color.

I’ve played with Rich a bit.  I know we can do better.

## A metadata table!

Rich lets us create and display [tables][] in the terminal.

```python
from rich.table import Table
```

We need to *build* the table, defining columns and adding values row by row.

```python
def file_table(filename, metadata):
    """Return a Rich Table showing the metadata for a file."""
    table = Table("Field", "Value", title=filename)

    for key, value in metadata.items():
        table.add_row(key, str(value))

    return table
```

:::warning

Hey, don’t miss that `str(value)`!  Rich tables need strings, and take
nothing for granted with the values you give it.  Numeric values won’t
necessarily convert straight to strings without a little help.

:::

```python
def main(...):
    """Display nicely-formatted file metadata."""
    ...

    if filter:
        metadata = filter_metadata(metadata, filter)

    table = file_table(filename, metadata)
    console.print(table)
```

What does our filtered view look like as a table?

    $ ./richexif.py hoku-hopes-for-snacksjpg.jpg --filter=Image

<pre class="rich"><span style="font-style: italic">                        hoku-hopes-for-snacksjpg.jpg                         </span>
┏━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃<span style="font-weight: bold"> Field                </span>┃<span style="font-weight: bold"> Value                                              </span>┃
┡━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ File:ImageWidth      │ 3672                                               │
│ File:ImageHeight     │ 2066                                               │
│ EXIF:ImageWidth      │ 4032                                               │
│ EXIF:ImageHeight     │ 2268                                               │
│ EXIF:ExifImageWidth  │ 4032                                               │
│ EXIF:ExifImageHeight │ 2268                                               │
│ EXIF:ImageUniqueID   │ J12LLKL00SM                                        │
│ EXIF:ThumbnailImage  │ (Binary data 6788 bytes, use -b option to extract) │
│ Composite:ImageSize  │ 3672 2066                                          │
└──────────────────────┴────────────────────────────────────────────────────┘
</pre>

Pretty nifty.

## A metadata tree!

We can do more than tables though.  with that `type:tag` split, there's kind
of a heirarchy.  We *could* add a column for the tag type, but why not use a
[Tree][tree]?

```python
from rich.tree import Tree
```

Hang on a second while we build our little tree with its branches.

```python
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
```

Except now we have two ways to display metadata.  Three, if you count the
dictionary we started with.  How are we going to show this tree without
discarding our table code?

For now, a callback table that says what to call for each of the options.

```python
from rich.tree import Tree

DISPLAYS = {
    "table": lambda f, m: file_table(f, m),
    "tree": lambda f, m: file_tree(f, m),
}
```

We don’t *need* to use lambdas here.  Functions can be passed around same as
any other value.  But if I wrap them in a lambda I can build my constant table
before Python knows the functions exist.

Typer uses [callback][] functions to validate options.  They do any processing or
checks they need to, then return the supplied value if everything goes well.

```python
def validate_display(value):
    """Return value if valid, or panic if it isn't."""
    if value not in DISPLAYS:
        raise typer.BadParameter(f"Format must be one of: {DISPLAYS.keys()}")
    return value
```

Add the `--display` Option, making sure to point Typer at the callback.
`main` itself knows the value is safe, or the script never would have reached
it.  So I can grab the displayer and call it without fear of consequence.

```python
def main(
    ...
    display: str = typer.Option(
        "table",
        help="How to display the metadata",
        callback=validate_display,
    ),
):
    """Display nicely-formatted file metadata."""
    ...

    displayer = FORMATS[display]
    output = displayer(filename, metadata)
    console.print(output)
```

Okay!  What do we have now?

``` text
$ ./richexif.py hoku-hopes-for-snacks.jpg --filter=Image --display=tree
```

<pre class="rich"><span style="font-weight: bold">hoku-hopes-for-snacks.jpg</span>
├── <span style="font-weight: bold">File</span>
│   ├── <span style="font-style: italic">ImageWidth:</span> 3672
│   └── <span style="font-style: italic">ImageHeight:</span> 2066
├── <span style="font-weight: bold">EXIF</span>
│   ├── <span style="font-style: italic">ImageWidth:</span> 4032
│   ├── <span style="font-style: italic">ImageHeight:</span> 2268
│   ├── <span style="font-style: italic">ExifImageWidth:</span> 4032
│   ├── <span style="font-style: italic">ExifImageHeight:</span> 2268
│   ├── <span style="font-style: italic">ImageUniqueID:</span> J12LLKL00SM
│   └── <span style="font-style: italic">ThumbnailImage:</span> (Binary data 6788 bytes, use -b option to extract)
└── <span style="font-weight: bold">Composite</span>
    └── <span style="font-style: italic">ImageSize:</span> 3672 2066
</pre>

Oooooh.

Anyways, that’s what I wanted to show you.  Got plenty more ideas for mashing
ExifTool and Rich together, as I’m sure you can imagine.

[shared]: /post/2020/04/getting-file-info-from-the-shell
[exiftool]: https://exiftool.org
[rich]: https://rich.readthedocs.io/en/stable/introduction.html
[python]: link:/tags/python
[perl]: /tags/perl
[tty-toolkit]: https://ttytoolkit.org
[pyexiftool]: https://smarnach.github.io/pyexiftool/
[sven-marnach]: https://github.com/smarnach
[typer]: https://typer.tiangolo.com
[image-exiftool]: https://metacpan.org/pod/distribution/Image-ExifTool/lib/Image/ExifTool.pod
[cpanm]: https://metacpan.org/pod/App::cpanminus
[homebrew]: https://brew.sh
[minimal]: https://typer.tiangolo.com/tutorial/first-steps/#add-a-cli-argument[minimal]
[logging]: https://rich.readthedocs.io/en/latest/logging.html
[console]: https://rich.readthedocs.io/en/latest/console.html
[tags]: https://exiftool.org/TagNames/index.html
[get-metadata]: https://smarnach.github.io/pyexiftool/#exiftool.ExifTool.get_metadata
[now]: /now
[with-exiftool]: https://www.linux-magazine.com/Online/Blogs/Productivity-Sauce/Remove-EXIF-Metadata-from-Photos-with-exiftool
[option]: https://typer.tiangolo.com/tutorial/options/
[tables]: https://rich.readthedocs.io/en/stable/tables.html
[tree]: https://rich.readthedocs.io/en/stable/tree.html
[callback]: https://typer.tiangolo.com/tutorial/options/callback-and-context/