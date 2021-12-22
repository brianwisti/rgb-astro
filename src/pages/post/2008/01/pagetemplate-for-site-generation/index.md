---
aliases:
- /blogspot/2008/01/06_pagetemplate-for-site-generation.html
- /post/2008/pagetemplate-for-site-generation/
- /2008/01/06/pagetemplate-for-site-generation/
category: blogspot
date: 2008-01-06 00:00:00
layout: layout:PublishedArticle
slug: pagetemplate-for-site-generation
tags:
- pagetemplate
- ruby
title: PageTemplate for Site Generation
updated: 2015-03-28 00:00:00
uuid: a0b992ad-9140-4c61-af51-8c38479c2c45
---

[Python Blogger client]: /post/2007/12/python-loves-blogger-part-1/
[gdata-ruby]: https://code.google.com/p/gdata-ruby-util/
[PageTemplate]: /tags/pagetemplate/

So I was looking at my [Python Blogger client][] and I tried implementing the same thing in Ruby. [gdata-ruby][] confusion stymied me. I still don't know whether library issues or my own ignorance blocked me.
<!--more-->

[ZenWeb]: http://zenspider.com/ZSS/Products/ZenWeb/index.html
[WebMake]: http://webmake.taint.org
[coolnamehere]: /categories/coolnamehere/

That, of course, set me off on yet another thought. What if I tried to define my posts in a [PageTemplate][] file and used filters to handle the dirty work? Well, that might be a little challenge. But what if I used this approach to generate a whole Web site? Okay, yeah. That may have come out of nowhere for you. The truth is that I love static site generation tools, from [ZenWeb][] to [WebMake][]. These tools appeal to me because [coolnamehere][] is pretty much a static site and I love anything which can give that pile of pages a common format without making heavy server demands. Honestly, loading up PHP just so I can have a templated site seems like overkill.

Let's see if I can build a site like coolnamehere with Ruby and PageTemplate. I plan to borrow heavily from ZenWeb, since there are a lot of things to like about the ZenSpider approach. I especially like
  building a site from a collection of pages and a chain of filters. Hey, PageTemplate has filters thanks to Greg Millam. Why don't I try *using* them?

## Start Small

[Maruku]: https://github.com/bhollis/maruku

I am going to start small, by teaching SiteTemplate about [Maruku][].

It took me a bit of time to get that much done, because I needed to relearn how PageTemplate initializes. *Note to self: don't ever go a full year without using your own library.*

The test is simple: create a template using the Maruku filter. Compare the output of that template
with the text minus PageTemplate directives and fed into Maruku. The test passes if they look alike,
or close enough.

``` ruby
#!/usr/local/bin/ruby

require 'rubygems'
require 'test/unit'
require 'sitetemplate'

class TC_MarukuFilter < Test::Unit::TestCase
  require 'maruku'

  def test_maruku_filter
    content = "This is a paragraph"

    # template_file contains the text "[%filter :maruku%]This is a paragraph[%end%]"
    template_file = "maruku.txt"
    maruku_doc = Maruku.new(content)
    pt = PageTemplate.new()
    pt.load(template_file)
    assert_equal(maruku_doc.to_html + "\n", pt.output,
      "Check if Maruku filter ran successfully")
  end
end
```

Then the code I needed to make that test pass:

``` ruby
#!/usr/local/bin/ruby
# Utility for generating a static site with PageTemplate

require 'rubygems'
require 'maruku'
require 'pagetemplate'

class PageTemplate
  class DefaultPreprocessor
    class << self
      def maruku(text)
        return Maruku.new(text).to_html
      end
    end
  end
end
```

I cut corners by adding the `maruku` filter method to PageTemplate's DefaultPreprocessor. PageTemplate's internals need a little work, since this isn't the prettiest way a person might want to add filters. It works well, but it's not pretty.

That works well enough. Next time I'll try a template filter, which puts the Maruku output into a template file of my choosing. That way we get the standard look for pages.