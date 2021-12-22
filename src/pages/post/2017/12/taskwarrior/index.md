---
aliases:
- /2017/12/16/taskwarrior/
caption: '`task -work` report showing everything but my work tasks'
category: tools
cover_image: cover.png
date: 2017-12-16
draft: false
layout: layout:PublishedArticle
series:
- Taskwarrior Babysteps
slug: taskwarrior
tags:
- taskwarrior
title: Taskwarrior
updated: 2017-12-22 00:00:00
uuid: 1f30d9d2-77e0-4c05-beff-06d6c5745445
---

[Taskwarrior]: https://taskwarrior.org/

I ended up with a mess after half a year trying to use *every feature* of
[Taskwarrior][]. It’s time to focus on building solid knowledge one step at a
time.

<aside class="admonition">

I sat on this draft for a couple weeks. Rather than change task dates to make it
look like I wrote this yesterday, I’ll leave `task` output as-is. Otherwise I’ll
have to change those details every time I revisit Taskwarrior on the blog.

</aside>

## What Is Taskwarrior?

Taskwarrior helps you manage tasks and ideas from the command line. It provides
a convenient interface, assuming your idea of convenient is a rich collection of
commands you can enter, customize, and pipe to other utilities.

[Org]: /tags/org-mode
[Vim-OrgMode]: https://github.com/jceb/vim-orgmode

<aside class="admonition">
<p class="admonition-title">What's wrong with Org mode?</p>

Nothing at all! [Org][] provides similar functionality and more for GNU Emacs
users. Taskwarrior focuses narrowly on task management and reporting, while Org
is also a time tracker, note-taking tool, markup language for publishing, and
more.

Taskwarrior works better than Org mode for people that don’t live in Emacs.
Wait. [Vim-OrgMode][] exists. I should be more general: Taskwarrior works better
for people that don’t live in their editor.

Ultimately it comes down to personal taste.I enjoy using Taskwarrior today.

</aside>

## Starting from scratch

I archived my confused earlier attempts at usage. Here I am with a fresh slate.

    $ task –-version
    2.5.1
    $ task
    [task next] No matches.

When you don’t tell `task` what you want, it assumes by default that you want to
see your `next` report. You can customize many aspects of Taskwarrior, but for
my own understanding I will not look at customization today.

## The Tutorial, Summarized

[30-Second Tutorial]: https://taskwarrior.org/docs/30second.html

Let’s review the [30-Second Tutorial][].

[`add`]: https://taskwarrior.org/docs/commands/add.html
[`done`]: https://taskwarrior.org/docs/commands/done.html
[report]: https://taskwarrior.org/docs/report.html

[`add`][]
: creates a new task

[`done`][]
: marks a task as complete

`delete`
: marks a task as deleted

`next`
: show a [report][] listing tasks in decreasing order of Urgency

[Urgency]: https://taskwarrior.org/docs/urgency.html

Taskwarrior calculates [Urgency][] based on multiple factors, including your own
`priority:` ranking. I plan to ignore Urgency and `priority` until life no
longer seems sorted into "it’s on fire" and "it’s just an idea."

I’ll add a few tasks.

    $ task add knit fingerless gloves
    Created task 1.
    $ task add write about Taskwarrior
    Created task 2.
    $ task add get a size G crochet hook
    Created task 3.
    $ task next

    ID Age Description               Urg
     1 29s knit fingerless gloves       0
     2 14s write about Taskwarrior      0
     3 1s  get a size G crochet hook    0

I added that last one about the crochet hook to convince myself to get off my
tush and go get that hook from my friendly Local Yarn Store. Give me a minute.

Okay, done.

    $ task 3 done
    Completed task 3 'get a size G crochet hook'.
    Completed 1 task.

What about `delete`? Say I want to see a movie this weekend.

    $ task add go see that movie
    Created task 3.

Turns out it’s not in theaters anymore.
I need to pay closer attention to these things.

`delete` lets you abandon a task.

    $ task 3 delete
    Delete task 3 'go see that movie'? (yes/no) yes
    Deleting task 3 'go see that movie'.
    Deleted 1 task.

Those are the core Taskwarrior commands. It’s enough to make and manage a useful
task list.

## A few more "core" commands

I consider a few more features core to my own Taskwarrior experience.

* editing a task
* recording a completed task that I never added
* reporting my completed tasks

### `modify`

I see a typo in my task descriptions. `modify` helps there.

    $ task 1 modify crochet fingerless gloves
    Modifying task 1 'crochet fingerless gloves'.
    Modified 1 task.

### `log` and `completed`

I don’t just track things I want to do. I track things I did. I feel better on
days when I barely dent my `next` list but can point to other accomplishments.

    $ task log mailed presents
    Logged task 0ef63b0b-ba36-495c-8684-d2c45258ea3d.

The `completed` report shows my completed tasks, including those I logged and
those marked `done`.

    $ task completed

    ID UUID     Created    Completed  Age Description
     - 20334a63 2017-12-01 2017-12-01 20h get a size G crochet hook
     - 0ef63b0b 2017-12-02 2017-12-02 19s mailed presents

    2 tasks

Taskwarrior tells you all sorts of interesting things about your tasks with a
wealth of reports] Explore them!

## Projects

It can be demoralizing to have one huge task that just sits there forever, even
though you work on it and make progress. A good way to keep yourself motivated
is to split it into smaller subtasks. Taskwarrior does that with projects.

Let’s go with a knit vest that I have *almost* finished.

    $ task add knit vest project:ruana
    Created task 3.
    The project 'ruana' has changed.  Project 'ruana' is 0% complete (1 task remaining).
    $ task next

    ID Age Project Description                Urg
     3 3s  ruana   knit vest                    1
     1 20h         crochet fingerless gloves    0
     2 20h         write about Taskwarrior      0

Hey look a column for `Urgency`. Ignoring that.

    $ task add finish vest project:ruana
    $ task add knit belt project:ruana
    $ task add block vest project:ruana
    $ task add blog about vest project:ruana

Knitting the vest itself is still the largest task, but at least I have some
additional information about the other tasks involved in the project.

What does my task list look like now?

    $ task next

    ID Age  Project Description                Urg
     3 4min ruana   knit vest                    1
     4 3min ruana   finish vest                  1
     5 3min ruana   knit belt                    1
     6 3min ruana   block vest                   1
     7 2s   ruana   blog about vest              1
     1 20h          crochet fingerless gloves    0
     2 20h          write about Taskwarrior      0

<aside class="admonition note">
<p class="admonition-title">Note</p>

For the curious: "finishing" a knit project is a distinct step that involves
sewing in the loose ends.

</aside>

## Tags

Taskwarrior lets us add text tags to describe aspects of the task that may be
useful beyond its description or project.

Indicate a tag by prefixing it with `+`.

    $ task modify 1 +crochet
    Modifying task 1 'crochet fingerless gloves'.
    Modified 1 task.

The `next` report includes a new column for tags now.

    $ task next

    ID Age  Project Tag     Description                Urg
     3 7min ruana           knit vest                    1
     4 7min ruana           finish vest                  1
     5 6min ruana           knit belt                    1
     6 6min ruana           block vest                   1
     7 3min ruana           blog about vest              1
     1 20h          crochet crochet fingerless gloves  0.8
     2 20h                  write about Taskwarrior      0

Oh look.
Assigning a tag gave an `Urgency` to task the `+crochet` task. Still ignoring
it.

I added little information putting `+crochet` on a task that I already described
with "crochet," but tags make convenient filters for Taskwarrrior commands and
reports.

### Filters

Filters let you work with a defined set of tasks.

    $ task 3-7 modify +knitting
      - Tags will be set to 'knitting'.
    Modify task 3 'knit vest'? (yes/no/all/quit) all
    Modifying task 3 'knit vest'.
    Modifying task 4 'finish vest'.
    Modifying task 5 'knit belt'.
    Modifying task 6 'block vest'.
    Modifying task 7 'blog about vest'.
    Modified 5 tasks.
    Project 'ruana' is 0% complete (5 of 5 tasks remaining).

What if the tasks aren’t right next to each other? No problem.

    $ task 2,7 modify +blog
    Modifying task 2 'write about Taskwarrior'.
    Modifying task 7 'blog about vest'.
    Modified 2 tasks.
    Project 'ruana' is 0% complete (5 of 5 tasks remaining).

How have these modifications changed my `next` report?

    $ task next

    ID Age   Project Tag           Description                Urg
     7 8min  ruana   blog knitting blog about vest            1.9
     3 12min ruana   knitting      knit vest                  1.8
     4 12min ruana   knitting      finish vest                1.8
     5 12min ruana   knitting      knit belt                  1.8
     6 11min ruana   knitting      block vest                 1.8
     1 20h           crochet       crochet fingerless gloves  0.8
     2 20h           blog          write about Taskwarrior    0.8

Filters work on reports, too.

    $ task 3-7 next

    ID Age   Project Tag           Description      Urg
     7 11min ruana   blog knitting blog about vest  1.9
     3 15min ruana   knitting      knit vest        1.8
     4 15min ruana   knitting      finish vest      1.8
     5 15min ruana   knitting      knit belt        1.8
     6 14min ruana   knitting      block vest       1.8

    5 tasks

What if I filter to a single ID without a command?

    $ task 1
    No command specified - assuming 'information'.

    Name          Value
    ID            1
    Description   crochet fingerless gloves
    Status        Pending
    Entered       2017-12-01 14:49:32 (20h)
    Last modified 2017-12-02 11:08:25 (18min)
    Tags          crochet
    Virtual tags  PENDING READY TAGGED UNBLOCKED
    UUID          fadd9280-6796-4fe9-9f97-0a3ff0f5fd4b
    Urgency        0.8

        tags    0.8 *    1 =    0.8
                             ------
                                0.8

    Date                Modification
    2017-12-02 10:51:12 Description changed from 'knit fingerless gloves' to 'crochet fingerless gloves'.
    2017-12-02 11:08:25 Tags set to 'crochet'.

I get a lot of stuff I’m not ready for yet. I’ll come back to this some other
day.

Filters don’t have to be task IDs. Use plain text to filter based on task
description.

    $ task gloves
    [task next ( gloves )]

    ID Age Tag     Description                Urg
     1 20h crochet crochet fingerless gloves  0.8

    1 task

Prefix with `+` for a tag filter.

    $ task +blog
    [task next ( +blog )]

    ID Age   Project Tag           Description             Urg
     7 12min ruana   blog knitting blog about vest          1.9
     2 20h           blog          write about Taskwarrior  0.8

    2 tasks

Prefix with `-` to show tasks that *do not* have a particular tag.

    $ task -knitting
    [task next ( -knitting )]

    ID Age Tag     Description               Urg
     1 20h crochet crochet fingerless gloves  0.8
     2 20h blog    write about Taskwarrior    0.8

Prefix with `project:` to list tasks associated with a particular project.

    $ task project:ruana
    [task next ( project:ruana )]

    ID Age   Project Tag           Description     Urg
     7 12min ruana   blog knitting blog about vest  1.9
     3 16min ruana   knitting      knit vest        1.8
     4 15min ruana   knitting      finish vest      1.8
     5 15min ruana   knitting      knit belt        1.8
     6 15min ruana   knitting      block vest       1.8

    5 tasks

Org mode lets you write quick notes about a task. Can Taskwarrior do that?

Of course it can!

### Annotations

Annotations let you add a one line note to a task.

    $ task knit vest annotate pattern at http://www.redheart.com/free-patterns/ruana-style-vest
    Annotating task 3 'knit vest'.
    Annotated 1 task.
    Project 'ruana' is 0% complete (5 of 5 tasks remaining).

Taskwarrior presents these annotations with their tasks in reports.

    $ task project:ruana
    [task next ( project:ruana )]

    ID Age   Project Tag           Description                                                                    Urg
     3 24min ruana   knitting      knit vest                                                                       2.6
                                     2017-12-02 pattern at http://www.redheart.com/free-patterns/ruana-style-vest
     7 20min ruana   blog knitting blog about vest                                                                 1.9
     4 24min ruana   knitting      finish vest                                                                     1.8
     5 24min ruana   knitting      knit belt                                                                       1.8
     6 24min ruana   knitting      block vest                                                                      1.8

Notice how a task’s Urgency automatically increases as we add more information
to it? I know — I’m still ignoring it, but it does make it convenient that the
tasks I spend more time on in Taskwarrior get pushed to the top.

Anyways I’m done knitting the vest.

    $ task 3 done
    Completed task 3 'knit vest'.
    Completed 1 task.
    The project 'ruana' has changed.  Project 'ruana' is 20% complete (4 of 5 tasks remaining).

<aside class="admonition">
<p class="admonition-title">denotate</p>

A couple days after posting this article I made an annotation on the wrong task.

    $ task annotate 5 edges done

That’s when I learned about the `denotate` command, which removes a matching
annotation from a task.

    $ task denotate 5 edges done
    $ task annotate 3 edges done

Good to know!

</aside>

## Oops

Let’s go shopping!

    $ task add groceries +misc project:home
    Created task 7.
    The project 'home' has changed.  Project 'home' is 0% complete (1 task remaining).

Sometimes I need to remove a tag, or remove a task from a project.

Prefixing the tag with `-` in a `modify` command removes that tag.

    $ task groceries modify -misc +food
    Modifying task 7 'groceries'.
    Modified 1 task.
    Project 'home' is 0% complete (1 task remaining).

`home` isn’t a project — at least not in this context.
Assigning an empty project removes a task’s project connection.

    $ task groceries modify project:
    Modifying task 7 'groceries'.
    Modified 1 task.

## Summary

Here’s what I have so far for my task list, without `work` stuff because you
don’t need to know about that.

    $ task -work
    [task next ( -work )]

    ID Age   Project Tag              Description                                      Urg
     6 1h    ruana   blog knitting    blog about vest                                   1.9
     3 1h    ruana   knitting         finish vest                                       1.8
     4 1h    ruana   knitting         knit belt                                         1.8
     5 1h    ruana   knitting         block vest                                        1.8
     2 21h           blog taskwarrior Taskwarrior tags, projects, annotations, filters  1.7
                                        2017-12-02 basic flow done
     7 22min         food shopping    groceries                                         1.7
                                        2017-12-02 shopping list done
     8 14min         blog taskwarrior Taskwarrior due dates, priorities, recurrences    0.9
    15 5min          clothes shopping get winter coat                                   0.9
     1 21h           crochet          crochet fingerless gloves                         0.8
    16 9s                             visit library                                       0

    10 tasks

That’s enough for now. I feel comfortable using Taskwarrior to manage
and describe my tasks. Next time I write about Taskwarrior I might
choose to focus on tiny pieces so I can post more often.

    $ task 2 done
    Completed task 2 'Taskwarrior tags, projects, annotations, filters'.
    Completed 1 task.
    You have more urgent tasks.

[Urgency]: https://taskwarrior.org/docs/urgency.html

Oh hush, you. I’ll get to [Urgency][] when I feel like it.