---
aliases:
- /2017/10/31/wellington-for-sass/
category: tools
date: 2017-10-31
draft: false
layout: layout:PublishedArticle
slug: wellington-for-sass
tags:
- site
- css
title: Wellington for Sass
uuid: 458a7b5c-c67a-49e7-be3d-5a3a987bb961
---

[Wellington]: https://getwt.io/
[Sass]: http://sass-lang.com/
[Go]: https://golang.org/

I found [Wellington][], a [Sass][] compiler written in [Go][].

[Homebrew]: https://brew.sh/
[Linuxbrew]: http://linuxbrew.sh/

I installed Wellington with [Homebrew][] -
actually [Linuxbrew][] but that’s a post for another day maybe, once I’m sure
this Linuxbrew experiment worked for me.

    $ brew install wellington

This is not the night to redesign the whole site, though. Make sure everything
works.

    $ wt compile assets/scss/main.scss -b static/css
    2017/10/31 21:09:54 Compilation took: 28.333622ms

Seems to produce the same style output. I had no complaint about the speed of
Ruby’s Sass compiler, but Wellington is certainly quicker.

I guess now I can start thinking about redesigning the site layout.