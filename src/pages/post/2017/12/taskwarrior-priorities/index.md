---
aliases:
- /2017/12/25/taskwarrior-priorities/
caption: '`task` report with a column showing priority levels'
category: tools
cover_image: cover.png
date: 2017-12-25
draft: false
layout: layout:PublishedArticle
series:
- Taskwarrior Babysteps
slug: taskwarrior-priorities
tags:
- taskwarrior
title: Taskwarrior Priorities
uuid: 7e0321e9-f2c7-410a-a477-25990378b00f
---

[Taskwarrior]: /tags/taskwarrior

Merry Christmas!
Time to organize my [Taskwarrior][] tasks.

My more focused approach to Taskwarrior is working well.
I add a task when I get an idea, and mark it `done` sometime after I finish.
Annotations let me add noteworthy details.
Tags and projects help both for organizing tasks and describing them.
A task bubbles up to the top of `task next` as I add more information to it.

    $ task -work
    [task next ( -work )]

    ID Age  Project Tag              Description                                   Urg
    26 9min fitbit  health           get fitbit data                               2.7
                                       2017-12-24 can only grab 31 days at a time
                                       2017-12-24 want all data back to 2016-01
     2 3w   ruana   blog knitting    blog about vest                              2.02
    27 8min fitbit  health           see activity when closest to weight goal      1.8
    28 7min fitbit  health           make 2018 exercise plan                       1.8
    24 3d           home             living room curtains                         1.62
                                       2017-12-20 dimensions 94.25 wide 56.5 high
     3 3w           blog taskwarrior due dates, recurrences                       1.02
    12 9d           crochet home     door panel                                   0.95
    15 7d           learn music      submit to acousticbrainz                     0.94
    18 6d           blog taskwarrior Priorities                                   0.93
     1 3w           crochet          fingerless gloves                            0.92
     8 2w           home             move my stuff upstairs                       0.88
    10 10d          music            experiment with setting itunes play stats    0.85
    11 10d          blog             create links section                         0.85
    16 6d           music            music server                                 0.83
    17 6d           learn            try timewarrior                              0.83
    19 6d           home             make flylady daily and weekly list           0.83
    20 4d           music            merge rating files                           0.82
    21 4d           music            filter duplicate tracks                      0.82
    22 4d           knitting         circular hat variant                         0.82
    25 3d           music            restore backup                               0.82

That bubbling behavior gets in the way sometimes.

I created some tasks for playing with my Fitbit data and added relevant annotations.
Taskwarrior follows a rule of "it must be important if you’re talking so much about it,"" and dutifully puts those tasks high on the list.

[Duplicates]: http://beets.readthedocs.io/en/v1.4.6/plugins/duplicates.html

Thing is, right now I care more about fixing my music library.
Long story, but the moral of _that_ tale is be careful with Beets and the [Duplicates] plugin.
I have slightly different versions of the library on each of my machines, and a backup with all of the music but none of the Beets import information.
I could make a project out of it, but it’s more of a thing I poke at when I can.

[Priority]: https://taskwarrior.org/docs/priority.html

Anyways — I want my `next` report to more closely resemble my current priorities.
I can do that by manually setting [Priority][] for each of my tasks.

## Task priority

Priority can be added to any task as an attribute, using `priority:` followed by the Priority you wish to assign.
Priority also works as a filter for your reports.
The default choices are `H`, `M`, `L`, and none at all — to remove a Priority.

    $ task add return library books priority:M
    Created task 29.
    $ task modify 18 priority:H
    Modifying task 18 'Priorities'.
    Modified 1 task.

Looking at the first few entries of `next` shows me the effect of setting Priority.

    $ task -work
    [task next ( -work )]

    ID Age  P Project Tag              Description                                   Urg
    18 6d   H         blog taskwarrior Priorities                                   6.93
    29 3min M                          return library books                          3.9
    26 1h     fitbit  health           get fitbit data                               2.7
                                         2017-12-24 can only grab 31 days at a time
                                         2017-12-24 want all data back to 2016-01

[Urgency]: https://taskwarrior.org/docs/urgency.html

I see a new column reflecting that I now describe some tasks with Priority.
Over on the end, [Urgency][] jumps for tasks with any Priority at all.
`H` Priority tasks get a large boost.
But what do these Priority values *mean*?

Priority means something different for everyone.
The basic idea is the higher a task’s Priority is, the more important it is to me.

Here’s how I use Priority values for now.

| Priority | Represents | Description
| -------- | ---------- | -----------
| `H`      | High       | I am — or want to be — working on it right now.
| `M`      | Medium     | I want to work on this soon.
| `L`      | Low        | I want to work on this eventually.
| *empty*  | None       | I haven’t thought about it.

My usage will change as I learn more about Taskwarrior but this works.

I don’t need to think too much about priority when I’m just adding to the idea bucket.
Probably a good idea to periodically review unprioritized tasks and assign a Priority or delete them if they won’t ever be worth my time.

    $ task -work priority:
    [task next ( -work priority: )]

    ID Age Project Tag              Description                                   Urg
    26 1h  fitbit  health           get fitbit data                               2.7
                                      2017-12-24 can only grab 31 days at a time
                                      2017-12-24 want all data back to 2016-01
     2 3w  ruana   blog knitting    blog about vest                              2.02
    27 1h  fitbit  health           see activity when closest to weight goal      1.8
    28 1h  fitbit  health           make 2018 exercise plan                       1.8
    24 3d          home             living room curtains                         1.62
                                      2017-12-20 dimensions 94.25 wide 56.5 high
     3 3w          blog taskwarrior due dates, recurrences                       1.02
    12 9d          crochet home     door panel                                   0.95
    15 7d          learn music      submit to acousticbrainz                     0.94
     1 3w          crochet          fingerless gloves                            0.92
     8 2w          home             move my stuff upstairs                       0.88
    10 10d         music            experiment with setting itunes play stats    0.85
    11 10d         blog             create links section                         0.85
    16 6d          music            music server                                 0.83
    17 6d          learn            try timewarrior                              0.83
    19 6d          home             make flylady daily and weekly list           0.83
    20 5d          music            merge rating files                           0.83
    21 5d          music            filter duplicate tracks                      0.83
    22 5d          knitting         circular hat variant                         0.83
    25 3d          music            restore backup                               0.82

    19 tasks

Give me a minute while I assign priorities.

    $ task -work
    [task next ( -work )]

    ID Age P Project Tag              Description                                      Urg
    18 7d  H         blog taskwarrior Priorities                                      6.94
    25 4d  H         music            restore backup                                  6.82
    26 1d  M fitbit  health           get fitbit data                                 6.61
                                        2017-12-24 can only grab 31 days at a time
                                        2017-12-24 want all data back to 2016-01
     2 3w  M ruana   blog knitting    blog about vest                                 5.92
     1 3w  M         crochet          fingerless gloves                               4.83
     8 2w  M         home             move my stuff upstairs                          4.79
    19 7d  M         home             make flylady daily and weekly list              4.74
    29 23h M                          return library books                             4.7
                                        2017-12-25 due 2017-12-30
    28 1d  L fitbit  health           make 2018 exercise plan                         4.41
                                        2017-12-24 keep on what I do now is an option
    27 1d  L fitbit  health           see activity when closest to weight goal        3.61
    24 4d  L         home             living room curtains                            3.42
                                        2017-12-20 dimensions 94.25 wide 56.5 high
     3 3w  L         blog taskwarrior due dates, recurrences                          2.82
    12 10d L         crochet home     door panel                                      2.75
    15 8d  L         learn music      submit to acousticbrainz                        2.74
    10 11d L         music            experiment with setting itunes play stats       2.66
    11 11d L         blog             create links section                            2.66
    16 7d  L         music            music server                                    2.64
    17 7d  L         learn            try timewarrior                                 2.64
    20 5d  L         music            merge rating files                              2.63
    21 5d  L         music            filter duplicate tracks                         2.63
    22 5d  L         knitting         circular hat variant                            2.63

    21 tasks

I could have added due date information to the library task rather than an annotation,
but I’m sticking with this approach of a few features at a time. Otherwise I’ll
try to learn everything at one sitting, get overwhelmed and distracted, then abandon
the whole thing.

[dates]: https://taskwarrior.org/docs/dates.html

That said, it looks like next I should learn [dates][] in Taskwarrior.