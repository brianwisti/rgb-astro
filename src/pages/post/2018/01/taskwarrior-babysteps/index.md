---
aliases:
- /2018/01/02/taskwarrior-due-dates/
category: tools
cover_image: cover.png
date: 2018-01-02 00:00:00
draft: false
layout: layout:PublishedArticle
series:
- Taskwarrior Babysteps
slug: taskwarrior-babysteps
tags:
- taskwarrior
title: Taskwarrior Due Dates
uuid: fada3e78-ba5c-44d5-9905-6d308249a1c7
---

I checked out some library books again. Time to correctly record their
due date in [Taskwarrior](https://taskwarrior.org).

The Taskwarrior documentation includes an excellent page on [using
dates](https://taskwarrior.org/docs/using_dates.html). This post just
takes what I need from that page.

## Due dates

Picked up some new stuff from the library the other day. Oh BTW I highly
recommend [The Girl from the Other
Side](https://www.goodreads.com/book/show/30139736-the-girl-from-the-other-side).
I already finished the first volume and put the second on hold.

Anyways, this stuff is due on January 20th. Up until now I used
[annotations and priorities](/post/2017/12/taskwarrior-priorities) to
remind me about the urgency and any calendar-related details. That
worked, in a clunky sort of way. I returned everything on time.

Thing is, Taskwarrior supports assigning due dates directly.

### Add a due date

Give a task a due date with `due:` and a date. Taskwarrior lets you
describe dates in [many
ways](https://taskwarrior.org/docs/named_dates.html). When in doubt, use
`yyyy-mm-dd`.

    $ task add return to library due:2018-01-20
    Created task 55.

The `next` report has a new column, but my library task gets lost in the
shuffle.

    $ task
    [task next]

    ID Age   P Project      Tag              Due Description                                     Urg
    51 2d    H fixmusic     homeops music        beet import all Sync Music                      7.91
     2 4w    H              blog taskwarrior     due dates                                       7.06
    46 3d    H              blog music           processing for basic lyrics video               6.92
    26 6d    M fitbit       code health          munge data into csv per type                    5.83
    32 5d    M fixmusic     homeops music        find itunes tracks not in Sync                  5.83
    33 5d    M fixmusic     homeops music        find itunes tracks not on MBP                   5.83
     1 4w    M              crochet              fingerless gloves                               4.87
     7 3w    M              home                 move my stuff upstairs                          4.83
    17 2w    M              home                 make flylady daily and weekly list              4.78
    34 5d    M              home                 evaluate menu planning routine                  4.73
    44 4d    M              learn                run py processing from cli                      4.72
    45 3d    M              homeops              get cat-6 for new office                        4.72
    19 13d   L fixmusic     homeops music        filter duplicate tracks                         3.77
    37 4d    L lyricsvideos learn music          simple text on Linux                            3.72
    39 4d    L lyricsvideos learn music          analyze with libROSA music                      3.72
    24 8d    L fitbit       health               see activity when closest to weight goal        3.64
    11 2w    L              crochet home         door panel                                       3.6
                                                   2017-12-27 maybe use
                                                 http://crochetandknitting.com/curtains.htm
    23 11d   L              homeops music        restore backup                                  3.56
                                                   2017-12-25 windows sucks find that hard drive
    22 12d   L              home                 living room curtains                            3.47
                                                   2017-12-20 dimensions 94.25 wide 56.5 high
    31 5d    L              art blog code        circular grid generation                        2.83
    55 1min  L              blog taskwarrior     recurrences                                      2.7
     9 2w    L              music                experiment with setting itunes play stats        2.7
    10 2w    L              blog                 create links section                             2.7
    18 13d   L              music                merge rating files                              2.67
    47 3d    L              homeops              move pics to Sync                               2.62
    53 9min                                  2w  return to library                                2.4
    40 4d      lyricsvideos learn music          processing text timed by libROSA                1.92
    41 4d      lyricsvideos learn music          processing visualization manually timed         1.92
    42 4d      lyricsvideos learn music          processing visualization timed by libROSA       1.92
    36 5d                   blog taskwarrior     custom priority report                          0.93

    30 tasks

Where is it? Oh there it is.

### List tasks with a due date

Fortunately, Taskwarrior lets me use filters. `due.any:` filters tasks
to those which have an assigned due date.

    $ task due.any:
    [task next ( due.any: )]

    ID Age   Due Description       Urg
    53 12min 2w  return to library  2.4

## Waiting tasks

A friend and I chatted a minute ago. We plan to meet up on Thursday. Why
not add that as a task, since I have this blog post open?

    $ task add meet rainy due:thursday

Taking advantage of Taskwarrior’s [date
flexibility](https://taskwarrior.org/docs/named_dates.html) is often
quicker than remembering a calendar date.

    $ task due.any:
    [task next ( due.any: )]

    ID Age   Due Description       Urg
    54 26s   2d  meet rainy        7.83
    53 14min 2w  return to library  2.4

I don’t need a big urgent reminder for that one though. Just remind me
on Thursday that we’re meeting Thursday.

    $ task 54 modify wait:due
    Modifying task 54 'meet rainy'.
    Modified 1 task.

Now it doesn’t show up in my due list or in my regular task list. I
assume it will appear on Thursday morning.

Of course there’s a report available to see only waiting tasks.

    $ task waiting

    ID Age  Wait       Remaining Due        Description
    54 7min 2018-01-04        2d 2018-01-04 meet rainy

    1 task

## Scheduled tasks

As long as I’m sitting here: how about a credit card bill?

    $ task add credit card +pay due:2018-01-22
    Created task 56.
    $ task due.any:
    [task next ( due.any: )]

    ID Age  Tag Due Description       Urg
    56 2min pay 2w  credit card        3.2
    53 1h       2w  return to library  2.4

    2 tasks

I don’t get paid until the 15th, so there’s no point fussing about it
right now.

What happens if I schedule the credit card for payday?

    $ task 56 modify scheduled:15th
    Modifying task 56 'credit card'.
    Modified 1 task.

The task still shows up in `next`, which is fine. I want to stay aware
of it. I can use the `scheduled` filter to see tasks which have a
scheduled date.

    $ task scheduled
    [task next ( scheduled )]

    ID Age  Tag Due Description Urg
    56 4min pay 2w  credit card  3.2

    1 task

What about all the non-waiting tasks that are due this month? Time for
my first [virtual tag](https://taskwarrior.org/docs/tags.html#supported)
— provided by Taskwarrior as a shorthand for specific complex queries.
The `+MONTH` virtual tag filters on tasks that are due this month.

    $ task +MONTH
    [task next ( +MONTH )]

    ID Age  Tag Due Description       Urg
    56 6min pay 2w  credit card        3.2
    53 1h       2w  return to library  2.4

    2 tasks

This has been a quick post, but I still want something kind of cool for
the opening screenshot.

Oh I know: how about a calendar?

    $ task calendar