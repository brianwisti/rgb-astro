---
aliases:
- /blogspot/2008/01/02_reinstalling-jruby.html
- /post/2008/reinstalling-jruby/
- /2008/01/02/reinstalling-jruby/
category: blogspot
date: 2008-01-02 00:00:00
layout: layout:PublishedArticle
slug: reinstalling-jruby
tags:
- java
- jruby
- ruby
title: Reinstalling JRuby
uuid: 71d6b5ea-49a4-470e-add4-a84231732c62
---

[JRuby]: http://jruby.org
I'm still getting everything back together after the iMac upgrade fiasco. [JRuby][],
my favorite Ruby implementation, is still missing. I think I'll fix that now.
<!--more-->

 * Grab the binary of 1.03 from the [JRuby][] site.
 * `cd /usr/local`
 * `sudo tar xfvz ~/jruby-bin-1.0.3.tar.gz`
 * `sudo ln -s /usr/local/jruby-1.0.3/ /usr/local/jruby`
 * Add JRuby details to my (somewhat busy) bash profile

``` bash
# ~/.bash_profile
export JRUBY_HOME="/usr/local/jruby"</strong>
# OS X is normally conservative about paths, while I am generous about them.
export LOCALBINS=/usr/local/bin:/opt/local/bin:/opt/local/sbin:/usr/X11R6/bin
export APPBINS=$JRUBY_HOME/bin
export PATH=$APPBINS:$LOCALBINS:$PATH

if [ -r ~/.bashrc ]; then
    . ~/.bashrc
fi
```

Source the file and test my path ...

    $ . ~/.bash_profile
    $ which jruby
    /usr/local/jruby/bin/jruby
    $ which gem
    /usr/local/jruby/bin/gem

Test with the sample code from <a href="https://github.com/jruby/jruby/wiki/GettingStarted">Getting Started</a>
on the JRuby wiki.

``` ruby
require "java"

include_class "java.util.TreeSet"

puts "Hello from JRuby"
set = TreeSet.new()
set.add( "foo" )
set.add( "Bar" )
set.add( "baz" )
set.each { |v| puts "value: #{v}" }
```

Run it.

    $ jruby call_java.rb

Wait a very long time (why does Java startup have to be so slow on our Mac and how
the heck can I make it faster? It's one thing that's significantly worse on our Mac
compared to my PC). *Eventually* see:

    $ jruby call_java.rb
    Hello from JRuby
    value: Bar
    value: baz
    value: foo

Excellent, it worked. It's 2:46 now. I better post this and go to bed.