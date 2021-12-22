---
aliases:
- /coolnamehere/2009/12/09_nqp-not-quite-perl.html
- /post/2009/nqp-not-quite-perl/
- /2009/12/09/nqp-not-quite-perl/
category: coolnamehere
date: 2009-12-09 00:00:00
layout: layout:PublishedArticle
slug: nqp-not-quite-perl
tags:
- parrot
- perl
title: NQP - Not Quite Perl
uuid: d1b60fc6-bd57-460d-9469-aede4bc366ad
---

[Parrot]: http://parrot.org
[Rakudo]: http://rakudo.org
[NQP]: http://docs.parrot.org/parrot/latest/html/docs/book/pct/ch05_nqp.pod.html

[Parrot][] is more than just PIR and PASM. I'm not talking about the
ability to use languages like [Rakudo][] written for the Parrot virtual 
machine. I am also not talking about the ability to write your own language.
Both of those are quite nifty, of course. It is fair to say that those two
items are probably why you are experimenting with Parrot in the first place.
However, the Parrot distribution also ships with an extra language: NQP.
<!--more-->

[NQP][] - Not Quite Perl - is an implementation of a small subset of Perl 6 that
can be used as a higher level Parrot language than PIR. It is especially useful
in defining the grammars for your Parrot languages.

## Getting NQP

[here]: /post/2009/07/parrot-babysteps-01-getting-started


You already have NQP if you have a fresh installation of [Parrot][]. You can
find directions for installing [here][] if
you do not yet have Parrot installed.

## Example

Let's just do a brutally fast NQP example.

    #!/usr/local/bin/parrot-nqp

    my $name := get_input("What is your name?");
    say("Hello $name");

    my $valid_input := 0;

    while ($valid_input == 0) {
        my $in_good_mood := get_input("Are you in a good mood?[y/n]");
        if ($in_good_mood eq "y") {
            say("Glad to hear it! Must be all the Parrot hacking.");
            $valid_input := 1;
        } elsif ($in_good_mood eq "n") {
            say("Oh, that's too bad. Try hacking on Parrot.");
            $valid_input := 1;
        } else {
            say("Sorry, I'm not too bright. Please answer 'y' or 'n'.");
        }
    }

    sub get_input($prompt) {
        print("$prompt ");
        my $name := Q:PIR{
            .local pmc stdin
            stdin = getstdin
            %r = stdin.'readline_interactive'()
        };

        return $name
    }

We see that NQP variables look a little like Perl variables, and familiar 
control structures like `if` and `while` are supported. Another bit of niftiness
is that inline PIR is supported.

    $ parrot-nqp hello.nqp
    What is your name? Brian
    Hello Brian
    Are you in a good mood?[y/n] waffles
    Sorry, I'm not too bright. Please answer 'y' or 'n'.
    Are you in a good mood?[y/n] y
    Glad to hear it! Must be all the Parrot hacking.

Mind you, NQP is not really great for casual scripting. It's intended to be
a higher level bootstrap language that makes it easier to define grammars.
I wouldn't go complaining to anybody that it's missing Feature X. Unless you
know how to implement it. Maybe. If you want Feature X, it might be better
to use [Rakudo][] or implement it in your own [Parrot][] language.

You could even use [NQP][] to implement it. Is my logic circular enough for
you?

## Learning NQP

There is a good overview of NQP available at
[wikibooks](http://en.wikibooks.org/wiki/Parrot_Virtual_Machine/Not_Quite_Perl).