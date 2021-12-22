---
aliases:
- /2018/11/10/using-hugo-data-templates/
category: tools
date: 2018-11-10 00:00:00
draft: false
layout: layout:PublishedArticle
slug: using-hugo-data-templates
tags:
- hugo
- site
title: Using Hugo Data Templates
uuid: 881b6c52-2a66-4c9f-b86b-fc5fa1daf9f3
---

I put my frequently used links in a [Hugo](https://gohugo.io/) data
template to cut down on copying and pasting between posts.

## Motive

I often create several [knitting](/tags/knitting) or
[crochet](/tags/crochet) projects from the same book, or reference the
same tutorial for a technique that I find tricky. Today, linking to
those references in a post involves copying and pasting the URL from
somewhere else – usually the blog post for a previous project. This is
tedious at best, and becomes downright troublesome if and when the link
for that reference changes.

Hugo [data templates](https://gohugo.io/templates/data-templates/) could
fix all that.

Data templates are written in [YAML](https://yaml.org),
[TOML](https://github/toml-lang/toml), or [JSON](https://json.org)
format and saved to your site’s `data` folder. Your data templates and
their contents become available to Hugo via the `$.Site.Data` variable.
Organize your data templates however you like, and make them as complex
as you want.

## My data template for links

Before getting carried away with visions of complex structures to meet
my every desire, what do I need *right now*?

I need a glossary of links I can reference at any time. Its entries must
provide what I consider the canonical resource URL for a book or topic.
That’s it. I can revisit the glossary idea if my needs change later.

So let’s start with the links I just used. I like to talk about YAML,
TOML, and JSON sometimes, after all.

**`data/links.toml`**

```toml
# Frequently used URLs
JSON = "https://json.org/"
TOML = "https://github.com/toml-lang/toml"
YAML = "http://yaml.org/"
```

The filename provides part of the data structure for Hugo. For example,
the "TOML" entry in `data/links.toml` becomes `$.Site.Data.links.JSON`.

Nobody but me sees these keys – except right now, while I am telling
*you* about them. Since they’re for me, it’s most important that I pick
keys I can remember easily within the limitations of the data format.
"JSON" works. "TheJsonSpecificationSite" probably would not. "The JSON
Site" is a legal key in TOML, but in this case not a helpful one.

## Getting the data from my template

How do I *use* these URLs? With a
[shortcode](https://gohugo.io/templates/shortcode-templates/)\! Again,
focusing on exactly what I need right now: the URL in
`$.Site.Data.links` corresponding to a key.

`layouts/shortcodes/linkFor.html` provides just that. It uses its first
positional argument as a key, returning the value at that
[index](https://gohugo.io/functions/index-function/) in the glossary.

``` html
{{- with .Get 0 -}}{{ index $.Site.Data.links . }}{{- end -}}
```

Then in my content Markdown:

``` md
[TOML]({{</* linkFor "TOML" */>}})
```

That’s *almost* everything I need. I should throw in error checking for
inevitable typos such as the one I made a couple minutes ago.

``` md
[TOML]({{</* linkFor "YOML" */>}})
```

I don’t need anything fancy, but I do need something to tell me if
there’s a problem. The system quietly returns nothing if there is no
entry for the key. I would hate to have empty links all over my site due
to a lazily written shortcode.

```
{{- with .Get 0 -}}
   {{- $url := index $.Site.Data.links . -}}
   {{- if $url -}}
       {{- $url -}}
   {{- else -}}
       {{- errorf "No link for key %s" . -}}
   {{- end -}}
{{- end -}}
```

Now I get an error both on the console and in the browser:

    $ hugo server -D
    Building sites … ERROR 2018/11/10 15:53:14 No link for key YOML
    Total in 1389 ms
    Error: Error building site: logged 1 error(s)

![Hugo shows the error in-browser](error-screenshot.png)

This provides what I need for today.

## Other thoughts?

- When do I put a link in the data template? Like so many things in
  life, it depends. Sometimes I’ll want to add it immediately. Other
  times I have the URL practically memorized.
- I’ll probably need to keep that `data/links.toml` handy when writing
  a post, since the keys will get harder to remember.
- I could have used a Params entry in the site’s `config.toml`, but
  keeping the glossary in its own file keeps the configuration from
  getting cluttered.