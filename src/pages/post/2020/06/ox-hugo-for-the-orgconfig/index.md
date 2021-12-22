---
category: tools
cover_image: cover.png
date: 2020-06-27
description: Putting a couple how-to details down for easy searching later
draft: false
format: md
layout: layout:PublishedArticle
slug: ox-hugo-for-the-orgconfig
tags:
- OrgConfig
- OrgMode
- site
title: Ox Hugo for the Orgconfig
uuid: ae095031-0ca3-4fd5-b35d-0f92832c747c
---

## What?

I’m combining all my [orgconfig][] files into one, and then using
[`ox-hugo`][ox-hugo] to generate Markdown files for my [Hugo][hugo] site.

## Why?

Hugo renders Org files just fine, but I wanted my config to be a bit more
tightly integrated.  `ox-hugo` works well as both plain old Org and as an
intermediary that exports Hugo content.  A single Org file can become as many
Hugo pages as I want.

## Getting it to work

This week my favorite Emacs flavor is [Doom Emacs][doom-emacs].  Their [org
module][org-module] supports `ox-hugo` as an option, so enabling that option in
my init should do the trick — after a `doom sync` of course.

``` elisp
(doom!
 ⋮
 :lang
 (org +hugo))
```

Off in the depths of my `~/org/` folder, I create a new `config.org`.

``` text
#+title: My Orgconfig
#+hugo_base_dir: ~/Sites/random-geekery-blog/
#+hugo_section: config
```

Everything here will end up going in the `config` section of my site, under
`~/Sites/random-geekery-blog/content/config`.

:::note

A while back I got stuck with `ox-hugo` for my site because of how big each
section is.  Using an Org file per section might work really well!  It works
great for this case, that’s for sure.

:::

Each top-level section will be a page in `/config/`.
I show *which* page in the subtree’s `:properties:`.

``` text
+ Emacs config
:properties:
:export_description: Be kinda weird if I didn't manage that one in Org, yes?
:export_file_name: emacs
:export_hugo_weight: 5
:end:
```

`ox-hugo` automatically [converts][] the `export` properties to Hugo front
matter.  `:export_file_name:` of `emacs` maps out to a generated file
`emacs/index.md` under `content/config/`.

:::warning

If you’re playing along, remember to tag sensitive config sections as
`:noexport:`!

:::

Since I’m showing off [Babel][babel]’s ability to tangle, I want to show the
tangle references.  `:noweb no-export` tells Babel to tangle when evaluating
the block, but *not* when exporting.

``` text
#+name: zsh/base-variables
#+begin_src text :noweb no-export
<<zsh/set-base-path>>
<<zsh/define-editor>>
<<zsh/clicolor>>
<<zsh/add-home-bin>>
#+end_src
```

And — yeah.  I still haven’t figured out a nice way to highlight those tangle
bits, so for the moment I default to calling my mostly-tangled blocks "text".

I also create a subtree for the section `_index.md`.

``` text
+ My personal orgconfig
:properties:
:export_file_name: _index
:end:

#+begin_note
This is my live config, written as an [[https://orgmode.org/][Org]] file and integrated with my site with [[https://ox-hugo.scripter.co/][=ox-hugo=]].
⋮
```

Now my config section summary is part of the config org file.  I find this
aesthetically pleasing.

## The rest is implementation details

This whole process is fiddly.  Org mode.  Literate config.  Hugo.  `ox-hugo`.
That makes the whole thing fiddly^4 or something.  But these quick notes
covered things that got in my way while gluing the whole thing together.  If
you want to try it out, at least *some* of the fiddliness should be clearer.

[orgconfig]: /tags/orgconfig
[ox-hugo]: https://ox-hugo.scripter.co
[hugo]: https://gohugo.io
[doom-emacs]: https://github.com/hlissner/doom-emacs
[org-module]: https://github.com/hlissner/doom-emacs/tree/develop/modules/lang/org
[converts]: https://ox-hugo.scripter.co/doc/org-meta-data-to-hugo-front-matter/%5D
[babel]: https://orgmode.org/worg/org-contrib/babel/intro.html