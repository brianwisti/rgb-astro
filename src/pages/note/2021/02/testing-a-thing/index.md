---
date: 2021-02-15 02:29:10
layout: layout:PublishedArticle
slug: testing-a-thing
tags:
- asciidoctor
- hugo
- site
title: testing a thing
uuid: 6b015a2e-f610-4e7f-885e-f5d92c80d9ae
---

[last year]: /post/2020/05/letting-ruby-build-asciidoctor-files-for-hugo/
[Asciidoctor]: https://asciidoctor.org/
[Hugo]: https://gohugo.io

Sometime [last year][] I had half of a great idea for better [Asciidoctor][]
handling in [Hugo][]. I *might* have the other half now:

* keep my content in the content folder.
* Use `adoc.txt` for the extension so Hugo ignores it.
* Point my `build-adoc` script there instead of a neighboring `adoc` folder.
* profit?

[reStructuredText]: /tags/rst

Would work for [reStructuredText][] too.

Need to get through a few post cycles to see how it works.