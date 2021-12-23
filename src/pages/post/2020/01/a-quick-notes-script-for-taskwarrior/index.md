---
aliases:
- /2020/01/12/a-quick-notes-script-for-taskwarrior/
category: Programming
cover_image: cover.png
date: 2020-01-12
draft: false
layout: layout:PublishedArticle
slug: a-quick-notes-script-for-taskwarrior
tags:
- taskwarrior
- python
title: A Quick Notes Script for Taskwarrior
updated: 2020-01-13
uuid: 2a29788c-e66c-47a1-a706-5eae3b9b0351
---

I need more than annotations for my [Taskwarrior](/tags/taskwarrior)
tasks. Let’s write some [Python](/tags/python)!

:::note

I labeled this as part of the [Taskwarrior
Babysteps](/series/taskwarrior-babysteps) series at first. Really this
post is more about Python code than task management.

:::

It’s the weekend, and I have a task that started with [a
tweet](https://twitter.com/brianwisti/status/1210771041783447553).

<blockquote class="twitter-tweet">
  <p lang="en" dir="ltr">
    The more blogs the merrier.<br /><br />
    And especially noteworthy: introduce your readers to RSS. My &quot;follow&quot; page assumes potential blog readers know RSS, but TBH that&#39;s not a safe assumption in 2020.<br /><br />
    So blurbed goal:<br /><br />
    * have the RSS links<br />
    * explain what RSS is<br />
    * link to reading tools.
    <a href="https://t.co/xhqktOR3de">https://t.co/xhqktOR3de</a>
  </p>
  &mdash; brian wisti (@brianwisti)
  <a href="https://twitter.com/brianwisti/status/1210771041783447553?ref_src=twsrc%5Etfw">December 28, 2019</a>
</blockquote>
<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

People with blogs need to keep in mind that most people do not know how
blogs work. A little bit of explanatory text can go a long way towards
making your site easier to follow.

I plan to work on that today, but — well — there’s another problem too.

## What’s the problem?

What tasks am I working on right now? Let’s get the
[active](/post/2018/12/active-tasks-in-taskwarrior/) task report.

    $ task active

    ID  Started    Active Age P Project Tags        Due        Description
    232 2020-01-12 2min   2h  H         taskwarrior 2020-01-12 quick and easy notes script
    220 2020-01-12 51min  2w    Site    content     2020-01-11 describe RSS and link to
                                                               tools in Follow page
                                                                 2019-12-28 reference
                                                               https://twitter.com/brianwi-
                                                               sti/status/1210771041783447-
                                                               553

This is a mess. My task descriptions can get verbose. That makes my
reports look busy. Annotations give additional information, but at the
cost of cluttering the report even more.

The [edit](/post/2019/09/taskwarrior-editing-refinements/) view isn’t
any better, really.

    $ task 220 edit

`task edit` gives me something like this:

```
# Annotations look like this: <date> -- <text> and there can be any number of them.
# The ' -- ' separator between the date and text field should not be removed.
# A "blank slot" for adding an annotation follows for your convenience.
  Annotation:        2019-12-28 14:33:53 -- reference https:\/\/twitter.com\/brianwisti\/status\/1210771041783447553
  Annotation:        2020-01-12 13:43:40 --
```

I want some way of adding and reviewing information about a particular
task without cluttering my Taskwarrior reports.

:::note

Honestly [org](/tags/org-mode) mode provides all this functionality and more.
Someday I may even get comfortable enough to prefer it. But right now?
Taskwarrior and shell tools are easier for me.

:::

## What I need today

I need the ability to open a text file with notes for a specific task. I
shouldn’t have to find or name the file myself. If the file doesn’t
exist yet, it should be created.

## What I don’t need today

Things I’m sure will be useful at some point, but I don’t need *today*.

- Listing notes
- Adding metadata like task description or tags before editing
- Deleting notes
- Adding one note to multiple tasks
- Deep taskwarrior integration
- Configuration. For now, everything’s hard-coded in the script.
  Except `$EDITOR`.

## Let’s get to it.

I’m not good at Python for quick glue tasks. Maybe [Perl](/tags/perl)? I
need to learn how to do this in Python at some point. Let’s try anyways.

That will be today’s learning experience.

### Writing notes

> Given a task, open `$EDITOR` in a Markdown file for that task. The task
> can be indicated via ID, UUID, or a filter that returns a single task

How can we identify tasks consistently? IDs change as we complete tasks.
Task descriptions change as we modify them. Fortunately, Every task has
a [UUID](https://en.wikipedia.org/wiki/Universally_unique_identifier) —
a Universally Unique Identifier.

[`_get`]: https://taskwarrior.org/docs/commands/_get.html

The [`_get`][] command gives us access to specific attributes of a task.

    $ task _get 220.uuid
    7887cab7-5ec4-4e8f-a257-edbd28f61301

But how do I get this information *from Python*?

``` python
#!/usr/bin/env python

"""Manage Taskwarrior notes"""

import os

task_id = 220
task_uuid = os.popen(f"task _get {task_id}.uuid").read().rstrip()
print(f"Task {task_id} has UUID {task_uuid}")
```

    $ task-note.py
    Task 220 has UUID 7887cab7-5ec4-4e8f-a257-edbd28f61301

That wasn’t so hard. I got lost in
[subprocess](https://docs.python.org/3/library/subprocess.html) last
time I tried anything interesting with Python and processes. Turns out
[os.popen](https://docs.python.org/3/library/os.html#os.popen) provides
a relatively straightforward approach.

Where will I put my notes? Maybe `~/task-notes`. No,
`~/Dropbox/task-notes`. That way everything is synchronized across my
machines.

``` python
notes_dir = os.path.expanduser("~/Dropbox/task-notes")
os.makedirs(notes_dir, exist_ok=True)
print(f"Saving notes to {notes_dir}")
```

Later I might want to be more careful with directory creation. But
today’s guideline is "quick and dirty."
[os.makedirs](https://docs.python.org/3/library/os.html#os.makedirs)
will recursively create `notes_dir` if needed. Since I specified
`exist_ok=True`, we silently move on if `notes_dir` already exists.

I want the file to be named something like `UUID.md`.

``` python
notes_basename = f"{task_uuid}.md"
notes_file = os.path.join(notes_dir, notes_basename)
print(notes_file)
```

    $ task-note.py
    Task 220 has UUID 7887cab7-5ec4-4e8f-a257-edbd28f61301
    Saving notes to /home/randomgeek/Dropbox/task-notes
    /home/randomgeek/Dropbox/task-notes/7887cab7-5ec4-4e8f-a257-edbd28f61301.md

``` python
editor = os.environ["EDITOR"]
os.execlp(editor, editor, notes_file)
```

The various `exec*` functions of module
[os](https://docs.python.org/3/library/os.html) replace the Python
process with a new command. The suffixes indicate additional details.

- The `l` — that’s a lowercase `L` — simplifies the case when you know
  exactly what arguments to use. All I needed was `$EDITOR <file>`.
  `execl*` functions let me specify program arguments as arguments to
  the function itself.
- The `p` indicates that I expect `$EDITOR` to be somewhere in the
  current `$PATH`.

So [os.execlp](https://docs.python.org/3/library/os.html#os.execlp)
tells Python I’m running `editor`. I expect to find `editor` in my
environment path. The rest of the function arguments will be handed to
`editor`.

![Neovim launched by Python](task-notes-view.png)

Sweet. It worked!

<aside class="admonition">

Specifying the program twice confused me at first. Things clicked for me
when I tried the `v` variant:

``` python
os.execvp(editor, [editor, notes_file])
```

With v, you construct your program arguments with a list or tuple. Now
It looks we’re constructing the `ARGV` list — or
[sys.argv](https://docs.python.org/3/library/sys.html#sys.argv) in
Python. The program itself usually gets the first slot in `ARGV`. For
example, here’s sys.argv for my `task-note.py` invocation:

``` python
['/home/randomgeek/bin/task-note.py', '220']
```

Most user-facing programs hide that detail from you — even Vim.

``` vim
:echo argv()
['/home/randomgeek/Dropbox/task-notes/7887cab7-5ec4-4e8f-a257-edbd28f61301.md']
```

I *think* that’s what’s going on anyways.

I won’t lie. This `exec*` stuff is easier to say in Perl:

``` perl
exec($ENV{EDITOR}, $notes_file);
```

</aside>

## Generalize for any task

I learned what I needed to learn. Next is cleaning up and accepting
command line arguments.

[argparse](https://docs.python.org/3/library/argparse.html) will take
care of the command line arguments. Might as well replace `print` with
[logging](https://docs.python.org/3/library/logging.html) calls. You
know, just a little bit of tidying.

**`task-note.py`**

```python
#!/usr/bin/env python

"""Manage Taskwarrior notes"""

import argparse
import logging
import os
import sys

NOTES_DIR = "~/Dropbox/task-notes"
EDITOR = os.environ["EDITOR"]

logging.basicConfig(level=logging.DEBUG)

def write_note(task_id: int):
    """Open `$EDITOR` to take notes about task with ID `task_id`."""
    task_uuid = os.popen(f"task _get {task_id}.uuid").read().rstrip()

    if not task_uuid:
        logging.error(f"{task_id} has no UUID!")
        sys.exit(1)

    logging.debug(f"Task {task_id} has UUID {task_uuid}")

    notes_dir = os.path.expanduser(NOTES_DIR)
    os.makedirs(notes_dir, exist_ok=True)
    notes_basename = f"{task_uuid}.md"
    notes_file = os.path.join(notes_dir, notes_basename)
    logging.debug(f"Notes file is {notes_file}")

    if not os.path.exists(notes_file):
        logging.info("Adding description to empty notes file")
        task_description = os.popen(f"task _get {task_id}.description").read()

        with open(notes_file, "w") as f:
            f.write(f"description: {task_description}\n\n")
            f.flush()

    os.execlp(EDITOR, EDITOR, notes_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Write Taskwarrior notes")
    parser.add_argument('task_id', metavar='ID', type=int, help="ID of the task to note")
    args = parser.parse_args()

    write_note(args.task_id)
```

I know. I didn’t want task metadata yet. It quickly became obvious that
I would forget what task is involved unless I put *something*. So now
the script adds the task description to a header line the first time a
note is opened.

:::warning

Remember to `flush` your filehandles before handing control over to
external processes like [Vim](/tags/vim). Python takes care of files and
buffers on its own schedule. Launching an external process interrupts
Python’s schedule. So let Python know\!

:::

Also threw in some error checking after the first time I tried writing
notes for a nonexistent task.

## What’s Next?

- Keeping that description header current
- Adding other task data?
- Maybe a [UDA](https://taskwarrior.org/docs/udas.html) to integrate
  this more with Taskwarrior itself

But what’s really next is finishing that other task. Should be easier
now that I have my notes.