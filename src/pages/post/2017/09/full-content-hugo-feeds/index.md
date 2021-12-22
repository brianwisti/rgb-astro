---
aliases:
- /post/2017/full-content-hugo-feeds/
- /2017/09/15/full-content-hugo-feeds/
category: tools
date: 2017-09-15
draft: false
layout: layout:PublishedArticle
slug: full-content-hugo-feeds
tags:
- site
- hugo
title: Full Content Hugo Feeds
updated: 2019-09-19
uuid: 0d74e0d0-c835-499e-bdce-6f5bb1eeaa90
---

[Hugo]: http://gohugo.io/
[RSS file]: /index.xml

[Hugo][] defaults to filling your [RSS file][] with the summary of every post. I
prefer the full content of the most recent posts. Today I make my RSS feed
reflect my preferences.

## The Problem

Hugo RSS feeds have minor quirks that annoy me.

[Feedly]: https://feedly.com/

First off, it includes *every* page and post by default. The site content
includes posts going all the way back to the year 2000. Most sites I subscribe
to on [Feedly][] show only the most recent posts. I want to do the same here.

Also, Hugo uses the `.Summary` of my content in the description for each item of
the feed. There’s nothing wrong with this, but I like being able to read a full
post without leaving Feedly - or whatever I use for RSS this week.

## A Solution

[Hugo RSS Template documentation]: https://gohugo.io/templates/rss/

The [Hugo RSS Template documentation][] tells me what I need to know. I can
change the entry count in site config, and handle the content of each entry with
a template.

### Limit Entry Count

Just the relevant bits of my `config.json`. Twenty entries seems like a good
arbitrary value.

```json
{
  "languageCode": "en-us",
  "copyright": "This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License",
  "rssLimit": 20,

  "author": {
    "name": "Brian Wisti",
    "email": "brianwisti@pobox.com"
  }
}
```

### All The Content

[default]: https://gohugo.io/templates/rss/#the-embedded-rss-xml

All I need to do here is copy the [default] RSS template into
`layouts/_default/rss.xml`, then make my changes.

My changes are small indeed. I place the post `.Content` in the description
instead of the `.Summary`.

```xml
<description>{{ .Content | html }}</description>
```

The full entry looks like this.

<aside class="admonition note">
<p class="admonition-title">Note</p>

Updated for Hugo 0.57, which changed how `.Pages` worked.
Now use `.RegularPages`, and for top-level RSS use `.Site.RegularPages`

</aside>

```xml
{{- $pages := .RegularPages -}}
{{- if .IsHome -}}
  {{- $pages = .Site.RegularPages -}}
{{- else -}}
{{- end -}}
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>{{ if eq  .Title  .Site.Title }}{{ .Site.Title }}{{ else }}{{ with .Title }}{{.}} on {{ end }}{{ .Site.Title }}{{ end }}</title>
    <link>{{ .Permalink }}</link>
    <description>Recent content {{ if ne  .Title  .Site.Title }}{{ with .Title }}in {{.}} {{ end }}{{ end }}on {{ .Site.Title }}</description>
    <generator>Hugo -- gohugo.io</generator>{{ with .Site.LanguageCode }}
    <language>{{.}}</language>{{end}}{{ with .Site.Author.email }}
    <managingEditor>{{.}}{{ with $.Site.Author.name }} ({{.}}){{end}}</managingEditor>{{end}}{{ with .Site.Author.email }}
    <webMaster>{{.}}{{ with $.Site.Author.name }} ({{.}}){{end}}</webMaster>{{end}}{{ with .Site.Copyright }}
    <copyright>{{.}}</copyright>{{end}}{{ if not .Date.IsZero }}
    <lastBuildDate>{{ .Date.Format "Mon, 02 Jan 2006 15:04:05 -0700" | safeHTML }}</lastBuildDate>{{ end }}
    {{ with .OutputFormats.Get "RSS" }}
        {{ printf "<atom:link href=%q rel=\"self\" type=%q />" .Permalink .MediaType | safeHTML }}
    {{ end }}
    {{ range $pages }}
    <item>
      <title>{{ .Title }}</title>
      <link>{{ .Permalink }}</link>
      <pubDate>{{ .Date.Format "Mon, 02 Jan 2006 15:04:05 -0700" | safeHTML }}</pubDate>
      {{ with .Site.Author.email }}<author>{{.}}{{ with $.Site.Author.name }} ({{.}}){{end}}</author>{{end}}
      <guid>{{ .Permalink }}</guid>
      <description>
        {{- $coverImage := .Resources.GetMatch "cover*" -}}
        {{- if $coverImage -}}
          &lt;a href=&#34;{{ .Permalink }}&#34; title=&#34;{{ .Title }}&#34;&gt;
            &lt;img src=&#34;{{ ($coverImage.Resize "600x").RelPermalink }}&#34; alt=&#34;{{ .Title }}&#34;&gt;
          &lt;/a&gt;
        {{- end -}}
        {{ .Content | html }}
      </description>
    </item>
    {{ end }}
  </channel>
</rss>
```

That ought to do it.

### What Else?

What else I could do with the feed?

[RSS Best Practices Profile]: http://www.rssboard.org/rss-profile
[Raymond Camden wrote a post]: https://www.raymondcamden.com/2017/05/18/creating-a-json-feed-for-hugo/
[JSON Feed]: https://jsonfeed.org/

* This [RSS Best Practices Profile][] includes things I could tweak in my RSS
  template, though that’s more about nice form than any urgent need.
* [Raymond Camden wrote a post][] about adding a [JSON Feed][] to your Hugo site.
  It might be fun to do that here.