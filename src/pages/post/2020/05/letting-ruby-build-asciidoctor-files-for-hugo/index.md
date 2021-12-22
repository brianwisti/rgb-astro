---
caption: actually really proud of myself but this post needs all the disclaimers
category: programming
cover_image: cover.jpg
date: 2020-05-18 21:15:00
description: Stuff like this is why i don't advertise my site repo
draft: false
format: md
layout: layout:PublishedArticle
slug: letting-ruby-build-asciidoctor-files-for-hugo
tags:
- ruby
- hugo
- asciidoctor
- site
- don't try this at home
- fine go ahead
- but I warned you
title: Letting Ruby build Asciidoctor files for Hugo
uuid: be41fa2a-8ebb-4739-bda0-108ae33b8a31
---

:::tldr

Normal people: don't do any of this.  The whole post is me compensating for
making Hugo do things it's not good at.

Stick with [Markdown][markdown] if you use [Hugo][hugo].  Use [shortcodes][] or
[render hooks][render-hooks] if you want to make things interesting.
Experiment with [reStructuredText][rst] or [Asciidoctor][adoc] — but anything
past a few pages slows builds dramatically.  Move *away* from Hugo if you
prefer those formats.  Try [Nikola][nikola] for `rst` blogs.  [Gatsby][gatsby]
has a [plugin][] to directly transform `adoc` content.  You have options!

:::

## Asciidoctor?

Asciidoctor is yet another lightweight formatting language, with official
implementations in Ruby, JavaScript, and Java.  Processing tools transform it
into HTML, PDF, and other formats.  Like Markdown, I find it easy to read and
write the format.  Like reStructuredText and [Org][org], it provides structures
suited for technical and long form writing.  Oh, and clearly labeled hooks for
extending if the built-in structures don’t quite meet your needs.

## What’s this got to do with Hugo?

Hugo shines with Markdown, but you can use other [content
formats][content-formats] as well.  It supports Org files directly through
[go-org][].  reStructuredText is supported if you have `rst2html.py` installed.
Asciidoc and Asciidoctor are supported if you have their processors installed.
And like [Jekyll][jekyll], Hugo supports HTML as an HTML authoring language if
you tack some front matter onto it.

I enjoy the flexibility.  And that bit about supporting HTML as an authoring
language is about to come in real handy.

:::tip

go-org is nice, but [`ox-hugo`][ox-hugo] excels if you want Hugo support
tightly integrated with Org mode.

:::

## So what’s the problem?

What’s up with this?

    $ hugo

                    |  EN
    -------------------+-------
    Pages            | 1353
    Paginator pages  |  128
    Non-page files   |  442
    Static files     |   31
    Processed images | 1195
    Aliases          | 1261
    Sitemaps         |    1
    Cleaned          |    0

    Total in 15929 ms

Sixteen seconds might look impressive compared to Jekyll.  It’s more alarming
if you know Hugo’s reputation for speed.

I think my Asciidoctor files might be causing this slowdown.  I do have quite a
few of them.

    $ make formats
    hugo list all | raku -e 'bag(lines[1..*].map({ .split(",")[0].IO.extension })).say'
    Bag(adoc(206), html, md(424))

How to confirm this?  Well, I could run `hugo` in debug mode and scan the
output.

    $ hugo --debug > debug.log

    Building sites … INFO 2020/05/14 21:44:50 syncing static files to /home/random/Sites/rgb-hugo/randomgeekery.org/
    ⋮
    INFO 2020/05/14 21:44:50 Rendering contact.adoc with /home/random/Sites/rgb-hugo/scripts/asciidoctor ...
    ⋮
    INFO 2020/05/14 21:45:07 Rendering post/2020/05/querying-hugo-content-with-python/index.adoc with /home/random/Sites/rgb-hugo/scripts/asciidoctor ...
    ⋮
    Total in 17235 ms

Interesting.  I only updated a single `.adoc` file — this one — but Hugo
rebuilds *all* of them.  It also spends about 17 seconds doing so.  17,000 of
the 17,235 milliseconds spent in this build go to rebuilding mostly unchanged
Asciidoctor files.

Okay.

## Fine I’ll do it myself

I could always build the `adoc` files myself instead of making Hugo do it.

### Hang on — is that even worth it?

How long does it take for a single process to build HTML from all the `adoc`
files in my site?  Not much point in this idea if Asciidoctor takes 17 seconds
on its own.

All right.  Let’s try this with roughly the same arguments Hugo does with
[external helpers][external-helpers].

**`build-adoc`**

``` ruby
require "fileutils"

require "asciidoctor"

SRC_DIR = "content"
BUILD_DIR = "adoc-out"

if File.exist? BUILD_DIR
  FileUtils.rm_r BUILD_DIR
end

Dir["#{SRC_DIR}/**/*.adoc"].each do |filename|
  # Mirror the nested folder structure where I found the `adoc` file
  dirname = File.dirname(filename)
  branch = dirname.sub %r[^#{SRC_DIR}/?], ""
  target_dir = "#{BUILD_DIR}/#{branch}"
  target_base = File.basename(filename).sub %r{adoc$}, "html"
  target_file = "#{target_dir}/#{target_base}"

  Asciidoctor.convert_file filename, to_file: target_file,
    header_footer: false, safe: true, mkdirs: true
end
```

This fills a temporary folder with Asciidoctor’s generated HTML, keeping it out
of Hugo’s way.

    $ time ruby scripts/build-adoc
    0.61user 0.03system 0:00.65elapsed 98%CPU (0avgtext+0avgdata 20584maxresident)k
    0inputs+3680outputs (0major+7188minor)pagefaults 0swaps

0.65 seconds to build all the `.adoc` files.

So yes.  Building them fresh myself is quicker than 17 seconds.  That’s about
what I figured, since Hugo apparently starts a fresh Ruby process for each
`adoc` file.  I used a single process for all of them.

This experiment is worth pursuing further.

## Give it a shot

It will be fiddly, though.  I’m going to end up adding a build step, and
complicating Hugo’s normally straightforward site generation process.

### Keep the front matter

Asciidoctor has its own [document header][document-header] rules, but I don’t
have to think too much about that.  To better support [static site
generators][ssg], Asciidoctor can be told what to do with YAML front matter.  I
want front matter glued back to output before saving to Hugo’s `content`
folder.

You can [extend][] Asciidoctor at multiple points in the conversion pipeline,
with code blocks or full classes.  I’ll register a block extension for the
postprocessor stage: after the document has been converted, but before it gets
saved.

```ruby
# ...
require "asciidoctor"
require "asciidoctor/extensions"

Asciidoctor::Extensions.register do
  # reinsert "front-matter" attribute
  postprocessor do
    # Create a YAML front matter + HTML content document that Hugo can work with
    process do |document, output|
      front_matter = document.attr "front-matter"
      output = "---\n#{front_matter}\n---\n\n#{output}"
    end
  end
end

# ...

Dir["#{SRC_DIR}/**/*.adoc"].each do |filename|
  # ...
  Asciidoctor.convert_file filename, to_file: target,
    header_footer: false, safe: true, mkdirs: true,
    # extract front matter into a `front-matter` document attribute.
    attributes: {
      "skip-front-matter" => true,
    }
end
```

### What about page resources?

For adoc files, I’ll treat the Asciidoctor content folder as the source of
truth.  Cover images and other [page bundle][page-bundle] files go with the
`adoc`.  `build-adoc` will copy them over when converting files.

```ruby
# ...
Dir["#{SRC_DIR}/**/*.adoc"].each do |filename|
  # ...
  Dir["#{dirname}/*"].each do |supplemental|
    # We're just looking for resource bundle files
    next if File.directory? supplemental

    # We already grabbed the adoc file(s)
    next if supplemental =~ %r{adoc$}

    FileUtils.cp supplemental, target_dir
  end
end
```

### Only rebuild new stuff

I might save a little more time — and disk writes — by limiting my build to
updated adoc and supplemental files.

Course, it helps to stop deleting `BUILD_DIR`.

```ruby
# ...
Dir["#{dirname}/*"].each do |supplemental|
  # We're just looking for resource bundle files
  next if File.directory? supplemental

  # We already grabbed the adoc file(s)
  next if supplemental =~ %r{adoc$}

  supplemental_base = File.basename supplemental
  target_file = "#{target_dir}/#{supplemental_base}"

  copy_needed = if File.exist? target_file
                  File.mtime(filename) > File.mtime(target_file)
                else
                  true
                end

  if copy_needed
    puts "Converting #{filename}"

    FileUtils.copy supplemental, target_file
  end
```

If processing a single file was more expensive, I’d use something more careful
than a timestamp check.

### Make it official

Let’s skip the gory details, but I eventually moved all the `adoc` posts,
notes, and drafts to their own folder.  Now `build-adoc` officially generates
HTML content with YAML front matter for Hugo.

```ruby
SRC_DIR = "adoc"
BUILD_DIR = "content"
```

Since Asciidoctor finishes so promptly, I’ll run it every time I build the site.

```
.PHONY: adoc build
adoc:
    ruby scripts/build-adoc

build: adoc ## Build live version of site
    INCLUDE_ANALYTICS=1 hugo
    cp etc/robots.txt randomgeekery.org/
    cp etc/htaccess randomgeekery.org
```

### What do we have now?

I finished my basic Asciidoctor + Hugo flow. How long does it take to build the
site now? Let’s find out.

Every `adoc` file gets processed in the first run.

    $ time make build
    # every adoc file is converted
    ...
    done
    INCLUDE_ANALYTICS=1 hugo

                    |  EN
    -------------------+-------
    Pages            | 1353
    Paginator pages  |  128
    Non-page files   |  431
    Static files     |   31
    Processed images | 1188
    Aliases          | 1261
    Sitemaps         |    1
    Cleaned          |    0

    Total in 1416 ms
    cp etc/robots.txt randomgeekery.org/
    cp etc/htaccess randomgeekery.org
    3.80user 0.78system 0:02.87elapsed 159%CPU (0avgtext+0avgdata 198236maxresident)k
    24inputs+505056outputs (0major+19157minor)pagefaults 0swaps

Less than three seconds. I like that time more than 15-18 seconds.

I went to a bit of trouble to only process updated `adoc` files.
Does it help?

    $ time make build
    ruby scripts/build-adoc
    Converting adoc/draft/letting-ruby-build-asciidoctor-files-for-hugo/index.adoc
    done
    INCLUDE_ANALYTICS=1 hugo

                    |  EN
    -------------------+-------
    Pages            | 1354
    Paginator pages  |  128
    Non-page files   |  432
    Static files     |   31
    Processed images | 1189
    Aliases          | 1271
    Sitemaps         |    1
    Cleaned          |    0

    Total in 1458 ms
    cp etc/robots.txt randomgeekery.org/
    cp etc/htaccess randomgeekery.org
    3.11user 0.72system 0:01.90elapsed 200%CPU (0avgtext+0avgdata 212324maxresident)k
    64inputs+500976outputs (0major+61675minor)pagefaults 0swaps

Less than two seconds.  Then again, load from other system processes can add a
second — or more, if I opened a browser tab to some JavaScript-intensive URL.

But it appears to help somewhat.  And again, I get happy when there are fewer
disk writes.

## Highlighting code samples

So at first, Asciidoctor wasn’t highlighting code samples. I had
`:source-highlighter: rouge` in my document header, but it was being ignored.
Rather than add preprocessor logic to ensure that the document header gets
processed, I specified the same attributes for *every* file converted:

``` ruby
# ...
Asciidoctor.convert_file filename, to_file: target_file,
  header_footer: false, safe: true, mkdirs: true,
  attributes: {
    "icons" => "font",
    "source-highlighter" => "rouge",
    "skip-front-matter" => true,
  }
```

All good now, right?

    Rebuild failed:
    "/home/random/Sites/rgb-hugo/content/post/2015/07/making-a-jekyll-collection/index.html:223:53": got closing shortcode, but none is open

Uh oh.

That’s not good.

When Hugo sees `{{ … }}` in my new HTML content files, it thinks that’s a
shortcode!  That’s great if I *want* to invoke a shortcode.  Not so great in a
[post with code samples][post-with-code] for working with templates.  Those
aren’t supposed to get processed.

No problem.  [Rouge][rouge] handles syntax highlighting for my `adoc` files.  I
need to take tokens that have already been transformed and make sure paired
double curly braces are replaced with appropriate [HTML
entities][html-entities].  All I need is a slight adjustment to
`Rouge::Formatters::HTML#safe_span`.

I’d prefer to subclass `Rouge::Formatter::HTML`, but Asciidoctor chooses and
creates formatters right in the middle of a [highlight][] method.  I would also
need to create a new Asciidoctor adapter for syntax highlighting and update all
my `adoc` content to use that adapter.  Great idea for later, but I don’t have
that kind of time today.

I’ll [monkey patch][monkey-patch] `Rouge::Formatters::HTML` directly,
redefining `safe_span` to perform the needed transformation.

```ruby
# ...
require "asciidoctor/extensions"
require "rouge"

# Make Rouge output safe for Hugo
class Rouge::Formatters::HTML
  def safe_span(tok, safe_val)
    safe_val = safe_val.gsub(/\{\{/, "&#123;&#123;").gsub(/\}\}/, "&#125;&#125;")

    if tok == Rouge::Token::Tokens::Text
      safe_val
    else
      shortname = tok.shortname \
        or raise "unknown token: #{tok.inspect} for #{safe_val.inspect}"

      "<span class=\"#{shortname}\">#{safe_val}</span>"
    end
  end
end
```

:::admonition{title="What about the shortcodes I want to keep?"}

This is just general advice to make Asciidoctor and Hugo play nice with each other.
You don’t need to rebuild your entire site flow to use this information.

Say I’ve got a shortcode for displaying images as figures.

```
{{</* show-figure image="cover.png" description="Taskwarrior edit view" */>}}
```

Asciidoctor transforms unsafe characters into HTML entities.

```html
{{​&lt; show-figure image="cover.png" description="Taskwarrior edit view" &gt;}}
```

And it looks kind of embarrassing.

![screenshot showing image shortcode instead of an image](escaped-shortcode.png "my shortcode got escaped")

The solution? Wrap that shortcode in a [passthrough macro][passthrough-macro].

``` adoc
pass:[{{</* show-figure image="cover.png" description="Taskwarrior edit view" */>}}]
```

![correct shortcode](correct-shortcode.png "using a passthrough macro")

Much better.

:::

### *Now* what do we have?

I’m not sure. Let’s find out with a typical `build all`.

    $ time make all
    ruby scripts/build-adoc
    Converting adoc/draft/letting-ruby-build-asciidoctor-files-for-hugo/index.adoc
    done
    INCLUDE_ANALYTICS=1 hugo

                    |  EN
    -------------------+-------
    Pages            | 1354
    Paginator pages  |  128
    Non-page files   |  432
    Static files     |   31
    Processed images | 1189
    Aliases          | 1271
    Sitemaps         |    1
    Cleaned          |    0

    Total in 1447 ms
    cp etc/robots.txt randomgeekery.org/
    cp etc/htaccess randomgeekery.org
    perl scripts/generate-archives
    prove -r
    ./t/site/test_archive.t .... ok
    ./t/site/test_links.t ......
    # [mailto:brianwisti@pobox.com] is an email link, friend
    ./t/site/test_links.t ...... ok
    ./t/test_db.t .............. ok
    ./t/test_db_persistence.t .. ok
    ./t/test_pod.t ............. ok
    All tests successful.
    Files=5, Tests=10,  7 wallclock secs ( 0.26 usr  0.05 sys +  6.65 cusr  0.29 csys =  7.25 CPU)
    Result: PASS
    make all  10.44s user 1.15s system 114% cpu 10.108 total

Yeah there’s a lot of stuff there I still need to write about.  Long story
short: by directly using Ruby to convert Asciidoctor files into HTML for
Asciidoctor, build and test *combined* take noticeably less time than build
alone when Hugo had to manage the whole thing.  And it’s not that different
from how `ox-hugo` manages Org content.  A similar approach would probably work
for `rst` files.

I like it for now. Keeps me from getting bored.

:::note

But — and this is a big but — I couldn’t recommend this approach for normal
people with things to do. Site generation now has more moving parts, which I
must test and maintain if I want to share the least little note_.

:::

## What now?

Yay, everything works!

What’s next?  I’m not sure.  Hugo is an ever-smaller piece of my site-building
workflow.  That’s *somewhat* intentional.  Still [grumbly][] about having to
fiddle with all my Markdown files last year.  But still.

- Probably explore some AsciiDoctor extensions. If most of the work happens when I write a file, I won’t care much if that file takes a second to turn into HTML. And there are so many to choose from, from [Asciidoctor Diagram][adoc-diagram] to the [Extensions Lab][extensions-lab] and beyond.
- Maybe turn my shortcodes into macros? Write some of my *own* extension classes?
- Keep exploring site generators. I love to putter. A framework that encourages puttering might suit me better than Hugo.  [Eleventy][eleventy], for example.

[markdown]: https://commonmark.org
[hugo]: https://gohugo.io
[shortcodes]: https://gohugo.io/content-management/shortcodes/
[render-hooks]: https://gohugo.io/getting-started/configuration-markup#markdown-render-hooks
[rst]: /tags/rst
[adoc]: https://asciidoctor.org/
[nikola]: https://getnikola.com/
[gatsby]: https://www.gatsbyjs.org/
[plugin]: https://www.gatsbyjs.org/packages/gatsby-transformer-asciidoc/?=asciidoctor
[content-formats]: https://gohugo.io/content-management/formats/
[go-org]: https://github.com/niklasfasching/go-org
[jekyll]: https://jekyllrb.com/
[ox-hugo]: https://ox-hugo.scripter.co/
[external-helpers]: https://gohugo.io/content-management/formats/#external-helpers
[document-header]: https://asciidoctor.org/docs/asciidoc-syntax-quick-reference/#document-header
[ssg]: https://asciidoctor.org/docs/user-manual/#static-website-generators
[extend]: https://asciidoctor.org/docs/user-manual/#extensions
[page-bundle]: https://gohugo.io/content-management/page-bundles/
[post-with-code]: /post/2015/07/making-a-jekyll-collection/
[rouge]: http://rouge.jneen.net/
[html-entities]: https://dev.w3.org/html5/html-author/charref
[highlight]: https://github.com/asciidoctor/asciidoctor/blob/master/lib/asciidoctor/syntax_highlighter/rouge.rb#L15
[monkey-patch]: https://en.wikipedia.org/wiki/Monkey_patch
[passthrough-macro]: https://asciidoctor.org/docs/user-manual/#pass-macros
[grumbly]: /note/2019/12/removing-mmark-has-me-grumbly/
[org]: /tags/org-mode
[adoc-diagram]: https://asciidoctor.org/docs/asciidoctor-diagram
[extensions-lab]: https://github.com/asciidoctor/asciidoctor-extensions-lab
[eleventy]: https://www.11ty.dev
