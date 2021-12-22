---
aliases:
- /tools/2015/09/08_restructuredtext-in-jekyll.html
- /post/2015/restructuredtext-in-jekyll/
- /2015/09/08/restructuredtext-in-jekyll/
category: tools
date: 2015-09-08 00:00:00
description: I can write Jekyll posts with reStructuredText now.
layout: layout:PublishedArticle
slug: restructuredtext-in-jekyll
tags:
- jekyll
- rst
- site
title: reStructuredText in Jekyll
uuid: 67f50090-056d-4d2b-97d4-79856e45252b
---

[Jekyll]: http://jekyllrb.com/
[reStructuredText]: http://docutils.sourceforge.net/rst.html
I can write [Jekyll][] posts with [reStructuredText][] now.
<!--more-->

I spent the last few days fiddling with [Pelican][] and [Nikola][] to see how
much work it would take to convert my site. So far? Lots of work. I 
customized the build for this silly site quite a bit.

Meanwhile I decided that I *must* have [reStructuredText][] available for my posts.
I grabbed the [jekyll-rst][] Jekyll plugin and followed its directions.

[Pelican]: http://blog.getpelican.com
[Nikola]: http://getnikola.com
[jekyll-rst]: https://github.com/xdissent/jekyll-rst

    $ mkvirtualenv jekyll-rst
    $ pip install docutils pygments
    $ gem install RbST
    $ git submodule add https://github.com/xdissent/jekyll-rst.git _plugins/jekyll-rst

Let me just build real quick to make sure this works at all.

Well, no.

    $ bundle exec jekyll build -D
    # ...
    TypeError: Unicode-objects must be encoded before hashing
    Exiting due to error.  Use "--traceback" to diagnose.
    Please report errors to <docutils-users@lists.sf.net>.
    Include "--traceback" output, Docutils version (0.12 [release]),
    Python version (3.4.3), your OS type & version, and the
    command line used.

Oh I know that smell. You get that with code that isn't completely ready for
Python 3. Here's the smallest change to make that error go away.

``` python
# _plugins/jekyll-rst/directives.py line 54-55
content_text = u'\n'.join(self.content).encode('utf-8')
cache_file_name = u'%s-%s.html' % (lexer_name, hashlib.md5(content_text).hexdigest())
```

*Now* it builds.

Then I ripped out all the special options because that was easier than
adjusting my stylesheets to take them into account.

So. It works. Yay! I can write Jekyll posts with reStructuredText!

That should keep me a little happier while I continue porting the site to
another generator.