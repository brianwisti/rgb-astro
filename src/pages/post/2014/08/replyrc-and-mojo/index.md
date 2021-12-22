---
aliases:
- /tools/2014/08/19_replyrc.html
- /post/2014/replyrc/
- /2014/08/18/.replyrc-and-reply-mojo/
- /2014/08/19/replyrc-and-mojo/
category: tools
cover_image: cover.png
date: 2014-08-19 00:00:00
description: Customizing Perl Reply and using -Mojo
layout: layout:PublishedArticle
series:
- The Reply Perl REPL
slug: replyrc-and-mojo
tags:
- perl
- reply
- mojolicious
title: replyrc And Mojo
uuid: c83ec892-40ca-402e-97d1-11150500587e
---

[started playing]: /post/2014/08/repl-in-perl-with-reply
[Reply]: https://metacpan.org/pod/Reply
[GNU ReadLine]: http://cnswww.cns.cwru.edu/php/chet/readline/rltop.html
[ReadLine plugin]: https://metacpan.org/pod/Reply::Plugin::ReadLine
[Term::ReadLine::Gnu]: https://metacpan.org/pod/Term::ReadLine::Gnu

It has been a few days since I [started playing][] with [Reply][], and
I still enjoy it. Command history features from the
[ReadLine plugin][] became available once I installed [GNU ReadLine][]
and [Term::ReadLine::Gnu][].
<!--more-->

[subroutine signature]: http://perldoc.perl.org/perldelta.html#Experimental-Subroutine-signatures
[postderef]: http://perldoc.perl.org/perldelta.html#Experimental-Postfix-Dereferencing

There are still customizations that I would like to make. For
example, I write most of my personal code using Perl 5.20's experimental
[subroutine signature][] and [postderef][] features.

## Use Shiny Perl 5.20 Features Automatically

A default `$HOME/.replyrc` is created the first time you run
Reply - unless you already have one, of course. It includes a
selection of plugins that will be loaded and a collection of
`script_line` entries that are evaluated automatically for any new
Reply session. I fiddled with mine so that I had a Perl with
syntactical sugar in place.

``` ini
script_line1 = use 5.20.0
script_line2 = use warnings
script_line3 = use feature qw(signatures postderef)
script_line4 = no warnings 'experimental'
```

Each line gets its own numbered `script_line` entry because of the INI
format and the way that input is parsed by Reply.

With this base level of behavior defined, I can run `reply` and
rewrite my `greet` subroutine.


    0> sub greet ($name) { "Hello $name!" }
    1> my $me = "Brian"
    $res[0] = 'Brian'
    2> greet $me
    $res[1] = 'Hello Brian!'

That's better.

## Enabling The Editor

[Proc::InvokeEditor]: https://metacpan.org/pod/Proc::InvokeEditor
[Editor plugin]: https://metacpan.org/pod/Reply::Plugin::Editor

You need [Proc::InvokeEditor][] in order to activate the
[Editor plugin][]. I suppose that makes sense. Proc::InvokeEditor is a
module that makes it easy to launch your default text editor on behalf
of the application, sending the editor buffer back to your application
as user input.

    $ cpanm Proc::InvokeEditor

Add the [Editor plugin][] entry to your `.replyrc`.

``` ini
[Editor]
```

And just like that, here is a new `#e` command.

    0> #e

[EmacsClient]: /post/2014/06/start-using-emacsclient

It can probably work with [EmacsClient][], but I have been lazy lately
and fallen back to Vim as my `$EDITOR` default.

## Specifying a Module at Start

[Mojolicious]: http://mojolicio.us/
[ojo]: http://mojolicio.us/perldoc/ojo

I have been exploring [Mojolicious][], which is a surprisinglly
full-featured framework considering its small size. The [ojo][]
library is a Mojolicious command line tool focused on making your
one-liners even more useful. Since [Reply][] is sort of an
extended one-liner environment - okay, you can call it a "shell" -
ojo and Reply can go together perfectly.

There is no need to add ojo to my `.replyrc`, because I will not be
needing its functionality every single time I load Reply. Instead I
will just tell Reply to load the library when starting those
particular sessions.

[earlier post]: /post/2014/08/repl-in-perl-with-reply

Let's keep with the Questhub.io example from the [earlier post][].
I start `reply` with the `-M` flag to load a specific module on startup.

    $ reply -Mojo
    0> sort map { $_->{name} } j( g( 'https://questhub.io/api/realm' )->body )->@*
    $res[0] = [
    'Big Data',
    'Chaos',
    'Code',
    'DC Metro Region',
    'Fitness',
    'Haskell',
    'Japanese',
    'Lisp',
    'MOOCs',
    'Meta',
    'Node.js',
    'Perl',
    'Portland',
    'Python (Ru)',
    'Read',
    'Testing',
    'Yoga + Meditation'
    ]

I know. This is confusing if you are unfamiliar with
[ojo][] and the experimental Perl 5.20 [postderef][] feature. We can
look at it in smaller pieces.

``` perl
# Using ojo::g
g( 'https://questhub.io/api/realm' )->body

# is roughly the same as this
$ua->get( 'http://questhub.io/api/realm' )->res->body
```

[g]: http://mojolicio.us/perldoc/ojo#g
[Mojo::UserAgent]: http://mojolicio.us/perldoc/Mojo/UserAgent

[g][] is a shortcut for the `get` method of [Mojo::UserAgent][]. There
are shortcuts for numerous HTTP verbs in [ojo][].

``` perl
# using ojo::j and ojo::g
j( g( 'https://questhub.io/api/realm' )->body )

# is rougly the same as this
decode_json( $ua->get( 'https://questhub.io/api/realm' )->res->body )
```

[j]: http://mojolicio.us/perldoc/ojo#j
[Mojo::JSON]: http://mojolicio.us/perldoc/Mojo/JSON#j

[j][] is a convenience function from [Mojo::JSON][] for encoding and
decoding JSON. My experience so far has been that it does what I mean
when I use it.

``` perl
# using j, g, and postderef
j( g( 'https://questhub.io/api/realm' )->body )->@*

# is rougly the same as this
@{ decode_json( $ua->get( 'https://questhub.io/api/realm' )->res->body) }
```

`$ref->@*` is an experimental new syntax for accessing the contents of
an array reference. It is equivalent to `@{ $ref }` or `@$ref`. The
[postderef][] syntax is a little easier for me to read, but your
experience may be different.

## All Done

That is enough for now. With the [ReadLine plugin][] and
[Editor plugin][] enabled, a nice 2014-ish Perl setup in my `.replyrc`,
and [ojo][] available when I want it, [Reply][] is downright useful
for me.
