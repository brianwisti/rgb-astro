---
cover_image: cover.png
date: 2020-05-09 03:25:00
layout: layout:PublishedArticle
slug: debugging-my-site-with-a-little-help-from-my-friends
tags:
- IndieWeb
- data
- i fixed it!
- before I pushed it
- yay for tests
title: Debugging My Site With a Little Help From My Friends
uuid: 72e20ceb-c3da-47b3-9736-3c397bc63da5
---

[what the heck]: /note/2020/03/passing-tests-is-now-required-to-push/

> It’s probably redundant to test HTML structure for my pages, but [what the heck][].
>
> -- <cite>Me, a couple months ago</cite>

[every webmention]: /note/2020/04/yay-i-added-mentions-and-replies/

> There’s no rule, but *obviously* [every webmention][] to my site will have
> full author info including photo.
>
> -- <cite>Me, a few weeks ago</cite>

[Datasette dashboard]: /note/2020/05/datasette-sure-is-nifty/

> Look honey I added Webmentions to my [Datasette dashboard][]!
>
> -- <cite>Me, this morning</cite>

[mention]: /note/2020/05/pondering-my-indieweb-guinea-pig/

> Sweet, jmac liked my [mention][]!  Wait why are tests failing? Maybe check
> the dashboard?
>
> -- <cite>Me, an hour ago</cite>

> I fixed it!
>
> -- <cite>Me, a few minutes ago</cite>

[Jason McIntosh]: https://jmac.org

The fix is reasonable defaults for response author info. I got other
fixes in mind, including a default "card" for anonymous response
authors. Also, inferring author info from source site. Thanks for the
help and the ideas, [Jason McIntosh][]!