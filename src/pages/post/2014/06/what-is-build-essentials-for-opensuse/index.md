---
aliases:
- /tools/2014/06/22_what-is-build-essentials-for-opensuse.html
- /post/2014/what-is-build-essentials-for-opensuse/
- /2014/06/22/what-is-build-essentials-for-opensuse/
category: tools
date: 2014-06-22 00:00:00
layout: layout:PublishedArticle
slug: what-is-build-essentials-for-opensuse
tags:
- suse
title: What is build-essentials for openSUSE
uuid: d6ec715c-08b5-463e-bc35-7f6e2949c4e5
---

*TL;DR* `devel_basis`
<!--more-->

[build-essential]: http://packages.ubuntu.com/trusty/build-essential
[openSUSE]: http://opensuse.org
[devel_basis]: http://software.opensuse.org/package/patterns-openSUSE-devel_basis

This is the umpteenth time I looked up what [build-essential][] is on [openSUSE][].
For my purposes, it's the [devel_basis][] pattern.

To see what packages have the pattern,

    $ zypper info -t pattern devel_basis

Yes it has a lot of packages, but I usually end up installing many of those anyways.

To install `devel_basis`:

    $ sudo zypper install -t pattern devel_basis

That's all. I've started remembering to *use* the notes on my site, which 
means it occurs to me that more notes would be helpful.
