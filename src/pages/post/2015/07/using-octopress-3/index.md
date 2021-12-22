---
aliases:
- /tools/2015/07/12_using-octopress-3.html
- /post/2015/using-octopress-3/
- /2015/07/12/using-octopress-3/
category: tools
date: 2015-07-12 00:00:00
description: Experiments with the Octopress Jekyll extension bundle
layout: layout:PublishedArticle
slug: using-octopress-3
tags:
- site
- jekyll
title: Using Octopress 3
uuid: 1683f702-7c5e-459d-adce-d6829fe607f4
---

[Octopress]: http://octopress.org/
[Jekyll]: http://jekyllrb.com/
[blog post]: http://octopress.org/2015/01/15/octopress-3.0-is-coming/
[Octopress 3]: https://github.com/octopress/octopress
[Github]: https://github.com/octopress/octopress

[Octopress][] is "an obsessively designed toolkit for writing and deploying [Jekyll][] blogs."
A [blog post][] earlier this year by author Brandon Mathis described frustrations with
Octopress 2, along with plans for [Octopress 3][]. I didn't use Octopress before, so I can't 
tell you anything about how much better or worse the newest Octopress is. This release
feels like a straightforward and useful extension to Jekyll. Apparently the older releases
did not.
<!--more-->

Instructions for installing and using Octopress 3 are on [Github][]. Here is what I did to 
incorporate and use the new Octopress on my site.

I need to install [Octopress 3][] first, obviously.

    $ gem install octopress

Octopress provides a handful of commands for creating and managing content in a Jekyll
site. I head into my site folder and start things off with `octopress init`.

    $ cd randomgeekery.org
    $ octopress init
    Added Octopress scaffold:
     + _templates/
     +   draft
     +   page
     +   post

`init` creates the templates that will be used by other Octopress commands.

I'll start with the draft for this post.

    $ octopress new draft "Using Octopress 3"
    New draft: _drafts/using-octopress-3.markdown

I add my content, drink some coffee, and fix the most grievous errors in my draft. Time to publish
the draft. Octopress commands can complete partial filenames. Let's see if that works.

    $ octopress publish octopress
    Published: _drafts/using-octopress-3.markdown → _posts/2015-07-12-using-octopress-3.markdown

Sure does. That is convenient.

Wait. I organize `_posts` by category folders. I'll back out of the last publish and try again
with a location specified.

    $ octopress unpublish octopress
    Unpublished: _posts/2015-07-12-using-octopress-3.markdown → _drafts/using-octopress-3.markdown
    $ octopress publish octopress --dir tools
    Published: _drafts/using-octopress-3.markdown → _posts/tools/2015-07-12-using-octopress-3.markdown

I already have my own deployment script, so for now I will not worry about the Octopress `deploy` command.
I'll just publish it.

Oh before I do that, I just want to mention that [Octopress 3][] does a
great job streamlining management of individual posts. I like it.