---
caption: a screenshot of the HTML that I created to show I don't need screenshots
category: Tools
cover_image: cover.png
date: 2021-08-24 22:08:00
description: Okay maybe not so much on the profit but definitely fun!
draft: false
format: md
layout: layout:PublishedArticle
slug: extracting-rich-output
tags:
- python
- rich
title: Extracting Rich Output for fun and profit
updated: 2021-08-25T09:30-07:00
uuid: 21ae1088-beb3-438e-a406-d82a98d911d5
---

Somewhere in the middle of [Tooting with Python][tooting-with-python], I mentioned I how I get
[Rich][rich] output into a post.  That approach was a little clumsy though. I want to
run my code and paste its output into whatever draft I'm editing.

So I'll figure that one out now.

:::admonition

*2021-08-25 Update*

I initially posted a version of this post using [BeautifulSoup][bs4] for HTML
extraction. Then Rich creator [Will McGugan][will-mgcgugan] pointed out that I could get
what I need from Rich itself!

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">Great write up!<br><br>You may be able to skip the Beautiful Soup step with the following:<br><br>console.export_html(code_format=&quot;&lt;pre style=&quot;font-family:Menlo,&#39;DejaVu Sans Mono&#39;,consolas,&#39;Courier New&#39;,monospace&quot;&gt;&#123;code}&lt;/pre&gt;&quot;)</p>&mdash; Will McGugan (@willmcgugan) <a href="https://twitter.com/willmcgugan/status/1430452309536956421?ref_src=twsrc%5Etfw">August 25, 2021</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

Yeah let's do that instead. Much less to remember.

:::

## What are we printing?

How about a [Table][table] of the most popular pages on my site? I use [Plausible][plausible] for
stats, and I've been meaning to play with their [API][plausible-api]. But I'm here to talk
about Rich, not Plausible. Let's use a static copy of API results so everyone's
using the same data.

```python title="showstats.py"
import rich
from rich.table import Table

STATS = {
    "results": [
        {
            "page": "/post/2017/11/drawing-grids-with-python-and-pillow/",
            "visitors": 1114,
        },
        {"page": "/post/2017/01/cinnamon-screenshot-shortcuts/", "visitors": 580},
        {"page": "/", "visitors": 458},
        {
            "page": "/post/2014/06/what-is-build-essentials-for-opensuse/",
            "visitors": 340,
        },
        {"page": "/config/emacs/doom/", "visitors": 303},
        {"page": "/post/2020/06/csv-and-data-tables-in-hugo/", "visitors": 293},
        {"page": "/post/2019/05/kitty-terminal/", "visitors": 265},
        {
            "page": "/post/2018/02/setting-task-dependencies-in-taskwarrior/",
            "visitors": 263,
        },
        {"page": "/post/2019/02/taskwarrior-projects/", "visitors": 260},
        {
            "page": "/post/2019/01/circular-grids-with-python-and-pillow/",
            "visitors": 242,
        },
    ]
}


def build_stats_table(stats):
    """Construct a Rich Table from site traffic breakdown."""

    table = Table(title="Plausible.io Traffic Breakdown")
    table.add_column("Page")
    table.add_column("Visitors", justify="right", style="green")

    for entry in stats["results"]:
        table.add_row(entry["page"], "{:,}".format(entry["visitors"]))

    return table


def show_stats():
    """Display Plausible's breakdown of site traffic."""

    table = build_stats_table(STATS)
    rich.print(table)


if __name__ == "__main__":
    show_stats()
```

Here's a screenshot, so you know what this produces in my own terminal.

![table output](showstats-table.png "table output")

Okay. Now let's start talking about exporting output.

## `xclip` is usually good enough

This post focuses on the "blog writing and pretty reports" situations. For
everyday sharing, all I need is a legibly formatted data dump. [`xclip`][xclip] works for
those situations.

``` bash
python showstats.py | xclip
```

I don't see anything on my screen, of course, because I piped everything to
`xclip`. But when I paste from the clipboard:

**output**

``` text
                    Plausible.io Traffic Breakdown
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┓
┃ Page                                                    ┃ Visitors ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━┩
│ /post/2017/11/drawing-grids-with-python-and-pillow/     │    1,114 │
│ /post/2017/01/cinnamon-screenshot-shortcuts/            │      580 │
│ /                                                       │      458 │
│ /post/2014/06/what-is-build-essentials-for-opensuse/    │      340 │
│ /config/emacs/doom/                                     │      303 │
│ /post/2020/06/csv-and-data-tables-in-hugo/              │      293 │
│ /post/2019/05/kitty-terminal/                           │      265 │
│ /post/2018/02/setting-task-dependencies-in-taskwarrior/ │      263 │
│ /post/2019/02/taskwarrior-projects/                     │      260 │
│ /post/2019/01/circular-grids-with-python-and-pillow/    │      242 │
└─────────────────────────────────────────────────────────┴──────────┘
```

`xclip` preserves the basic shape of my output. I see a table. The *Visitors*
column is right-aligned. The title is centered. But it loses some of the finer
formatting bits: bold, italicization, color.

:::note

Also? This renders great on Chrome-based browsers and weird on Firefox.  There
are definite limitations to just copying and pasting from the terminal.

:::

Let's pull that clipboard management into the script with Al Sweigart's
[Pyperclip][pyperclip] library.

## Let Rich and Pyperclip handle the clipboard

Pyperclip gives our code access to the system clipboard, letting us copy and
paste from Python.  The Rich [Console][console] can [`capture`][capture] the
characters it would have printed, and hand them to us when needed. Sounds like
a great team.

``` python
import pyperclip
from rich.console import Console
```

I set up Pyperclip and create a local Console to handle capturing.

``` python
def show_stats(stats):
    """Display Plausible's breakdown of site traffic."""

    table = build_stats_table(stats)
    pyperclip.set_clipboard("xclip")
    console = Console()

    with console.capture() as capture:
        console.print(table)

    text_output = capture.get()
    pyperclip.copy(text_output)
    print(text_output)
```

I need to tell Pyperclip about `xclip` or it gets a bit confused on WSL.
Also, since I captured the output, I need to print it myself. Why print`
instead of `rich.print` or `console.print`?

Let me answer that question by pasting the contents of my clipboard:

``` text
[3m                    Plausible.io Traffic Breakdown                    [0m
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┓
┃[1m [0m[1mPage                                                   [0m[1m [0m┃[1m [0m[1mVisitors[0m[1m [0m┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━┩
│ /post/2017/11/drawing-grids-with-python-and-pillow/     │[32m [0m[32m    1114[0m[32m [0m│
│ /post/2017/01/cinnamon-screenshot-shortcuts/            │[32m [0m[32m     580[0m[32m [0m│
│ /                                                       │[32m [0m[32m     458[0m[32m [0m│
│ /post/2014/06/what-is-build-essentials-for-opensuse/    │[32m [0m[32m     340[0m[32m [0m│
│ /config/emacs/doom/                                     │[32m [0m[32m     303[0m[32m [0m│
│ /post/2020/06/csv-and-data-tables-in-hugo/              │[32m [0m[32m     293[0m[32m [0m│
│ /post/2019/05/kitty-terminal/                           │[32m [0m[32m     265[0m[32m [0m│
│ /post/2018/02/setting-task-dependencies-in-taskwarrior/ │[32m [0m[32m     263[0m[32m [0m│
│ /post/2019/02/taskwarrior-projects/                     │[32m [0m[32m     260[0m[32m [0m│
│ /post/2019/01/circular-grids-with-python-and-pillow/    │[32m [0m[32m     242[0m[32m [0m│
└─────────────────────────────────────────────────────────┴──────────┘
```

Uh. Oops? `console` captured *exactly* what it would have printed, including
terminal [escape codes][escape-codes].

Rich supports [exporting][] output beyond a raw dump, though.

## Let Rich get you some HTML

:::note

For safety reasons, most Markdown converters must be explicitly configured to
allow raw HTML through. Check the documentation of your converter or blogging
tools to see if and how you need to do that.

:::

A Console created with the `record` option enabled remembers everything it
prints. You can get export your copy at any point. The
[`export_text`][export-text] method provides a copy with minimal formatting,
while [`export_html`][export-html] produces HTML pages. That's for sure
something I can paste into my post source. Nice!

One *slight* wrinkle. Unless you tell it otherwise, `export_html` produces a
complete HTML file — with `<head>`, `<body>`, and even a `<style>` section.
All I want is the `<pre>...</pre>` describing my output.

Fortunately, `export_html` also lets us tell it exactly what we want:

- `code_format` lets me specify the HTML fragment to generate
- turn on `inline_styles` to directly embed style rules; handy if I don't have my own CSS definitions for Rich-specific classes

Let's make some HTML for Pyperclip to copy.

``` python
def show_stats():
    """Display Plausible's breakdown of site traffic."""

    # print the stats
    table = build_stats_table(STATS)
    console = Console(record=True)
    console.print(table)

    # copy the stats
    pyperclip.set_clipboard("xclip")
    exported_html = console.export_html(
        inline_styles=True, code_format="<pre>{code}</pre>"
    )
    pyperclip.copy(exported_html)
```

What do the contents of my clipboard look like now?

<pre><span style="font-style: italic">                    Plausible.io Traffic Breakdown                    </span>
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┓
┃<span style="font-weight: bold"> Page                                                    </span>┃<span style="font-weight: bold"> Visitors </span>┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━┩
│ /post/2017/11/drawing-grids-with-python-and-pillow/     │<span style="color: #008000; text-decoration-color: #008000">    1,114 </span>│
│ /post/2017/01/cinnamon-screenshot-shortcuts/            │<span style="color: #008000; text-decoration-color: #008000">      580 </span>│
│ /                                                       │<span style="color: #008000; text-decoration-color: #008000">      458 </span>│
│ /post/2014/06/what-is-build-essentials-for-opensuse/    │<span style="color: #008000; text-decoration-color: #008000">      340 </span>│
│ /config/emacs/doom/                                     │<span style="color: #008000; text-decoration-color: #008000">      303 </span>│
│ /post/2020/06/csv-and-data-tables-in-hugo/              │<span style="color: #008000; text-decoration-color: #008000">      293 </span>│
│ /post/2019/05/kitty-terminal/                           │<span style="color: #008000; text-decoration-color: #008000">      265 </span>│
│ /post/2018/02/setting-task-dependencies-in-taskwarrior/ │<span style="color: #008000; text-decoration-color: #008000">      263 </span>│
│ /post/2019/02/taskwarrior-projects/                     │<span style="color: #008000; text-decoration-color: #008000">      260 </span>│
│ /post/2019/01/circular-grids-with-python-and-pillow/    │<span style="color: #008000; text-decoration-color: #008000">      242 </span>│
└─────────────────────────────────────────────────────────┴──────────┘</pre>

That works well enough for a blog post!

If you're curious about the exported HTML, here's a chunk of it:

``` html
    <pre><span style="font-style: italic">                    Plausible.io Traffic Breakdown                    </span>
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┓
    ┃<span style="font-weight: bold"> Page                                                    </span>┃<span style="font-weight: bold"> Visitors </span>┃
    ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━┩
    │ /post/2017/11/drawing-grids-with-python-and-pillow/     │<span style="color: #008000; text-decoration-color: #008000">    1,114 </span>│
    ...
    │ /post/2019/01/circular-grids-with-python-and-pillow/    │<span style="color: #008000; text-decoration-color: #008000">      242 </span>│
    └─────────────────────────────────────────────────────────┴──────────┘
    </pre>
```

Anyways, this was just another thing I wanted to get down before I forgot again.

## What else?

There are a few more pieces that tie it into my particular workflow, but this
covers what you'd need to export output from your own Rich programs for easy
blogging or information sharing.

[tooting-with-python]: /post/2021/08/tooting-with-python/
[rich]: https://rich.readthedocs.io
[will-mcgugan]: https://www.willmcgugan.com/
[bs4]: https://www.crummy.com/software/BeautifulSoup/
[export-html]: https://rich.readthedocs.io/en/stable/reference/console.html#rich.console.Console.export_html
[export-text]: https://rich.readthedocs.io/en/stable/reference/console.html#rich.console.Console.export_text
[table]: https://rich.readthedocs.io/en/stable/tables.html
[plausible]: https://plausible.io
[plausible-api]: https://plausible.io/docs/stats-api
[xclip]: https://github.com/astrand/xclip
[pyperclip]: https://pypi.org/project/pyperclip/
[capture]: https://rich.readthedocs.io/en/stable/console.html#capturing-output
[console]: https://rich.readthedocs.io/en/stable/reference/console.html
[escape-codes]: https://en.wikipedia.org/wiki/ANSI_escape_code
[exporting]: https://rich.readthedocs.io/en/stable/console.html#exporting