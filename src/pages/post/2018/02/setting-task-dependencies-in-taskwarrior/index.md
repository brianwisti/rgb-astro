---
aliases:
- /2018/02/19/setting-task-dependencies-in-taskwarrior/
category: tools
cover_image: cover.png
date: 2018-02-19 00:00:00
description: 'I''m not done reading a book until I finish the exercises. Taskwarrior
  can help me remember.

  '
draft: false
layout: layout:PublishedArticle
series:
- Taskwarrior Babysteps
slug: setting-task-dependencies-in-taskwarrior
tags:
- taskwarrior
title: Setting Task Dependencies in Taskwarrior
uuid: 364c3bf7-fc22-492b-b24e-39fcbd902cf5
---

I recently realized I could track my reading in
[Taskwarrior](https://taskwarrior.org/), since I use it to track so many
other things.

    $ task +readlist

    ID Age   P Tag                    Description                        Urg
    67 22h   H community readlist     Forge Your Future with Open Source  6.9
    70 29min M fiction readlist       Binti                               4.8
    71 21min M health readlist        Emmerich Keto Guide                 4.8
    74 16min   health readlist reread The Healthy Programmer                1
    63 6d      dev readlist           Practical Data Science with R      0.93
    72 19min   dev readlist           Think Stats                         0.9
    73 17min   dev readlist           Understanding Computation           0.9
    75 16min   home readlist          Sink Reflections                    0.9

I use [Priority](/post/2017/12/taskwarrior-priorities) to show what I’m
reading right now. The highest priority goes to the book which I intend
to finish next.

[Forge Your Future with Open
Source](https://pragprog.com/book/vbopens/forge-your-future-with-open-source)
is my current main read. The book guides you through making your first
open source community contributions. It includes exercises to help you
make your best contribution.

I want to complete these exercises, but I know I won’t unless I create
some kind of reminder.

I’ll add tasks for the exercises described so far.

    $ task add +community Set FOSS contribution goals
    $ task add +community Set FOSS project requirements
    $ task add +community Collect FOSS candidate projects
    $ task add +community Select FOSS project

There will certainly be more exercises. I will create tasks for them as
they come up.

Assigning a shared [project](/post/2017/12/taskwarrior/#_projects) makes
their connection clearer.

    $ task 67,76-79 modify project:fosscontrib
      - Project will be set to 'fosscontrib'.
    Modify task 67 'Forge Your Future with Open Source'? (yes/no/all/quit) all
    Modifying task 67 'Forge Your Future with Open Source'.
    Modifying task 76 'Set FOSS contribution goals'.
    Modifying task 77 'Set FOSS project requirements'.
    Modifying task 78 'Collect FOSS candidate projects'.
    Modifying task 79 'Select FOSS project'.
    Modified 5 tasks.
    The project 'fosscontrib' has changed.  Project 'fosscontrib' is 0% complete (5 of 5 tasks remaining).

All right but how do I show the dependencies? Let’s describe them first.

- I must collect candidate projects before I can select a FOSS
  project.
- I must set my FOSS project requirements before I can collect
  candidate projects.
- I must define my personal FOSS contribution goals before I can set
  my project requirements.
- I must complete all the tasks before I can mark the book as complete

Each item depends on another being completed before I can work on it. It
is *blocked*, and the task it depends on is *blocking* it.

Use the `depends` attribute to show when one task blockeds another.

    $ task 79 modify depends:78
    Modifying task 79 'Select FOSS project'.
    Modified 1 task.
    Project 'fosscontrib' is 0% complete (5 of 5 tasks remaining).

What does that look like now?

    $ task project:fosscontrib

    ID Age   Deps P Project     Tag                Description                        Urg
    78 25min        fosscontrib community          Collect FOSS candidate projects     9.8
    67 23h        H fosscontrib community readlist Forge Your Future with Open Source  7.9
    76 25min        fosscontrib community          Set FOSS contribution goals         1.8
    77 25min        fosscontrib community          Set FOSS project requirements       1.8
    79 22min 78     fosscontrib community          Select FOSS project                -3.2

    5 tasks

The report shows a new `Deps` column, indicating dependencies. The `Urg`
column shows that "Select FOSS project" gets a lower priority — it’s
blocked by "Collect FOSS candidate projects", which now has a higher
priority because it blocks a task.

The report visually highlights the blocking task while downplaying the
blocked task. This is easier to show with a screenshot.

![fosscontrib project with one dependency set](single-dependency.png)

Let’s assign the rest of the dependencies.

    $ task 78 modify depends:77
    $ task 77 modify depends:76

Wait a minute.

How do I describe the book’s dependencies? I want to say it depends on
all of these tasks, but that’s not possible in Taskwarrior — unless
there’s an [extension](https://taskwarrior.org/tools/), but I’m not
ready for those yet.

There’s a missing task, isn’t there? Completing all the exercises in the
book is its own task. *That* is what finishing the book depends on.

    $ task add Complete all tasks in book priority:H project:fosscontrib depends:79
    Created task 80.
    The project 'fosscontrib' has changed.  Project 'fosscontrib' is 0% complete (6 of 6 tasks remaining).

Today it depends on selecting a FOSS project. That will change as the
book presents new exercises. This is a small inconvenience that makes
the tasks' overall relationships clearer to *me*. I am the important
audience for my personal task list.

Now I can correctly describe what I must do to complete the book.

    $ task 67 modify depends:80
    Modifying task 67 'Forge Your Future with Open Source'.
    Modified 1 task.

What does this project look like now?

    $ task project:fosscontrib

    ID Age Deps P Project     Tag                Description                        Urg
    80 53s 79   H fosscontrib                    Complete all tasks in book           10
    76 1h         fosscontrib community          Set FOSS contribution goals         9.8
    77 1h  76     fosscontrib community          Set FOSS project requirements       4.8
    78 1h  77     fosscontrib community          Collect FOSS candidate projects     4.8
    79 1h  78     fosscontrib community          Select FOSS project                 4.8
    67 23h 80   H fosscontrib community readlist Forge Your Future with Open Source  2.9

    6 tasks

Right but what does it *look* like?

![taskwarrior report](cover.png "I have my work cut out for me")

The report deemphasizes everything but the task that blocks everything
else. You can see some urgency math going on in that last column where
tasks are both blocking and blocked.

## New virtual tags!

Dependencies give us new virtual tags to filter reports based on task
dependencies.

### `+BLOCKED`

The `+BLOCKED` virtual tag filter includes only those tasks which depend
on another task.

    $ task +BLOCKED

    ID Age  Deps P Project     Tag                Description                        Urg
    80 3min 79   H fosscontrib                    Complete all tasks in book           10
    77 1h   76     fosscontrib community          Set FOSS project requirements       4.8
    78 1h   77     fosscontrib community          Collect FOSS candidate projects     4.8
    79 1h   78     fosscontrib community          Select FOSS project                 4.8
    67 23h  80   H fosscontrib community readlist Forge Your Future with Open Source  2.9

    5 tasks

### `+BLOCKING`

The `+BLOCKING` virtual tag filter includes only those tasks which I
assigned as dependencies for another task.

    $ task +BLOCKING

    ID Age  Deps P Project     Tag       Description                     Urg
    80 4min 79   H fosscontrib           Complete all tasks in book        10
    76 1h          fosscontrib community Set FOSS contribution goals      9.8
    77 1h   76     fosscontrib community Set FOSS project requirements    4.8
    78 1h   77     fosscontrib community Collect FOSS candidate projects  4.8
    79 1h   78     fosscontrib community Select FOSS project              4.8

    5 tasks

## What now?

By looking at what *is* blocking and is *not* blocked, you can focus on
the tasks that block everything else.

    $ task +BLOCKING -BLOCKED

    ID Age Project     Tag       Description                 Urg
    76 4h  fosscontrib community Set FOSS contribution goals  9.8

    1 task

I should start working on those goals so I can finish that book.