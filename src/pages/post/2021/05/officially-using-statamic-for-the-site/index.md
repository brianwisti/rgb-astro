---
cover_image: cover.png
date: 2021-05-07
description: Hugo's fine but I needed to try something new
format: md
layout: layout:PublishedArticle
slug: officially-using-statamic-for-the-site
tags:
- site
- statamic
- cause-its-there
- my brand
- ooh-a-sparkly
title: Officially Using Statamic For The Site
uuid: 5917577e-0296-4515-83ae-09b8d3d7b166
---

Got the [Webmention][webmention] pingbacks up.  Got the [Plausible][plausible] token in place.  Got
server configuration and deployment working.

Got — server configuration?  Well yeah.  The [Statamic][statamic] CMS runs on [PHP][php].  I
*could* generate and push a static site with it, but I want to try some
[Laravel][laravel] stuff.  Been watching [Laracasts][laracasts] even.

## What’s different?

The visual style, obviously.  But I cycle through those routinely.  This one’s
[PaperCSS][paper-css] with a few tweaks.

I added a new section for my [art][] — specifically for the art you can buy
somewhere.  That’s been on my [task][] list for a long time.  Feels nice to get it
out of the way.  I have a sizable backlog of stuff I wanted to put on my
[store][].  That art section will remind me to get through that backlog a bit more
quickly.

You can search!
Just by title or tag for now, but I’ll add more as I figure out how to fine tune it.
And because you can search, I’m not *as* worried about how pagination is handled.
I’m sure I’ll add something later.

And also because you can search, I haven’t gotten to the page aliases yet.
Lots of broken inbound links, I expect.
If this were some kind of professional site, I would’ve waited until I had those in place.
But it’s not.
So I don’t.

## Anything else?

From your perspective, that’s about it.  It’s pretty much the same site.

From my perspective, so much!  I get an awesome control panel to manage and
edit content.  All my pages are still in flat text files, so I can edit them in
my favorite text editor with no fuss.

Okay that’s not new for the site.  It’s new compared to when I tried this with
WordPress though.

## What’s different from stock Statamic Solo?

The styling is set up with [SASS][sass] instead of the starter’s default of
[Tailwind][tailwind].  Probably shift back once I figure out an approach to
content styling that I prefer to Tailwind Prose.

I don’t entirely trust server-side for a blog.  Nothing to do with Statamic or
PHP mind you.  It’s just too easy to miss important details when you’re running
a solo project.

With that in mind, I added [2FA][2fa] for two factor authentication and
[Gitamic][gitamic] for Git integration.  Both are paid add-ons.  Much as I love
open source software, I love knowing that good developers get a good dinner
even more.  Sponsorship and patronage only go so far — on my monthly budget, at
least.

## What’s next?

There’s still some basic deployment stuff to figure out.  Metadata for sharing,
or what the boring kids call "SEO." Ugh.  I ain’t optimizing *nothin’*, least
of all some search engine’s job.

Anyways.  Then comes automating the non-RSS syndication: posting toots and
tweets when I hit "Publish." Until I get that code in it’s manual, so I’ll
probably skip those for my notes.

After that?  Watch Laracasts.  Learn Laravel.  Learn Statamic.  Have fun.

[webmention]: https://webmention.io
[plausible]: https://plausible.io
[statamic]: https://statamic.com
[php]: https://php.net
[laravel]: https://laravel.com/
[laracasts]: https://laracasts.com/
[paper-css]: https://www.getpapercss.com/
[art]: /art
[task]: /tags/taskwarrior
[store]: https://www.designbyhumans.com/shop/randomgeek/
[sass]: https://sass-lang.com/
[tailwind]: https://tailwindcss.com/
[2fa]: https://statamic.com/addons/jrc9designstudio/2fa
[gitamic]: https://statamic.com/addons/simonhamp/gitamic
