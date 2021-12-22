---
aliases:
- /blogspot/2007/02/03_late-night-thoughts-about-fm.html
- /post/2007/late-night-thoughts-about-fm/
- /2007/02/03/late-night-thoughts-about-fm/
category: blogspot
date: 2007-02-03 00:00:00
layout: layout:PublishedArticle
slug: late-night-thoughts-about-fm
tags:
- project
- ruby
title: Late Night Thoughts About FM
uuid: 24728f0d-5162-464c-bbc5-54e21ce1b910
---

FM. FXRuby Media. Or f-m, as known on Rubyforge. I probably should have gone for fmm or something like that, but these things are always more obvious when it is too late.
<!--more-->

Oh right. I had thoughts.

Development of version 1 is moving along swimmingly. The basic Track abstraction is in place, along with the code to create Track objects when given MP3 and M4A files. That's all for now, because that's what I have. More formats will be supported as I need them or as users submit the needed TrackFormat code.

And I've almost made it to the heel on my knitted sock. The last couple of days have just been loaded with accomplishments.

[ruby-mp3info]: https://github.com/moumar/ruby-mp3info
[mp4info]: https://github.com/arbarlow/ruby-mp4info

I noticed that [ruby-mp3info][] and [mp4info][] were choking on a couple of the files in my library. There needs to be a solid way to test both of them against a reasonably large dataset so I can find the issue and fix it. Oh, I know! I can use my iTunes Library XML file as a reference ...

<ol><li>Parse the XML file, creating a hash of hashes - track information keyed to filenames.</li><li>Send ruby-mp3info and mp4info chugging along in my Music library, comparing parsed results to those claimed by the XML file.</li></ol>
It'll take a while, but at least I will know if my fixes break something else. That's always handy for patches.


[SQLite 3]: http://sqlite.org
[KirbyBase]: https://github.com/gurugeek/KirbyBase/

Version zero of FM used [SQLite 3][] for storing track details. I might do
that again, but I am also taking a serious look at [KirbyBase][]. I really
like the idea of using Ruby code for my query. Installed system libraries
matter less when your application relies less on non-Ruby code. Then again,
I had a nice little abstraction layer on top of the SQL calls which already
makes my life easy enough for this app. It wasn't as pretty as real code,
though. Maybe I'll try both. Maybe I'll just use KirbyBase. Maybe I'll stick
to the practical side of lazy for now and keep using SQLite. This is my
project, so it's subject to my whims.

FM files won't be available for at least a week. I want to have something that approximates what I have now (plus tests) before I go posting code all over the globe.

I also need to do a little research on mock objects (for testing the database layer) and ... what do they call it when you automate UI testing? Well, whatever they call it - that's something else I want to look into.

It's 3:21. I'm coding, blogging, drinking wine, and watching Black Books. Fun as all that is, I think it's time for sleep.