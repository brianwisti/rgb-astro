---
aliases:
- /2020/03/31/listing-hugo-content-extensions-with-raku/
caption: We like quick answers to important questions
category: programming
cover_image: cover.jpg
date: 2020-03-31 21:33:29
description: Twenty seconds to write a one-liner, and two days to think about it
draft: false
layout: layout:PublishedArticle
slug: listing-hugo-content-extensions-with-raku
tags:
- hugo
- Raku Lang
- csv
- site
title: Listing Hugo Content Extensions With Raku
uuid: 91515a6d-5afa-415a-b4d9-a38beca96fb3
---

How many text formatting languages have I used for my Hugo site? For
that matter, how many content files were written in each?

    $ hugo list all | raku -e 'bag(lines[1..*].map({ .split(",")[0].IO.extension })).say'
    Bag(adoc(4), html, md(327), rst(109))

Mostly Markdown, with a fair chunk of reStructuredText and a little bit
of Asciidoctor. Oh and one HTML source file, originally an [Org-Jekyll
experiment](/post/2014/10/blog-writing-in-org-mode/).

Okay that’s it. That’s the post, everyone. Time to go home\!

## Breaking it down

It helps me to understand the pieces I smash together in my one-liners.
Read along if you like, or move on to more interesting topics. I don’t
judge.

### First off: why?

The [Hugo](https://gohugo.io) static site generator supports multiple
[content formats](https://gohugo.io/content-management/formats/). I use
a few of them, which complicates my occasional urge to rebuild the whole
site with something else.

If I know how my content formats are distributed, it will help me
understand how much work I have cut out for me in The Eventual
Inevitable Rebuild.

### `hugo list`

Hugo’s [list](https://gohugo.io/commands/hugo_list) commands print a
[CSV](https://en.wikipedia.org/wiki/Comma-separated_values) list of
your site’s content files. The content listed depends on which
subcommand you use:

`list all`
: Everything\! Well, except section indexes.

`list draft`
: Content with `draft: true`

`list expired`
: Content with `expiryDate` in the past

`list future`
: Content with `date` in the future

What does that output look like?

    $ hugo list all
    path,slug,title,date,expiryDate,publishDate,draft,permalink
    content/draft/listing-hugo-content-extensions-with-raku/index.adoc,,Listing Hugo Content Extensions With Raku,2020-03-27T22:36:13-07:00,0001-01-01T00:00:00Z,0001-01-01T00:00:00Z,true,https://randomgeekery.org/draft/listing-hugo-content-extensions-with-raku/
    content/draft/managing-music-with-beets/index.adoc,,Managing My Music With Beets,2020-03-27T10:31:41-07:00,0001-01-01T00:00:00Z,0001-01-01T00:00:00Z,true,https://randomgeekery.org/draft/managing-music-with-beets/
    content/post/2020/03/stdu-viewer/index.rst,,STDU Viewer,2020-03-26T23:42:16-07:00,0001-01-01T00:00:00Z,2020-03-26T23:42:16-07:00,false,https://randomgeekery.org/2020/03/26/stdu-viewer/
    content/note/2020/03/every-post-has-a-uuid/index.rst,,Every Post Has a UUID,2020-03-21T19:06:00-07:00,0001-01-01T00:00:00Z,2020-03-21T19:06:00-07:00,false,https://randomgeekery.org/note/2020/81/every-post-has-a-uuid/

I could feed that to any language with a nice library for handling CSV
files — which is most of them. Heck, I could feed it to Excel\!

Now that I think to look, there’s the [Awesome
CSV](https://github.com/secretGeek/awesomecsv) list of tools and
resources.

But no. Today I handed it off to the first tool that came to mind.

### `raku -e`

Look, we’ve all been stuck at home for a bit. I need a break from
[Python](/tags/python). How about [Perl](https://www.perl.org/)'s sister
language, [Raku](https://raku.org/)?

    bag(lines[1..*].map({ .split(",")[0].IO.extension })).say

#### `bag(…).say`

[`bag`](https://docs.raku.org/routine/bag) uses its arguments to create
a [Bag](https://docs.raku.org/type/Bag) — basically, a set that gives
each member a "weight" based on integer values.
[`say`](https://docs.raku.org/type/Mu#method_say) prints the
[`gist`](https://docs.raku.org/routine/gist) of the Bag, telling me what
I need to know. The highest level view of this one-liner is "make a Bag
and give me a general idea what it looks like."

#### `lines[1..*].map({ … })`

Now I need to create that bag from `hugo list all`.
[`lines`](https://docs.raku.org/type/IO::Handle#routine_lines) called as
a routine creates a list of lines from
[`$*ARGFILES`](https://docs.raku.org/language/variables#$*ARGFILES),
which currently holds the piped output from my Hugo invocation. I don’t
need the header line, so I use a
[Range](https://docs.raku.org/type/Range) to
[slice](https://docs.raku.org/language/subscripts#Slices) the remaining
lines.

[`map`](https://docs.raku.org/routine/map#class_Any) applies a block to
each of those lines, returning a new list to create our Bag. What’s
going on in that map?

#### `.split(",")[0].IO.extension`

That leading dot? It’s an [item
context](https://docs.raku.org/language/contexts#Item_context) view of
the [topic
variable](https://docs.raku.org/language/variables#The_$__variable)
handed to the block by `map`. Yes, for folks who don’t feel like
clicking: *topic variable* is Raku’s name for `$_`, an easily abused
blessing of Perl languages.

So the line of comma-delimited values is
[`split`](https://docs.raku.org/type/Str#routine_split) into values.
Each line from Hugo’s CSV gets `split` into a list of values, but I only
care about the first one. The first value is the path to the content
file itself.

Coercing that to an [IO::Path](https://docs.raku.org/type/IO::Path)
object lets me ask for an
[`extension`](https://docs.raku.org/type/IO::Path#method_extension).

The block returns that extension, so when `map` is all done it has a
list of file extensions:

    (adoc adoc rst rst md md md rst ...)

During initialization, the Bag counts how many times each extension
appears in the list. Since the result of that tally is all I care about,
I print it out.

    $ hugo list all | raku -e 'bag(lines[1..*].map({ .split(",")[0].IO.extension })).say'
    Bag(adoc(4), html, md(327), rst(109))

## Alternate versions

While I was learning more about my impulsive little invocation, I
wondered about other ways to get the same information from Raku.

### A bit more Perlish

All those method dots bother you? No problem. We can use them like plain
old subroutines too. Course, we have to reach for
[`$*SPEC`](https://docs.raku.org/language/variables#$*SPEC). This
lower-level [IO::Spec](https://docs.raku.org/type/IO::Spec) object
understands file extensions on our platform.

    $ hugo list all | raku -e 'say bag(map({ $*SPEC.extension(split(",", $_)[0]) }, lines[1..*]))'
    Bag(adoc(4), html, md(327), rst(109))

### Using Text::CSV

I know what to expect from Hugo’s CSV output, but what if I didn’t? I’d
feed the standard input handle `$*IN` to H. Merijn Brand’s
[Text::CSV](https://github.com/Tux/CSV) module.

    $ zef install Text::CSV
    $ hugo list all | raku -MText::CSV -e \
      'bag(csv(in => $*IN, headers=>"skip", fragment=>"col=1").map({ .IO.extension })).say'
    Bag(adoc(4), html, md(327), rst(109))

Though if I was being *this* careful, I’d probably also move away from a
one-liner. But that takes us a long ways away from my original goal of
getting a quick answer to an idle question.

Well, I satisfied my curiosity and understood a little more Raku. That
was fun!
