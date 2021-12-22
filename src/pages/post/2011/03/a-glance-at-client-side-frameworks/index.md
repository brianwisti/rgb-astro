---
aliases:
- /blogspot/2011/03/16_glance-at-client-side-frameworks.html
- /post/2011/glance-at-client-side-frameworks/
- /2011/03/16/a-glance-at-client-side-frameworks/
category: Blogspot
date: 2011-03-16 00:00:00
layout: layout:PublishedArticle
slug: a-glance-at-client-side-frameworks
tags:
- javascript
title: A Glance at Client-Side Frameworks
uuid: 333f0c7d-5c9c-4112-9b17-dc8b3b95aed0
---

[Google CR-48 netbook]: http://www.google.com/chromeos/pilot-program-cr48.html

I was one of those lucky suckers who got a [Google CR-48 netbook][] a few months back.
Although I've failed miserably in making it my primary machine, it has gotten me thinking a lot more about browser applications and JavaScript frameworks.
That's good.
It got me out of my twelve year server-side rut.

<!--more-->

A lot has happened to JavaScript since I started hating it in 1998.
It's a real programming language, with multiple solid implementations.
Smart people have been making it work from the command line, while other smart people have been establishing a solid base to build browser applications on.
I've been looking at a few different frameworks, thinking that I'll find the One True Framework.
No such luck.
There are three biggies that I'm going to end up bouncing back and forth between.

## jQuery

[jQuery]: https://jquery.com

[jQuery][] gives me what I need to add awesome interactive features to a site *right now*.
I would like to compare its virtue of immediate gratification to that of PHP.
There's a lot of hate out there for PHP, so I won't.
Except I just did.
Oh, the inconsistency.

## Google Closure

[Google Closure]: https://code.google.com/closure

[Google Closure][] is this massive collection that seemingly provides everything that core JavaScript is missing:
type annotations, templating, compilation, and probably a lot of other stuff.
Oh, and the basic framework stuff you get in toolkits like jQuery.
It could be amazing.
It could be terrible.
It will take me a while to find out.
One thing's for sure.
Closure rewards the patient more than those of us who like instant gratification.

## Sproutcore

[SproutCore]: https://www.sproutcore.com
[NPR webapp]: https://www.npr.org/webapp
[JSDoc]: http://code.google.com/p/jsdoc-toolkit/

[SproutCore][] is somewhere in between the two.
There's some instant gratification, assuming you're already familiar with basic MVC as seen on the Web.
It's designed for building full-scale client applications, though.
Stuff like the [NPR webapp][].
Closure is as well, but it's not as locked into the single point of entry that SproutCore seems to be.
It could be.
I don't know.
I'm still learning about [JSDoc][] tags.

SproutCore is the most interesting to me right now, probably because it's the newest.
Its main disadvantage to me is that it targets HTML 5.
My job forces me to maintain compatibility with Internet Explorer 6, which is most definitely *not* compatible with HTML 5 features.
So I can learn SproutCore, but should not expect to use it on the clock.

# Conclusion

There you have it.
Three frameworks that charm me in different ways.
I plan to more or less learn each of them.
All because Google sent me a netbook.