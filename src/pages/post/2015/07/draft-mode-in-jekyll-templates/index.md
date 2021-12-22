---
aliases:
- /tools/2015/07/20_draft-mode-in-jekyll-templates.html
- /post/2015/draft-mode-in-jekyll-templates/
- /2015/07/20/draft-mode-in-jekyll-templates/
category: tools
date: 2015-07-20 00:00:00
description: 'Use site.show_drafts in your template to keep site development from
  cluttering analytics

  '
layout: layout:PublishedArticle
slug: draft-mode-in-jekyll-templates
tags:
- jekyll
title: Draft Mode in Jekyll Templates
uuid: aa03f645-f865-4dda-967c-6b7dfbb3960e
---

[Jekyll]:  http://jekyllrb.com

Use `site.show_drafts` in templates if the local and live versions of your [Jekyll][] site need to be different.

[a post about Jekyll collections]: /post/2015/07/making-a-jekyll-collection
[Google Analytics]: http://www.google.com/analytics/

Yesterday I published [a post about Jekyll collections][].  Today I checked [Google Analytics][] to see if
anybody looked at my site. 99 visits! Hey, nice. But I also noticed several "localhost" entries: those times I
was double-checking my page locally with `jekyll serve -Dw` counted as visits, because the browser saw
the analytics code and dutifully notified Google's servers. So - less than 99 visits to my site. Oh well.

At some point I may disconnect Analytics altogether and go back to analyzing server logs directly. That
certainly solves the localhost entries. Today I only want to adjust Jekyll's build process so that it
skips analytics code when building drafts.

[configuration documentation]: http://jekyllrb.com/docs/configuration/
Turns out that the [configuration documentation][] lists `show_drafts: null` down there in the default
configuration. I only needed an `unless` block in my template.

``` handlebars
{% unless site.show_drafts %}
  {% include analytics.html %}
{% endunless %}
```

[Disqus]: https://disqus.com/
I added a similar block for comments, since [Disqus][] handles those -  another external service I don't need
in draft mode.

You may need something more elaborate than this for your needs, such as  ad code for a live site and a
placeholder image when building drafts. No matter what the details, `site.show_drafts` provides the key that
you need.