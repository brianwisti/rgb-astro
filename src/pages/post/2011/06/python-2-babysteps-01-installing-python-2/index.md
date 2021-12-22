---
aliases:
- /coolnamehere/2011/06/16_01-installing-python-2.html
- /post/2011/01-installing-python-2/
- /2011/06/16/python-2-babysteps-01-installing-python-2/
category: coolnamehere
date: 2011-06-16 00:00:00
description: Think of it as Step Zero for the other Python tutorials.
layout: layout:PublishedArticle
slug: python-2-babysteps-01-installing-python-2
tags:
- python
- learn
title: Python 2 Babysteps 01 Installing Python 2
updated: 2011-06-21 00:00:00
uuid: d0a153f2-91e6-45e3-9ff7-cdf08137e0db
---

## Installation

You need to *get* [Python](http://python.org) before you can *use*
Python. There are many versions available, such as
[ActivePython](http://www.activestate.com/activepython),
[Jython](http://jython.org/), and
[IronPython](http://www.codeplex.com/wikipage?ProjectName=IronPython).
They each offer distinct advantages. ActivePython offers commercial
support. Jython runs on the [Java](http://www.java.com/en/) platform,
providing access to the underlying JVM and many support libraries.
IronPython runs on the [.NET](http://www.microsoft.com/NET/) and
[Mono](http://www.mono-project.com/Python) platforms, providing access
to *their* underlying virtual machine and support libraries.

I decided to focus on the official release of Python rather than get
overwhelmed by choice. You can probably follow along if you decide to
install an alternate Python. I will provide notes where I can, but
cannot make any guarantees about their accuracy. Check the documentation
for your Python choice.

### Why Not Python 3?

Python 3 has been available for a while now, and is actually up to
[Python 3.2](http://python.org/download/releases/3.2/). Why don’t I
cover it in this Babystep? I would rather talk about the newest Python
release. but that’s impractical. Many widely used libraries have not
been updated so that they are compatible with the Python 3 series.
Although the differences between Python 2 and Python 3 are small, they
add up for large projects like [Django](http://djangoproject.com). I
want you to be able to use your Python skills right away.

Fortunately, the Python developers continue to support the 2.x line, and
continue to release versions with fixes and new features for Python 2.
If you started learning Python 2 today, it would continue to be useful
for quite some time.

### OS X

You must install the Xcode and Developer Tools to get the full usage out
of Python on OS X, although I will not be spending any time in the XCode
environment. The Developer Tools should have come with your installation
kit. If not, they are available online.

OS X 10.6 includes Python 2.6.1, which is probably good enough for our
purposes. I like having the latest version of a language, though.

#### Just Download It

If you are using a version of OX X older than 10.6, or you don’t care
about 64 bit functionality, just grab the [Mac OS X 32-bit
i386/PPC](http://python.org/ftp/python/2.7.2/python-2.7.2-macosx10.3.dmg)
installer and skip to "Installing Python From the Disk Image".

Python uses [TCL/Tk](http://www.tcl.tk/) for its default graphical
development environment IDLE. These Python Babysteps assume that we will
be using IDLE. Since there are [cautionary
notes](http://www.python.org/download/mac/tcltk/) about using IDLE with
Apple’s default TCL, we will heed those notes and grab our own copy of
[ActiveTcl](http://www.activestate.com/activetcl). We can just grab the
[current ActiveTcl
download](http://www.activestate.com/activetcl/downloads).

Opening the ActiveTCL disk image in the Finder will present us with an
installer called `ActiveTCL-8.5.pkg`. Double-click that package file to
start the installer and accept its defaults.

Right. Now you have ActiveTCL installed. Eject the ActiveTCL disk image
whenever you like.

<aside class="admonition note">
<p class="admonition-title">Note</p>

All of this is unnecessary to play with Python in general. These steps
just make it possible for us to take advantage of the full 64 bit
functionality of OS X, using the latest Python release and IDLE. Feel
free to skip the ActiveTCL download if you do not want to use IDLE.

</aside>

Now that we have the right TCL/Tk installed (or have decided that we
don’t care), go to the download page for
[Python 2.7.2](http://python.org/download/releases/2.7.2/) and grab the
[Mac OS X 64-bit/32-bit
Installer](http://python.org/ftp/python/2.7.2/python-2.7.2-macosx10.6.dmg).

#### Installing Python From the Disk Image

Open the image and double click `Python.mpkg` to run the installation.
The default settings should be good enough.

Well that wasn’t hard. Okay, there were a few details if you insisted on
the latest and greatest.

#### MacPorts

On my home machine, I use [MacPorts](http://macports.org) to access a
large repository of open source software that can be installed on OS X.
Although [installing MacPorts](http://www.macports.org/install.php) is
not difficult, it is well beyond the scope of this tutorial. I will
instead show you the commands I ran from a Terminal to install Python
2.7 on that machine.

    $ sudo port install python-2.7
    $ sudo port select python python-2.7
    $ python -V
    Python 2.7.1

That will do. The differences between 2.7.1 and 2.7.2 are so small that
I doubt I will notice any of them.

#### Homebrew

And some of you use [Homebrew](http://mxcl.github.com/homebrew/) to
install open source software. No problem. Here are the instructions for
installing and verifying a fresh Python once you [install
Homebrew](https://github.com/mxcl/homebrew/wiki/Installation).

    $ brew install python
    $ python -V
    Python 2.7.2

### Linux

Python is well supported in Linux.

#### Redhat-based distributions (Fedora)

[Fedora](http://fedoraproject.org) 15 ships with Python 2.7.1, and that
is good enough for me. We need to install the `python-tools` package if
we want IDLE, though.

    $ su -
    # yum install python-tools

#### Debian-based Distributions (Ubuntu, Mint)

[Ubuntu](http://ubuntu.com) 11.04 has Python 2.7.1 installed by default,
and that’s good enough for us.

    $ python -V
    Python 2.7.1+

I am not sure what the `+` means. I assume the Ubuntu developers made
some customizations to Python.

IDLE is not installed by default, though. That can be fixed.

    $ sudo apt-get install idle

#### Others

Check the documentation for your distribution. The odds are that you
already have Python installed, or can easily install it using your
distribution’s tools.

### Windows

I do not have a Windows installation handy right now, so most of this
section is just going from memory. Thank goodness installation on
Windows is easy.

You can always find links to download the latest version of Python at
the Python site itself:

> <http://www.python.org/download>

Somewhere around the top of the page is a link to the latest version.
Look for the first version that doesn’t have "alpha", "beta", or
"release candidate" in its name. Follow that link, which is currently:

- <http://python.org/ftp/python/2.7.1/python-2.7.1.msi> for 32-bit
  Windows, and
- <http://www.python.org/ftp/python/2.7.1/python-2.7.1.amd64.msi> for
  64-bit Windows installations

The kind folks who run the python.org site make sure there are links to
the latest Windows Python 32 bit download from their [front
page](http://python.org). Look on the left side of the page for *"Quick
Links >> Windows Installer"*.

Windows will ask you if you want to save the file or run it directly
from the site. That’s up to you. If you have the disk space, and know
how to find and run a file on your hard drive, I recommend you save the
installer program to disk. That way you can redo an installation you
messed up. On the other hand, if you don’t have much space on the
computer, or you aren’t sure how to find a file once you’ve save it, you
are probably better off opening the file straight from the site. I have
screwed up so many installations that I pretty much automatically select
"Save" when downloading an installer.

Once you have downloaded the installer, you need to run it. If you told
Windows that you wanted to open it from the current location, you can
skip this step. Otherwise, you will need to find your file. You will
probably find it in "Downloads", within the "My Documents" section of
the computer. Dig or search in your hard drive until you find the
installer executable, named `Python-2.7.1.msi`. Double-click the icon to
run the program, and you are on your way to installing Python\!

I’m going to skim through the next bit here, because most of the
installation is simply "Do you want me to install Python in folder X?"
and "Do you want me to call it Python?" Most of the options you can
safely run through by clicking "Next", but stay alert for anything that
you might want different from the defaults.

Eventually, you are presented with a little progress bar while the
installer puts all of the Python files where they belong. This is the
stage where you sip some coffee (or tea, or soda) and dream about all
the great things you will be able to do as a programmer.

Guess what? You are now a proud owner of Python 2\! All that’s left is
learning how to program.

### Building From Source

And if you are feeling bold, you can grab the [source
distribution](http://python.org/ftp/python/2.7.2/Python-2.7.2.tar.bz2)
and build your own copy. It is not difficult, but will require
installing different tools on different machines. Go right ahead and do
this if you want to. The instructions within the source distribution are
clear enough. I am not going to build my own copy. I have installed
Python four times today, and frankly that is enough.

It is time to get acquainted with this new language.

## Using Python

There are already a lot of online tutorials for learning Python. Maybe
that’s because Python is as fun to teach as it is to learn. Anyways, I
am not going to try and tell you that *my* rough little Web site has the
best introduction you’ll ever find.

You can pick and choose from links at the Python [BeginnersGuide wiki
page](http://wiki.python.org/moin/BeginnersGuide).

That page has links to articles which discuss Python, tutorials, and
comparisons to other languages. Python was largely written for
educational environments: learning how to do things "the Python way"
makes it easier to write clean, readable programs for any language.
Plus, its flexibility makes it useful way past the classroom — unlike
the stuff like Applesoft BASIC that *I* learned in class. There is
nothing like spending years trying to forget what BASIC taught me about
programming.

Even though those links will teach you about how to program in Python, I
ask you to stick with me a little bit longer. I still have to tell you
how to get started with the tools that you just installed.

I will be focussing on IDLE — and the simple stuff — at that. You can
just as easily use PythonWin or the Python shell, which you get into
from the console by typing python.

IDLE is Python’s Integrated DeveLopment E\>nvironment. It’s just a
coincidence that the acronym *happens* to spell out the last name of one
of the members of a British comedy troupe — whose name just *happens* to
contain the word "Python". That’s right, just a coincidence. *Wink wink,
nudge nudge*

IDLE gives you access to everything you need to write Python code in a
graphical pointy-clicky environment like Windows. There’s a version of
the Python shell, as well as features allowing you to write, save, and
run your own Python programs with ease.

You can find some information about IDLE at its [documentation
page](http://docs.python.org/library/idle.html).

In the next couple of sections, I will help you with the basics of using
IDLE. We’ll use the shell for some simple code, then make and run our
own little Python script. That’s right, you’ll be creating your own
programs within the next few minutes.

## How to use IDLE

Starting IDLE under Windows is a matter of finding it in your Start
menu.

1.  Find the Python folder in your Start menu.
2.  Find the menu item for IDLE within the Python folder.
3.  Select it.

On Windows Vista and Windows 7, you can launch IDLE by entering "idle"
in the Start Menu search field and selecting the program when it appears
in search results.

Given the wide, wild range of desktop environments available for Linux,
there is no way I could simply tell you which menu option runs IDLE.
Instead, you get these instructions:

1.  Open a terminal (XTerm, Konsole, Gnome Terminal … whatever)
2.  In the terminal, type `idle[ENTER]`

If you happen to have IDLE in your environment’s equivalent of a Start
menu, then you can just use that. It’s in the "Programming" group on
Ubuntu.

IDLE will start with something that looks like some sort of command line
interface (kind of like a colorful DOS box or XTerm). That is the shell,
and it allows you to perform the next step:

### Using the IDLE Shell (*Writing Code\!*)

Let’s see, how do we run Python code in the IDLE shell?

1.  Type it in and watch it go\!

Hmm… maybe a *little* more detail would be helpful here.

The IDLE shell allows you to enter code (from simple statements to
function and class definitions), and execute it immediately. Since you
have the shell open already, type in this example:

    >>> print "Hello, world!"

![IDLE screenshot](idle.png)

The `>>>` is the shell prompt, showing that you can type something here.
You may notice that the characters you type show up in different colors
as you enter them into the shell. This is called "syntax highlighting."
It’s basically just the environment helping you out so that you know
more or less how the code will be broken down by Python (important
*keywords* are one color, *strings* of text are another, etcetera).

Press the ENTER key, and the shell will perform that command right away:

    >>> print "Hello, world!"
    Hello, world!

The shell allows you to define more complex things, too. Say you want to
get the user’s name, and print a customized "Hello you\!" for the user.

First, you have to get their name:

    >>> name = raw_input("Please enter your name: ")

`raw_input()` is a function that displays a prompt to the user, gets
some keyboard input from them, and sends what they typed back to you. I
want to use that typed-in name in a moment, so I save the result in the
variable `name`. A *variable* is basically just something you want the
computer to remember so that you can use it later. What’s a *function*?
Basically, it’s something you feed data into, and get data out of — kind
of a mini-program in your program. That’s all we need to know for right
now.

When you press `[ENTER]` this time, you will be shown a prompt. In IDLE,
this prompt shows up simply as some text printed out in the shell.

    >>> name = raw_input("Enter your name: ")
    Enter your name:

I provide my name ("Brian"), and Python quietly saves that answer in the
variable `name`, then waits for me to do something new. One of the
things that confused me when I first tried `raw_input()` in the Python
shell: how do I know that Python actually grabbed the name I gave? Well,
it turns out that it’s easy enough to ask:

    >>> print name
    Brian

When you want to get at a value that Python has stored for you, all you
have to do is call it by name. In this case, I just wanted to print out
the value of `name` — which was filled in when I typed my name at the
prompt — and that’s exactly what I told Python to do. Pretty simple,
yes?

Okay, so it has my name. What was I trying to do again? Oh yeah, the
custom "Hello" thing. Let’s make it print "Hello, Brian" - or "Craig",
or "Susan", or whatever name you gave to `raw_input()` …​ ummm …​ I lost
myself again. Let me get back on track here.

Wait. How are we supposed to do this? You know, take a value, and write
it along with some other text?

Here’s the easiest way:

    >>> print "Hello", name
    Hello Brian

Every time you normally tell Python to print something, it will print
that something out, and then start a new line. If you paste a comma onto
the end of the thing you want to print, it’s just like a comma in
conversation. It means that you’re pausing for air, and the sentence
isn’t done yet. Instead of starting a new line, Python just inserts a
space. The next thing that gets printed will show up on the same line.

In this case, Python prints the phrase "Hello", followed by a space, and
ending with the name that was given to it by `raw_input`.

You can print several things at once, too. Just put a comma in between
each item to be printed.

    >>> print "Hello", name, "- good to see you!"
    Hello Brian - good to see you!

Wow. That made me feel pretty good. It’s amazing how just a few nice
words can lift your mood — even if you have to write them yourself.

What if we wanted to be able to get that warm fuzzy feeling any time?
It’s only two lines of code. We could probably enter that in the shell
when we wanted some warm words. But there’s a school of programming that
tells us Laziness is a virtue. Why write the same two lines again and
again, when we could write them once, call it a program, and run that
program anytime we felt blue?

Let’s find out how to do just that.

## How to Make Your Own Python Program

Even though the IDLE shell is pretty neat, and *very* useful for
figuring out whether a code idea will work, it’s not any good for actual
programs.

Don’t get all huffy. I said the IDLE *shell* wasn’t good for programs,
not that *IDLE* is no good for programs.

To edit a Python script in IDLE, simply go to the "File" menu and select
"New Window". This will open a new window for editing Python stuff. This
is not a shell, but a NotePad-like text editing environment.

In your new window, enter this code:

    # hello.py
    #  Get the user's name and print a friendly hello
    name = raw_input("Please enter your name: ")
    print "Hello", name, "- good to see you!"

Most of it is the same as what we entered in the shell, but what’s with
those first couple of lines?

Well, they’re Python comments. Comments start from the character `#`,
and extend to the end of the line that you wrote them on. Python ignores
comments, which means that you can use them to explain what is going on
in your code. Comments are good. When you come back to look at a complex
script after several months, you might forget what some block of code
does. Having the comments there to remind you will make it that much
easier to sort everything out.

I like to start every one of my scripts off with a quick header to
describe the purpose of the program. Here is the rough template:

Python docstrings would actually be better for script headers, but:

1.  I haven’t described those yet
2.  I needed an excuse to show you what comments look like.

``` python
# filename
#  A quick description of what this program does
```

Of course, your header can be as complicated as you like:

``` python
# # # # # # # #
# hello.py
#  Get the user's name and print a friendly hello
#
# AUTHOR
#  Brian Wisti (brianwisti@pobox.com)
# DATE
#  26 December 2008
# VERSION
#  1.1
# PURPOSE
#  Demonstration script for my python tutorial at
#  http://www.coolnamehere.com/geekery/python/pythontut.html
# USAGE
#  python hello.py
# LICENSE
#  You may copy and redistribute this program as you see fit, with no
#  restrictions.
# WARRANTY
#  This program comes with NO warranty, real or implied.
# HISTORY
#  1.0 19 January 2001
#    Initial release for Python Babysteps Tutorial
#  1.1 26 December 2008
#    Updated for Python version 2.6
#  1.2 16 June 2011
#    Updated for Python version 2.7.2
# # # # # # # #
```

Just try to match the header complexity to the program. Using this
header for a program that consists of two lines of code might be a
*little* bit of overkill. I usually start with something like the
two-line header and expand it as I see fit.

After you enter your script, you need to save it. That’s easy. Just go
to the "File" menu and select "Save As…​" You will be shown a dialog
that should look pretty familiar if you’ve ever worked with an editing
program. Choose a directory to place your program, enter a name ending
with `.py` to let your computer know that this is a Python file, and
click "Save". You have now saved your file.

I bet you’re just itching to run that program\! Since you’ve already got
`hello.py` open, all you have to do is go to the "Run" menu, and select
"Run module". Python puts you in the IDLE shell, where you see something
like this:

    Python 2.7.1 (r271:86832, Nov 27 2010, 18:30:46) [MSC v.1500 32 bit (Intel)] on win32
    Type "copyright", "credits" or "license()" for more information.
    >>> ================================ RESTART ================================
    >>>
    Please enter your name:

Enter your name, press ENTER, and there’s your warm fuzzy greeting\!

You may be happy with `hello.py` right now, but you will probably want
to change it later: make it print out a different greeting, for example.
To do that, you need to know how to open a Python file for editing.

Actually, it’s pretty easy. Go to the "File" menu, select "Open…​" and
select your file. IDLE automatically opens your file in an editing
window, where you can edit, save, and run your program to your heart’s
content.

There are two more ways to run a Python program in Windows.

The Python installation automatically associates the `py` extension with
Python program. That tells Windows that anything ending with `.py`
should be handed over to Python. That means you can just double-click on
hello.py, and Python will automatically run it. Unfortunately, that’s
not very helpful for most of the stuff we’ll be writing. Try it
yourself. You get a DOS box prompting you for your name, but the box
disappears almost as soon as you press ENTER\! That is kind of annoying.

But there’s another trick which we can use until we’re writing more
complex applications which can keep themselves open or don’t need a DOS
box. Simply open your own DOS box ('Start MenuAccessories|Command
Prompt'), move to the directory that contains your script, and call
Python yourself:

    C:>cd scripts
    C:\scripts>python hello.py
    Please enter your name: Brian
    Hello Brian - good to see you!
    C:\scripts>

In order for this to work, you’ll have to have your Python installation
directory specified as part of your environment variable `PATH`. How you
do that depends on what version of Windows (or which command line shell
for Linux) you are running. Once again, I’m lazy, so I’m leaving it
alone.

To be honest, I recommend you stick with IDLE interface for now. There
is less to remember.

Finally, you might want to know how to *leave* IDLE. The menu command
'File|Exit' is all you need to remember. If you haven’t saved all of the
files you have been editing, IDLE will check if you want to save them
before you quit. Answer as you see fit, save any files you want, and
you’re out of IDLE in the real world.

And you know what? You know how to use the IDLE shell, as well as how to
edit, save, and run your very own Python scripts. You’re a programmer
now\! Okay, there’s still plenty more to learn, but you are ready to
start exploring.

## What Next?

This was just the quickest introduction to Python. Hopefully you are
warmed up and ready for more. Now you should start one of the
recommended tutorials at the [Python
BeginnersGuide](http://wiki.python.org/moin/BeginnersGuide).

I have a few favorites of my own.

- The Official Python Tutorial
  <http://docs.python.org/tutorial/>
- Dive Into Python
    - <http://www.diveintopython.net/>
    - <http://www.diveintopython3.net/>
- How To Think Like a Computer Scientist In Python
  <http://openbookproject.net/thinkcs/python/english2e/>

### Quick Reference: Using IDLE

| To Do This…             | Use This Menu Command                         |
| ----------------------- | --------------------------------------------- |
| Start IDLE              | "Start/Programs/Python 2.7/IDLE (Python GUI)" |
| Edit a New Python File  | "File/New Window"                             |
| Save a New Python File  | "File/Save As…"                               |
| Open a Python File      | "File/Open"                                   |
| Save a Python File      | "File/Save"                                   |
| Run your script in IDLE | "Run/Run Module"                              |
| Quit IDLE               | "File/Exit"                                   |