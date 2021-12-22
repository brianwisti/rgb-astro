---
aliases:
- /coolnamehere/2001/01/17_python-babysteps-tutorial.html
- /post/2001/python-babysteps-tutorial/
- /2001/01/17/python-babysteps-tutorial/
category: coolnamehere
date: 2001-01-17 00:00:00
description: Before the basics
layout: layout:PublishedArticle
slug: python-babysteps-tutorial
tags:
- python
- learn
title: Python Babysteps Tutorial
updated: 2020-02-24
uuid: 19d5a324-dc8a-4224-9f0a-89120a23b01a
---

<aside class="admonition note">
<p class="admonition-title">Note</p>

[better version]: /post/2011/06/python-2.x-babysteps/

This is my original Python Babysteps tutorial, which has existed in more
or less the same form since 2001. I’ve finally committed to writing a [better version][].

</aside>

## Introduction

If you have never programmed before in your life, then do I have the
perfect programming language for you. It’s called Python, and it is easy
to learn, flexible, and loaded with capabilities that you never thought
would be so easy to use. Imagine your thrill when you write a complete
program in just a few lines\!

If you have spent years programming Perl, and are just about sick of all
of the weird little context dependencies — "My function does this when
you hand it a single object, and that when you hand it a list, unless
you are assigning the result to a list, in which case it does this other
thing" — then do I have the perfect language for you. It’s called
Python, it has clear, unambigous syntax, and it is simple to create your
own modules and objects. Imagine your thrill when you write a complete
program in just a few lines, and somebody else can read it\!

This is a tutorial to help the non-programmer learn the basics of using
Python. When you are done with it, you will be ready to learn this new
language, and have no problems figuring out where to find the
information you need to go farther.

Experienced programmers may get some small value out of this, too, but
you will get bored quickly. I am aiming for simplicity, rather than
rigid accuracy. There is always the [official Python
tutorial](https://docs.python.org/tutorial) to provide an introduction
for veterans.

If anybody has any suggestions or comments about this tutorial, please
[send me some mail](mailto:brianwisti@pobox.com) and let me know\!

I hope you enjoy this!

## Installing Python

Before you can *use* Python, you need to *get* Python.

### Which Version of Python?

<aside class="admonition note">
<p class="admonition-title">Note</p>

You can also try Python 3, but this tutorial is just going to discuss
2.6. Why is that? I prefer people use the latest version of Python.
People who are using this tutorial in the context of a classroom
probably aren’t going to have 3.0 as their default yet. There are enough
differences between 2.6 and 3.0 that I’ll probably need a distinct
Python 3 section on coolnamehere.

</aside>

There are a few versions of Python available for download:

1.  ActiveState’s
    [ActivePython](https://www.activestate.com/Products/ActivePython)
2.  The official release of
    [Python 2.6.1](https://www.python.org/download/releases/2.6.1)

Okay, there is also [Jython](http://jython.org) and
[IronPython](http://www.codeplex.com/Wiki/View.aspx?ProjectName=IronPython),
but both of these are for special platforms -
[Java](http://java.sun.com) and [.NET](http://www.microsoft.com/net/),
respectively. As such, they have more specific requirements than I am
interested in covering here. Don’t let that stop *you* from feeling
bold, though!

Which one you install is mostly a personal choice. The language itself
is the same as long as you’re looking at the same version number,
regardless of where you download it from. The main differences are the
type of support you can get, and the tools that they come packaged with.

The ActiveState version has the benefit of being from a real, live
company. You can purchase support and take advantage of the fact that it
comes from a single source. It — the Windows version, anyways — comes
with the excellent PythonWin program for developing your Python programs
in a Windows environment. Because of the support and the
Windows-friendly tools, ActivePython may be the best choice for business
users. It’s the version that I’m using for testing the tutorial in
Linux, so maybe that has some bearing on your decision.

<aside class="admonition note">
<p class="admonition-title">Note</p>

PythonWin is still available to you as part of the
[win32all](http://starship.python.net/crew/mhammond/win32/) package, but
you need to download and install it separately from your Python
distribution. ActiveState Python for Linux includes IDLE, so I will be
getting my Python from them for this article.

</aside>

Python 2.6, on the other hand, is the "official" version. It comes with
a standard set of tools which are available on every platform that
Python can support. Instead of PythonWin, Python 2.6 comes with IDLE: a
cross-platform graphical environment for developing your Python
programs. IDLE works pretty much the same for you whether you are
sitting in front of Windows, Linux, or OS X.

## Installing Python 2.6

Now that you have decided which version of Python you are going to use,
you need to get it and put it on your machine.

### Linux

Your distribution probably has some version of Python available, but I
prefer to get mine from [ActiveState](https://activestate.com). It’s
easy enough to install, and is usually more up-to-date than what ships
with most Linux distributions. There are also fewer concerns about
figuring out whether you installed the `idle` or `pydoc` packages. You
just install ActivePython and get to work.

The latest ActivePython downloads are available from

> <http://downloads.activestate.com/ActivePython/releases/>

Open up a terminal after your download finishes and move to the
directory that is holding the archive. Use `sudo` to run the
`install.sh` script with administrative privileges.

    $ tar xfz ActivePython-2.6.0.0-linux-x86.tar.gz
    $ cd ActivePython-2.6.0
    $ sudo ./install.sh
    press 'Enter' to use the default [/opt/ActivePython-2.6].
    Install directory:
    ()
    Installing ActivePython to '/opt/ActivePython-2.6'...
    Relocating dir-dependent files...
    Pre-compiling .py files in the standard library...

    ActivePython has been successfully installed to:

        /opt/ActivePython-2.6

    You can add the following to your .bashrc (or equivalent)
    to put python on your PATH:

        export PATH=/opt/ActivePython-2.6/bin:$PATH

    The documentation is available here:

        /opt/ActivePython-2.6/doc/python2.6/index.html
        web: http://aspn.activestate.com/ASPN/docs/ActivePython

    Please send us any feedback you might have or log bugs here:

        activepython-feedback@ActiveState.com
        http://bugs.activestate.com/ActivePython/

    Thank you for using ActivePython.

Now we get the required settings into the bashrc file, reload the shell
configuration, and make sure python is where we expect it to be.

    $ echo 'export PATH=/opt/ActivePython-2.6/bin:$PATH' >> ~/.bashrc
    $ . ~/.bashrc
    $ which python
    /opt/ActivePython-2.6/bin/python
    $ which idle
    /opt/ActivePython-2.6/bin/idle

There you go. ActivePython 2.6 has been installed on our Linux machine.

### Windows

Now I am going to describe installation in the Windows environment. It’s
even easier to install Python for Windows (short version: download and
run the installer, click "Next" until done).

You can always find links to download the latest version of Python at
the Python site itself:

> <http://www.python.org/download>

Somewhere around the top of the page is a link to the latest version.
Look for the first version that doesn’t have "alpha", "beta", or
"release candidate" in its name. Follow that link, which is currently:

> <http://python.org/ftp/python/2.6.1/python-2.6.1.msi>

Recently, the kind folks who run the [python.org](https://python.org)
site have started making links to the latest Windows Python download
from their front page. So, even though the stuff I said before is still
true, now you can just look at the menu on the left side of the
python.org front page for "Quick Links \>\> Windows Installer".

Windows will ask you if you want to save the file or run it directly
from the site. That’s up to you. If you have the disk space, and know
how to find and run a file on your hard drive, I recommend you save the
installer program to disk. That way you can redo an installation you
messed up. On the other hand, if you don’t have much space on the
computer — or you aren’t sure how to find a file once you’ve save it,
you are probably better off opening the file straight from the site. I
have screwed up so many installations that I pretty much automatically
select "Save" when downloading an installer.

Once you have downloaded the installer, you need to run it. If you told
Windows that you wanted to open it from the current location, you can
skip this step. Otherwise, you will need to find your file. Open Windows
Explorer ('Start Menu | Programs | Accessories | Windows Explorer'), and
dig through your hard drive until you find the installer executable,
named `Python-2.6.1.msi`. Double-click the icon to run the program, and
you’re on your way to installing Python\!

I’m going to skim through the next bit here. Most of the installation is
simply "Do you want me to install Python in folder X?" and "Do you want
me to call it Python?" Most of the options you can safely run through by
clicking "Next", but stay alert for anything that you might want
different from the defaults.

Eventually, you are presented with a little progress bar while the
installer puts all of the Python files where they belong. This is the
stage where you sip some coffee (or tea, or soda) and dream about all
the great things you will be able to do as a programmer.

Guess what? You are now a proud owner of Python 2.6\! All that’s left is
learning how to program.

## Using Python

There are already a lot of online tutorials for learning Python. Maybe
that’s because Python is as fun to teach as it is to learn. Anyways, I
am not going to try and tell you that *my* rough little article is the
best introduction you’ll ever find.

You can pick and choose from links at the [Python
BeginnersGuide](https://wiki.python.org/moin/BeginnersGuide).

That page has links to articles which discuss Python, tutorials, and
comparisons to other languages. Python was largely written for
educational environments: learning how to do things "the Python way"
makes it easier to write clean, readable programs for any language.
Plus, its flexibility makes it useful way past the classroom — unlike
the stuff like Applesoft BASIC that *I* learned in class. There is
nothing like spending years trying to forget the stuff that BASIC taught
me about programming.

Even though those links will teach you about how to program in Python, I
ask you to stick with me a little bit longer. I still have to tell you
how to get started with the tools that you just installed.

I will be focussing on IDLE — and the simple stuff, at that — but you
can just as easily use PythonWin or the Python shell (which you get into
from the console by typing `python`).

IDLE is Python’s Integrated DeveLopment Environment. It’s just a
coincidence that the acronym *happens* to spell out the last name of one
of the members of a British comedy troupe — whose name just *happens* to
contain the word "Python". That’s right, just a coincidence. *Wink wink,
nudge nudge*

IDLE gives you access to everything you need to write Python code in a
graphical pointy-clicky environment like Windows. There’s a version of
the Python shell, as well as features allowing you to write, save, and
run your own Python programs with ease.

You can find documentation for IDLE at:

> <https://docs.python.org/2/library/idle.html>

It’s a pretty standard and dry user manual, but should hold answers to
any questions you might come up with for the details of using IDLE.

In the next couple of sections, I’ll help you with the basics of using
IDLE. We’ll use the shell for some simple code, and make & run our own
little Python script. That’s right, you’ll be creating your own programs
within the next few minutes\!

## How to use IDLE

Starting IDLE under Windows is a matter of finding it in your Start
menu.

1.  Find the Python folder in your Start menu.
2.  Find the menu item for IDLE within the Python folder.
3.  Select it.

Given the wide, wild range of desktop environments available for Linux,
there is no way I could simply tell you which menu option runs IDLE.
Instead, you get these instructions:

1.  Open a terminal (XTerm, Konsole, Gnome Terminal …​ whatever)
2.  In the terminal, type `idle` and hit ENTER

If you happen to have IDLE in your environment’s equivalent of a Start
menu, then you can just use that.

IDLE will start with something that looks like some sort of command line
interface — kind of like a colorful DOS box or XTerm. That is the shell,
and it allows you to perform the next step:

### Using the IDLE Shell (*Writing Code\!*)

Let’s see, how do we run Python code in the IDLE shell?

1.  Type it in and watch it go\!

Hmm… maybe a *little* more detail would be helpful here.

The IDLE shell allows you to enter code — from simple statements to
function and class definitions — and execute it immediately. Since you
have the shell open already, type in this example:

    >>> print "Hello, world!"

![IDLE screenshot](idle.png)

The `>>>` is the shell prompt, showing that you can type something here.
You may notice that the characters you type show up in different colors
as you enter them into the shell. This is called "syntax highlighting".
It is basically just the environment helping you see more or less how
the code will be broken down by Python — important *keywords* are one
color, *strings* of text are another, and so on.

Press the ENTER key, and the shell will perform that command right away:

    >>> print "Hello, world!"
    Hello, world!
    >>>

The shell allows you to define more complex things, too. Say you want to
get the user’s name, and print a customized "Hello you\!" for the user.

First, you have to get their name:

    >>> name = raw_input("Please enter your name: ")

[raw_input](https://docs.python.org/2/library/functions.html#raw_input)
is a function that displays a prompt to the user, gets some keyboard
input from them, and sends what they typed back to you. I want to use
that typed-in name in a moment, so I save the result in the variable
`name`. A *variable* is basically just something you want the computer
to remember so that you can use it later. What’s a *function*? Don’t
worry about that today. Basically, it’s something you feed data into,
and get data out of — kind of a mini-program in your program. That’s all
we need to know for right now.

When you press ENTER this time, you will be shown a prompt. In IDLE,
this prompt shows up simply as some text printed out in the shell. In
PythonWin it opens a little window showing the message you handed to
`raw_input()` and a space for giving your answer.

Here’s what I see in IDLE:

    >>> name = raw_input("Enter your name: ")
    Enter your name:

I provide my name ("Brian"), and Python quietly saves that answer in the
variable `name`, then waits for me to do something new. One of the
things that confused me when I first tried `raw_input()` in the Python
shell was: how do I know that Python actually grabbed the name I gave?
Well, it turns out that it’s easy enough to ask:

    >>> print name
    Brian

When you want to get at a value that Python has stored for you, all you
have to do is call it by name. In this case, I just wanted to print out
the value of `name` — which was filled in when I typed my name at the
prompt — and that’s exactly what I told Python to do. Pretty simple,
yes?

Okay, so it has my name. What was I trying to do again? Oh yeah, the
custom "Hello" thing. Let’s make it print "Hello, Brian" — or "Craig",
or "Susan", or whatever name you gave to `raw_input()` — ummm — I lost
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
words can lift your mood — even if you have to write them yourself\!

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
is not a shell, but a
[Notepad](https://en.wikipedia.org/wiki/Microsoft_Notepad)-like text
[editor](/tags/editors).

In your new window, enter this code:

``` python
# hello.py
#  Get the user's name and print a friendly hello
name = raw_input("Please enter your name: ")
print "Hello", name, "- good to see you!"
```

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

<aside class="admonition note">
<p class="admonition-title">Note</p>

[Docstrings](https://www.python.org/dev/peps/pep-0257/) would actually
be better for script headers, but:

1.  I haven’t described those yet
2.  I needed an excuse to show you what comments look like.

</aside>

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
# # # # # # # #
```

Just try to match the header complexity to the program. Using this
header for a program that consists of two lines of code might be a
*little* bit of overkill. I usually start with something like the
two-line header and expand it as I see fit.

After you enter your script, you need to save it. That’s easy. Just go
to the "File" menu and select "Save As…​". You will be shown a dialog
that should look pretty familiar if you’ve ever worked with an editing
program. Choose a directory to place your program, enter a name ending
with `.py` — to let your computer know that this is a Python file — and
click "Save". You have now saved your file.

I bet you’re just itching to run that program\! Since you’ve already got
`hello.py` open, all you have to do is go to the "Run" menu, and select
"Run module". Python puts you in the IDLE shell, where you see something
like this:

    Python 2.6 (r26:66714, Nov 11 2008, 12:18:59)
    [GCC 3.3.1 (SuSE Linux)] on linux2
    Type "copyright", "credits" or "license()" for more information.

        ****************************************************************
        Personal firewall software may warn about the connection IDLE
        makes to its subprocess using this computer's internal loopback
        interface.  This connection is not visible on any external
        interface and no data is sent to or received from the Internet.
        ****************************************************************

    IDLE 2.6
    >>> ================================ RESTART ================================
    >>>
    Please enter your name:

Enter your name, press ENTER, and there’s your warm fuzzy greeting\!

You may be happy with `hello.py` right now, but you will probably want
to change it later: make it print out a different greeting, for example.
To do that, you need to know how to open a Python file for editing.

Actually, it’s pretty easy. Go to the "File" menu, select "Open…" and
select your file. IDLE automatically opens your file in an editing
window, where you can edit, save, and run your program to your heart’s
content.

There are two more ways to run a Python program in Windows.

The Python installation automatically associates the `py` extension with
Python program, which tells Windows that anything ending with `.py`
should be handed over to Python. That means you can just double-click on
`hello.py`, and Python will automatically run it. Unfortunately, that’s
not very helpful for most of the stuff we’ll be writing. Try it
yourself. You get a DOS box prompting you for your name, but the box
disappears almost as soon as you press ENTER\! That is kind of annoying.

But there’s another trick which we can use until we’re writing more
complex applications which can keep themselves open or don’t need a DOS
box. Simply open your own DOS box ('Start Menu | Programs | Accessories
| Command Prompt'), move to the directory that contains your script, and
call Python yourself:

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
now! Okay, there’s still plenty more to learn, but you are ready to
start exploring.

### What Next?

This was just the quickest introduction to Python. Hopefully you are
warmed up and ready for more. Now you should start one of the
recommended tutorials at the [Python
BeginnersGuide](https://wiki.python.org/moin/BeginnersGuide).

I have a few favorites of my own.

- The Official Python Tutorial
    - <http://docs.python.org/tutorial/>
    - <http://docs.python.org/py3k/tutorial/index.html>
- Dive Into Python
  <http://www.diveintopython.net/>
- How To Think Like a Computer Scientist In Python
  <http://openbookproject.net/thinkcs/python/english2e/>

### Quick Reference: Using IDLE

| To Do This              | Use This Menu Command                             |
| ----------------------- | ------------------------------------------------- |
| Start IDLE              | Start > Programs > Python 2.6 > IDLE (Python GUI) |
| Edit a New Python File  | File > New Window                                 |
| Save a New Python File  | File > Save As…                                   |
| Open a Python File      | File > Open                                       |
| Save a Python File      | File > Save                                       |
| Run your script in IDLE | Run > Run Module                                  |
| Quit IDLE               | File > Exit                                       |