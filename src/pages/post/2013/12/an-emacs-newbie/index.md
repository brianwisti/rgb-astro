---
aliases:
- /emacs/2013/12/26_an-emacs-newbie.html
- /post/2013/an-emacs-newbie/
- /2013/12/26/an-emacs-newbie/
category: marginalia
date: 2013-12-26 00:00:00
layout: layout:PublishedArticle
slug: an-emacs-newbie
tags:
- emacs
title: An Emacs Newbie
uuid: 41215bcb-0aa0-4cc3-9a0b-e503b3cb3d61
---

[suggestion]: http://ryanmacklin.com/2013/12/getting-back-on-the-creative-horse/

Right. I am going to attempt to follow Ryan Macklin's [suggestion][] to write at least 250 words per day.
They don’t have to be good words.
Fortunately, I have this blog sitting here.

[GNU Emacs]: http://www.gnu.org/software/emacs/
[video]: http://bling.github.io/blog/2013/10/16/emacs-as-my-leader-evil-mode/
[evil-mode]: http://www.emacswiki.org/emacs/Evil

I have been spending more time with [GNU Emacs][] lately.
This is because of a [video][] by Bailey Ling describing [evil-mode][].
Evil is an Emacs mode that provides effective Vim emulation.

[Vim script]: http://vimdoc.sourceforge.net/htmldoc/usr_41.html
[Vim]: http://www.vim.org/

Emacs is not completely foreign to me.
I started experimenting with it at roughly the same time that I was introduced to [Vim].
My fingers were happier with the controls in Vim, so that is what I stuck with.
I was never happy with the default extension language, though.
[Vim script][] evolved from the old ex commands of vi.
I would rather customize or extend my editing environment with a general purpose language.
I know that support for Ruby, Python, Perl, and others can be compiled into Vim, but they are not default options.
You still feel the ex roots when you start digging into the Vim API for these languages.
Emacs LISP will work for me.

[packages]: http://www.emacswiki.org/emacs/ELPA

Oh and Emacs has a built-in idea of [packages][] as of version 24.
This makes it easier to use somebody’s excellent extension.
That contrasts with the many packaging options to choose from for Vim.

I even made a repo for my Emacs init.
It is unimpressive today. I plan to improve it.
It exists so that I have a central source for Emacs settings when I sit in front of a new machine.

We will see how long that lasts.
I can be fickle.
But as I was mentioning to a friend earlier today:

Emacs is a lot more fun when I think of it as a LISP-powered shell with editing capabilities.