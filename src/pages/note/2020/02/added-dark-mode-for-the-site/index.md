---
aliases:
- /note/2020/33/added-dark-mode-for-the-site/
cover_image: cover.png
date: 2020-02-03 03:45:13
layout: layout:PublishedArticle
slug: added-dark-mode-for-the-site
tags:
- site
- css
title: Added dark mode for the site
uuid: d2c9f3f3-8e9a-4ecb-b2c8-a264474713e9
---

Got tired of blowing my eyeballs out during evening work.

How? I used
[prefers-color-scheme](https://developer.mozilla.org/en-US/search?q=prefers-color-scheme).
It tries to respect existing light/dark mode settings. Here’s the
stylesheet short version.

``` scss
:root {
  --text-color:                 hsl(0, 0%, 0%);
  --content-background-color:   hsla(0, 0%, 100%, 0.8);
}

@media (prefers-color-scheme: dark) {
  :root {
    --text-color:               hsl(0, 0%, 100%);
    --content-background-color: hsla(0, 0%, 0%, 0.8);
  }
}

#page-content {
   background-color: var(--content-background-color)
   color:            var(--text-color);
}
```