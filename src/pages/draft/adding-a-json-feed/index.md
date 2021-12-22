---
category: Tools
description: I added a JSON Feed to my site. I’ll figure out what to do with it later.
draft: true
layout: layout:Article
tags:
- site
- hugo
title: Adding a Json Feed
uuid: 6bd677b0-9e8f-4fd3-8946-68b4059cc2fe
---

## What?

[JF2 feed]: https://www.w3.org/TR/jf2/#jf2feed
[RSS feed]: https://en.wikipedia.org/wiki/RSS

A [JF2 feed][] is similar to a [RSS feed][], except JSON instead of XML.
That’s not particularly helpful, is it? Well, a feed provides a way for
folks to stay caught up with what you publish on your site, without
needing to visit the site every day (or wait for you to mention the post
on Twitter / Facebook / whatever).

* What is [JSON Feed][]?
* How might people use a JSON feed?
  * news reader
  * dude it’s JSON

## How?

[hugo-jf2]: https://github.com/kaushalmodi/hugo-jf2
[Hugo]: https://gohugo.io
[Theme components]: https://gohugo.io/themes/theme-components/

[hugo-jf2][] is a theme component for the [Hugo][] static site generator.
[Theme components][] are not complete themes, but bits that add some new aspect to your site:
shortcodes, styles, maybe a new output format. You wouldn’t go too far
off by thinking of them as plugins.

``` toml
[outputFormats.JSON]
MediaType = "application/json"
BaseName = "feed"
suffix = "json"
IsHTML = false
IsPlainText = true
noUgly = false # What is this?
Rel = "alternate"

[outputs]
  home = [ "HTML", "RSS", "JSON" ]
  section = [ "HTML", "RSS", "JSON" ]
  tag = [ "HTML", "JSON" ]
  year = [ "HTML", "JSON" ]
```

[jq]: https://stedolan.github.io/jq

* PART TWO
  * Neat. Lemme do some cool JSON shit.
  * dude it’s JSON
    * Do some filter type thing with [jq][]
    * Have some fun with `-Mojo` _yagni_