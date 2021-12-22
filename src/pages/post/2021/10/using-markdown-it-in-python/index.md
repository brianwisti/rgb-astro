---
date: 2021-10-16
description: Figuring out just enough markdown-it-py to write this post
draft: false
is_md_it: true
layout: layout:PublishedArticle
tags:
- python
- markdown
title: Using markdown-it in Python
---

[user guide]: https://markdown-it-py.readthedocs.io/en/latest/using.html

::: note

I hope the information I share here is useful, but I'm just documenting what I
needed to know *after* reading the markdown-it-py [user guide][] for basic
usage and principles.

:::

## What is it

[markdown-it]: https://github.com/markdown-it/markdown-it
[MyST Markdown]: https://myst-nb.readthedocs.io/en/latest/use/markdown.html
[Executable Book Project]: https://executablebooks.org/en/latest/

[markdown-it-py][] is a Python markdown library based on [markdown-it][] from the
JavaScript world. markdown-it-py provides the core flexibility needed by
[MyST Markdown][], a particularly capable Markdown flavor for the
[Executable Book Project][].

markdown-it-py is configurable, extensible, and --- most important for me today ---
not too hard to get started with.

## How do I install it

[CommonMark]: https://commonmark.org

markdown-it-py alone gets you "enough". Everything you need for [CommonMark][],
at least. But I want more than enough. I want all the features I can reasonaly
gather under one install.

```console
$ pip install markdown-it-py[linkify,plugins]
```

What did that just install?

[`markdown-it-py`][markdown-it-py]
: provides core markdown handling sufficient for common expected behavior

[`linkify-it-py`][linkify-it-py]
: enables recognition of URLs embedded in text strings; needs additional plugins
  to *do* anything with those URLs

[`mdit-py-plugins`][mdit-py-plugins]
: provides a collection of core plugins that make `markdown-it-py` useful to a
  feature-happy person such as myself

[markdown-it-py]: https://pypi.org/project/markdown-it-py/
[linkify-it-py]: https://pypi.org/project/linkify-it-py/
[mdit-py-plugins]: https://pypi.org/project/mdit-py-plugins/

## How do I use it

```python
from markdown_it import MarkdownIt

markdown = "Hello, **world**"
md = MarkdownIt()
print(md.render(markdown))
```

```html
<p>Hello, <strong>world</strong></p>
```

[Typer]: https://typer.tiangolo.com
[neovim rplugin]: /post/2021/08/trying-a-thing-with-neovim/

But I need to be just a *little* fancier than "Hello World." Let's build a
little [Typer][] application that takes a markdown path and makes an HTML
fragment. While I'm at it, I can borrow from my [neovim rplugin][] to fit
everything into my Hugo site.


```python
import typer
from markdown_it import MarkdownIt

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
```

For the moment I'll rely on Python to let me know if I try rendering a Markdown
file that doesn't exist.

This will turn a single `.md.txt` file - the extension I'm using to slide past
Hugo's default Markdown handling - into HTML. I even get a nice `--help` blurb.

```console
$ python rendermd.py --help

Usage: rendermd.py [OPTIONS] SOURCE_PATH

  Transforms markdown into HTML with markdown-it-py.

Arguments:
  SOURCE_PATH  [required]

Options:
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.
  --help                          Show this message and exit.
```

Now I start adding capabilities. If you see this post on the site, you'll know
it worked.

## Picking a preset for common patterns

`markdown-it-py` provides predefined parser presets, allowing you to choose
between common parsing patterns.

`commonmark`
: the default; sticks with the core CommonMark specification; probably good
  enough for 80% of the Markdown that gets written

`gfm-like`
: similar to Github-flavored Markdown; better if you need tables and URL
  transformation

`js-default`
: similar to markdown-it base behavior; adds typographical replacements like
  "smart quotes" to the `gfm-like` set

`zero`
: basically just breaks text into paragraphs; provides a bare minimum for you
  to build a highly custom Markdown parser

I went with `js_default` for my own baseline because it enables the most core
features.

```python
def make_html(markdown):
    """Return HTML string rendered from markdown source."""

    md = MarkdownIt("js-default")

    return md.render(markdown)
```

## Using options to tune your parser

Even with presets available, there are common tweaks that some folks can't live
with and others can't live without. `markdown-it-py` wraps those up in a single
dictionary of options.

[typographic conventions]: https://markdown-it-py.readthedocs.io/en/latest/using.html#typographic-components

`maxNesting`
: recursion protection; think of it as a number for "how fancy can I get with my
  Markdown?"

`html`
: allow raw HTML through

`linkify`
: transform URLs into links

`typographer`
: processes assorted [typographic conventions][] including proper quote marks

`quotes`
: what double and single quotes look like if you enable `typographer`

`xhtmlOut`
: ensure output is valid in the ancient XHTML dialect

`breaks`
: treat line breaks in source as `<br>` elements

`langPrefix`
: CSS class prefix for code blocks; `language-python`, `language-console` etc

`highlight`
: a function to provide syntax highlighting for code blocks

Presets have default values for each of these options.


| Option        | `commonmark` | `gfm_like`  | `js_default` | `zero`      |
|---------------|--------------|-------------|--------------|-------------|
| `maxNesting`  | `20`         | `20`        | `100`        | `20`        |
| `html`        | enabled      | enabled     | —            | —           |
| `linkify`     | —            | enabled     | —            | —           |
| `typographer` | —            | —           | —            | —           |
| `quotes`      | `“”‘’`       | `“”‘’`      | `“”‘’`       | `“”‘’`      |
| `xhtmlOut`    | enabled      | enabled     | —            | —           |
| `breaks`      | —            | —           | —            | —           |
| `langPrefix`  | `language-`  | `language-` | `language-`  | `language-` |
| `highlight`   | —            | —           | —            | —           |

I like fancy quotes. I expect URLs to display as links. I occasionally need to
fall back to raw <abbr title="HyperText Markup Language">HTML</abbr>.But most
importantly on this here blog: I insist on syntax highlighting.

### Adding a highlight function

Rather than decide for themselves how syntax highlighting is done, the
markdown-it-py folks added a single option for us to hook in a function using
*our* preferred approach.

The highlight function should take three arguments:

- the string of code to highlight
- the lexer name
- a dictionary of any additional attributes

[Pygments]: https://pygments.org

You could use whatever highlighting code you want. You could even have your
function call out to an external program. I use [Pygments][] because it's
familiar.

Also, I'm going to ignore `attrs` for now. I rarely add special options to my
code samples, so it's kind of wasted on me. So far.

Better make a note or something in case I forget that I'm ignoring it.

```python
def highlight_code(code, name, attrs):
    """Highlight a block of code"""

    if attrs:
        rich.print(f"Ignoring {attrs=}")

    lexer = get_lexer_by_name(name)
    formatter = HtmlFormatter()

    return highlight(code, lexer, formatter)
```

Okay, what's `make_html` look like now, with options set and highlighting
function defined?

```python
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

    return md.render(markdown)
```

Still a few pieces missing from *my* minimal toolkit. I need to dig a little
deeper than I planned for a "hey friends, markdown-it-py looks like fun" post.
But I at least want to render the kind of posts I would write.

For that I need to use some plugins. Good thing I installed [mdit-py-plugins][].

## Adding parser functionality with plugins

mdit-py-plugins bundles many plugins into a single library. Today I need no
plugins beyond what that library provides.

### definition lists

[dl-tag]: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/dl
[deflist]: https://mdit-py-plugins.readthedocs.io/en/latest/#definition-lists

[Description lists][dl-tag] have been core to my HTML authoring flow since
forever. I'll write the HTML myself if I have to. Fortunately, I don't have to,
thanks to the [deflist][] plugin.

```python
from mdit_py_plugins import deflist

def make_html(markdown):
    # ...
    md.use(deflist.deflist_plugin)

    return md.render(markdown)
```

Now I can write a definition list:

```markdown
[`markdown-it-py`][markdown-it-py]
: provides core markdown handling sufficient for common expected behavior

[`linkify-it-py`][linkify-it-py]
: enables recognition of URLs embedded in text strings; needs additional plugins
  to *do* anything with those URLs

[`mdit-py-plugins`][mdit-py-plugins]
: provides a collection of core plugins that make `markdown-it-py` useful to a 
  feature-happy person such as myself
```

And markdown-it-py produces a proper description list:

```html
<dl>
    <dt><a href="https://pypi.org/project/markdown-it-py/"><code>markdown-it-py</code></a></dt>
    <dd>provides core markdown handling sufficient for common expected behavior</dd>
    <dt><a href="https://pypi.org/project/linkify-it-py/"><code>linkify-it-py</code></a></dt>
    <dd>Enables recognition of URLs embedded in text strings; needs additional plugins
    to <em>do</em> anything with those URLs</dd>
    <dt><a href="https://pypi.org/project/mdit-py-plugins/"><code>mdit-py-plugins</code></a></dt>
    <dd>Provides a collection of core plugins that make <code>markdown-it-py</code> useful to a
    feature-happy person such as myself</dd>
</dl>
```
### admonition blocks

So about a week ago, I was writing the first version of this post. I was nearly
done. Then I got a little too tired and deleted the wrong file --- without
adding it to the repo first!

Oops.

[containers]: https://mdit-py-plugins.readthedocs.io/en/latest/#containers

Anyways, this redraft is less of a tutorial and more of a notes dump. I want
to warn folks about that with a little blurb at the top. I can use the
[containers][] plugin for that. The plugin provides slots for validation and
deeper processing. All I want today is a `<div>` with custom class. I can use
CSS for the rest.

Using the container plugin with a `name` option provides that much.

```python
from mdit_py_plugins import container, deflist

def make_html(markdown):
    # ...
    md.use(container.container_plugin, name="note")

    return md.render(markdown)
```

A `note` container looks like this in the markdown:

```markdown
::: note

This is my *note*.

:::
```

Without any additional configuration, it produces this HTML:

```html
<div class="note">
    <p>This is my <em>note</em>.</p>
</div>
```

## Good enough!

[tokens]: https://markdown-it-py.readthedocs.io/en/latest/using.html#the-token-stream

Stopping here because it's good enough for what I wrote so far today. But there
is plenty more to explore. markdown-it-py allows reviewing and manipulating
parsed [tokens][] directly. Plus there's the whole MyST Markdown thing to
explore.

[Invoke]: https://pyinvoke.org

But for now we're good. Let me drop in the Python code that transformed
this post in the context of my Hugo site, then go convert the Typer logic to
[Invoke][].

<details>
    <summary><tt>rendermd.py</tt></summary>

```python
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
```

</details>