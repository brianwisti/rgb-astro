---
aliases:
- /coolnamehere/2002/07/11_getting-it.html
- /post/2002/getting-it/
- /2002/07/11/pagetemplate-getting-it/
category: coolnamehere
date: 2002-07-11 00:00:00
layout: layout:PublishedArticle
slug: pagetemplate-getting-it
tags:
- pagetemplate
title: PageTemplate - Getting It
updated: 2009-07-11 00:00:00
uuid: 4aa396ca-4a13-4e4d-80a0-5ec078811631
---

We have tried to make installing PageTemplate as easy as possible. There
are three basic ways to install PageTemplate:

- With RubyGems
- With Rake
- Manually

## With RubyGems

This is by far the easiest approach.

  $ gem install pagetemplate

See? Okay, you might need to use `sudo` if you are on a UNIX-y machine,
but that’s still not too hard.

You can download the gem from the [PageTemplate project
page](http://rubyforge.org/projects/pagetemplate) and install with your
local copy it if that’s your preference:

  gem install -l PageTemplate-x.y.z.gem

## With Rake

Download the archived file from the [PageTemplate project
page](http://rubyforge.org/projects/pagetemplate). Extract the file into
a convenient location and enter the top-level directory.

  $ rake
  $ rake test
  $ sudo rake install

## Manually

Download the archived file from the [PageTemplate project
page](http://rubyforge.org/projects/pagetemplate). Extract the file into
a convenient location and enter the top-level directory.

  $ sudo ruby setup.rb

You can also install files into your favorite directory by supplying
`setup.rb` some options. Try `ruby setup.rb --help`. Since we don’t
really know how `setup.rb` works, we’ve included the English-language
version of the setup usage file in the archive. Enjoy.