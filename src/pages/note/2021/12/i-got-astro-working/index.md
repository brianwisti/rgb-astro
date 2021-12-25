---
date: 2021-12-23
format: md
title: I got Astro working!
caption: this time you get a screenshot **and** some links
tags:
- astro-dot-build
- ssg
- site
layout: layout:PublishedArticle
---

[Astro][]'s great once you get started. A bit funky if you have twenty years of
legacy content.

Rather than do my usual — a screenshot and *maybe* a "lesson learned" post —
this time around I made a public [repo][] and [live instance][] of this
in-progress experiment available for your entertainment and edification.

Oh and lesson learned: components are *fussy*, and the errors don't always
happen where you expect. Treat all your imported HTML as XHTML, and look for
stray `{` characters. You might need to convert those to `&#123;`.

Took me months to figure that out. Hopefully it saves you a few hours of
confusion.

[Astro]: https://astro.build
[repo]: https://github.com/brianwisti/rgb-astro
[live instance]: https://quirky-wozniak-e4e36f.netlify.app
