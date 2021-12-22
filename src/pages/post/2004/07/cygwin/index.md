---
aliases:
- /coolnamehere/2004/07/08_cygwin.html
- /post/2004/cygwin/
- /2004/07/08/cygwin/
category: coolnamehere
date: 2004-07-08 00:00:00
layout: layout:PublishedArticle
slug: cygwin
tags:
- cygwin
title: Cygwin
updated: 2017-04-09 00:00:00
uuid: 5e6e243c-38d1-4bc5-b866-01942d3424c4
---

Unix for the Windows World
--------------------------

Okay, so you’re a geek. Or you’d like to be. All of your cool friends
are running [Linux](http://www.linux.org/) — or maybe even
[FreeBSD](http://www.freebsd.org/). You’d like to install something with
a distinctly geeky UNIX flavor. There’s a problem, though. You’ve got a
PC, it runs [Microsoft
Windows](https://www.microsoft.com/en-us/windows), and your parents /
spouse / girlfriend / boyfriend / children will cause you great
pain — or at least a great headache — if you do anything to endanger
their comfortable environment. Chopping your hard drive in half to put a
new operating system on it will probably end in tears. What to do?

Or maybe you’re like me. You are sort of a geek. You like to program,
and you enjoy the command line. Heck, you even like X11. Trouble is,
you’ve also got a few decent Windows programs, and you don’t feel like
rebooting every time you want to play Civilization IV or muck about with
[Adobe Photoshop](http://www.adobe.com/products/photoshop/main.html). If
you were a real geek, you could probably do something with
[Wine](http://winehq.com/). You’re not a real geek, though – at least
not the sort who can work their way through a binary compatibility
layer. I’m with you. Heck, I can’t even type “binary compatibility
layer” without a spellchecker handy. What should we do?

The solution is surprisingly straightforward. Get
[Cygwin](http://www.cygwin.com/) (pronounced “Sig-win”). Cygwin provides
a Linux-like environment for the Microsoft Windows platform. It’s a
simple point-and-click install, which should provide a pleasant surprise
for some of the grizzled (well, lightly toasted) folks who attemped a
Linux install. As much as it looks like Linux or whatever derivative of
UNIX you happen to like, it’s still Windows underneath. Cygwin is not
binary compatible with Linux, which means that you can’t just pick up a
compiled Linux program and run it on your Cygwin install. The good news
is that it *is* possible to compile many of those programs to run under
Cygwin. It can be a challenge, though — don’t say you weren’t warned!

So that’s all I’ll say for now. If I ever talk about some UNIXy thing on
this site, the odds are good that you can also do it from Cygwin.

Cygwin Ports Project
--------------------

Cygwin on its own is fairly handy, but one of the blessings of a major
open source project like this is that people are always working to add
more. These additions may eventually get incorporated into the main
Cygwin repository. It wasn’t that long ago that X11 was considered an
experimental add-on which only the brave should try. Nowadays it’s
standard and readily available.

You may want to play with the packages which haven’t been incorporated
into Cygwin yet. My advice to you is to go straight to the [Cygwin Ports
Project](http://cygwinports.org/) and follow the instructions there.