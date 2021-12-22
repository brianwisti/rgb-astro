---
aliases:
- /programming/2015/03/16_ruby-itunes-ratings-fun.html
- /post/2015/ruby-itunes-ratings-fun/
- /2015/03/16/ruby-itunes-ratings-fun/
category: Programming
date: 2015-03-16 00:00:00
description: Using Ruby to summarize my iTunes music ratings
layout: layout:PublishedArticle
slug: ruby-itunes-ratings-fun
tags:
- ruby
- itunes
- graphing
- music
title: Ruby iTunes Ratings Fun
updated: 2015-07-26 00:00:00
uuid: 5229ba59-6edf-417a-b69e-9c3536164480
---

I use the [plist](https://github.com/bleything/plist) and
[gruff](https://github.com/topfunky/gruff) gems to summarize my iTunes
music ratings.

<aside class="admonition">
<p class="admonition-title">Updates</p>

2015-07-26
: There was a missing `format` in the version of `graph-ratings.rb` that I pasted here. I am properly shamed.

</aside>

Introduction
------------

Earlier this year I did a fresh operating system install on my laptop.
Part of that install involved moving all my music from an older machine.
I moved the music, but not the iTunes details. My tastes changed over
the years. Why not start with a fresh listen and fresh ratings for all?

A few months passed. How much progress have I made?

First off let me roll 1d100 and check the Random Language Chart. I
rolled a 73, and that means I write this in Ruby.

I decided to look at the XML file that gets exported by iTunes whenever
a library detail changes. [Property List
XML](https://developer.apple.com/legacy/library/documentation/Darwin/Reference/ManPages/man5/plist.5.html)
frustrates quickly if you attack it with naive XML parsing. Fortunately,
Ben Bleything wrote a [plist](https://github.com/bleything/plist) gem
that simplifies the task in Ruby.

Since I like pretty pictures, I may as well use Geoffrey Grosenbach’s
[gruff](https://github.com/topfunky/gruff) to make a pretty pie chart.

    $ ruby --version
    ruby 2.2.0p0 (2014-12-25 revision 49005) [x86_64-darwin14]
    $ gem install plist
    $ gem install gruff

Here It Is
----------

No big code explanation this time around. My last few attempts at that
have gone stale in my drafts folder. Plus, I’m worn out. I *tried* the
naive XML parsing thing, and it frustrated me quickly. Thank goodness
for [plist](https://github.com/bleything/plist).

**`graph-ratings.rb`**

```ruby
require 'plist'
require 'gruff'

SOURCE = "#{ENV['HOME']}/Music/iTunes/iTunes Music Library.xml"

plist = Plist.parse_xml SOURCE
tracks = plist['Tracks']

songs = tracks.values.reject do |track|
  track['Kind'] !~ /audio file$/ || track['Genre'] == 'Podcast'
end

ratings = {}

# Group the songs by rating.
songs.each do |song|
  rating = song['Rating'] || 0
  total_time = song['Total Time'] || 0

  ratings[rating] ||= { songs: 0, time: 0 }
  ratings[rating][:songs] += 1
  ratings[rating][:time] += total_time
end

# Print it.
puts 'Rating Songs Percent Duration'

ratings.keys.sort.each do |rating|
  song_count = ratings[rating][:songs]
  total_seconds = ratings[rating][:time] / 1000.0
  seconds = total_seconds % 60
  minutes = (total_seconds / 60) % 60
  hours = (total_seconds / (60 * 60)) % 24
  days = total_seconds / (60 * 60 * 24)

  percentage = song_count.to_f() / songs.count.to_f() * 100.0
  duration = format '%02d:%02d:%02d:%02d', days, hours, minutes, seconds
  description = format '%6d %5d %6.1f%% %s', rating, song_count, percentage, duration
  puts description
end

# Graph it.
data = ratings.map { |rating, info| [ rating, [ info[:songs]]] }

graph = Gruff::Pie.new
graph.title = "Songs Grouped By Rating"

ratings.keys.sort.each { |rating| graph.data rating, ratings[rating][:songs] }

graph.write "song-pie.png"
```

Running it shows me that I have more than a month of music to rate, and
only if I can rate music in my sleep.

    Rating Songs Percent Duration
         0 13907   83.0% 38:05:56:14
        20    60    0.4% 00:03:41:48
        40   179    1.1% 00:12:28:46
        60  1351    8.1% 03:16:21:32
        80   984    5.9% 02:14:57:47
       100   273    1.6% 00:17:44:35

It seems I still like most of the music I own at least a little bit.
Many former favorites have drifted to the 60 rating (3 stars), though.
Time does change tastes a little bit.

The graph. Let’s look at that pretty picture.

![Ratings pie chart](song-pie.png)

Yes. I have much music listening ahead of me.