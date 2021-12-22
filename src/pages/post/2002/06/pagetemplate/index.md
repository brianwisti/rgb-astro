---
aliases:
- /coolnamehere/2002/06/02_pagetemplate.html
- /post/2002/pagetemplate/
- /2002/06/02/pagetemplate/
category: coolnamehere
date: 2002-06-02 00:00:00
layout: layout:PublishedArticle
slug: pagetemplate
tags:
- pagetemplate
title: PageTemplate
updated: 2015-03-22 00:00:00
uuid: b8181016-869f-4dd5-8437-6d5e9641d380
---

## Vital Information and Links

Version
: `2.2.3`

Project Page
: [PageTemplate on
  RubyForge](http://rubyforge.org/projects/pagetemplate)

Instructions
: Start with [installation](/post/2002/07/pagetemplate-getting-it/)

<aside class="admonition warning">
<p class="admonition-title">Warning</p>

Haven't touched PageTemplate in ages. This stuff is only here for the
historical record.

</aside>

## Introduction

PageTemplate is a Ruby package which allows you to utilize text
templates for your Web projects. It is mainly intended for use in a CGI
environment, but has been designed to be helpful in a broad range of
similar applications. It is inspired by, yet almost entirely unlike, the
[HTML::Template](http://html-template.sourceforge.net/) package
available for Perl. It has many features in common with other templating
engines:

- Variable substitution
- “if/else” blocks - inserting chunks of content depending on the
  existence of a flag variable
- “loop/no” blocks - repeatedly inserting a chunk of content, using
  values from a list
- Simple default syntax - *I hope it’s simple*

It also has a few features of its own (otherwise, where’s the fun?).

- Ruby-style access to fields and methods of objects
- Preprocessors to alter formatting of variables
- Support for defining values inside template
- Our Loops Are Crazy Fun:
    - Iteration over multiple loop variables
    - Named loop variables for easy-to-read object access
    - Loop meta-variables to simplify things like formatting alternate
      rows
- Customizable markup syntax to simplify integration with your own
  tools
    - Included `HTGlossary` for HTML::Template style syntax
- Cached templates for faster output

More features are planned, such as support for localization to allow
native-language markup. Development is currently at the "make it work
better" stage, to be followed by adding nifty features.

## What PageTemplate Is Not

- It’s not a programming language. If you want a programming language
  for your Web pages, try [PHP](/tags/php/)
- It’s not a tool for embedding Ruby code into your Web pages.
  [ERB](http://ruby-doc.org/stdlib-2.4.1/libdoc/erb/rdoc/ERB.html)
  already does a fine job of that.
- It is *definitely* not XML. PageTemplate serves a much narrower
  field. If you want to use Ruby with XML, there are [excellent
  resources](http://www.rubyxml.org/) for that.
- PageTemplate is a personal project, which means that it’s not a
  commercial product. As much as I hope that it’s functional and
  stable on your computer, I can’t make any promises. If installing
  PageTemplate levels New Jersey, there’s nothing I can do about it.
  This is my version of the standard “no warranty” warranty.
- Last but not least, PageTemplate is not HTML::Template.
  HTML::Template has been growing and evolving for years, while
  PageTemplate was the result of a week alone with 5 pounds of coffee.
  Things have improved, but PT still suffers from the fact that it’s
  written and supported by two guys in their ever-dwindling spare
  time.

## Motivation

Brian has been a fan of Perl’s HTML::Template package for a long time,
and he missed its robust usefulness whenever using a language that isn’t
Perl. After delving deeper into other languages, he thought it might be
fun to make some of that utility available in [Ruby](/tags/ruby/). It
would give Brian a decent-sized personal project, which would stretch
his skills with project development and unit testing. Plus, if a
templating system was available, maybe he wouldn’t miss Perl so badly.

So those were the primary motivations: personal education and
homesickness.

Once the code started taking shape, though, he decided that he wanted
this to be useful for other people. “Download and use” kind of useful.
Greg Millam found PageTemplate to be *so* useful that he opted to join
in the development process and add loads of new features. PageTemplate
has continued to be used by a small but apparently loyal group of
people, despite Brian and Greg’s periodic hibernation. The continued
contributions of Greg Millam have made PageTemplate a powerful tool for
Web development rather than the mild distraction it started out as.

## Using PageTemplate

First, you’ll want to [download and
install](/post/2002/07/pagetemplate-getting-it/) the latest version of
PageTemplate. Then,
[designers](/post/2002/06/pagetemplate-the-designers-perspective/) will
make templates,
[programmers](/post/2002/06/pagetemplate-the-programmers-perspective/)
will write code, and some of us will do both. Eventually, you will
probably get tired of the default syntax, and want to make your own. If
you’re an especially geeky sort of person, you’ll no doubt want to look
at the source for lasses and methods that are available in the
PageTemplate package.

Most importantly, *enjoy yourself\!* PageTemplate is supposed to be good
geeky fun, not hard work with lots of sweat and turmoil\!

## Users

I would love to hear about what you’ve done with PageTemplate. Until
then, I’ll be forced to look PageTemplate up on Google and see what I
find:

- [A Web-based library consult service for evidence-based
  medicine](http://www.pubmedcentral.nih.gov/articlerender.fcgi?artid=1484475)
  - We’re mentioned a ways down there, but they are using
  PageTemplate. If you have the keen eye required to read names in big
  letters near the top of the page, you’ll notice Greg was part of
  this team.
- [Weft QDA](http://www.pressure.to/qda/) - Text analysis? Sounds
  impressive. I’m guessing PageTemplate gets used for exporting to
  HTML.
- PageTemplate also seems to be available on a lot of Web hosts out
  there via RubyGems. I don’t know if it is *used*, but at least it’s
  available.

## The License

PageTemplate is distributed under The MIT License, which is detailed
below.

### The MIT License

Copyright (c) 2002-2006 Brian Wisti, Greg Millam

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the
“Software”), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.