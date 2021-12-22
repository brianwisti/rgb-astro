---
date: 2019-09-19 08:43:31
layout: layout:PublishedArticle
slug: i-fixed-my-dot-pages
tags:
- hugo
- oops
title: I FIXED MY .Pages
uuid: 23aaf1bf-9e0d-476b-8048-fe8aa05a7f58
---

Too tired to make it make sense. My site broke under Hugo .58. No front page listing. I fixed it. Yay!

Instead of (for notes):

```
{{- range first 1 (where .Pages "Section" "note") -}}
```

I used

```
{{- range first 1 (where .Site.RegularPages "Section" "note") -}}
```

I also fixed the RSS feed, and updated the [feeds post][] with those (very similar) details.

[feeds post]: /post/2017/09/full-content-hugo-feeds/