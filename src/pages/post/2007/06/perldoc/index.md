---
aliases:
- /coolnamehere/2007/06/16_perldoc.html
- /post/2007/perldoc/
- /2007/06/16/perldoc/
category: coolnamehere
date: 2007-06-16 00:00:00
layout: layout:PublishedArticle
slug: perldoc
tags:
- perl
- learn
title: Perldoc
updated: 2009-07-11 00:00:00
uuid: 36ea676b-9cdc-4183-b03e-cff613b129f6
---

I have heard first-time Perl programmers complain about the lack of documentation. 
This is understandable. They don't know all the nifty stuff that comes with the 
standard Perl distribution. 
<!--more-->

Perl has a built-in documentation system referred to as `perldoc`. Perl modules 
are spiked with documentation about how to access the features of that module. 
This documentation is in the form of POD, or Plain Old Documentation. `perldoc` 
reads the POD, formats it into something more pleasing to the eye, and presents 
it to you in one form or another. I'll be talking about the command-line `perldoc` 
utility, but the documentation is also transformed into HTML for the ActiveState 
Perl distribution, [CPAN](http://cpan.org/), and the [perl.org perldoc 
repository](http://perldoc.perl.org/). You may think you don't need to worry about 
the `perldoc` command if you have ready access to the Internet, but it is still 
useful for finding exactly the details you need. Accessing documentation from 
the command line also means that you can view the details for the specific version 
that is installed on your machine. And really, these are my notes. You can stop 
reading any time you like.

Using `perldoc` is easy. Basic usage looks like this:

    $ perldoc name-of-article-or-module

`perldoc` goes looking for the POD associated with the specific article or 
module. If it finds the POD, it formats it using a special program (usually 
`nroff` on Linux) and feeds the formatted text to a screen reader such as 
`more` or `less`. You can then search or page through the documentation using 
the normal commands for your screen reader.

It is as simple as that. I am going to look at some of the things `perldoc` can
find for you, but first I need to make a small confession. All I'm doing is reviewing
the documentation for `perldoc` itself. You can skip my rambling notes and get
directly to the meat of the information with the following command:

    $ perldoc perldoc

All the information you could possibly want is in the perldocs, or it should be.
It may not always make sense the first time through. It will seem clear as a bell
after a little practice. You can always refer to other sources until it starts to
make sense.

    $ perldoc perl

This provides a simple summary of perl's command line options, a very brief summary 
of the available documentation, and a description of Perl itself. Use use this 
for the summary, but there is a more detailed summary available.

    perldoc perltoc

This contains an extensive overview of the documentation available, including 
summaries, keywords, and a table of contents for each article. Look close enough 
and you will notice that there are several tutorials available.

## Accessing information about a specific module

    $ perldoc <module>

### Viewing the source of that module

    $ perldoc -m <module>

### Finding out exactly which file contains the documentation

    $ perldoc -l <module>

## Accessing specific information

### Perl built-in functions

    $ perldoc -f <function>

### The Perl FAQ

    $ perldoc -q <search-expression>

`perldoc` will then look for a FAQ question containing the search expression, and 
present it to you.

## Wrapping Up

These are the main features of `perldoc` that I use, but that's not all there is 
to it. Check `perldoc perldoc` for all the gory details.