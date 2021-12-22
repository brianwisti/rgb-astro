---
aliases:
- /coolnamehere/2009/07/11_01-getting-started.html
- /post/2009/01-getting-started/
- /2009/07/12/parrot-babysteps-01-getting-started/
category: coolnamehere
date: 2009-07-12 00:00:00
layout: layout:PublishedArticle
series:
- Parrot Babysteps
slug: parrot-babysteps-01-getting-started
tags:
- parrot
- learn
title: Parrot Babysteps 01 - Getting Started
updated: 2011-04-11 00:00:00
uuid: 22715718-e39d-492c-a45d-9cb8fafa0131
---

## Introduction

[Parrot Intermediate Representation]: http://docs.parrot.org/parrot/latest/html/docs/book/pir/ch03_basic_syntax.pod.html

I want to explore basic installation and usage of Parrot. The usage will include output,
simple variables, and input. PIR, the [Parrot Intermediate Representation][] language, will be my
language of choice. This is the same pattern as my other Babysteps tutorials, but the fact 
that PIR is a lower level language means that these are going to be some pretty big steps. I 
encourage you to walk along with me if you're curious about PIR.

As always, I welcome suggestions from both novice and experienced Parrot hackers on how 
to improve this material for newcomers to Parrot.

### My Setup

[Vim]: /tags/vim/

#### Linux

[Ubuntu]: http://www.ubuntu.com
[build-essential]: http://packages.ubuntu.com/lucid/build-essential
[wget]: http://packages.ubuntu.com/lucid/wget

I'm running [Ubuntu][] 10.10 with [build-essential][] and Perl 5 installed.
Perl 5 is installed by default on Ubuntu, and `build-essential` is easy enough.

    $ sudo apt-get install build-essential

There may be other dependencies already installed on this machine that I do not know
about. I tend to install *many* packages on my system, such as [wget][]. Perl 5 and 
`build-essential` should do it as far as I know, though.

You will probably want a good text editor as well. [Vim][]
is my choice, but you're welcome to use anything that makes you happy.

#### OS X

[MacPorts]: http://www.macports.org

The iMac which rules our home is currently running OS X 10.6 with the Developer Tools
and [MacPorts][]. As usual, my text editor of choice for this platform is [Vim][]. I 
have my essential toolkit including `wget` installed via MacPorts.

#### Windows

I'm using 32 bit Microsoft Windows 7 Ultimate on the other partition of my laptop. Hey, 
it's better than Vista. I'm also using [Vim][] to edit my
files on this platform because I am a creature of habit.

## Installation

You need to get Parrot before you can use it. 
The [download page](http://www.parrot.org/download) shows where you can get 
versions of Parrot appropriate to your system, including [Windows 
packages](http://sourceforge.net/projects/parrotwin32/). 

### Linux and OS X

[stable source release]: http://parrot.org/source.html

I will be grabbing the latest [stable source release][].

    $ cd ~/src
    $ wget http://www.parrot.org/release/supported

Previous versions of these Babysteps were using the development releases of Parrot.
Why did I switch? I have trouble keeping my articles up to date with the pace
of Parrot development while also developing new material and working, so my focus moved
to the slower "supported" cycle. I may switch back to using development releases
if stable is horribly broken for something the Babysteps need. You're welcome
to use development. Most of the material will *probably* work as-is.

I've gone through a few installations of Parrot by now, and have finally noticed that
bad things happen if you ignore your old installation. Cleaning up the important
files for the old installation is a good idea. So, if you are upgrading:

    $ sudo rm -rf /usr/local/lib/*parrot*

Of course, you better make sure that anything matching that name pattern is actually
related to your old Parrot install before nuking them like this.

Next I'll unpack, build, and test my download.

    $ tar xfvz parrot-3.0.0.tar.gz
    $ cd parrot-3.0.0
    $ perl Configure.pl
    $ make
    $ make test

`make test` takes a little longer each time I install a new version of Parrot. They add tests in every 
iteration. Just think of those extra few seconds as proof that someone cares about the quality of
software they're writing for the world.

The Parrot authors can always use additional feedback about how well their baby works on
different platforms. One piece of information that can be useful for them is a smoke report
with test results telling them how well Parrot works on your machine. You can very easily do
this on Linux and OS X:

    $ sudo cpan TAP::Harness::Archive
    $ make smoke
    ...
    All tests successful.
    Files=381, Tests=13848, 155 wallclock secs ( 2.36 usr  1.43 sys + 102.37 cusr 28.89 csys = 135.05 CPU)
    Result: PASS

    TAP Archive created at /Users/brian/src/parrot/parrot-3.0.0/parrot_test_run.tar.gz
    Test report successfully sent to Smolder at
    http://smolder.parrot.org/app/projects/report_details/14424
    You can see other recent reports at
    http://smolder.parrot.org/app/projects/smoke_reports/1 .

[list of recent reports]: http://smolder.parrot.org/app/projects/smoke_reports/1

My smoke report and the [list of recent reports][] are fun to look at in a nerdy
sort of way.

There. Now I'll install Parrot.

    $ sudo make install

Oh, editor support is also available. Since I'm using Vim, I'll need to make `vim-install`.

    $ cd editor
    $ make vim-install

This gives me syntax highlighting and template generation for new PIR files.

### Windows

It appears to be even more straightforward to install Parrot on Microsoft Windows.
The [Parrot download page](http://www.parrot.org/download) includes a link to 
an installer file. 

> [parrot-win32 setup files](http://sourceforge.net/projects/parrotwin32/files/parrotwin32%20setup/)

[Rakudo]: /tags/rakudo

The stable setup file available currently is `setup-parrot-3.0.0.exe`. If you browse around,
you will find a lot of interesting setup files. I won't be exploring them right now,
but I encourage you to check them out.

I will download the latest stable installer and run it, following all the defaults for now. 
That was easy. Don't miss the CHM Parrot documentation in `C:\Parrot-2.3.0\share\doc\parrot`! 
It is good to have documentation handy when exploring strange new software.

I'm not sure if this warning is still true, since my recent reinstallation of Windows
means I don't have a previous Parrot install to overwrite. Still, it's worth checking out.

When you install a new version of Parrot, the default behavior is to place it in the
same location as your previous installation. This means 3.0 would sit in `C:\Parrot-2.9.0`
on my machine. That can cause trouble, since some important Parrot settings may be based
on assumptions about where it was installed. The safest thing before upgrading Parrot
on Windows is to uninstall old versions through the Control Panel, and to make sure
that previous Parrot bin folders are not sitting on your Path. Check for that in 
Computer &rarr; System Properties &rarr; Advanced System Settings &rarr; 
Environment Variables. It gets easier to remember those steps after you've clicked them
a few times. **Do not install a new Parrot until you have removed the old one!**

So - installing Parrot is easy, but I still want my Vim support. The installer was made with
the reasonable assumption that Parrot users on Windows weren't going to need support for their
favorite Unix editors. Reasonable assumptions tend to break down around me, though.

If you're not using Vim on Windows, you can just move on to the next section. As for the rest of us,
let's get to it.

[editor]: https://github.com/parrot/parrot/tree/RELEASE_3_0_0/editor
[README.pod]: https://github.com/parrot/parrot/blob/RELEASE_3_0_0/editor/README.pod

1. Take your browser to the [editor][] directory for the latest stable Parrot release.
2. Download the files that are important for Vim support:
    * `filetype_parrot.vim`
    * `indent_pir.vim`
    * `pasm.vim`
    * `pmc.vim`
    * `pir_vim.in`
    * `skeleton.pir`
3. Create a `vimfiles` directory in your home folder if you don't already have one.
4. Using [README.pod][] as your guide, move the support files into your `vimfiles` directory:
    * `filetype_parrot.vim` &rarr; `vimfiles\ftdetect\filetype_parrot.vim`
    * `indent_pir.vim` &rarr; `vimfiles\indent\pir.vim`
    * `pasm.vim` &rarr; `vimfiles\syntax\pasm.vim`
    * `pmc.vim` &rarr; `vimfiles\syntax\pmc.vim`
    * `pir_vim.in` &rarr; `vimfiles\syntax\pir.vim`
    * `skeleton.pir` &rarr; `vimfiles\skeleton.pir`
5. Open `vimfiles\ftdetect\filetype_parrot.vim` and execute the following:
    * `:4s/\.vim/vimfiles`
    * Or yeah, you can move to where it says `.vim` and manually replace that 
      with `vimfiles` if that's how you like to do things.

The steps may be a little more involved than just "click and run", but it's worth
it for me. I *like* having Vim support.

## Output

It is time to start writing code. Move to your projects
directory and create a new directory for the Parrot Babysteps project.

    $ cd ~/projects
    $ mkdir parrot-babysteps
    $ cd parrot-babysteps
    $ gvim example-01-01.pir

When I'm connected to the iMac via `ssh` I settle for

    $ vim example-01-01.pir

The steps are the more or less the same on Windows. First, open a command
prompt by whatever means you're comfortable with. I prefer typing `cmd`
into the "Search programs and files" field of the Start menu. Then, move to your projects
directory and create a new directory for the Parrot Babysteps project.

    C:\Users\brian> cd \projects
    C:\projects> mkdir parrot-babysteps
    C:\projects> cd parrot-babysteps
    C:\projects\parrot-babysteps> gvim example-01-01.pir

From here on, the differences between Windows and other platforms become
small enough that I feel comfortable ignoring them until something really significant
catches my attention.

We immediately see some benefit from installing editor support.

    # Copyright (C) 2011 Parrot Foundation.

    .sub 'main' :main
        # For Parrot developers.
    .end

    # Local Variables:
    #   mode: pir
    #   fill-column: 100
    # End:
    # vim: expandtab shiftwidth=4 ft=pir:


That looks like a heck of a lot for an otherwise empty file, but most of those
lines are actually comments.

### Comments

PIR comments start with a `#` character. Everything from that `#` to the end of the line is
ignored by the parser.

    # This is a comment

Comments are handy. They can explain why you chose a particular solution, 
concerns you have about the code, or pretty much anything else. The
comments in our template serve to identify where the template file came from
and a few directives for Vim to remember when editing this file.

### Directives

There are only two important lines left when we ignore the comments.

    .sub main :main
    .end

Lines that start with a period (`.`) are *directives*, special instructions for PIR. There
are a number of directives for Parrot, and it is possible to create your own. The `.sub`
line is telling PIR that this line begins a compilation unit called "main" which serves as the `:main`
compilation unit in the program. Compilation units are tasty named tidbits of code that get a 
particular job done. They seem roughly the same as subroutines in other languages, so that's
what I'm going to call them from here on. Less typing that way. Once you have created a subroutine, 
you can call it elsewhere in your code. 

Subroutines can also have a tag after their name to add a little extra information. The
subroutine tagged as `:main` is the main entry point for a PIR application - it's where
the program actually starts running. When you hand a `.pir` script to parrot, it directly 
executes the code contained in `:main`. If it can't find a subroutine tagged 
with `:main`, then Parrot will directly execute the first subroutine in your code. It is a 
good idea to specify which is `:main` so you don't have to rely on the default behavior.

The `.end` directive tells PIR that it has reached the end of this particular subroutine.
Any `.sub` must be followed by `.end` eventually. Everything in between is the
body of the subroutine - the stuff that gets executed when the subroutine is called.

We now basically know what a subroutine is, what it looks like, and how Parrot goes
about figuring out which one to run first. We still don't have anything to be executed,
though. How about making this program *do* something?

### Building The Program

    # example-01-01.pir
    .sub main :main
        say "Hello, world!"
    .end

Finally - code! Fairly self-explanatory code at that. Well, almost. `say` is 
an [*opcode*](http://docs.parrot.org/parrot/latest/html/ops.html) - a 
native Parrot command - for presenting values to the user. `say` won't normally speak the
phrase "Hello, world!" through your speakers. It will, however print the phrase on a line in your
console.

    $ parrot example-01-01.pir
    Hello, World!
    $

## Variables

What if I want to change the greeting, so that it displays my name as part of the greeting?
While simply rewriting the phrase does technically work ...

    # example-01-02.pir
    .sub main :main
        say "Hello, Brian!"
    .end

... I want something a little more flexible. I want to be able to define a name, and then
print a greeting with the name. This will require adding a variable.
We use variables whenever we want the program to remember something.

There are four types of things that Parrot can keep track of:

integers
: Simple counting numbers, like 13 or -485

numbers
: Decimal numbers like 1.3 or -1.3e+5

strings
: text and phrases like "Hello, Brian"

Polymorphic Containers, or PMCs
: A special type that basically refers to anything that's not an integer, number, or string

Parrot has special rules for dealing with each of these types, so it is important to tell Parrot
how you want your variable treated. One way to do that is with *register variables*. Registers
can be thought of as variable buckets: one bucket for each type. Okay, maybe not a bucket. More
like four rows of nicely organized variables, with each variable type in its own row.

Register variables are prefixed with the dollar sign `$` and an uppercase letter indicating their
type. The rest of the variable name is a whole number from zero on up. Here, let me show you:

    # example-01-03.pir
    .sub main :main
        $S0 = "Brian"
        $S1 = "Hello, " . $S0
        $S1 = $S1 . "!"
        say $S1
    .end

Assignment to register variables is pretty straightforward, as you can see. You tell Parrot which
position in which row is being assigned to on one side of the `=` symbol, and the value
to assign on the other. 

Oh, did you see what I did when creating `$S1`? I did mention that Parrot has special rules for
handling each type of variable. One thing you can do with string variables is paste two of them
together, making a whole new string. You use the `.` operator for that. But only for pasting two
strings together. If you want more, you'll need to do it on two lines like I did.

Back to register variables. No, it doesn't really matter which numbers you use. I could have 
used `$S9999` to hold the name and Parrot wouldn't care. We just need to remember what purpose 
each variable serves.

Actually, that's the main problem with register variables. Their names don't tell you much about
what purpose the variable serves. Sure, it's easy enough to see that `$S1` is a string, but will I
still remember that it's being used to hold the name once I've added a few hundred lines of code?
Probably not. I'm getting flashbacks to programming BASIC in grade school, when I kept a cheat 
sheet of variable names handy. 

Parrot is thankfully there for us with the `.local` directive. `local` allows us to create a
readable name for our variable, asking Parrot to deal with the register side of things. 

Creation of a local variable requires the `.local` directive, followed by type information and
lastly a variable name. 

    .local <type> <name>

The type names match up to the Parrot types, of course:

* `int` for integers
* `num` for numbers
* `string` for strings
* `pmc` for PMCs

Variables created with the `.local` directive can be treated the same as a
register variable.

    # example-01-04.pir
    .sub main :main
        .local string name
        .local string greeting

        name = "Brian"
        greeting = "Hello, " . name
        greeting = greeting . "!"
        say greeting
    .end

You know, that line where we append an exclamation to our greeting is longer than it needs to be.
The PIR provides special operators for when you are doing something to a variable and then assigning
the result back to the same variable. That means we could describe "append an exclamation point to 
`greeting`" this way, too:

    # example-01-05.pir
    # ...
    greeting = "Hello, " . name
    greeting .= "!"
    # ...

## Input

We've covered a lot of conceptual ground already. What has it earned us?

    $ parrot example-01-05.pir
    Hello, Brian!

This is not impressive. We've actually increased the amount of code significantly compared
to just saying "Hello, Brian!". Splitting the name off into its own variable does lay the groundwork
for a slightly more impressive task, though. Let's make the program ask the user for his name
when run.

    # example-01-06.pir
    .sub main :main
        .local string name
        .local string greeting
        .local pmc stdin

        stdin = getstdin
        name = stdin.'readline_interactive'("Please enter your name: ")
        greeting = "Hello, " . name
        greeting .= "!"
        say greeting
    .end

We've only added a few lines, but these few lines have added a lot of functionality. The first thing
you probably noticed was the *pmc* variable named `stdin`. PMCs are used in Parrot for complex types,
like classes in other languages. They often have special subroutines called *methods* tied to them.
Those methods can greatly simplify the creation of complex programs.

We use the opcode `getstdin` to figure out standard input and assign
it to our `stdin` PMC. Standard input - widely referred to as *stdin* - is a 
[FileHandle](http://docs.parrot.org/parrot/latest/html/src/pmc/filehandle.pmc.html) that
describes where we expect user input to come from. That can be any number of places, but 
usually refers to the keyboard. The FileHandle method we care about most today is `readline_interactive`. 
`readline_interactive` prompts the user for input, and hands that input back to the program.

    $ parrot example-01-06.pir
    Please enter your name: Brian
    Hello, Brian

## Conclusion

We've done quite a bit today. We installed Parrot, created a simple script that prints a greeting
to the console, then expanded our script to get the user's name and incorporate the name into the
greeting. It took less effort than I thought it would despite the fact that PIR is low-level
compared to languages like Python and Perl 5. 

[PMCs]: http://docs.parrot.org/parrot/latest/html/pmc.html

The ability to handle user input makes it easier to create meaningful programs even with a bare
minimum of knowledge, and can be very handy as we explore Parrot, the PIR syntax, and the
many [PMCs][]. From this starting point, 
we can go deeper into the [Parrot](http://docs.parrot.org/parrot/latest/html/) and [PIR](http://docs.parrot.org/parrot/latest/html/docs/pdds/pdd19_pir.pod.html) documentation, and search the Web
for Parrot tutorials.

Remember also that Parrot is released monthly. I do try to keep these pages up to date, but sometimes
work and life demand more of my time, or I get distracted by bright shiny things. So don't assume
my version numbers are correct. Double-check them for yourself.

Most of all, have fun!