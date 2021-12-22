---
aliases:
- /2020/02/17/python-invoke/
category: tools
date: 2020-02-17 19:56:29
description: I got to know the Python `invoke` task runner a little better.
draft: false
layout: layout:PublishedArticle
slug: python-invoke
tags:
- python
- site
- pyinvoke
- hugo
title: Python Invoke
uses:
- python: 3.8.0
- pyinvoke: 1.3.0
- hugo: 0.64.1/extended
uuid: de6ebe84-8631-407b-bc41-e03a36bceaa2
---

## The problem

I manage my site with
[make](https://www.gnu.org/software/make/manual/make.html) and a
hodgepodge of shell scripts. This approach sort of collapsed under its
own weight the other day. I needed to update the "ask Hugo to create a
new post or note" scripts to accommodate a change in folder layout. I
wrote one of the scripts in bash, and the other in Perl. All of it
managed by `make`, with a string of `.PHONY` targets.

Not that there’s anything wrong with that.

## A solution: Invoke

But I want to try a more unified approach. I also decided that 2020 is
my year of [Python](/tags/python).

<aside class="admonition">

Don’t hold me to that "year of Python" thing. I get distracted.

</aside>

I could use the [Invoke](https://www.pyinvoke.org/) tool created by
[Jeff Forcier](http://bitprophet.org/) for this unified approach.

Invoke gives you a task runner and support library for managing those
tasks. It works a bit like Make, except that you define tasks with
Python. Decorate some functions in a `tasks.py` file and you’re ready to
go!

I like Invoke’s approach to little annoyances like options and external
commands, too. I no longer need to care about
[argparse](https://docs.python.org/3/library/argparse.html) or
[subprocess](https://docs.python.org/3/library/subprocess.html) for so
many little projects.

Let’s get started.

### Installing it

Mercifully simple. Do you have [Homebrew](https://brew.sh/)? Use that.

    $ brew install pyinvoke

You can also use `pip` if you want Invoke in a particular Python
environment.

    (rgbhugo) $ pip install pyinvoke

Using Invoke with or near pyenv

No matter how I installed Invoke, I couldn’t get it to run in any
environment at first. That’s more likely my mistake than any fault of
pyenv or Invoke. Installing
[pyenv-which-ext](https://github.com/pyenv/pyenv-which-ext) fixed that
problem. pyenv-which-ext looks for an executable in your regular path if
it can’t be found in your pyenv stubs.

Thought I’d mention it in case you saw similar issues.

### The tasks.py file

Tasks are defined in a `tasks.py` file. Seems reasonable so far. Import
the [task
decorator](http://docs.pyinvoke.org/en/stable/api/tasks.html#invoke.tasks.task)
to use Invoke’s powers.

``` python
from invoke import task
```

### A "Hello World" task

There’s not *much* boilerplate to a task, but there’s still a little.

``` python
@task
def hello(c):
    print("Hello, world!")
```

`@task` is important. It tells Invoke to pay attention. Without the
decoration, `hello` is just another function. That’s great for adding
support logic, but not so much for "Hello World."

The `c` argument is Invoke’s
[context](http://docs.pyinvoke.org/en/stable/api/context.html). We’ll
get to that. The thing to remember for now is that every task gets
called with context as its first argument.

To *run* that task?

    $ invoke hello
    Hello, world!

My Makefile uses a clever bit of
[sed](https://www.grymoire.com/Unix/Sed.html) to list available targets
when you call `make help`. With Invoke? No cleverness needed.

    $ invoke --list
    Available tasks:

      hello

I strongly prefer Invoke’s built-in behavior to my `sed` one-liner.

#### Documenting the task

This list could be more helpful, though. We know what the `hello` task
does because I wrote it a few minutes ago. What about in a few months,
when I have dozens of tasks?

<aside class="admoonition">

Trust me. In a few months I will have dozens of tasks. Maybe in a few
hours.

</aside>
Add a docstring!

``` python
@task
def hello(c, name):
    """
    Print the standard greeting

    "Hello world" is the classic first program to see what a language looks like.
    So of course I used it to understand Invoke.
    """
    print(f"Hello, {name}!")
```

Invoke takes the first line from that docstring and uses it to summarize
our task in `--list`.

    $ invoke --list
    Available tasks:

    hello   Print the standard greeting

Nice.

<aside class="admonition note">
    <p class="admonition-title">Note</p>

Since Invoke only uses the docstring’s first line for the summary, keep
it short and to the point. Deep dives and technical explanations can go
in following paragraphs. But you should be doing that anyways. It’s a
good documentation habit.

</aside>

#### Task parameters

Your task is a Python function. Add arguments to your function and
you’ve added
[parameters](http://docs.pyinvoke.org/en/stable/getting-started.html#task-parameters)
to the task.

``` python
@task
def hello(c, name):
    """
    Print the standard greeting

    "Hello world" is the classic first program to see what a language looks like.
    So of course I used it to understand Invoke.
    """
    print(f"Hello, {name}!")
```

Invoke accepts both long and short form parameters. Either `--name` or
`-n` count for `name`. I’ll use the long form today to keep things
clear.

    $ invoke hello --name Rumpelstiltskin
    Hello, Rumpelstiltskin!

If we ask Invoke about a specific task, it tells us about available
parameters — along with the rest of the task function’s docstring.

    $ invoke --help hello
    Usage: inv[oke] [--core-opts] hello [--options] [other tasks here ...]

    Docstring:
      Print the standard greeting

      "Hello world" is the classic first program to see what a language looks like.
      So of course I used it to understand Invoke.

    Options:
      -n STRING, --name=STRING

We can document the parameters by handing a dictionary of names and
summary strings to the decorator.

``` python
@task(help={"name": "Who or what is being greeted"})
def hello(c, name):
    ...
```

    invoke --help hello
    Usage: inv[oke] [--core-opts] hello [--options] [other tasks here ...]

    Docstring:
      Print the standard greeting

      "Hello world" is the classic first program to see what a language looks like.
      So of course I used it to understand Invoke.

    Options:
      -n STRING, --name=STRING   Who or what is being greeted

#### Optional parameters

Right now, the `name` option is required. Invoke gets confused when we
skip it.

    $ invoke hello
    'hello' did not receive required positional arguments: 'name'

Positional? Well yeah. You don’t *need* the name for a required
parameter.

    $ invoke hello world
    Hello, world!

I prefer to be explicit about things. But we weren’t talking about
positional parameters. Not on purpose anyways.

It’s reasonable to want a default parameter for your task. Do that by
giving your function argument a default value.

``` python
DEFAULT_NAME = "world"

@task(help={"name": f"Who or what is being greeted (default '{DEFAULT_NAME}')"})
def hello(c, name=DEFAULT_NAME):
    ...
```

Now we have a default name. Setting it as a variable makes it easier to
identify and update later. We even noted the default in \`name’s
documentation, as a special favor to future us.

And hey — we can invoke the `hello` task without a name\!

    $ invoke hello
    Hello, world!

It gets confusing again if we try a positional parameter though.

    $ invoke hello Canute
    No idea what 'Canute' is!

And that’s why I prefer explicit invocations. But if you must know:

- Parameters without defaults *can* be specified by position rather than name.
- Parameters with defaults *must* be specified by name.

#### Running multiple tasks

Thankfully Invoke supports another useful feature of Make: requesting
more than one task at a time.

<aside class="admonition note">
    <p class="admonition-title">Note</p>

Took me years to learn `make build && make test && make install` could
be said `make build test install`

</aside>

Let’s add a setup task.

``` python
@task
def setup(c):
    """Get things ready for hello"""
    print("Creating the world")

...
```

We can ask Invoke to run both of them.

    $ invoke setup hello --name Enobarbus
    Creating the world
    Hello, Enobarbus!

#### Pre-tasks

If we find ourselves running the same tasks in the same sequence all the
time, we may be describing a dependency. Invoke lets us make the
dependency explicit.

``` python
@task(
    pre=[setup],
    help={"name": "Who or what is being greeted (default {DEFAULT_NAME})"},
)
def hello(c, name=DEFAULT_NAME):
    ...
```

The decorator takes `pre` as a list of task names. Invoke calls each of
these pre-tasks in order — using their default options if any — before
calling the specified task.

<aside class="admonition note">
    <p class="admonition-title">Note</p>

Make sure your pre-tasks have been defined *before* listing them in `pre`!

</aside>

    $ invoke hello
    Creating the world
    Hello, world!

Pre-tasks can be chained: if `setup` had its own dependencies, they
would be called before `setup`. Invoke’s documentation on [how tasks
run](http://docs.pyinvoke.org/en/stable/concepts/invoking-tasks.html#how-tasks-run)
explains task dependencies much better than I could.

#### Setting the default task

We have default parameters. What about default tasks?

Sure thing. Just let the decorator know.

``` python
@task(
    setup,
    default=True,
    help={"name": f"Who or what is being greeted (default 'world')"},
)
def hello(c, name="world"):
    ...
```

Run `invoke` without specifying a task, and it calls `hello` using
default parameters.

    $ invoke
    Creating the world
    Hello, world!

Thankfully Invoke mentions its default when listing tasks.

    $ invoke --list
    Available tasks:

      hello    Print the standard greeting
      setup    Get things ready for hello

    Default task: hello

You can’t pass task arguments to the default task. Why? Well, once you
add an argument you’re no longer asking for default behavior.

    $ invoke --name Rapunzel
    No idea what '--name' is!

### A useful task

Here’s what we have for our "Hello World" `tasks.py` file.

**`tasks.py`**

```python
"""Tasks for exploring Invoke"""

from invoke import task

DEFAULT_NAME = "world"


@task
def setup(c):
    """Get things ready for hello"""
    print("Creating the world")


@task(
    pre=[setup],
    default=True,
    help={"name": "Who or what it being greeted (default {DEFAULT_NAME})"},
)
def hello(c, name=DEFAULT_NAME):
    """
    Print the standard greeting

    "Hello world" is the classic first program to see what a language looks like.
    So of course I used it to understand Invoke.
    """
    print(f"Hello, {name}!")
```

It’s all nice and educational, but there isn’t anything useful yet.
That’s the problem with "Hello World". It can only give us the general
idea.

I’ll wrap up today by starting a fresh `tasks.py` for my Hugo site.

What am I doing most often while developing my site? At some point I
need to preview the site, right? Need to make sure the layout and
content looks how I expect.

That’s the answer I was looking for: running the Hugo server in drafts
mode. That will be my first site task. Let’s make it the default while
we’re at it.

Hugo’s built-in development
[server](https://gohugo.io/commands/hugo_server/) takes many options,
but I care about these:

    -D, --buildDrafts   include content marked as draft
    --navigateToChanged navigate to changed content file on live browser reload
    --bind string       interface to which the server will bind (default "127.0.0.1")

That way I can see the post I’m writing, and can preview from my phone
if needed. Assuming my phone is on local wifi, which it usually is.

``` python
"""Tasks for managing my Hugo site."""

from invoke import task

@task(default=True)
def server(c):
    """Run hugo server in drafts mode"""
    c.run("hugo server --buildDrafts --navigateToChanged --bind 0.0.0.0")
```

We’re finally using the
[context](http://docs.pyinvoke.org/en/stable/api/context.html) object\!
Invoke’s context holds details about the environment our tasks run in.
Most important for today, they give us a way to
[run](http://docs.pyinvoke.org/en/stable/api/context.html#invoke.context.Context.run)
shell commands.

    $ invoke server
    SHOW_INFO=1 hugo server --buildDrafts --bind 0.0.0.0 --navigateToChanged
    Building sites …
                       |  EN
    -------------------+-------
      Pages            | 1114
      Paginator pages  |    7
      Non-page files   |  452
      Static files     |   25
      Processed images | 1338
      Aliases          |  452
      Sitemaps         |    1
      Cleaned          |    0

    Built in 4092 ms
    Watching for changes in /home/randomgeek/Sites/random-geekery-blog/{archetypes,content,data,layouts,static,themes}
    Watching for config changes in /home/randomgeek/Sites/random-geekery-blog/config.toml
    Environment: "development"
    Serving pages from memory
    Running in Fast Render Mode. For full rebuilds on change: hugo server --disableFastRender
    Web Server is available at http://localhost:1313/ (bind address 0.0.0.0)
    Press Ctrl+C to stop

Technically a
[Runner](http://docs.pyinvoke.org/en/stable/api/runners.html#invoke.runners.Runner)
subclass takes care of running the shell command. We don’t have to care
about that though. We can pass a command string to `c.run` and let *it*
care.

*Now* I feel like I can post this.

## What’s next?

How about the rest of the workflow? Let me get back to you on that. I
need to reread my Makefile.

As for you, why not check out [Invoke](https://www.pyinvoke.org/) and
set up a `tasks.py` to drive your own workflow? It’s fun\!
