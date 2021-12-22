---
aliases:
- /note/2020/119/how-many-recent-authors-on-cpan/
date: 2020-04-28 18:40:00
layout: layout:PublishedArticle
slug: how-many-recent-authors-on-cpan
tags:
- perl
- gist
title: How many recent authors on CPAN?
uuid: d05d5c7b-ce4c-40cd-b0c9-56103a2b2ff4
---

Sorry, I couldn’t fit this in a tweet.

[Yanick]: http://techblog.babyl.ca/
[CPAN]: https://cpan.org

[Yanick][]'s concerned about [CPAN][].

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">Sweet meejus. Visiting CPAN these days feels like entering the gloomy, foreboding halls of Moria. :&#39;-(</p>&mdash; Yanick (@yenzie) <a href="https://twitter.com/yenzie/status/1254874808774516738?ref_src=twsrc%5Etfw">April 27, 2020</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

[MetaCPAN]: https://metacpan.org
[Mojolicious]: https://mojolicious.org

So I grabbed the authors of the last 5,000 releases and counted authors, using
[Mojolicious][] and the [MetaCPAN][] API.

    $ export MCP_LATEST='https://fastapi.metacpan.org/v1/release/_search?q=status:latest&fields=author&sort=date:desc&size=5000'
    $ http $MCP_LATEST > _search.json
    $ perl -Mojo -E 'say c(j(f("_search.json")->slurp)->{hits}{hits}->@*)->map( sub { $_->{fields}->{author} } )->uniq->size . " authors made the last 5000 releases"'
    974 authors made the last 5000 releases

[`-Mojo g()`]: https://mojolicious.org/perldoc/ojo#g
[httPie]: https://httpie.org/

Downloaded the file with [httPie][] because I felt bad hammering MetaCPAN with
[`-Mojo g()`][] while sorting out the rest of the :v:one-liner:v:.

I have no idea if these results are good or bad, but I half-expected less than
100 authors.

Getting useful information like spread of release dates is left as an exercise
for the reader.