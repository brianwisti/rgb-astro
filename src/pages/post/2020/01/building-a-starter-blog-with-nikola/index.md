---
aliases:
- /2020/01/05/building-a-starter-blog-with-nikola/
category: tools
cover_image: cover.png
date: 2020-01-05
description: In which I play with another site builder
draft: false
layout: layout:PublishedArticle
slug: building-a-starter-blog-with-nikola
tags:
- python
- site
- nikola
title: Building a starter blog with Nikola
uuid: 74f3d86f-f2f9-4899-ad71-16c9318a5565
---

[Nikola]: https://getnikola.com
[Hugo]: /tags/hugo

I messed with [Nikola] a while back, but ended up going with [Hugo].
Nikola has evolved in the last couple years, though.
Let’s check it out!

[Python]: /tags/python
[features]: https://getnikola.com/features

Nikola is a static site generator written in [Python][].
Its [features][] support a flexible workflow while still providing a solid blogging experience "out of the box."
You can extend that flexibility further via plugins.

[Cleaning]: /note/2019/12/removing-mmark-has-me-grumbly/
[deprecated]: https://gohugo.io/news/0.60.0-relnotes/
[mmark]: https://mmark.miek.nl/

That focused flexibility intrigues me.
[Cleaning][] my site after Hugo [deprecated][] the [mmark][] format was a chore.
My site has too many moving parts for me to casually port it, but I can still play a little.

## Setup

[pyenv]: https://github.com/pyenv/pyenv
[pyenv-virtualenv]: https://github.com/pyenv/pyenv-virtualenv

It’s generally a good idea to have a dedicated Python environment for each of your projects.
So I’ll set something up with [pyenv][] and [pyenv-virtualenv][].

    $ pyenv virtualenv 3.8.0 nikola
    $ pyenv activate nikola

[suggestion]: https://getnikola.com/getting-started.html

Next is Nikola itself.
I’ll follow the [suggestion][] to install Nikola\[Extras\], which includes all sorts of niftiness.

    $ pip install --upgrade "Nikola[Extras]"

## Initialize the site

Let’s initialize an empty site.

    $ nikola init starter-blog
    Creating Nikola Site
    ====================

    This is Nikola v8.0.3.  We will now ask you a few easy questions about your new site.
    If you do not want to answer and want to go with the defaults instead, simply restart with the `-q` parameter.
    --- Questions about the site ---
    ...
    --- Questions about languages and locales ---
    ...
    --- Questions about comments ---
    ...
    That's it, Nikola is now configured.  Make sure to edit conf.py to your liking.
    If you are looking for themes and addons, check out https://themes.getnikola.com/ and https://plugins.getnikola.com/.
    Have fun!
    [2020-01-04T07:08:02Z] INFO: init: Created empty site at starter-blog.

Okay, no need to paste the entire exchange.
Suffice to say that many questions are asked.
And as Nikola itself mentions, we can skip those questions questions with `nikola init -q`.

[bootblog4]: https://themes.getnikola.com/v8/bootblog4/

We get a configuration file written in Python and a handful of empty directories.
I see nothing for themes, but that’s okay.
Nikola starts us off with the [bootblog4][] theme.
We can pick or make new themes later.

    $ tree
    .
    ├── conf.py
    ├── files
    ├── galleries
    ├── listings
    ├── pages
    └── posts

    5 directories, 1 file

My answers to Nikola’s setup questions sit up there near the top of `conf.py`.

``` python
# Data about this site
BLOG_AUTHOR = "Brian Wisti"  # (translatable)
BLOG_TITLE = "Random Geekery"  # (translatable)
# This is the main URL for your site. It will be used
# in a prominent link. Don't forget the protocol (http/https)!
SITE_URL = "https://randomgeekery.org/"
# This is the URL where Nikola's output will be deployed.
# If not set, defaults to SITE_URL
# BASE_URL = "https://randomgeekery.org/"
BLOG_EMAIL = "brianwisti@pobox.com"
BLOG_DESCRIPTION = "The Random Geekery Blog, built with Nikola"  # (translatable)
```

[documentation]: https://getnikola.com/documentation.html

The rest of the file lists and explains default configuration.
You could learn *almost* everything you need about Nikola from the configuration file.
Nevertheless, I plan to keep the [documentation][] handy.

### Local Development

Nikola includes a built-in server to check your site locally. We have no
content yet, but let’s take a look anyways.

    $ nikola auto --browser
    [2020-01-04T17:51:45Z] INFO: serve: Serving on http://127.0.0.1:8000/ ...
    [2020-01-04T17:51:45Z] INFO: serve: Opening http://127.0.0.1:8000/ in the default web browser...

The `auto` command instructs Nikola to serve your site, refreshing
whenever you save a change. With the `--browser` flag, it also opens a
new browser tab to your development site.

<aside class="admonition note">
  <p class="admonition-title">Note</p>

Unless you’re in tmux, in which case it depends on how your desktop and
tmux are configured. I had to run `nikola auto --browser` from a
separate terminal tab in Linux Cinnamon to get the browser action. I’ll
look up how to fix that eventually.

</aside>

`http://127.0.0.1:8000` shows a basically empty front page. Nikola
filled in the templates for the default theme with values from
`conf.py`.

![screenshot of site header and footer](01-empty-site.png "The empty site")

Each of the "Archive," "Tags," and "RSS Feed" links lead to summary pages with nothing listed.
Since I have no content for Nikola to summarize yet, that makes sense.

Following the "Random Geekery" link at the top takes me to the live site.
I consider this incorrect behavior.
We want to see how the development site works, not the live site.

We can probably fix that in theme templates or with an option, but for the moment let’s just update `config.py`.

``` python
SITE_URL = "/"
```

And now the site title header links to the front page.
Perfect for today.

Let’s start blogging!

## Blogging with Nikola

Nikola supports an overwhelming number of options, especially when you start looking at plugins.
That works great for someone like me.
I constantly get new ideas not quite covered by the expected workflow, regardless of what that flow is.

Of course, "an overwhelming number of options' is not the same as "unopinionated."
Unopionated tools expect you to create your own workflow — or copy someone else’s.
Despite its many options, Nikola includes a default workflow.

### Writing a blog post

The `new_post` command asks you for a title and uses that to create a file from your settings.

    $ nikola new_post
    Creating New Post
    -----------------

    Title: Trying Out Nikola
    Scanning posts........done!
    [2020-01-04T20:39:06Z] INFO: new_post: Your post's text is at: posts/trying-out-nikola.rst

Fire up an editor — or do it automatically with `nikola new_post -e` —
and add something!

```
.. title: Trying Out Nikola
.. slug: trying-out-nikola
.. date: 2020-01-04 12:39:06 UTC-08:00
.. tags: nikola
.. category:
.. link:
.. description:
.. type: text

I can't think of anything to write here.
How about some filler with Perl and Text::Lorem?

.. code:: vim

    :r !perl -mText::Lorem -E 'say Text::Lorem->new->paragraphs(3)'

...
```

[ReStructuredText]: https://docutils.readthedocs.io/en/sphinx-docs/user/rst/quickstart.html
[Markdown]: https://daringfireball.net/projects/markdown/

Unless you configure it differently, Nikola uses [ReStructuredText][] for new posts.
RestructuredText, or ReST, is a formatting language similar in spirit to [Markdown][].
The syntax looks different, but they share a purpose: simplified writing compared to HTML for everything.
And of course Markdown is supported for those who prefer it.

[metadata documentation]: https://getnikola.com/handbook.html#metadata-fields

Nikola reads our post’s metadata from ReST comments at the front of the file.
I know I will miss something important if I tried summarizing it.
Let’s just link to Nikola’s own [metadata documentation][].

What does the site look like now that it has a post?

![screenshot of page with post content](02-index-with-post.png "Index page with one post")

This theme shows post content.
I prefer showing a quick summary of posts on the front page.

``` python
# Show teasers (instead of full posts) in indexes? Defaults to False.
INDEX_TEASERS = True
```

And a comment in the post to show where the cutoff point is:

```
.. TEASER_END

Delectus ut aut ea et dolore autem. Sint nihil sapiente voluptate id aut quo impedit. Aut
numquam delectus pariatur non accusantium. Aperiam aspernatur nemo sequi in est. Expedita
```

![screenshot with truncated post content](index-with-teaser.png "Index page with teaser")

Now the index has a summary and the main content is on the post page.
The tag rests at the bottom, and a source link sits with the headline.

![screenshot with post content with metadata](03-post.png "The post itself")

What about that "Source" link?
Nikola lets you download the ReST source of a post.
Neat, but not a feature I care about.

``` python
# Copy the source files for your pages?
# Setting it to False implies SHOW_SOURCELINK = False
COPY_SOURCES = False
```

Okay I need to stop.
I intended to focus on the default Nikola flow.
But here I am poking at `config.py`.
Oh well.
I gotta be me.

But still let’s move on.

The Archive, Tags, and RSS Feed links work, listing posts as expected.
The lists aren’t very interesting with only one post though.
I’ll see what I can come up with for next time.
Oh and I’m not sure I can properly describe how excited I am that Archive automatically generates pages for years.
I didn’t have to make a special-purpose taxonomy or anything\!

## Adding Pages

Anyways.
Blogging is good, but a site needs more than blog posts.
Let’s use `nikola new_post -p` to create a page instead of a post.

    $ nikola new_post -p
    Creating New Page
    -----------------

    Title: Now
    Scanning posts........done!
    [2020-01-05T09:37:40Z] INFO: new_page: Your page's text is at: pages/now.rst

Everybody could use a [/now](/now/) page.
Excuse me a moment while I edit `pages/now.rst`.
Oh!
Since it’s not a post, it won’t show up unless we link to it.
The `/now` page is significant enough that it should go on the site menu.

Back over to `config.py`:

``` python
NAVIGATION_LINKS = {
    DEFAULT_LANG: (
        ("/pages/now/", "Now"),
        ("/archive.html", "Archive"),
        ("/categories/", "Tags"),
        ("/rss.xml", "RSS feed"),
    ),
}
```


![screenshot of /now page](now.png "The Now page")

## What’s left?

If this was a really real site, we would build and deploy.

    $ nikola build
    $ nikola deploy

[deployment]: https://getnikola.com/handbook.html#deployment
[rsync]: https://rsync.samba.org/

Nikola has a `deploy` command?
Well sure!
You can configure multiple [deployment][] options.
[rsync][] — my favorite — even gets highlighted in the commented example.

``` python
# DEPLOY_COMMANDS = {
#     'default': [
#         "rsync -rav --delete output/ joe@my.site:/srv/www/site",
#     ]
# }
```

But I’m leaving that section of `config.py` alone for now.

This was fun!
Will I replace Hugo with Nikola?
I don’t know yet.
I’d have to try importing and building the current site.

That sounds like a project for another day.
