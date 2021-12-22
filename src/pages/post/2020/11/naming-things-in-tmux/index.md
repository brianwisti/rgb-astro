---
category: tools
date: 2020-11-21
description: In which I sort out which tmux session is which
draft: false
format: md
layout: layout:PublishedArticle
slug: naming-things-in-tmux
tags:
- shell
- tmux
title: Naming things in tmux
uuid: d2d22a2d-dc8e-4079-91aa-0afbb11dd2fd
---

I got the basics of [tmux][] down:

- starting a new session
- creating new windows
- moving between windows
- scrolling back in a window buffer

And that’s about it.

After this long you might expect me to know more.  Alas, no.

At some point I realized you can have more than one tmux session going at a
time.  Now my normal day includes the site in one session, work in another, and
sometimes a third for random puttering.

I need to manage everything better.

## Using Tmux commands

Although tmux binds keys to commands, it’s easier for me to remember words than
keys.  It’s part of why I still use [taskwarrior][taskwarrior] more than [Org
mode][org-mode].  Because of that, I’ll focus on the tmux commands.

You can send them directly to `tmux` in an open shell.

``` text
$ tmux <command> [arguments]
```

You don’t have a shell handy?  [[C-b :]] will pull up a quick Tmux command
prompt to enter your commands:

``` text
C-b :<command> [arguments]
```

If your command produces output, it will display in place of your current
window until you hit [[ENTER]].

On to the commands themselves.  I’ve added some highlights along the way, with
command full names, aliases, and useful arguments — but not *all* arguments.

## Sessions

First things first.  Let’s figure out what I have.

### Listing sessions

command
: `list-sessions`

alias
: `ls`

I can list sessions with `list-sessions`.

``` text
$ tmux list-sessions

0: 3 windows (created Wed Nov 18 22:25:18 2020) (attached)
2: 1 windows (created Sat Nov 21 12:08:28 2020)
```

This shows two sessions.  The first one — currently attached, which means its
the one I’m typing in right now — contains three windows, and has been open a
few days.  The other is open with some work stuff.  Yes, I know.  On a
Saturday.  I’m working on that "life/work balance" thing.

By writing a blog post.

Whatever.

Anyways, that number on the start of each entry identifies the session.  It
starts at zero, and keeps going up with each new session until you quit all
your tmux sessions and start again.  Quitting a session won’t affect the
numbering.  `2` is the name of the session, and that stayed true even when I
quit session `1`.

### Switching to different sessions

command
: `switch-client`

alias
: `switchc`

shortcut
: [[C-b )]] / [[C-b (]]

options
: `-t N`  target
: `-n`    next
: `-p`    previous

Used to be I’d get at that other session by opening a new tab in my terminal
and telling `tmux` to attach to it, making sure to detach it from whatever
other connections I may have had open.

``` text
tmux attach -d -t 2
```

Then I learned that we can switch to my other sessions with `switch-client`.

``` text
:switch-client -t 2
:ls

0: 3 windows (created Wed Nov 18 22:25:18 2020)
2: 1 windows (created Sat Nov 21 12:08:28 2020) (attached)
```

We can cycle through sessions without targeting them, too.  A `-n` argument
cycles to the next, while `-p` cycles to the previous.

``` text
:switch-client -n
```

:::note

Okay, key bindings might help here.  Cycle through your Tmux sessions with
[[C-b )]] and [[C-b (]].

:::

I don’t think so much about tabbed terminals anymore.  I do forget which
session holds work stuff and which holds site stuff, though.

### Renaming sessions

command
: `rename-session`

shortcut
: [[C-b $]]

alias
: `rename`

usage
: `rename -t N <name>`

options
: `-t`  target

I’m not stuck with the tmux-assigned session numbers for identification.
I can rename them!

``` text
:rename-session -t 0 site
:rename -t 2 work
```

Does that help?

``` text
:ls

site: 3 windows (created Wed Nov 18 22:25:18 2020) (attached)
work: 1 windows (created Sat Nov 21 12:08:28 2020)
```

It sure does.  Oh and it sorts the listing alphabetically.  Good to know.

With several sessions going at once — it happens sometimes — names tell me what
I intended to do with my time.  Makes switching to a targeted session easier
for me as well.

I gave each of my sessions a purpose.  Now.  What’s going on with the windows
*inside* the sessions?

## Windows

### Listing windows

command
: `list-windows`

alias
: `lsw`

options
: `-a`  all

`list-windows` summarizes the windows in my current session.

``` text
:list-windows

1: zsh* (2 panes) [282x65] [layout eb16,282x65,0,0{142x65,0,0,0,139x65,143,0,1}] @0 (active)
2: zsh#- (1 panes) [282x65] [layout c59f,282x65,0,0,2] @1
3: zsh# (1 panes) [282x65] [layout c5a0,282x65,0,0,3] @2
```

Let’s see.  There’s a window with two panes, one of which is a Zsh session.
There’s a second Zsh session.  And — uh — a third Zsh session.

I can even list every window in every session!

``` text
:lsw -a

site:1: zsh* (2 panes) [282x65]
site:2: zsh#- (1 panes) [282x65]
site:3: zsh# (1 panes) [282x65]
work:1: zsh* (1 panes) [282x63]
```

That’s not very helpful. The named sessions help clarify things somewhat, but
the windows are just a lot of Zsh.

Let’s fix that.

### Renaming windows

command
: `rename-window`

alias
: `renamew`

usage
: `rename-window -t N <NAME>`

options
: `-t N`  target window

I can rename the windows within my session.

``` text
:rename-window -t 1 writing
:renamew -t 2 hugo
:renamew -t 3 kexp
```

There we go.  I’m writing this post in [Neovim][neovim], serving my site with
[Hugo][hugo] locally for review, and listening to the [KEXP][kexp] stream via
`mplayer`.

Heck, I can rename windows in my other session if I like.

``` text
:rename-window -t work:1 compiling
```

Does *that* help?

``` text
:lsw -a

site:1: writing* (2 panes) [282x65]
site:2: hugo# (1 panes) [282x65]
site:3: kexp#- (1 panes) [282x65]
work:1: compiling* (1 panes) [282x65]
```

It does!  My sessions and windows all make sense!  More or less.

Some folks might prefer naming their windows according to the current process.
Maybe even automating that process.  For my own brain, a named purpose is
generally more informative and more persistent than any executable.

So much more I could learn, but this covers enough to call it a post.

Besides, I need to get back to work.

## Resources

Where did I get all this?

- [tmux cheat sheet](https://tmuxcheatsheet.com/)
- [tmux man page](https://linux.die.net/man/1/tmux) — which you can get at on your own system with ``man tmux``

[tmux]: https://github.com/tmux/tmux
[taskwarrior]: /tags/taskwarrior
[org-mode]: /tags/org-mode
[neovim]: /tags/vim
[hugo]: /tags/hugo
[kexp]: /tags/kexp