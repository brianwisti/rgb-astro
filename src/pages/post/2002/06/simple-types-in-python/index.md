---
aliases:
- /coolnamehere/2002/06/12_simple-types-in-python.html
- /post/2002/simple-types-in-python/
- /2002/06/12/simple-types-in-python/
category: coolnamehere
date: 2002-06-12 00:00:00
description: In which I attempt to explain value types
layout: layout:PublishedArticle
slug: simple-types-in-python
tags:
- python
- learn
title: Simple Types in Python
updated: 2009-07-11 00:00:00
uuid: e04cf200-d823-4422-b047-b76e2c4ba51d
---

Ok, it’s been over a year since the first step of my [Python Babysteps
Tutorial](/post/2001/01/python-babysteps-tutorial/). It’s about time to
dig a little deeper.

In this step, we will take our first look at variables and types in the
Python language. We will use variables for storing and retrieving
information. We will also tiptoe into the wild and woolly world of
types, which computer languages rely on for tasks such as telling the
difference between numbers and words.

You’re not expected to be some kind of expert to work through this
tutorial. I only expect you to know how to use your development
environment (such as IDLE) to work within the Python shell and create
your own Python scripts. If this sounds unfamiliar to you, you’re in
luck — I happen to cover exactly that in the Babysteps tutorial.

<aside class="admonition">

I am aiming for simplicity over rigid accuracy with this tutorial, but
it sure would be appreciated if you happen to notice any unforgivable
Python or general computer science errors within these pages. Being
self-taught results in some really odd holes in my programming
knowledge. So please, send me a quick note to sweetly and patiently
point out any errors you find. Thanks!

</aside>

For the rest of us non-experts, let’s take the first steps into real,
live programming!

## Variables

Your program needs something to work with. You need names and addresses
for your mailing list program, you need debits and credits for your
accounting program, and you need weapons and critters for your
fast-paced arcade game.

How are we supposed to do that? Well, that’s where *variables* come in.
What’s a variable? In my attempts to uncover the secrets of computer
science, I found something describing them as:

> named locations in memory used to store a value.

Ummm … that’s all fine and good, but if you’ve got a small brain like
me, you’ll spend too much time trying to remember what those words
**mean** to actually use them in a program. We need a simpler definition
that we can rattle off in casual conversation. How about this?

> A *variable* is something you want your program to remember.

It’s to the point and uses words in a way I can understand. I like that.
It also kinda describes the situation in Python, where nearly anything
can be used as a variable. Numbers, text, code, files, objects, other
programs… the list is longer than we care to imagine this early in our
studies.

To create a variable, make a name and assign a value to it using the
equals `=` character. To get the value, use the variable name in a
statement.

    >>> number = 5
    >>> print number
    5

You can change the value of a variable any time by using `=`.

    >>> print number
    5
    >>> number = 7
    >>> print number
    7

### Identifiers aka Variable Names

Python gives us a lot of freedom in creating variable names, also known
as *identifiers*. As long as they start with a letter or underscore
(`_`), and are followed by letters, numbers, or underscores, you’re
generally good to go. Case is important, so `number`, `NUMBER`, and
`Number` are three different names. The biggest restriction is that you
can’t use an identifier that is already used by Python. This means no
variables named `print`, for example.

Here is the complete list of identifiers that Python has reserved for
its own purposes::

    and       del       for       is        raise
    assert    elif      from      lambda    return
    break     else      global    not       try
    class     except    if        or        while
    continue  exec      import    pass      yield
    def       finally   in        print

Here are a few guidelines to follow when deciding on a variable name:

- Identifiers starting with `_` are treated differently by Python, so
  avoid them until you know what they’re for.
- Use descriptive names rather than abbreviations or inside jokes.
  When you are naming a variable that holds the radius of a circle, it
  is usually better to use `radius` than `r` or `halfway_there`
- Use a name that indicates what the variable will be used for.
  `radius` is much better than `fnord` for describing the radius of a
  circle. Plus, "fnord" breaks the "no inside jokes" guideline.
- Find a balance between names that are too long or too short.
    - *Too short* would be `n`
    - *Too long* might be
      `name_of_my_favorite_customer_in_walla_walla_washington`
    - *Just right* might be `name` or `customer_name`
- It is common practice to use all upper case letters for identifiers
  that describe constants — variables which will not be changing their
  values. Since pi will always have the value 3.1415926 — or so — you
  would use an identifier of `PI` for this variable.
- It’s okay to bend the guidelines in favor of common terms. If you
  are writing code to figure out the distance between two points, then
  `x1`, `y1`, `x2`, and `y2` are perfectly sensible identifiers.

There are two popular approaches to devising longer names (the ones that
consist of two or more words pasted together). In the first, the two
words are separated by underscores where the spaces would be. In this
tradition, "customer name" would be written as `customer_name`. The
other school uses capitalization to show separation, and would write the
same "customer name" as `CustomerName`, or maybe `customerName`.

I use underscores in my own code. I don’t really care which one you use,
but stay consistent. Try not to follow `customer_name` with
`CustomerAddress`. And whatever you do, *please* don’t mix the two in
the same variable. Identifiers like `Customer_Name` will only serve to
aggravate me and hasten the approach of carpal tunnel syndrome for you.
I am so emphatic about this silly little issue because I am saying this
as somebody who has to read code written by other people.

The sad truth is that you are going to encounter plenty of otherwise
great code that is downright mean about variable names. It’s just
something we have to live with.

### Literals aka Plain Old Values

Let’s throw in another fancy technical term, since it’ll help us
understand types in the next section. *Literal* is a fancy name for a
plain old value. In the statement `number = 5`, `5` is the literal. Most
often, you’ll see literals being used in assigning a value to your
variables. There are different ways to write literals, depending on what
type of variable you are assigning to.

## Types

I’ve used the word "type" a few times already, but haven’t explained
what a type is. That’s because I’ve been stalling. It’s a broad concept
and the best definition I could think of is circular:

> *Type* describes the type of variable you are using.

See what I mean? Let’s try a different approach.

You and I know that there’s a difference between numbers and words.
Imagine the following exchange between you and a random stranger who
we’ll call "Bob":

Bob
: Hi there\! What’s your name?

You
: Uhh … Brian

Bob
: What’s your name plus 5?

You
: Oh look, there’s my bus\!

Right away, you realized that Bob is a raving lunatic — or maybe a Zen
master — because `"Brian" + 5` just doesn’t work. You’re not supposed to
combine words and numbers like that. It isn’t polite.

*Types* are used by programming languages to recognize when programmers
are starting to sound like a raving lunatic. Every type has rules for
what you can do with them. You can do numbery things to numbers (add,
subtract, find the square root of, etcetera). You can do stringy things
to strings of text (search, capitalize, concatenate, and so on).
Capitalizing numbers is a no-no, as is finding the square root of your
name. When you learn how to create your own types later on, you will
also be writing the rules for how your new types can be used.

An *exception* is a special type in Python that we’ll be seeing a lot of
as we learn. Think back to that conversation with Bob. As soon as he
asked you to add `5` to your name, a little red flag went up in your
brain. This red flag told you that something was very wrong with dear
old Bob. *Exceptions* are the little red flags that Python uses to tell
you that something is very wrong. There are a lot of ways that things
can go wrong, so there are a lot of different types of exception that we
will see. Let’s see what Python does when we play the role of Bob.

    >>> name = "Brian"
    >>> print name + 5
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    TypeError: cannot concatenate 'str' and 'int' objects

All of the "File" gibberish is called a *traceback*, showing where
things went wrong. Yours will probably look a little different, but the
idea is the same.

The last line is the exception itself. It tells us what kind of problem
was found — `exceptions.TypeError` — and describes the specific issue —
`cannot concatenate 'str' and 'int' objects`.

We won’t really understand what to do with an exception for a while, but
the basic idea is clear. Python uses exceptions to warn us that we are
heading towards the path of madness.

### Numbers

Nothing illustrates the idea of types as clearly as the number. Most of
us know what a number is, and can understand the sorts of things we do
with numbers: add them, subtract them, ignore them when they’re written
on a bill, and so on. We know how to compare numbers to determine which
is greater. Things get a little murky when we start talking about the
String type or the HttpServer type, but we know what numbers are. Lucky
for us, so does Python.

To make things easier "under the hood", Python has four different
categories of numbers:

integers
: Whole numbers, like `1`, `2`, and `186212`.

long integers
: *Really big* integers, like `6209389143`

floating point numbers
: Decimal numbers, like `1.0`, `2.2`, or `3.1415926`

imaginary numbers
: I can’t imagine what these would be. A little more seriously, these
  are the complex numbers that higher-math types play with all the
  time. Something to do with the square root of `-1`, I think.

Amazingly enough, Python takes care of telling one from the other, and
we don’t need to worry about it most of the time. Just feed it a
literal, and it’ll try to do the right thing. Each of these types do
have their own rules, though, and these rules will bite us if we try to
treat Python numbers exactly the same as the numbers in our checkbook.

### Numeric Literals: How To Describe Numbers

    >>> 1
    1
    >>> 35
    35
    >>> 34456432
    34456432
    >>> 355556499871154247854
    355556499871154247854L

What? Where did that `L` come from? It turns out that computers are
faster at dealing with integers if they can fit them into a small chunk
of memory. That "small chunk" is still more than enough room for most of
the numbers that you’ll deal with in your day-to-day programming. Until
you start converting parsecs to inches, `2,147,483,647` should be more
than enough room.

When you hand it a really large literal like `355556499871154247854`,
Python notices right away that it won’t fit as a regular integer, and
automatically makes it a long integer. There are times when you know in
advance that your number will end up being very large. Specifying long
integer type is very very easy. Just paste the letter `L` to the end of
your literal.

    >>> 6209389143L
    6209389143L

While it is technically okay to use a lowercase `l`, it is *much* harder
to read when scanning program code. `6209389143l` looks too much like
`62093891431`. It’s a good idea to always use the upper case `L` for
specifiying long integers.

The next type of number is floating point. You can either write floating
point literals in the familiar decimal notation, or you can use
something more like scientific notation.

    >>> 1.0
    1.0
    >>> 1.234e+02
    123.40000000000001
    >>> 1.1
    1.1000000000000001

This is where things start to bite us if we’re not paying attention.
`1.0` made sense, but what in the world went wrong with our other two
numbers?

It’s like this, see. Computers are basically made up of switches. On and
off. `1` and `0`. That’s all a computer knows. It takes many layers of
programming to translate your value into something that a computer can
understand, and then more layers to turn it back into something you can
understand. With integers, it’s relatively easy. It’s a simple matter
for the computer to handle whole numbers. Floating point, however, is
much more fluid. It takes a lot of work for the computer to translate a
floating point value into a series of `1` and `0` switches. To save time
and memory, it fudges the number a little bit. For most programs, it’s
not a problem. It certainly hasn’t been an issue for me in *any* program
I’ve written. There are also some excellent programming libraries out
there when you do hit that particular wall. Everyday python does an
excellent job of protecting us from all the chaos when printing a
variable:

    >>> value = 1.1
    >>> print value
    1.1

Internally, it’s still `1.1000000000000001` or so, but Python realizes
that human readers are not going to be interested in the extra 14
zeroes.

Now, before you go storming off to Perl or C, you should learn the dark
secret: this is not limited to Python. It’s something to do with
computers in general, so this will come up no matter what language you
use. The classier ones like Python just hide it from you when they can.

Our last kind of number is the imaginary number. My own math skills
haven’t progressed far enough to present anything truly useful, but I
know how to write an imaginary literal.

I think I just melted my brain by putting those two words together.

An imaginary … uh … literal … thing … consists of a floating point
number (the *real* part), a `+` character, and another floating point
number followed by a `J` (the *imaginary* part). Here, just look at my
example, and you math people can figure it out yourself.

    >>> number = 1.1 + 9.87J
    >>> print number
    (1.1+9.87j)

I guess imaginary numbers don’t make it into everyday math that much,
but they do show up in my checkbook a lot. Wrong kind of "imaginary", I
guess.

Now that I’ve made a complete fool of myself, let’s move along quickly
to look at some things we can do to numbers.

### Numeric Operations: Some Things You Can Do With Numbers

The Python shell does make a handy calculator. You can do all of the
handy four-function operations, plus we get a nifty *exponent* operator
and *modulus* operator at no extra charge.

    >>> print 2 + 2
    4
    >>> print 10 - 2
    8
    >>> print 11 * 3
    33
    >>> print 27 / 3
    9
    >>> print 2 ** 3
    8
    >>> print 20 / 3
    6
    >>> print 20 % 3
    2

<aside class="admonition note">
<p class="admonition-title">Note</p>

Right about here I got distracted by a bright shiny object. Sorry about
that!

</aside>