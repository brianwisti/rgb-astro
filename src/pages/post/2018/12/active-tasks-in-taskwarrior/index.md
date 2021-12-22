---
aliases:
- /2018/12/01/active-tasks-in-taskwarrior/
category: tools
cover_image: cover.png
date: 2018-12-01 00:00:00
draft: false
layout: layout:PublishedArticle
series:
- Taskwarrior Babysteps
slug: active-tasks-in-taskwarrior
tags:
- taskwarrior
title: Active Tasks in Taskwarrior
uuid: 3f85998f-79d5-40ec-9cc2-13764481dc1f
---

<aside class="admonition tldr">
<p class="admonition-title">tl;dr</p>

Use the `start`, `stop`, and `active`
[Taskwarrior](https://taskwarrior.org/) commands to manage what you’re
doing right now.

</aside>

I use Taskwarrior’s [priority](/post/2017/12/taskwarrior-priorities)
system to show what I want to be working on now. What if there are
several things I want to be working on right now? Even with my priority
rules, I still find myself drawn to the lower priority tasks that are
more interesting. Realistically, I can only do one thing at a time. How
do I remind myself which task should have my active attention?

## `task start`

Easy! Use the `start` command.

    $ task 72 start

This assigns the virtual tag `+ACTIVE` to the task. The regular task
report highlights active tasks, as well as showing a new \`\`Active''
column indicating how long the task has been active.

    $ task

    ID Active Age  P Project Tag              Description                       Urg
    72 12min  1h   H         blog taskwarrior start, stop, and active           10.9
    61        7d   H         crochet gift     crochet crown for mom             6.94
    47        3mo  M         art              upload felix to dbh               5.35
    35        6mo  L site    layout           add Year link to content headers  4.75
    ⋮

Being active increases the urgency of a task, bubbling it up to the top
in this report. I can also request to see *only* the active tasks.

## `task active`

The `active` report shows me only those tasks that have been assigned
the `+ACTIVE` virtual tag. Very handy in my blog \[context\]\[\], when
many curious ideas are tugging at my easily distracted brain and I need
to see just what I’m doing.

    $ task active

    ID Started    Active Age P Project Tag              Description                      Urg
    72 2018-12-01 14min  1h  H         blog taskwarrior start, stop, and active          10.9

You can start as many tasks as you like. I find that distracting.
Taskwarrior helps me focus, and starting a dozen different tasks feels
like the opposite of focusing. I’ll limit `+ACTIVE` for *one* task that
I intend to be working on *at this moment*.

## `task stop`

I’m still writing this post, but I need to do something else real quick.
I could just `start` that other task, but that blows a hole in my “one
active task at a time” personal rule. Instead I’ll show that my
attention is elsewhere with `stop`.

    $ task 72 stop
    Stopping task 72 'start, stop, and active'.
    Stopped 1 task.

Okay excuse me for a few minutes.

    $ task 73 start
    Starting task 73 'walk the dog'.
    Started 1 task.
    ⋮
    $ task 73 done
    Completed task 73 'walk the dog'.
    Completed 1 task.
    You have more urgent tasks.

*You have more urgent tasks.* — Yeah, tell that to the dog.

    $ task 72 start
    Starting task 72 'start, stop, and active'.
    Started 1 task.

Now where was I? Oh yeah. I wanted to mention time tracking.

## Taskwarrior is not for time tracking

Those `start` and `stop` commands show up in the task’s modification
history, including timestamps and information about duration of active
status.

    $ task 72
    No command specified - assuming 'information'.

    Name          Value
    ID            72
    Description   start, stop, and active
    Status        Pending
    Entered       2018-12-01 12:27:44 (2h)
    Start         2018-12-01 14:43:08
    Last modified 2018-12-01 14:43:08 (17min)
    Tags          blog taskwarrior
    Virtual tags  ACTIVE PENDING READY TAGGED UDA UNBLOCKED PRIORITY
    UUID          f5f87929-a4e8-4af4-bb38-cf142235f693
    Urgency       10.9
    Priority      H

        active              1 *    4 =      4
        tags              0.9 *    1 =    0.9
        UDA priority.H      1 *    6 =      6
                                       ------
                                         10.9

    Date                Modification
    2018-12-01 13:25:51 Priority changed from 'L' to 'M'.
    2018-12-01 13:41:53 Priority changed from 'M' to 'H'.
    2018-12-01 13:42:01 Start set to '2018-12-01 13:42:01'.
    2018-12-01 13:59:06 Start deleted (duration: PT17M5S).
    2018-12-01 14:43:08 Start set to '2018-12-01 14:43:08'.

Even though there are timestamps in the task info, this is clumsy for
time tracking. The Taskwarrior team also wrote
[Timewarrior](https://taskwarrior.org/docs/timewarrior), a command line
tool dedicated to tracking and reporting time. It even hooks into
Taskwarrior’s `start` and `stop` commands, giving you time management
with your task management.

I may explore Timewarrior eventually, but for now I am content using
Taskwarrior alone to show what I’ve done with `completed`, what I’m
doing right now with today’s new commands, and what I want to do (with
everything else).