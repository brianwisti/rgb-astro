---
aliases:
- /coolnamehere/2004/12/26_01-getting-started.html
- /post/2004/01-getting-started/
- /2004/12/26/rebol-babysteps-01-getting-started/
category: coolnamehere
date: 2004-12-26 00:00:00
layout: layout:PublishedArticle
series:
- REBOL Babysteps
slug: rebol-babysteps-01-getting-started
tags:
- rebol
- learn
title: REBOL Babysteps - 01 Getting Started
updated: 2017-04-09 00:00:00
uuid: a49cdc3c-aa2c-4ffb-8b9e-28b3f85d93e3
---

[REBOL](http://www.rebol.com/) is the "Relative Expression-Based Object
Language", developed by Carl Sassenrath. Who is Carl Sassenrath? Why,
he’s one of the people responsible for the amazing operating system
which powered the Amiga computer. What’s the Amiga? Why, the Amiga was
only the incredibly robust and cool computer — released by the same
company that brought the world’s first personal computer, Commodore.
What’s Commodore? Stop bothering me, kid. Take it from a relative
old-timer: Amiga put a *heck* of a lot of power into a
consumer-affordable personal computer. It wasn’t really matched by other
computers for a good five or ten years. Nowadays, I look at
[REBOL](http://www.rebol.com/) and it feels like the first language I’ve
come across to take lessons from past languages and apply them in a new
context, rather than just reimplement them with different syntax.

So why would you want to learn REBOL? Because REBOL makes it
frighteningly easy to create programs that accomplish complex tasks. For
example, here’s one way you can download the HTML source of a Web page –
for example <https://randomgeekery.org/> – and view it in a text editing
area with REBOL/View:

    >> view layout [ area 800x600 read https://randomgeekery.org ]

This impresses me to no end. Maybe you’re not so impressed by it, but
that’s okay. I’m happy, and that’s what I care about most.

These pages are intended to provide the non-programmer with a gentle
introduction to the REBOL language and environment. When you are done
with it, you should feel ready to learn more, and curious to dig into
the possibilities. You won’t be an expert, but maybe you’ll feel bold
enough to become one and share what you’ve found with the rest of the
world. Beginners and experts alike should feel free to send suggestions
about how I can improve this tutorial.

## Installing REBOL

Installing REBOL is a straightforward task, as long as you are using one
of the 40+ supported platforms.

### Platform Notes

#### Installation on Windows

- Download the archived installer for your platform from
  - <http://www.rebol.com/download.html>
- Unpack the installer, if necessary
- Run the installer
- Follow the installation wizard until you have installed the version
  you downloaded.

#### Installation on Linux

Here is what I had to do in order to get REBOL/Core and REBOL/View
running on my Ubuntu 8.10 laptop:

- Install a compatibility version of the GNU Standard C++ library
  - `sudo apt-get install libstdc++5`
- Download, extract, and copy the `rebcore` executable into my path
  - `wget http://rebol.com/downloads/v276/rebcore-linx86.tar.gz`
  - `tar xfvz rebcore-linx86.tar.gz`
  - `sudo cp rebol-276/rebol /usr/local/bin`
- Download, extract, and copy the `rebview` executable into my path
  - `wget http://rebol.com/downloads/v276/rebview-linx86.tar.gz`
  - `tar xfvz rebview-linx86.tar.gz`
  - `sudo cp rebol-276/rebview /usr/local/bin`

Why did I install both Core and View? There’s no real need to. I just
prefer to include a version of REBOL that doesn’t depend on X libraries
for scripting tasks that will never need a Viewtop. It’s particularly
handy for Web programming tasks.

There’s an intermittent problem with ugly fonts when using View under
Linux. I’ll post instructions for handling that on this site as soon as
I find my notes.

### Which Version?

You have a few different choices for what version of REBOL to download,
depending on what you need and what is available for your platform.

#### REBOL/Core

> <http://www.rebol.com/prod-core.html>

REBOL/Core covers the vital language features, including all the
[datatypes](/post/2004/12/rebol-datatypes/) which make the language so
attractive to somebody like me. With Core, you can create system shell
scripts, CGI applications, or simple command-line applications. Core
also provides an interactive shell for testing out code on the fly,
which is a valuable asset for getting the hang of a language, or even
just trying out an obscure bit of code on a bored Thursday evening.

Find out if REBOL/Core has been released for your platform at this URL:

> <http://rebol.com/platforms.html>

REBOL/Core will probably do fine for most hobbyists, but you might want
to look on if you enjoy pointy clicky GUI environments as much as I do.

#### REBOL/View

> <http://www.rebol.com/prod-view.html>

View is the cool one, in my opinion. It adds an impressive GUI library
to Core, making it immediately useful for a broad range of applications.
The utility of View can be compared to Java, but here’s something to
really think about regarding the contrast between View and Java. How big
of a download is the JDK these days? 10 Megabytes, 40 Megabytes? The
REBOL/View installer for Windows is 600 Kilobytes. You can fit it on a
*floppy disk*.

What’s a floppy disk? I thought I told you to stop bothering me, kid.

Find out if REBOL/View has been released for your platform at this URL:

> <http://rebol.com/view-platforms.html>

#### REBOL/SDK and REBOL/Command

These are also very easy to get, and add a number of useful features to
REBOL/View. I’ll be ignoring them for now, because they have a dollar
cost associated with them.

Using REBOL
-----------

In Windows, all you need to do is find REBOL in your Start menu. In
Linux, it should be directly callable from your command line if you
handled installation the same way I described.

    $ rebol
    REBOL/Core 2.7.6.4.2 (15-Mar-2008)
    Copyright 2008 REBOL Technologies
    REBOL is a Trademark of REBOL Technologies
    All rights reserved.

    Finger protocol loaded
    Whois protocol loaded
    Daytime protocol loaded
    SMTP protocol loaded
    ESMTP protocol loaded
    POP protocol loaded
    IMAP protocol loaded
    HTTP protocol loaded
    FTP protocol loaded
    NNTP protocol loaded
    >>

So double-click its icon or run it from the command-line. Either way,
now the REBOL shell is running for you. If you’ve installed View, then
you’ve got this pretty Desktop thing. We’ll have to come back to it some
other time. For now, just click the icon on the left for \`\`Console''.
*Now* you’ve got the console. It is not as pretty, but it will work for
our purposes.

You can also go straight to the console when executing `rebview` from
the command line by using the `-v` option:

    $ rebview -v

How to use REBOL/Core
---------------------

Getting REBOL to do something for you is as simple as typing in the
commands and looking at the results.

    >> print "Hello, World!"
    Hello, World!

See? Not that hard at all. Of course, this is pretty standard stuff from
most programming languages these days. Well, except Java. But we all
just sort of snicker whenever a Java coder enters the room. We would
snicker more, but that Java coder is *probably* making twice what we
are. He deserves it, too, for all the carpal tunnel he’s going to get
when he tries to write a \`\`Hello World'' program.

Making the computer tell us things is kind of fun, but it would be nice
to customize it a little bit. Let’s have the computer ask our name. We
can use the `ask` function (or *word*) to ask a question and get a
response, which we will save in a variable.

    >> name: ask "Enter your name: "
    Enter your name:

REBOL uses *words* to remember everything. These words can describe a
number, your name, a chunk of programming logic, or pretty much anything
else you want to track. Here, we have created a word `name`, and used
the function described by `ask` to set `name` to whatever you enter as
your name. What? You still haven’t done that? Go ahead, it’s painless.

    >> name: ask "Enter your name: "
    Enter your name: Brian
    == "Brian"

Type in your name, whether it’s "Brian", "Craig", "Sarah", or "Zuul the
Destroyer". Your name is immediately printed back out onto the console.
But how do we know that REBOL has remembered it? Just `print` the name:

    >> print name
    Brian

That works, and is in the same spirit as the other tutorials on
coolnamehere, but this seems like a great opportunity to take a look at
the `help` word. `help` describes a function that can look up
information about any word that REBOL is currently tracking. Here, try
it for `name`:

    >> help name
    NAME is a string of value: "Brian"

[datatypes]: /post/2004/12/rebol-datatypes/

You can get even more information when the word is pointing to a
function or other complex [datatypes][]. See what happens when you
ask `help` about itself.

    >> help help
    USAGE:
        HELP 'word

    DESCRIPTION:
         Prints information about words and values.
         HELP is a function value.

    ARGUMENTS:
         word -- (Type: any-type)

Remember `help`. It may be just the thing you need when you’re confused
by what a word is supposed to do. As an exercise, go ahead and starting
by asking `help` about `ask` or `print`.

Let’s return to our tutorial, already in progress…

Now that we know REBOL has remembered the name, let’s print it as part
of a sentence. You can tell `print` to print several things at once by
putting them in a block. We do this by wrapping it in square brackets.

    >> print [ "Hello" name "- good to see you!" ]
    Hello Brian - good to see you!

Hey, that made me feel pretty good! As always, it’s great how much we
can be cheered up by just a few nice words, even if we have to write
them ourselves. What if we wanted to share that warm feeling with our
friends and neighbors, or at least the ones who have a copy of REBOL on
their machine?

Let’s find our how to do that.

How to make your own REBOL script
---------------------------------

Using your favorite [editor](/tags/editors/), type this text in and save
it as `hello.r`. I like to keep my code files in a special "projects"
directory, to keep from losing them in a mass of articles, pictures, and
random files. You might want to follow the same habit, but it’s entirely
up to you.

    REBOL [
       Title: "Hello User"
       File: %hello.r
    ]

    name: ask "Please enter your name: "
    print [ "Hello" name "- good to see you!" ]

Make sure that you are using an editor which saves its files as plain
text. REBOL can’t make any sense of Word documents or HTML.

### The Script Header

You recognize the code from before, but I imagine you’re curious about
the block prefaced by the word `REBOL`. That is the *script header*,
where you put important information about the script that you are
writing. You need to put something, even if it’s just an empty block, or
Rebol won’t recognize it as a script.

    REBOL [ ]

Still, the whole point of a script header is to get information about
what the script is, where it came from, and any other details which you
think might be useful to somebody who uses it. An empty block is hardly
useful. This is considered to be more of an acceptable minimal block for
a script you want to share with the world:

    REBOL [
        Title: "Hello User"
        Date: 22-Dec-2004
        File: %hello.r
        Author: "Brian Wisti"
        Version: 1.0.0
    ]

    name: ask "Please enter your name: "
    print ["Hello" name "- good to see you!"]

Of course, you could always provide more information if you want.

    REBOL [
        Title: "Hello User Example Script"
        Date: 24-Feb-2009
        Name: 'Hello-User

        Version: 1.0.2
        File: %hello.r
        Home: http://randomgeekery.org/tags/rebol/

        Author: "Brian Wisti"
        Owner: "Brian Wisti"
        Rights: "Copyright (C) 2017 Brian Wisti"

        Needs: [] ; Needs nothing beyond REBOL/Core
        Tabs: 4

        Purpose: {
            This program is a simple script to demonstrate usage of
            REBOL and warm you up for trying more complex tasks.
        }

        History: {
            1.0.0 [22-Dec-2004 "Wrote the code"]
            1.0.1 [23-Dec-2004 "Finished writing the header for the code"]
            1.0.2 [24-Feb-2009 "Re-examined for site update"]
            1.0.3 [09-Apr-2017 "Adjusted for site relocation"]
        }

        Language: 'English
    ]

    name: ask "Please enter your name: "
    print ["Hello" name "- good to see you!"]

Just try to keep the size of the script header appropriate for the size
of your script. A full script header might be overkill for a script with
only two lines of code - unless you happen to think that people need a
lot of information when handling your script.

### Running your script

There are two ways to actually load your script and make it do its
thing.

-   From the interactive Rebol console
-   From the command line.

Actually, there are a couple more ways to go about it, but these are the
main approaches if you are running a simple Rebol/Core script like the
one we’ve written.

From the interactive console, I use the `do` command to execute the
script `C:\projects\hello.r`:

    >> do %\c\projects\hello.r

The first time you do this, REBOL might ask you for permission to run
the script. Nothing to worry about, it’s just REBOL being conscious
about security. Just say \`\`Yes'', and the script will run through
merrily.

    >> do %hello.r
    Script: "Hello User" (none)
    Please enter your name: Brian
    Hello Brian - good to see you!

If REBOL is in your path, you can call the `rebol` executable with your
script name as an argument.

    $ rebol hello.r
    REBOL/Core 2.7.6.4.2 (15-Mar-2008)
    Copyright 2008 REBOL Technologies
    REBOL is a Trademark of REBOL Technologies
    All rights reserved.

    Finger protocol loaded
    Whois protocol loaded
    Daytime protocol loaded
    SMTP protocol loaded
    ESMTP protocol loaded
    POP protocol loaded
    IMAP protocol loaded
    HTTP protocol loaded
    FTP protocol loaded
    NNTP protocol loaded
    Script: "Hello User" (none)
    Please enter your name: Brian
    Hello Brian - good to see you!

Oof. That’s a whole lot of text before you actually see your program.
Use the `-q` option to make REBOL run your script more quietly.

    $ rebol -q hello.r
    Please enter your name: Brian
    Hello Brian - good to see you!

REBOL also supports the classic \`\`shebang'' line for UNIX shell
scripts.

- Insert a new line at the very beginning, pointing to the `rebol` executable
  - `#!/usr/local/bin/rebol -q`
- Make the script executable
  - `chmod 755 hello.r`
- Run it
  - `./hello.r`

Cool, eh? Now you can share this script with all of your Rebol friends
just by sending them the file. Of course, you might want to send them
something more impressive, but think of it this way - this just gives
you the motivation to learn how to do *more*!

Wrapping Up
-----------

There you have it. You’ve learned how to write a simple script. Heck,
I’ve even snuck in a couple of Rebol’s many [datatypes][] while you
weren’t looking. You’re well on the way to becoming a real Rebol
programmer!

There is a lot of documentation available for REBOL, especially
considering that the REBOL community is fairly small. RT keeps the
official manuals available for free, and there are loads of script
libraries and how-to guides written by the users themselves.

> <http://www.rebol.com/docs.html>

*P.S.:* What, you want me to tell you how to quit REBOL? Why would you
ever want to do that? Oh, okay. The command to quit from the REBOL
Console is easy to remember: `quit`. Happy now?