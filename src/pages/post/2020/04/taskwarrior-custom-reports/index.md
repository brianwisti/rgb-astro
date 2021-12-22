---
aliases:
- /2020/04/30/taskwarrior-custom-reports/
caption: output of my custom `task top` report
category: tools
cover_image: cover.png
date: 2020-04-30 08:02:43
description: I made a priority task to cut down on the priority tasks, and here we
  are
draft: false
format: md
layout: layout:PublishedArticle
series:
- Taskwarrior Babysteps
slug: taskwarrior-custom-reports
tags:
- taskwarrior
title: Taskwarrior Custom Reports
uuid: 1f4045e0-3765-43d7-8f1b-f5265ebbcf27
---

It happened again. I have a couple dozen great ideas for the blog. Loads of
other things I need to get at as well. So yeah. I got myself a little
overwhelmed, and I need to stop and get a solid idea of the top tasks: the ones
I want to be working on now or soon.

[priorities]: /post/2017/12/taskwarrior-priorities/

I’ve been dutifully adding everything to Taskwarrior, assigning [priorities][]
as I go.

[beginning]: /post/2017/12/taskwarrior/

In case you forgot, or haven’t been following from the [beginning][] , I use
Taskwarrior’s `Priority` field to show how soon I want to work on a task.
`Priority:M`? I want to work on it soon. `Priority:H`? Either I am working on
it right now or I really want to be.

[due dates]: /post/2018/01/taskwarrior-due-dates/
[dependencies]: /post/2018/02/setting-task-dependencies-in-taskwarrior/
[`task start`]: /post/2018/12/active-tasks-in-taskwarrior/

<aside class="admonition">
<p class="admonition-title">Yeah I know</p>

Taskwarrior lets you assign [due dates][] and [dependendies][] . Tasks that are
due or that block something else get higher `Urgency`, and bubble to the top of
reports. For some folks, that works great.

For me? They mostly lead to heartbreak and self-recrimination. I refer you to
these words of wisdom from a greater mind:

> I love deadlines. I love the whooshing noise they make as they go by.
>
> — Douglas Adams

I get more done quicker by flagging a few tasks as important, a few more tasks
as less important, and the rest as "whatever."

I still use [`start`][] to remember what I’m doing right now though. I’m not
completely weird.

</aside>

Time for me to figure out `or` in Taskwarrior.

## Filtering with `or`

Filters already have an implied `and`. It looks like this.

How many active tasks do I have?

    $ task +PENDING count
    198

How many active tasks do I want to work on soon?

    $ task +PENDING priority:M count
    28

That’s filtering tasks to those for which `+PENDING` **and** `priority:M` are
true.

How many active tasks do I want to be working on now?

    $ task +PENDING priority:H count
    6

That’s a bit much. It should be more like four or five.

How many active tasks do I want to work on now or soon? That is, which tasks
are `+PENDING` and have either `priority:M` or `priority:H`?

We can use `or` to join two filters. If either of them is true for the task,
that task is included. Use parentheses to build more complex filters.

    $ task +PENDING (priority:H or priority:M) count
    zsh: unknown file attribute: i

Tada — oops. Hang on. This stuff goes through the shell before it reaches
Taskwarrior. Let’s put the filter in a string.

    $ task '+PENDING (priority:H or priority:M)' count
    34

Tada!

Okay, it works, but I just know there will be more typos using this filter from
memory. How can I avoid typing it in every time?

## Use a context

I could add that priority filter to my "focused" [context](/post/2018/02/taskwarrior-contexts/), used when I need to ignore distracting ideas.

**`~/.taskrc`**

    context.focused=-idea -shelved (priority:H or priority:M)

Now *every* report skips low priority tasks.

    $ task context focused
    Context 'focused' set. Use 'task context none' to remove.
    $ task +PENDING count
    34

This is great, but I want to know my top tasks even when I’m not in focused context.

Plus it’s easy to forget which context you’re in. I once spent 15 minutes
trying to find a `+work` task before remembering I was still in `offwork`
context. Which reminds me — 

    $ task context blog

## Use a shell alias

Part of Taskwarrior’s charm is the fact that we use `task` from the command
line. I could take advantage of that with a shell alias for `task` using the
preface filter.

**`~/.aliases`**

``` bash
alias ttop='task +PENDING "(priority:H or priority:M)"'
```

This gives me sort of an on-the-fly context.

    $ ttop count
    34

I could use `ttop` with any Taskwarrior command, so `ttop next` would be a fine
way to look at my important tasks.

But I’d kind of like to have a custom report for reviewing tasks I’ve set as
important. Something with a little more information than `task minimal` but a
bit less than `task next`.

## Use a custom report

Might be easier to show than tell. For more of a "tell" approach, check the
"REPORTS" section of `man taskrc`. Here’s my custom "top" report, loosely based
on Taskwarrior’s `minimal` report.

**`~/.taskrc`**

```text
# Almost-minimal view of tasks I want to work on most
report.top.columns=id,priority,project,tags,description.count 
report.top.description='Minimal details of tasks'
report.top.filter=status:pending (priority:H or priority:M)
report.top.labels=ID,Pri,Project,Tags,Description
report.top.sort=priority-/,project-,description+ 
```

- `description.count` column is used for the description text and the number of
  annotations for the task.

- `sort` specifies columns to sort by, in descending or ascending order.
  `priority-/` means “descending, dividing each block of priorities with a
  blank row.”

And here’s what my `top` report looks like.

    $ task top
    ID  Pri Project    Tags              Description
     28 H   Site       blog taskwarrior  custom reports [1]
    194 H   Site       blog              describe workflow
    193 H   Site       ops               use content UUID in RSS feed
    192 H   Site       blog              walk through setting up webmention.io and bridgy
    184 H   Make.yarn  knitting personal hemmed edge hat for diedre
    185 H              ops               persist xrandr fix

    170 M   VimWiki    ops               back up current wiki pages
     76 M   Site.Notes site              note pics do not need zoom link
     70 M   Site       ops               Evaluate new permalink templates
    188 M   Site       ops               blogroll of indieweb folks I mentioned
    114 M   Site       blog ops          clean up hard drive
    198 M   Site       layout            consolidate content format
    148 M   Site       ops               cron job to fetch site logs
    181 M   Site       learn ops         pamac for manjaro
    191 M   Site       ops               permanent local server for site
    196 M   Site       blog ops          sending webmentions
     20 M   Site       layout            store link on every page
    167 M   Site       ops               task to list posts via `hugo list`
    147 M   Site       blog taskwarrior  taskwarrior aliases
    143 M   Site       blog              testing a static website
    146 M   Site       blog              update taskwarrior notes script post to show usage
    197 M   OrgConfig  ops               add awesomewm settings
     30 M   Artbiz     research          coloring book options
     39 M   Artbiz     art inventory     redo Voodoo Vince for dbh
     46 M   Artbiz     art learn         udemy affinity designer course [1]
     99 M              dev readlist      Art of PostgreSQL
    186 M              emacs ops         Try telega for emacs
    178 M              ops               add windows option to manjaro boot
    179 M              ops               folding at home fah-config
    176 M              ops               get task count in status
    187 M              ops               get wsl xorg emacs autostart in windows
     50 M              javascript learn  node-tap Node TAP testing library
    145 M              ops               refactor sync cronjob to script
     16 M              tools             try out newsboat news reader
    34 tasks
    Filter: ( status = pending and ( priority = H or priority = M ) )

I can apply additional filters just like with any other report.

    $  rgb-hugo (master) task project:OrgConfig top
    ID  Pri Project   Tags Description
    197 M   OrgConfig ops  add awesomewm settings
    1 task
    Filter: ( status = pending and ( priority = H or priority = M ) ) and ( project = OrgConfig )

So that’s pretty handy. But clearly I need to clean this up a bit. Some of
those aren’t really things I want to work on soon. But at least now I have one
less `priority:H` task.

You can see Taskwarrior’s settings for the `minimal` report, or any other, with
`show report.NAME`:

    $ task show report.minimal

    Config Variable            Value
    report.minimal.columns     id,project,tags.count,description.count
    report.minimal.description Minimal details of tasks
    report.minimal.filter      status:pending or status:waiting
    report.minimal.labels      ID,Project,Tags,Description
    report.minimal.sort        project+/,description+