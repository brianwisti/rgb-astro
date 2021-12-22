---
aliases:
- /coolnamehere/2007/01/25_gnu-screen.html
- /post/2007/gnu-screen/
- /2007/01/25/gnu-screen/
category: coolnamehere
date: 2007-01-25 00:00:00
layout: layout:PublishedArticle
slug: gnu-screen
tags:
- unix
title: GNU screen
updated: 2009-07-11 00:00:00
uuid: fd9ac7ab-35cc-421c-b3d0-727a3870cbfb
---

Sometimes it's helpful to have multiple consoles open. The best example I can 
think of is when you are logged in to a machine via `ssh`. There are other 
ways, of course. You could try to log in to the server with '-X' so that X11 
applications can run on the remote host but display on your computer. That's 
not always easy, though. The administrator of the server may not allow X11 
forwarding. Your machine may not allow or even understand X11 requests. You 
could log in to multiple `ssh` sessions. This is what I did for several years. 
It works, but it's not the most convenient approach, since it clutters up your 
desktop. `screen` is a better option.
<!--more-->

`screen` lets you log in once, and have multiple command line consoles open 
and controlled from within your single `ssh` session. It even keeps your 
session active as an added bonus. This means that after the inevitable network 
hiccup that hoses your `ssh` login, you can log in once more and simple start 
from where you left off with a simple `screen -Dr`.

## Where To Find `screen`

`screen` is part of the [GNU](http://www.gnu.org/) project. You can find more 
info at the [GNU Screen project page](https://savannah.gnu.org/projects/screen/). 
It's also on many distributions, so search with your package manager before 
you download and install the source package.

## How To Use `screen`

Once you've installed screen by whatever approach needed, starting a screen 
session is as simple as invoking the `screen` command.

    $ screen

From there the best way to learn is to monkey around with screen, using the 
quick list of commands below as your guide. All `screen` commands start with 
`Ctrl-A`, as seen below.

### Common `screen` Commands

Combination | Action
------------|-------
`Ctrl-A C`  | Create a new window
`Ctrl-A A`  | Switch to the last window you were in
`Ctrl-A N`  | Switch to the next window in `screen` internal list
`Ctrl-A P`  | Switch to the previous window in `screen` internal list
`Ctrl-A K`  | Kill the current window
`Ctrl-A D`  | Detach your `screen` session
`Ctrl-A ?`  | Get the help screen
`Ctrl-A A`  | Send an actual `Ctrl-A` signal to your current shell

<aside>
Note that using `exit` to quit the shell for that window will also close the window.
</aside>

The commands are fairly straightforward. For example, to create a new window:

1. Hold down the Control key
2. Press "A"
3. Release the Control key
4. Press "C"

You may already know this particular shorthand for key combos, but I wanted to 
have the information just in case you didn't.

Detaching your session may be the coolest aspect of `screen`. Your screen 
session stays in the same state until you can come back and resume later. 
This lasts days - I know, I have tested it - and won't actually go away unless 
forcibly killed by you or an admin. Well, shutting down the computer *will* 
end your screen session completely, so try to bear that in mind whenever you 
are about to reboot.

You reattach a session with `screen -r` from the command line. You can also 
reattach a session that you lost because of network failure or some other 
minor accident with `screen -Dr`.

[Emacs]: /tags/emacs/
Be careful with `Ctrl-A Ctrl-K`! If you are used to working in 
[Emacs][] or using emacs-style movement in your 
shell, you may be accustomed to that key combo moving you to the beginning of 
the current line and cutting that line into the kill ring. In the screen 
world, you would use `Ctrl-A A Ctrl-K` to get the same effect.