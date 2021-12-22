---
aliases:
- /emacs/2014/06/02_start-using-emacsclient.html
- /post/2014/start-using-emacsclient/
- /2014/06/02/start-using-emacsclient/
category: tools
date: 2014-06-02 00:00:00
layout: layout:PublishedArticle
slug: start-using-emacsclient
tags:
- emacs
title: Start Using Emacsclient
updated: 2017-07-06 00:00:00
uuid: 8d03dfe1-5e4f-4832-9268-b49cfcb1f570
---

[Emacs Client]: http://www.emacswiki.org/emacs/EmacsClient
I have been curious about the [Emacs Client][] for a long time. Because
Emacs can have a long startup time, it can be made to run in a
persistent mode. All buffers are handled by a central process. Your
editor interface connects to that central process rather than
managing its own buffers. Thinking about the Emacs client is what
started me down the path of studying Emacs as a client/server Lisp
environment. Anyways, I looked up some blog posts to tell me what to
do.
<!--more-->

[blog post]: http://devblog.avdi.org/2011/10/27/running-emacs-as-a-server-emacs-reboot-15/
[Emacs Reboot]: http://devblog.avdi.org/category/emacs-reboot/

It should not surprise me that a [blog post][] by Avdi Grimm is one of
the top hits for Emacs Client - or anything else, really. I am
willing to bet that all of his [Emacs Reboot][] posts are worth reading
and reviewing. Let's focus on just the one post for now.

He mentions having a short script `ec` to simplify invocation of
`emacsclient`.

``` bash
#!/bin/sh
exec /usr/bin/env emacsclient -c -a "" $*
```

I was tempted to create an alias, but his solution will work
regardless of which shell I happen to be fiddling around with that
day.

I'm also inclined to follow his thought of removing the keybinding
for `save-buffers-kill-terminal` and `suspend-frame`. There have
already been a few times where I quit when I meant to save.

``` elisp
;; Adding this to my ~/.emacs.d/init.el
(global-unset-key (kbd "C-x C-c"))
(global-unset-key (kbd "C-x C-z"))
```

[elscreen]: http://www.emacswiki.org/emacs/EmacsLispScreen

I use [elscreen][]. Since `emacsclient` keeps everything running, you
can switch back to a previously active screen with `C-z b`. So that
makes these the new important commands for me to remember.

| Function                          | Keybinding       | Description                         |
|-----------------------------------|------------------|-------------------------------------|
| `delete-frame`                    | `C-x 5 0`        | "Quit" an emacsclient session       |
| `elscreen-find-and-goto-by-buffer`| `C-z b <buffer>` | Switch to screen holding `<buffer>` |
| `kill-emacs`                      | *None*           | Shut down Emacs                     |

[this suggestion]: http://www.emacswiki.org/emacs/EmacsAsDaemon#toc7

It would probably be a good idea to set up a `kill-emacs-hook` or
make a custom shutdown function. EmacsWiki offers [this suggestion][].

Can't help noticing that the `delete-command` command learned in a
GUI context applies for `emacsclient` as well. Curious. There are
bound to be new issues. Expect a "my bad" post in the future when I
find out what those new issues are.
