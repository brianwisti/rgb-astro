---
aliases:
- /coolnamehere/2005/01/04_01-getting-started.html
- /post/2005/01-getting-started/
- /2005/01/04/perl-5-babysteps-01-getting-started/
category: coolnamehere
date: 2005-01-04
description: Installing and first steps with Perl
layout: layout:PublishedArticle
slug: perl-5-babysteps-01-getting-started
tags:
- perl
- learn
title: Perl 5 Babysteps 01 - Getting Started
updated: 2011-08-25
uuid: 2a728cf0-b5fb-451b-b895-5df3d882cb10
---

## Installing Perl

[Perlbrew]: link:/post/2011/09/perlbrew/
[Microsoft Windows]: https://www.microsoft.com/en-us/windows

Okay.
Everybody not on [Microsoft Windows][], go install [Perlbrew][].

Done?
Excellent.
Here is how you install Perl 5.14.1 and make it your default Perl.

    $ perlbrew install perl-5.14.1
    $ perlbrew switch perl-5.14.1

### Installing Perl on Windows

On Windows, the preferred option is usually to download an installation package.

#### ActivePerl

[ActivePerl]: http://activestate.com/Products/activeperl/
[ActiveState]: http://activestate.com

[ActivePerl][] is a commercially supported version of Perl for Windows.
ActivePerl can be downloaded for free.
It comes with a wealth of widely used third-party libraries such as an DBI, LWP, and the XML bundle.
It is released by [ActiveState][], a company based out of Canada.
It is also the only readily available release of Perl 5.14 for Windows at this exact moment.

### Verify Your Perl

We want to make sure that `perl` installed where we expected it to and that our system finds the right one.

    $ perl --version
    This is perl 5, version 14, subversion 1 (v5.14.1) built for darwin-2level

    Copyright 1987-2011, Larry Wall

    Perl may be copied only under the terms of either the Artistic License or the
    GNU General Public License, which may be found in the Perl 5 source kit.

    Complete documentation for Perl, including FAQ lists, should be found on
    this system using "man perl" or "perldoc perl".  If you have access to the
    Internet, point your browser at http://www.perl.org/, the Perl Home Page.

## Using Perl From The Command Line

It would be unfair of me to ignore simple command-line Perl.

### `perl -E`

Although most of my Perl time is spent on large projects, occasionally I just want a quick answer.
Because I usually have a terminal open, Perl presents itself as a convenient calculator:

    $ perl -E 'say 3.1415926 * 5 ** 2'
    78.539815

It is almost the same on Windows, except that you need to use double quotes:

    C:>perl -E "say 3.1415926 * 5 ** 2"
    78.539815

The `-E` flag tells `perl` that the next bit is code to be executed directly.
There are many flags to adjust the behavior of `perl` when you run it.
[perlrun](http://perldoc.perl.org/perlrun.html)shows all the gory details.

    $ perldoc perlrun

I don’t plan on talking any more about Perl one-liners.
I just thought you should know that they are available.
They can be useful, but I am not the person to teach them.
[Minimal Perl](https://minimalperl.com) is a great starting point for exploring that aspect of Perl’s power.

So.
What exactly are we doing with that one line?
There’s something that looks like math, and `say`.
I guess it is fairly obvious what `say` is doing here: it is printing stuff out to our terminal.

<aside class="admonition">
<p class="admonition-title">2020-02-24</p>

Reading back, and it looks like I was starting to write something about `perldoc`?

</aside>

### `perldoc -f`

We can ask about specific built-in functions using the `-f` parameter.

    $ perldoc -f say
    say FILEHANDLE LIST
    say FILEHANDLE
    say LIST
    say     Just like "print", but implicitly appends a newline. "say LIST"
            is simply an abbreviation for "{ local $\ = "\n"; print LIST }".
            To use FILEHANDLE without a LIST to print the contents of $_ to
            it, you must use a real filehandle like "FH", not an indirect
            one like $fh.

            This keyword is available only when the "say" feature is
            enabled; see feature. Alternately, include a "use v5.10" or
            later to the current scope.

            This keyword is available only when the "say" feature is
            enabled; see feature. Alternately, include a "use v5.10" or
            later to the current scope.

<aside class="admonition">

Yeah I had a bad habit of posting unfinished content in the pre-blog days.

</aside>

### `perldoc -q`

## Creating Perl Programs

The tradition in programming literature is to start by creating a program that prints a simple phrase, such as "Hello, World!"
The idea is to give you some clue how much work is involved in creating a minimal program.
I am not going to argue with tradition.
Not this one, at least.
Type the following into your text editor:

```perl
=head1 hello.pl

Displays a warm greeting.

=cut

# Depends on features not in older Perls.
use 5.14.0;

say "Hello, World!";
```

Save the file as `hello.pl`.
We will run it in a few moments -- but first, let’s take a quick look at what we’ve got so far.

### POD

```perl
=head1 hello.pl

Displays a warm greeting.

=cut
```

POD, or "Plain Old Documentation", is the standard system for documenting Perl programs.
POD directives exist within your application, but are ignored during execution.
They are instead processed by the `perldoc` application.
`perldoc` can convert your POD to different formats such as HTML, or simply format and display the documentation to your screen.
Use POD to write about what you want *users* to know about your Perl application.
A proper introduction to `perldoc` is far beyond the scope of this little tutorial, but you can see the potential usefulness of this tool from the console with a simple command:

    $ perldoc hello.pl

You get a simple display showing a formatted version of the POD you wrote.
There is a lot more information you can get about POD and perldoc within Perl’s own POD:

    $ perldoc perlpod

There’s also an [HTML version](http://perldoc.perl.org/perlpod.html) if
`perldoc` is not available on your system or you just want to see something
pretty.

### Comments

``` perl
# Depends on features not in older Perls.
```

On each line, everything from `#` to the end of the line is a _comment_.
Perl ignores comments, so they allow you to communicate with other people who read your code.
Comments are *good*.
When you come back to look at a complex script after a few months, you might forget what some block of code does, or why you chose one solution over another.
Having the comments there help to remind you what you were intending, and generally serve to make it much easier sorting everything out.

### `use`

``` perl
use 5.14.0;
```

The `use` statement is incredibly powerful.
It effectively changes the way Perl will behave for the duration of your program.
You can get extra functionality with `use` by loading a module, or you can significantly change the rules Perl runs under by loading a _pragma_.

I will be taking full advantage of the `use` statement in this tutorial,
because it takes Perl from a strong shell scripting language to an incredibly powerful programming language.

Oh, about that semi-colon (`;`): `perl` uses the semi-colon to separate statements.
Each statement contains a particular instruction for the Perl language.
You will usually - but not always - see Perl code with one statement per line, with a semi-colon at the end of each line.

// Explain `5.14.0`.

Let’s get back to looking at `hello.pl`

### `say`

``` perl
say "Hello, World!";
```

We use `say` to print things out on a line in Perl 5.14.
This time we’re asking Perl to say the phrase "Hello World!"".

Hm.
I really thought it would take more effort to explain that.
Oh well, guess there’s nothing left to do but see it in action.

## Running it

Now you would probably like to know how to actually run your program.
Save the file you have been editing and switch to a command line.
Make sure you are in the same directory as your script - this should be as simple as `cd project-directory`.
Once you are in the right place, type the following into the command line:

    $ perl hello.pl Hello, World!

All this is kind of cool, but it would be nice to customize it a little bit.
Maybe we could change the program so that it says "Hello" to us personally.

```perl
=head1 hello.pl

Displays a warm greeting.

=cut

# Depends on features not in older Perls.
use 5.14.0;

my $name = "Brian";
say "Hello, $name!";
```

We use the word `my` to declare variables.
Declaration is when we tell Perl that we have a variable we plan on using.
Perl 5.14 mode enforces the declaration of variables.

What’s a variable?
We’ll get to that in a second.
I’m impatient to see a running program! Save the file, and run it again.

    $ perl hello.pl Hello, Brian!

There, I feel better.
Let’s move on to talking about variables.

### Variables

We stored the string "Brian" in the variable `$name`.
You can think of a *variable* as a tag - a name we use for some value that we want the program to remember.
Later, we can get that value back by referring to the tag.

The `$` symbol at the beginning tells Perl what type of value this variable will be used for.
The _type_ of a variables gives clues for how it can be treated.
Most variables in Perl break down into two broad categories.


1. Individual things like strings and numbers
2. Collections of things like lists and dictionaries

Variables that refer to individual things are called *scalars* in Perl.
They are easy to recognize, because they are prefixed by a `$` symbol.

```perl
my $name = "Brian"; # I'm going to use a scalar variable called 'name'.
                    # It has the value "Brian".
```

*Strings* -- scalar values intended to be handled like simple text --
are always quoted in some way to show where the text of the string begins and where it ends.
There are many ways to quote a string, but for now I will use double-quote characters.
That is what quoted text looks like in American English, so it is easy for me to remember.
It also provides some other conveniences when displaying variables, such as when we say `"Hello, $name"` later in the program.

Anyways, this single line both declares the variable `$name`, letting Perl know you plan on using it, and assigns a value to `$name`, so that Perl will have something to remember.
What happens if you skip one or both of these steps?
It depends, so the best thing to do is try it and see.

``` perl
=head1 hello.pl

Displays a warm greeting.

=cut

use 5.14.0;

say "Hello, $name!";
```

We’ve removed the declaration and assignment.
Let’s see what happens now.

    $ perl hello.pl
    Global symbol "$name" requires explicit package name at hello.pl line 12.
    Execution of hello.pl aborted due to compilation errors.

Because we insisted on 5.14, Perl politely informed us that it found some mention of a variable called `$name` that we never declared.
This is considered rude by recent Perls, so the interpreter quit without running the program.

Okay, what if we declare `$name` but never assign a value to it?

```perl
use 5.014;

my $name;
say "Hello, $name!";
```

This time Perl runs, but the results are confusing.

    $ perl hello.pl Hello, !

Since `$name` has no value, Perl has nothing to put in that string.
That’s exactly what it puts there: nothing.

### `use warnings;`

Perl generally assumes that you know what you are doing.
It will not argue with you if you want to use a variable that has no value.
However, that behavior is not always helpful.
Using a variable without a value is usually a mistake, and it can often be a very difficult mistake to track down.

This is why Perl provides the [warnings pragma](http://perldoc.perl.org/warnings.html).
If you enable warnings, you will be told about common mistakes like these.

```perl
use 5.014;
use warnings;

my $name;
say "Hello, $name!";
```

That addition makes Perl much friendlier for learners or people with large, unpredictable applications.

    $ perl name.pl
    Use of uninitialized value $name in concatenation (.) or string at name.pl line 5.
    Hello, !

The combined behavior of `use 5.14.0;` and `use warnings;` may not seem like much right now, but they are vital when working with large applications that have thousands of lines of code.

With these behaviors enabled we have told Perl to behave more like a powerful application programming language with Perl’s latest features instead of as a quick and handy tool for system administrators.
Decide for yourself whether that transformation is important to you, but all of my code in this tutorial will use both of these pragmas.