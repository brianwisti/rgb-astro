---
aliases:
- /programming/2013/11/25_my-own-ruby-fibers-babystep.html
- /post/2013/my-own-ruby-fibers-babystep/
- /2013/11/25/my-own-ruby-fibers-babystep/
category: programming
date: 2013-11-25 00:00:00
layout: layout:PublishedArticle
slug: my-own-ruby-fibers-babystep
tags:
- ruby
- files
- site
title: My Own Ruby Fibers Babystep
uuid: d89b6b72-e030-4aac-81a8-742f2df1aedf
---

[rereading]: /post/2013/11/rereading-the-pickaxe/

My adventures [rereading][] the Pickaxe Book have reached the chapter on Fibers.
Interesting stuff.
Thought I would extrapolate from their initial example.
My old static pages started from a MANIFEST file that looked something like this:

    index.html
    /babblings/index.html
    /babblings/2013-05-30-javascript.html
    /babblings/2013-04-05-perl-and-opensuse.html
    /babblings/2013-03-big-updates.html
    /babblings/seattle.html
    /babblings/stalkingswfans.html
    /babblings/bra.html
    /brian/index.html

And so on.
The path components create a topic heirarchy.
There are only 89 files.
This is not a lot to track, but it is enough that I can still be hazy about some high level details.
For example, I have no idea how many pages are in each section.

```ruby
sections = Fiber.new do
  File.foreach "MANIFEST" do |line|
    line.match %r{^/(?<path>\w+)/} do |section|
      Fiber.yield section[:path]
    end
  end

  nil
end

counts = Hash.new 0

while section = sections.resume
  counts[section] += 1
end

counts.keys.sort.each { |section| puts "#{section}: #{counts[section]}" }
```

Yes, this is just the example from the Pickaxe book with `line.scan` changed to
`line.match` with a slightly altered regular expression.

    $ ruby nom-manifest.rb
    babblings: 7
    brian: 2
    geekery: 78

This isn’t that helpful though.
I already knew that the majority of my pages were in `/geekery/`.
Let’s adjust the regular expression so that the first two pieces of the entry count as a section.

```ruby
sections = Fiber.new do
  File.foreach "MANIFEST" do |line|
    line.match %r{
      ^/(?<path>\w+ # main section: /geekery
      (?:/\w+)?)    # subsection:   /ruby
      /             # stop at path separator
    }x do |section|
        Fiber.yield section[:path]
    end
  end
  nil
end
```

Now I’m looking for possible subsections and lumping them with the top level section.
Does this change get me more useful information (for varying definitions of useful)?

    $ ruby nom-manifest.rb
    babblings: 7
    brian: 2
    geekery: 2
    geekery/editors: 3
    geekery/js: 1
    geekery/lisp: 1
    geekery/osx: 1
    geekery/parrot: 17
    geekery/perl: 13
    geekery/php: 2
    geekery/python: 9
    geekery/rakudo: 3
    geekery/rebol: 10
    geekery/ruby: 10
    geekery/tools: 2
    geekery/unix: 2
    geekery/xml: 2

Yeah.
It does.
I can now see that the most of my static pages are about Parrot or Perl.

I recognize that all I’m doing in this example is shuffling complexity around.
There’s nothing in the task that screams "OMG YOU NEED FIBERS TO DO THIS!"
Still - I need to figure this stuff out somehow.

Anyways, back to work.