---
aliases:
- /post/2015/hugo/
- /2015/09/27/next-hugo/
category: tools
date: 2015-09-27 20:36:30
description: I Rebuilt Random Geekery with Hugo
layout: layout:PublishedArticle
slug: next-hugo
tags:
- site
- hugo
title: Next? Hugo
uuid: e15550df-5dee-4535-a348-f6cac5b6ac35
---

Hey it has been a while since I shuffled the site around completely. I'll
just redo the whole thing in [Hugo][].

[Hugo]: http://gohugo.io/

<!--more-->

[Jekyll][] is nice enough, but the long build times are tiresome. Even the 3.0
beta drags once your site gets complex. A fresh build usually took 15 seconds,
and some unoptimized template experimentation pushed that up briefly to 45 seconds.

I spent a few days converting this site to [Hugo][]. So far the longest the site has taken to build is
350 milliseconds. Plus it automatically handled the [reStructuredText][] posts. I think it hands
them off to `rst2html` but I have not checked that yet. No plugin is needed. That is nice.

All the URLS have been changed, but hopefully you won't notice thanks to [aliases][].
Plus I got the basics of [taxonomies][] well enough to get categories and tags working.
One way or another you should still be able to find content that people were actually
viewing. Things like the Crafts collection will wait until I get a better understanding
of taxonomy in Hugos.

The site looks nice because of the [Hyde-X][] theme. Of course I already modified
the theme for my own visual and organizational aesthetics. It'll probably look completely different by the time I'm done.
Hyde-X gives a great starting point though.

Okay I need to get back to it. There are a lot of rough edges to smooth out.

[Jekyll]: http://jekyllrb.com
[reStructuredText]: http://docutils.sourceforge.net/rst.html
[aliases]: http://gohugo.io/extras/aliases/
[taxonomies]: http://gohugo.io/taxonomies/overview/
[Hyde-X]: https://github.com/zyro/hyde-x