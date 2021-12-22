---
category: Programming
description: In which I sneak a little quality control into my site utility scripts
draft: true
format: md
layout: layout:Article
tags:
- python
- site
title: Python Doctest
uuid: 7fa4042f-20b8-43cf-8eb2-a1cb570972e8
---

Let’s use doctests to make sure this Python script I’m changing does
what I expect\!

Fiddling with my site utility scripts this morning. I decided to move
announcements — those social network links at the end of some
posts — from a data file into the front matter of the content
itself. Makes it a little easier for me if I end up rearranging my site
layout later.

I’ve been meaning to talk about those scripts for a while. Maybe someday
I’ll do a proper introduction. It’s a lot of functionality for managing
my Hugo site, inspired by frew’s Perl utilities. I use Python instead of
Perl — not for any innate virtue, but because I’m working a Python job
these days and need the practice.

Python 3.7, Pipenv, records, pyyaml, toml

<aside>
Yes, mention basics of environment: pipenv, Python 3.7
</aside>

## What am I doing

## Why

### How much Python do I have supporting my site

Hang on let me clean up the stuff I don’t use. Okay, what’s left?

    $ find ./scripts -name '*.py' -exec wc '{}' \+
       63   184  1969 ./scripts/demo-theme.py
      174   589  5882 ./scripts/public_weigh_site.py
      247   638  6969 ./scripts/find-announcements.py
      105   310  3834 ./scripts/announce.py
      220   568  6909 ./scripts/query.py
      281   926 10674 ./scripts/weigh_site.py
     1090  3215 36237 total

A thousand lines isn’t a lot, but it’s more than I can hold in my head
at once. No wonder I got nervous about adding more.

### Why doctest

These are scripts. They don’t have a coherent project structure. Sure,
they should. But I need to add functionality *today*. And I need some
confidence that this new functionality will work correctly *before* I
use it.

Plus, one school of thought believes tests are documentation. They’re
wrong, of course. Documentation is documentation. Tests are code. But
documentation often includes code samples, showing how to use a library
or script. And if you always check to make sure those samples are
correct, then your documentation becomes a test\!

If you don’t always check, then your documentation usually becomes a
lie.

## How

`query.py` is the script that’s sort of turning into a library. At its
core, it lets me use SQL queries to load information about the site.

    $ python scripts/query.py 'select service, count(service) from announcements group by service'
    service |count(service)
    --------|--------------
    facebook|5
    mastodon|49
    twitter |115

That’s where it started, anyways. It got more complicated than that.
`query.py` even gets loaded as a library by a couple of other utility
scripts.

It’s awful. I know. This stuff just sort of happens sometimes. I’m
trying to fix it, in my own way.

That’s where Doctest comes in.

### Usage: with no tests

The most convenient way for me to test `query.py` is to run it, but tell
Python to also load Doctest.

    $ python -m doctest -v scripts/query.py
    $

Oh good it *doesn’t* run my script. I would have gotten an error
message.

Okay, I need a little more than that. The `-v` flag puts Doctest in
verbose mode.

    $ python -m doctest -v scripts/query.py
    8 items had no tests:
        query
        query.add_contents
        query.build_permalink
        query.create_schema
        query.main
        query.site_config
        query.site_db
        query.update_frontmatter
    0 tests in 8 items.
    0 passed and 0 failed.
    Test passed.

In a perfect world, testing confirms what you already know. We confirmed
that I have no tests. I already knew that. Therefore this is a perfect
world!

No? Oh well.

### Usage: test a function that works

Look, I can be all proper TDD with "write a test that fails and make it
pass" but I’m trying to remember how doctest works in the first place.

``` python
def site_config(filename):
    """Load my site configuration files"""
    return toml.load(filename)
```

Easy enough, right? Let’s see what that looks like in an interactive shell.

    $ python
    Python 3.7.4 (default, Sep 11 2019, 21:09:05)
    [GCC 9.1.0] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>> from scripts.query import site_config
    >>> config = site_config('config.toml')
    >>> config['BaseURL']
    'https://randomgeekery.org'
    >>>

A doctest is basically — okay not basically. A doctest *is* that
interactive session. I can copy it over to my function docstring. The
only modification is that I don’t need `import` since the test will
already be in the module’s namespace.

``` python
def site_config(filename):
    """Load my site configuration files

    >>> config = site_config('config.toml')
    >>> config['BaseURL']
    'https://randomgeekery.org'
    """
    return toml.load(filename)
```

The report looks a little different now\!

    $ python -m doctest -v scripts/query.py
    Trying:
        config = site_config('config.toml')
    Expecting nothing
    ok
    Trying:
        config['BaseURL']
    Expecting:
        'https://randomgeekery.org'
    ok
    6 items had no tests:
        query
        query.add_contents
        query.build_permalink
        query.create_schema
        query.main
        query.site_db
    1 items passed all tests:
      2 tests in query.site_config
    2 tests in 7 items.
    2 passed and 0 failed.
    Test passed.

Notice that `Expecting nothing`? Doctest is pretty literal. If there was an
error or a logging message loading config, displaying that message would cause
a test failure. There are ways around that, but I’m not worried about that
today. I’m also not worried about the fact that the config file and `BaseURL`
are specific to my site. I’m testing that it works for me, not that it will
work for everyone.

### Usage: testing a new function

<aside>
Clarify here
</aside>

I forgot the functionality I wanted to add. Hang on. Oh right. I want to
update the frontmatter of a content file from `query.py`. After spending
way too much time thinking about this, I realize there are several
distinct steps:

  - Load the original frontmatter and body text from a content file

  - Change some details about the frontmatter

  - write the combined frontmatter and body text to a file

Naturally, I started backwards.

### Writing frontmatter and body text to a file

Any file. Executive decision so that I could confirm functionality
without breaking existing content.

### Write a test that fails


``` python
def write_content_file(path, frontmatter, body_text):
    """Write frontmatter and body text to the specified path, overwriting if present.

    >>> fm = {'title': 'doctest is still fun'}
    >>> body_text = "Doctest is fun!"
    >>> path = 'tmp/doctest-is-fun.md'
    >>> write_content_file(path, fm, body_text)
    >>> print(open(path).read())
    ---
    title: doctest is still fun
    ---
    Doctest is fun!
    """
```

It fails, of course. There’s no code in the function. So there isn’t
even a file to compare\!

    $ python -m doctest scripts/query.py
    **********************************************************************
    File "scripts/query.py", line 207, in query.write_content_file
    Failed example:
        print(open(path).read())
    Exception raised:
        Traceback (most recent call last):
          File "/home/random/.pyenv/versions/3.7.4/lib/python3.7/doctest.py", line 1329, in __run
            compileflags, 1), test.globs)
          File "<doctest query.write_content_file[4]>", line 1, in <module>
            print(open(path).read())
        FileNotFoundError: [Errno 2] No such file or directory: 'tmp/doctest-is-fun.md'
    **********************************************************************
    1 items had failures:
      1 of   5 in query.write_content_file
    ***Test Failed*** 1 failures.

### Make it pass

``` python
def write_content_file(path, frontmatter, body_text):
    """Write frontmatter and body text to the specified path, overwriting if present.

    >>> fm = {'title': 'doctest is still fun'}
    >>> body_text = "Doctest is fun!"
    >>> path = 'tmp/doctest-is-fun.md'
    >>> write_content_file(path, fm, body_text)
    >>> print(open(path).read())
    ---
    title: doctest is still fun
    ---
    Doctest is fun!
    """
    yaml_text = yaml.dump(frontmatter)
    delimiter = "---\n"

    # Write yaml and content to path
    new_content = f"{delimiter}{yaml_text}{delimiter}{body_text}"
    with open(path, "w") as f:
        f.write(new_content)
```

Of course, if I want to be sure `write_content_file` is behaving
correctly, I need to make sure `tmp/doctest-is-fun.md` doesn’t exist
before the test runs. Rather than putting any setup or teardown logic in
`query.py` I’m going to do that with the shortest path I can think of: a
`make` target.

```
clean_tmp:
    rm -f tmp/*

doctest: clean_tmp
    $(PYTHON) -m doctest scripts/query.py
```

## Why not

I wouldn’t want to use doctests to describe complex interactions.
pytest — or unittest, if you must — serves better for that.
