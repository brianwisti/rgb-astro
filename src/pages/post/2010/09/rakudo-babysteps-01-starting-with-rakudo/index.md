---
aliases:
- /coolnamehere/2010/09/09_starting-with-rakudo.html
- /post/2010/starting-with-rakudo/
- /2010/09/09/rakudo-babysteps-01-starting-with-rakudo/
category: coolnamehere
date: 2010-09-09 00:00:00
layout: layout:PublishedArticle
slug: rakudo-babysteps-01-starting-with-rakudo
tags:
- rakudo
- Raku Lang
- learn
title: Rakudo Babysteps 01 - Starting With Rakudo
updated: 2021-08-21
uuid: deae393e-c926-40c6-83ea-4cee9e338cfe
---

## Installation

You will obviously need to install Rakudo if you want to use it. There
are a couple of options, but I will focus on Rakudo Star. Rakudo Star is
a distribution which includes some important libraries and an excellent
book.

<aside class="admonition note">
<p class="admonition-title">Note</p>

Rakudo is released every month, so some of my details about version
numbers may be a little off. I will do my best to stay caught up.
Fortunately, my Babysteps are so basic that new releases have little
effect on their value.

</aside>

The easiest way to install Rakudo Star depends on your operating system.
Specifically, it depends on whether you’re using Microsoft Windows.

### Windows Installer

There is a lovely Rakudo Star installer available for Windows users. It
includes all the pieces needed to get started with Rakudo. Look on the
[Rakudo Star download page](http://github.com/rakudo/star/downloads) for
a filename ending in `.msi`. Right now, that file is
`rakudo-star.2010.07.msi`. It will probably be a different file when you
look.

Download that MSI file and run it. Go ahead and accept the defaults,
unless you have a good reason not to.

Once you have installed Rakudo, you need to add it to your environment
path so that you can run it from the command prompt. Open your Start
menu, right click "My Computer", and select "Properties". Open the
"Advanced" tab, and click the "Environment Variables" button. Scroll
through "System Variables" until you see the entry for "Path". Double
click "Path" to open the "Edit System Variable" dialog. Enter the
location of your Rakudo installation - probably `C:\Rakudo\bin` - at the
beginning of the "Variable Value" field, followed by the `;` path
separator character. Click "OK" to close this dialog, "OK" again to
close the Environment Variables dialog, then "OK" one more time to close
the "System Properties" dialog.

To test, run "Command Prompt" and try `perl6 --version`.

    C:\> perl6 --version
    This is Rakudo Perl 6, version 2010.07-47-g9fd5eaa built on parrot 2.6.0

    Copyright 2008-2010, The Perl Foundation

Double check your Path environment variable if you don’t see something
like this.

It looks like you’ve installed Rakudo\!

### From Source

    $ mkdir ~/rakudo
    $ cd rakudo
    $ wget http://github.com/downloads/rakudo/star/rakudo-star-2010.09.tar.gz
    $ tar xfvz rakudo-star-2010.09.tar.gz
    $ cd rakudo-star-2010.09
    $ perl Configure.pl --gen-parrot --prefix=~/rakudo/
    $ make
    $ make rakudo-test
    $ make install

Of course, there’s no point installing Rakudo to a custom directory if
your shell can’t find it. Add a couple lines to your `.bashrc`.

    export RAKUDO_HOME=$HOME/rakudo
    export PATH=$RAKUDO_HOME/bin:$PATH

This will make the `perl6` executable available the next time you log
in, or you can rush the process by running `~/.bashrc`.

    $ . ~/.bashrc
    $ perl6 --version

    This is Rakudo Perl 6, version 2010.08 built on parrot 2.7.0

    Copyright 2008-2010, The Perl Foundation

Now that we know Rakudo is installed, let’s take a look at what it gets
us.

## What Do You Get?

Obviously, you get [Rakudo](http://rakudo.org). But Rakudo is built on
top of the Parrot virtual machine, so you also get a fresh copy of
[Parrot](/tags/parrot/). You can learn more about coding directly to the
virtual machine at the [Parrot
Babysteps](/post/2009/07/parrot-babysteps/). And you also get NQP, which
is sort of a stripped-down version of Rakudo that makes writing new
languages in Parrot a lot easier.

## The `perl6` Shell

One thing I missed in Perl 5 was a simple interactive shell. There is a
debug shell, but it’s not quite the same thing. Fortunately, Rakudo has
an interactive shell, and you start it by calling `perl6` from the
command line.

    $ perl6

What can we do in this shell? Well, we can print things out.

    > say "Hello, world!"
    Hello, world!

We can use it as a calculator.

    > 2 + 2
    4

We can calculate the area of a circle that has a radius of ten units.

    > my $pi = 3.1415926
    3.1415926
    > my $radius = 10
    10
    > 2 * $pi * ( $radius ** 2 )
    628.31852

Okay, you get the idea. There is a lot we can do with the perl6 shell.
Let’s start looking a little bit at the Perl 6 language.

First up is variables.

    > my $pi = 3.1415926
    3.1415926

    > my $name = "Brian"
    Brian
    > say "Hello, $name - good to see you!"
    Hello, Brian - good to see you!"

Exciting as that was, it’s time to leave the Perl 6 shell and start
writing a simple script. It’s easy enough to quit the shell.

    > exit
    $

## Writing a Perl 6 Program

All we need now to write a Perl 6 program is a text editor. I prefer
[Vim](/tags/vim/), which provides syntax highlighting.

```
# Do not run on older Perl versions!
use v6;

print "Please enter your name: ";
my $name = $*IN.get;
say "Hello $name - good to see you!";
```

    $ perl6 hello.p6
    Please enter your name: Brian
    Hello, Brian - good to see you!

## What Now?

<aside class="admonition">

2021-08-21
: I guess we'll never know; plenty of fun to be had with [Raku](/tags/raku-lang)
  thought!

</aside>
