---
aliases:
- /tools/2015/07/19_making-a-jekyll-collection.html
- /post/2015/making-a-jekyll-collection/
- /2015/07/19/making-a-jekyll-collection/
category: tools
date: 2015-07-19 00:00:00
description: In which I try out Jekyll's experimental Collections
layout: layout:PublishedArticle
slug: making-a-jekyll-collection
tags:
- jekyll
- site
title: Making a Jekyll Collection
updated: 2020-02-25 00:00:00
uuid: bcfdd86c-4ebe-475a-a396-24c931022ca6
---

[Jekyll](http://jekyllrb.com) currently generates the HTML for my site.
I am curious about the experimental
[collections](http://jekyllrb.com/docs/collections/) feature, and
whether it could be useful for me.

This post should not be too difficult to read along with — and I will
happily fix any problems you notice — but I do assume you know the basics
of creating a blog with Jekyll. The code and templates were initially
build on Jekyll 3.0.0.beta8.

<aside class="admonition">
<p class="admonition-title">Updates</p>

2020-02-25
: Hey where’d the rest of the post go? Must have lost it with a cleanup
  script at some point. No worries. Thanks to the [Internet
  Archive](https://archive.org) everything is roughly back where it
  [was](https://web.archive.org/web/20160318224730/http://randomgeekery.org/post/2015/making-a-jekyll-collection).

2015-08-07
: Reader Eric Tirado noticed that I broke the individual crafts project
  links — again. So I fixed it for real. Just set the collection
  `permalink` to something useful in `_config.yml`.

2015-07-21
: I ended up having several issues attributable to either collections
  under Jekyll 3.0 beta or Octopress 3. Decided to switch to Jekyll 2.5.3
  and made a few adjustments to the collections template. Everything
  *seems* okay now.

</aside>

What? Why?
----------

So what the heck is a collection? From the Jekyll
[collections](http://jekyllrb.com/docs/collections/) documentation:

> Not everything is a post or a page. Maybe you want to document the
> various methods in your open source project, members of a team, or
> talks at a conference. Collections allow you to define a new type of
> document that behave like Pages or Posts do normally, but also have
> their own unique properties and namespace.

Collections could be useful when you have things you want to show on
your site without necessarily being tied to the blog-centric structure
of Posts or the simple content dump of a Page.

Who would that help, besides the slightly technical examples from the
description?

-   A writer could organize their stories into collections
-   An artist could present their works as one or more collections
-   A knitter could put their yarn projects in a collection.
-   Anyone who takes pictures could use collections as photo galleries.
-   Recipes, maybe?
-   Music playlists!
-   All the books I own, and the few I have actually read!

A blog post probably works for most of these use cases. Maybe fiddle a
bit with categories and put a tag here and there, and your content is
out there for anyone. Good enough.

"Good enough" isn’t good enough for every case, though. Occasionally you
want to tune some of your content in a special way. You may find this is
easier with collections than with blog posts.

There are also dedicated sites for all of these ideas, and those are
good enough too. Some excel at the services they provide. They have
concerns too. Now the visibility of your creations is tied to the
fortunes and policies of whoever provides that service. Keeping that in
a collection on your own site gives you a backup if the service goes
away, at least.

I could use collections for my knitting and crochet projects. I have a
couple of [knitting](/tags/knitting/) blog posts here. My
[account](http://www.ravelry.com/people/brianwisti) on
[Ravelry](https://www.ravelry.com) highlights a handful of other WIPs
and FOs: *Works In Progress* and *Finished Objects*.

The blog posts work fine as blog posts, but I still want a separate way
to organize those projects. The stuff on Ravelry can only be seen if you
have an account with the service. That’s fine, but I have spent 2015
consolidating material I’ve created elsewhere onto my site. Ravelry is a
reasonable next target for me.

Fine. How?
----------

First I need to add a `collections` entry to my `_config.yml`
[configuration](http://jekyllrb.com/docs/configuration/) file. This
entry contains a list of all collections in the site, and metadata for
each collection. I want these collections displayed on the site, so I
must set the `output` metadata for the collection to `true`. I also want
give consistent URLs for my project pages. This has been an issue for me
bouncing between Jekyll 2.5.3 and 3.0.0 beta. Setting `permalink` takes
care of that issue.

```yaml
collections:
  crafts:
    output: true
    permalink: /crafts/:path/
```

Next I create the folder to hold this collection. By default its name
must match the collection name with an underscore prefix.

    $ mkdir _crafts

### One Thing

Time to put something in the collection. I can use my recent [garter
stitch scarf post](/post/2015/04/quick-garter-stitch-scarf) as a
starting point, filling in the details of a new collection item from
that post.

**`crafts/garter-scarf-wrapped.md`**

```markdown
---
name: Quick Garter Stitch Scarf
layout: craft
image: /img/2015/garter-scarf-wrapped.jpg
finished: 2015-04-04
posts:
  - title: A Quick Garter Stitch Scarf
    url: /marginalia/2015/04/04_quick-garter-scarf.html
---

I made this scarf as a quick break from all the socks I made or tried to make
over the last few years. The scarf pleased its new owner immensely, and she
wears it whenever the weather permits.
```

I can add more detail later, but this gives me a good start.

How about a layout template for the project? This is the best I could
come up with using my current knowledge of [Liquid
templates](https://github.com/Shopify/liquid).

```liquid
---
layout: default
---
<article class="post">
  <header class="post-header">
    <h1 class="post-title">{{ page.name }}</h1>
    <span class="post-meta">
      Finished {{ page.finished | date: site.date_format }}
    </span>
  </header>
  <div class="post-content">
    <figure>
      {% img {{ page.image }} class="pure-img" alt="{{ page.name }}" %}
      <figcaption>{{ page.name }}</figcaption>
    </figure>
    {{ content }}
    {% if page.posts %}
    <h2>Posts About This Project</h2>
    <ul>
      {% for link in page.posts %}
        <li><a href="{{ link.url }}">{{ link.title }}</a></li>
      {% endfor %}
    </ul>
    {% endif %}
  </div>
</article>
```

As far as Jekyll is concerned, the collection item is just another page.
Use `page` to get at front matter for this item.

Oh and while I was putting this page together I learned about the
[Octopress Image Tag](https://github.com/octopress/image-tag) plugin. I
expect to be using that a lot more in the future!

![Voila!](crafts-project.png)

Now I have a page for this project, but how will visitors know it’s
there? How about I start with some sort of summary on the site’s index
page?

### Just The New Things

Here is a simple approach. Just make a list of the items in the
collection.

```liquid
<div class="home">
  <h2>My Crafts Projects</h2>
  <ul>
    {% for project in site.crafts %}
      <li><a href="{{ project.url }}">{{ project.name }}</a></li>
    {% endfor %}
  </ul>
  <ul class="post-list">
    {% for post in site.posts %}
```

![A short and sweet summary](crafts-summary-01.png)

Sure, that works for the moment. Let’s get some more projects in that
collection. I can add the projects from my Ravelry account for now.

![Listing every project](crafts-summary-02.png)

Ok, new problem.

I see aesthetic issues here, but that’s not the problem. My site index
limits itself to only showing this year’s blog posts. This collection
summary shows every craft project I ever documented.

The project list should only show projects I have finished so far in the
year.

``` liquid
{% assign this_year = 'now' | date: "%Y" %}
<h2>{{ this_year }} Crafts Projects</h2>
<ul>
  {% assign projects = site.crafts | sort: 'finished' | reverse %}
  {% for project in projects %}
    {% assign finished_in = project.finished | date: "%Y" %}
    {% if finished_in == this_year %}
      <li><a href="{{ project.url }}">{{ project.name }}</a></li>
    {% endif %}
  {% endfor %}
</ul>
```

Jekyll sorts collections by filename. Since time finished matters to me
now, I create a copy of the crafts collection sorted from most recently
finished to oldest. Now I can step through that copy, only summarizing
projects completed this year. Liquid may have an easier way, but I
haven’t learned it yet.

![Just the newest projects please](crafts-summary-03.png)

### All The Things

Wait. How will a visitor find those old projects? Time to make an
archive page. I can follow the idea of the [post archive](/post/) for
now, listing every project ever. `crafts/index.html` will hold that
archive.

``` liquid
---
title: My Crafts Projects
layout: page
permalink: /crafts/
---

<p>Not every project I have ever done, but every project I have ever documented.</p>

{% assign projects = site.crafts | sort: 'finished' | reverse %}
{% for project in projects %}
  {% assign year_finished = project.finished | date: "%Y" %}
  {% if year_finished != year %}
    {% unless forloop.first %}
      </ul>
    {% endunless %}
    <h2>{{ year_finished }}</h2>
    <ul>
    {% assign year = year_finished %}
  {% endif %}
  <li><a href="{{ project.url }}">{{ project.name }}</a></li>
  {% if forloop.last %}
    </ul>
  {% endif %}
{% endfor %}
```

Then add a link to my index page and craft project template.

    <p>See the <a href="/crafts/">Crafts</a> page to see all projects.

![Short and sweet version of the crafts index](crafts-index.png)

Well it is painfully obvious that I need to dig through my photos and
fill in gaps for those missing years.

The “Jekyll collections” part of this blog post is done. I talked about
building a collection, creating detail pages — though not every
collection needs those — along with a summary for the site index and a
page listing every item in the collection. We are done here.

### But —

I know. I mentioned an aesthetic issue earlier. You want to *see* the
knitting projects in those summaries. I will gloss over the details.
They deserve a blog post of their own.

-   Make thumbnails for each of my craft pictures.
-   Add a `thumbnail` item with a thumbnail path to the Front Matter for
    each project.
-   Include a thumbnail pic in the project summary.
-   Fiddle a bunch with CSS for the summary and craft index views.

Generating a thumbnail and associating it with the project sounds like
the sort of thing that should be automated, but none of the Jekyll
plugins I found were quite right for the task. I may end up making my
own plugin at some point, assuming I stick with a single blog generator
long enough to learn how to make plugins.

Anyways, I add a `thumbnail` front matter entry for each collection
item.

``` yaml
    thumbnail: /img/2015/garter-scarf-wrapped-thumbnail.jpg
```

Adding thumbnails and captions makes the item summary a little more
complex, so I create `_includes/craft-summary-item.html` to hold that
summary.

```liquid
<figure class="crafts-item-thumbnail">
  <a href="{{ project.url }}">
    <img src="{{ project.thumbnail }}"
      height="128" width="128"
      alt="{{ project.name }}">
  </a>
  <figcaption><a href="{{ project.url }}">{{ project.name }}</a></figcaption>
</figure>
```

I update `index.html` to reference the new include file.

```liquid
{% assign this_year = 'now' | date: "%Y" %}
<h2>{{ this_year }} Crafts Projects</h2>
<ul class="crafts-collection">
  {% assign projects = site.crafts | sort: 'finished' | reverse %}
  {% for project in projects %}
    {% assign finished_in = project.finished | date: "%Y" %}
    {% if finished_in == this_year %}
      <li>{% include craft-summary-item.html %}</li>
    {% endif %}
  {% endfor %}
</ul>
```

And then the same to the Crafts index.

**`crafts/index.html`**

```liquid
{% assign projects = site.crafts | sort: 'finished' | reverse %}
{% for project in projects %}
  {% assign year_finished = project.finished | date: "%Y" %}
  {% if year_finished != year %}
    {% unless forloop.first %}
      </ul>
    {% endunless %}
    <h2>{{ year_finished }}</h2>
    <ul class="crafts-collection">
    {% assign year = year_finished %}
  {% endif %}
  <li>{% include craft-summary-item.html %}</li>
  {% if forloop.last %}
    </ul>
  {% endif %}
{% endfor %}
```

Add just enough styling to make it work on my machine - then a little
more styling to make it work on my phone.

``` scss
figure {
  text-align: center;
  margin: 1em auto;

  img {
    border: thin solid $grey-color-dark;
    text-align: center;
    margin: auto;
  }
}

.crafts-collection {
  list-style: none;
  display: -webkit-flex;
  display: flex;

  figure {
    width: 160px;
    height: 160px;
  }
}
```

![Final version of the crafts summary](crafts-summary-04.png)

I’m fairly sure something is horribly wrong with my CSS, but if I clean
this bit up I’ll just have to clean everything. This works for now.

### Next?

Judging by my new yarncraft collection? More knitting and crochet. I
need to fill that space! Also, I will gradually hunt down other projects
I completed and add them to the collection. Probably some more layout
and automation work.

Mostly I want to find out what other Jekyll bloggers use collections
for, or want to use collections for. I’d love to hear what you’ve got
going on. Feel free to comment, email, tweet, or whatever!

Other Resources
---------------

-   [Explain Like I’m Five: Jekyll
    Collections](http://ben.balter.com/2015/02/20/jekyll-collections/)
    by Ben Balter
-   [Getting Started with Jekyll
    Collections](http://www.sitepoint.com/getting-started-jekyll-collections/)
    by Taylor Jones