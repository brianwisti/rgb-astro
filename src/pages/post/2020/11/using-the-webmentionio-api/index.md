---
caption: A spiderweb! For Webmention! Get it? Okay, yeah. Sorry.
category: tools
cover_image: cover.jpg
date: 2020-11-10
description: Fetching my IndieWeb mentions with HTTPie and Requests
draft: false
format: md
layout: layout:PublishedArticle
series:
- fixing my webmentions
slug: using-the-webmentionio-api
tags:
- Python
- IndieWeb
- FixingMySite
- Site
title: Using the Webmention.io API
uuid: 0f72149c-238d-4474-8ed5-38c281c9a7e4
---

So I hosed a local copy of my mentions feed the other month.  What’s my
"mentions feed," I hear you wondering?

Whenever somebody shares a reaction to something here — like, reshare, reply,
mention — that reaction gets sent to [Webmention.io][webmention-io].  There are
more moving parts than that, of course.  [Bridgy][bridgy] aggregates reactions
to my announcement toots and tweets and sends those to Webmention.  It shows in
my mentions feed as a reaction to site content when someone reacts to a
relevant tweet.

*Sometimes* folks even post mentions, replies, and reactions directly to the
Webmention endpoint.  Mostly it’s just social media reactions, though.

The Webmention.io [API][api] lets me gather all of these reactions.

Let’s acquaint ourselves with the important parts of this API.  You’ll need
your API token, which can be found in the Webmention [settings][] once you sign
up.

## Reading the feed with HTTPie

I’ll use [HTTPie][httpie] for my little exploration.  I like the way it works.

``` text
pip install httpie
```

### Getting recent reactions

We mainly care about the mentions endpoint.  Hand it your domain and API token,
and it will send you the 20 most recent responses for your site.

``` bash
http get https://webmention.io/api/mentions.jf2 \
  domain==randomgeekery.org \
  token==$WEBMENTION_KEY
```

HTTPie’s double-equals `==` syntax means "make a query string," so I end up
with something like this::

``` text
https://webmention.io/api/mentions.jf2?domain=randomgeekery.org&token=xxxxx
```

When `http` fetches that URL, I get back a [JF2][jf2] feed that looks something
like this.

``` json
{
    "children": [
        {
            "author": {
                "name": "Jumpei KAWAMI",
                "photo": "https://webmention.io/avatar/…",
                "type": "card",
                "url": "https://twitter.com/junkw"
            },
            "content": {
                "text": "I wrote a note:\n\nI added this note from org mode…"
            },
            "published": "2020-10-25T23:32:25+00:00",
            "repost-of": "https://randomgeekery.org/note/2020/10/i-added-this-note-from-org-mode/",
            "type": "entry",
            "url": "https://twitter.com/junkw/status/1320508544601509889",
            "wm-id": 887739,
            "wm-private": false,
            "wm-property": "repost-of",
            "wm-received": "2020-10-26T04:07:20Z",
            "wm-source": "https://brid-gy.appspot.com/repost/twitter/brianwisti/…",
            "wm-target": "https://randomgeekery.org/note/2020/10/i-added-this-note-from-org-mode/"
        },
        ⋮
    ],
    "name": "Webmentions",
    "type": "feed"
}
```

What’s JF2?  It’s obviously JSON.  Maybe something to do with [JSON
Feed][json-feed]?  Similar, but no.  JF2 is a JSON format for IndieWeb’s
[microformats2][microformats2].  The mnemonic I’ve been trying to drill into my
head is "JSON (micro)Formats 2."

It’s not a very good mnemonic.

Each entry summarizes the reaction, including which of my posts they were
reacting to.  That’s kind of important.  Most recently, Twitter user
[@junkw][junkw] retweeted my announcement about [adding a note from Org
mode][adding-a-nite-from-org-mode].

:::note

There’s also a `.json` endpoint for every feed that presents a different
structure for mentions.  I prefer it, because it contains fewer `wm-*`
fields.  But the documentation uses JF2, so that’s what I’ll do.

:::

### Checking for new reactions

Maybe I’m checking again later and only want to see the *new* reactions.  I
request mentions received since the value of the `wm-received` field in the
last entry I have.

``` bash
http get https://webmention.io/api/mentions.jf2 \
  domain==randomgeekery.org \
  token==$WEBMENTION_KEY \
  since=="2020-10-26T04:07:20Z"
```

``` json
{
    "children": [],
    "name": "Webmentions",
    "type": "feed"
}
```

Well, yeah.  That makes sense.  I don’t get the kind of traffic where you’d
expect fresh reactions every time you check.

### Fetching the oldest reactions first

As I mentioned at the start, my site is a little broken.  I need to rebuild the
full list of reactions so my [Hugo][hugo] site can work with a complete record.
To do that, I should probably start from the oldest mentions and work my way
forward.

Rather than the default `sort-dir` of `down`, I specify `up`.

``` bash
http get https://webmention.io/api/mentions.jf2 \
  domain==randomgeekery.org \
  token==$WEBMENTION_KEY \
  sort-dir==up
```

``` json
{
    "children": [
        {
            "author": {
                "name": "Steve Scaffidi",
                "photo": "https://webmention.io/avatar/…",
                "type": "card",
                "url": "https://twitter.com/hercynium"
            },
            "content": {
                "html": "This is where I wish Perl5 had something like Python's AST class hierarchy…",
                "text": "This is where I wish Perl5 had something like Python's AST class hierarchy…"
            },
            "in-reply-to": "https://randomgeekery.org/2020/02/17/python-invoke/",
            "published": "2020-02-18T03:11:58+00:00",
            "type": "entry",
            "url": "https://twitter.com/hercynium/status/1229604443651526656",
            "wm-id": 757935,
            "wm-private": false,
            "wm-property": "in-reply-to",
            "wm-received": "2020-02-18T22:32:20Z",
            "wm-source": "https://brid-gy.appspot.com/comment/twitter/brianwisti/…",
            "wm-target": "https://randomgeekery.org/2020/02/17/python-invoke/"
        }
    ],
    "name": "Webmentions",
    "type": "feed"
}
```

Aww, my first site reply. From [@hercynium][hercynium].

I only get 20 results by default, though.  Here.  Let’s make [jq][] show us.
Here’s a default page.

``` bash
http get https://webmention.io/api/mentions.jf2 \
  domain==randomgeekery.org token==$WEBMENTION_KEY sort-dir==up \
  | jq '.children | length'
```

``` text
20
```

### Handling result pagination

I can specify how many responses I want in each response with the `per-page`
parameter.  With `per-page` set to 100, I get a hundred entries.

``` bash
http get https://webmention.io/api/mentions.jf2 \
  domain==randomgeekery.org token==$WEBMENTION_KEY per-page==100 \
  | jq '.children | length'
```

``` text
100
```

Of course, if there aren’t a hundred entries to fill the page, I only get
what’s available.

``` bash
http get https://webmention.io/api/mentions.jf2 \
  domain==randomgeekery.org token==$WEBMENTION_KEY since=="2020-10-26T04:07:20Z" per-page=100 \
  | jq '.children | length'
```

``` text
0
```

The `page` parameter — which starts at zero — lets me step through the feed
in batches.

``` bash
http get https://webmention.io/api/mentions.jf2 \
  domain==randomgeekery.org \
  token==$WEBMENTION_KEY \
  sort-dir==up \
  page==1
```

``` json
{
    "children": [
        {
            "author": {
                "name": "brian wisti",
                "photo": "https://webmention.io/avatar/…",
                "type": "card",
                "url": "https://twitter.com/brianwisti"
            },
            "content": {
                "html": "…",
                "text": "…"
            },
            "in-reply-to": "https://randomgeekery.org/2020/01/19/restructuredtext-basics-for-blogging/",
            "published": "2020-03-10T06:24:45+00:00",
            "type": "entry",
            "url": "https://twitter.com/brianwisti/status/1237263101482823681",
            "wm-id": 766993,
            "wm-private": false,
            "wm-property": "in-reply-to",
            "wm-received": "2020-03-10T06:38:55Z",
            "wm-source": "https://brid-gy.appspot.com/comment/twitter/brianwisti/…",
            "wm-target": "https://randomgeekery.org/2020/01/19/restructuredtext-basics-for-blogging/"
        },
        ⋮
    ],
    "name": "Webmentions",
    "type": "feed"
}
```

Right.  That’s Bridgy catching a Twitter thread.  At least I can see the full
conversation from my site.  Or I will once I’m done fixing everything.

### Bonus: checking for reactions to a specific post

I could get a JF2 feed for specific URLs on my site if I was so inclined.

``` bash
http get https://webmention.io/api/mentions.jf2 \
  target==https://randomgeekery.org
```

``` json
{
    "children": [
        {
            "author": {
                "name": "",
                "photo": "",
                "type": "card",
                "url": ""
            },
            "mention-of": "https://randomgeekery.org",
            "published": null,
            "type": "entry",
            "url": "https://kevq.uk/blogroll/",
            "wm-id": 796241,
            "wm-private": false,
            "wm-property": "mention-of",
            "wm-received": "2020-05-14T11:25:47Z",
            "wm-source": "https://kevq.uk/blogroll/",
            "wm-target": "https://randomgeekery.org"
        }
    ],
    "name": "Webmentions",
    "type": "feed"
}
```

I deal with my site reactions in bulk so they can be incorporated in the Hugo
build.  This could be handy for JavaScript-driven update on reactions since the
site was last built and pushed, though.

## Rebuilding the local mentions file

Now I want to take what I learned about the API to build a local copy of my
site’s mention history.  Let’s step away from HTTPie and the command line
before I try something dangerous.

The [Requests][requests] library for [Python][python] can help me build one
list of Webmentions.

**`rebuild-mentions-feed.py`**

```python
import json
import os
import time

import requests

def rebuild_full_feed(domain: str, token: str, target_file: str) -> None:
    endpoint = "https://webmention.io/api/mentions.jf2"
    page_size = 100
    all_entries = []
    page_index = 0

    while True:
        params = {
            "domain": domain,
            "token": token,
            "page": page_index,
            "per-page": page_size,
            "sort-dir": "up",
        }
        r = requests.get(endpoint, params=params)
        this_page = r.json()
        entries = this_page["children"]
        all_entries += entries
        page_index += 1

        entry_count = len(entries)
        print(f"Added {entry_count} entries")

        # Be a polite Internet citizen
        time.sleep(1)

        # Stop when we're done
        if entry_count < page_size:
            print("Reached end of feed")
            break

    with open(target_file, "w") as f:
        json.dump(all_entries, f, indent=4)
        print(f"Wrote {len(all_entries)} entries to {target_file}")


if __name__ == "__main__":
    domain = "randomgeekery.org"
    token = os.environ["WEBMENTION_KEY"]
    target_file = "mentions.jf2"
    rebuild_full_feed(domain, token, target_file)
```

``` text
$ python rebuild-mentions-feed.py
```

``` text
Added 100 entries
Added 100 entries
Added 100 entries
Added 83 entries
Reached end of feed
Wrote 383 entries to mentions.jf2
```

This gives me the first requirement for rebuilding my mentions: an intact
historical record, up to the current moment.

## Intermission

Time to pause.

Why?  Why not just use this JSON as a [Hugo data file][data-file] — let it
filter through finding relevant mentions for each post?

Short answer: that’s how I got myself into this mess in the first place.
I want to take a more careful approach this time.

I have some ideas.  Spoiler alert: [sqlite-utils][] is involved. [Again][again].

But first push this and get ready for bed so I’m at least a little rested for
work.

[webmention-io]: https://webmention.io
[bridgy]: https://brid.gy
[api]: https://github.com/aaronpk/webmention.io#api
[settings]: https://webmention.io/settings
[httpie]: https://httpie.io
[jf2]: https://www.w3.org/TR/jf2/
[json-feed]: https://jsonfeed.org/
[microformats2]: http://microformats.org/wiki/microformats2
[junkw]: https://twitter.com/junkw
[adding-a-note-from-org-mode]: /note/2020/10/i-added-this-note-from-org-mode/
[hugo]: /tags/hugo
[hercynium]: https://twitter.com/hercynium
[jq]: https://stedolan.github.io/jq/
[requests]: https://requests.readthedocs.io/en/master/
[python]: /tags/python
[data-file]: https://gohugo.io/templates/data-templates/
[sqlite-utils]: https://sqlite-utils.readthedocs.io/en/stable/
[again]: link:/post/2020/05/querying-hugo-content-with-python/