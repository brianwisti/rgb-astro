---
date: 2021-05-14
format: md
layout: layout:PublishedArticle
slug: oh-no-i-added-a-javascript-search-thing
tags:
- site
- javascript
- hyperscript
title: oh no i added a javascript search thing
uuid: 138db20b-194e-4192-8e94-4556879f0f6d
---

[_hyperscript]: https://hyperscript.org/
[this post]: https://makewithhugo.com/add-search-to-a-hugo-site/

And a touch of [_hyperscript].
Started from [this post] and leaned on the _hyperscript to tie some bits together.

```html
<button _="on click
           get value of #searchQuery
           call executeSearch(it, false)">Search</button>

```

[GatsbyJS]: https://www.gatsbyjs.com/

And yeah I'm back on Hugo.
Spent so much time in the last couple weeks touching up the static repo and ignoring the Statamic live site.
Decided not to fight it.
Anyways, now that I started clearly the logical next step will be [GatsbyJS].
For flexible values of "logical."