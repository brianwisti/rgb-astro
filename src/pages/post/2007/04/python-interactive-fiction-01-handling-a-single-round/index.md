---
aliases:
- /coolnamehere/2007/04/19_01-handling-a-single-round.html
- /post/2007/01-handling-a-single-round/
- /2007/04/19/python-interactive-fiction-01-handling-a-single-round/
category: coolnamehere
date: 2007-04-19 00:00:00
layout: layout:PublishedArticle
series:
- Python Interactive Fiction
slug: python-interactive-fiction-01-handling-a-single-round
tags:
- python
- ifiction
- learn
title: Python Interactive Fiction - 01 Handling a Single Round
updated: 2009-07-11 00:00:00
uuid: 7218a5a7-3d1e-47f8-b959-1e1c9fc12b32
---

I think the next step is to write the code for a single round of the game. We'll 
limit ourselves to Scene 1 to stay focussed.
<!--more-->

### Presenting a Scene to the user

[editor]: /tags/editors/
First you want to show the description. Start a new Python file in your favorite
[editor][], or in IDLE with the menu command "File" -> "New".

``` python
# ifiction.py
#  - An interactive fiction game

description = "You are standing in a field. To the north of you are some mountains, " \
              "to the east of you is a forest, to the west of you is a cave, and to " \
              "the south of you is a valley."

print description
```

The `\` character at the end of lines 6 and 7 tells Python the string is continuing to the next line. 
Python would complain at us if we left that out. Let's run the script and see what we get.

Save your new file as `ifiction.py` and run it. Press the `F5` key to run the script if you are using IDLE.

    $ python ifiction.py

    You are standing in a field. To the north of you are some mountains, to the ea
    st of you is a forest, to the west of you is a cave, and to the south of you i
    s a valley.

This may not be happening for you, but when I run the script the description text
gets cut off at inconvenient points. What happens next is a little more advanced
than I was planning to show you, but that is just going to bug me too much if I 
don't fix it now.

#### Wrapping text with the `textwrap` module

One of Python's charms is the fact that it has a 
[huge standard library](http://docs.python.org/lib/ "Python Standard Library Reference"). This means
that a lot of things you would like to do have already been written and included 
for free. That's why some folks say that Python comes with "batteries included."
The standard library is a collection of modules with useful features and functions. I
am just concerned with the `fill` function from the
[textwrap](https://docs.python.org/2/library/textwrap.html)
module right now, because I want the text of the description wrapped so that no words
get cut off.

You aren't automatically carrying all of those libraries around in your script, though.
You need to use the `import` command to make the functions in a library available to
your program.

``` python
# ifiction.py
#  - An interactive fiction game

import textwrap

description = "You are standing in a field. To the north of you are some mountains, " \
              "to the east of you is a forest, to the west of you is a cave, and to " \
              "the south of you is a valley."

print textwrap.fill(description)
```

Notice that I had to use the module name as part of my call to `fill`. That is because 
Python needs to know where it can find the `fill` function, and for library functions 
it uses *modulename* followed by a dot (.) and then the function. You will be seeing 
a lot more of the dot operator as your Python knowledge expands. 

There are ways to import the function in a way which removes that requirement, 
but for now I will stick with the more explicit version because it is easier for 
*us* to know where we found the function.

See what it looks like now?

    $ python ifiction.py
    You are standing in a field. To the north of you are some mountains,
    to the east of you is a forest, to the west of you is a cave, and to
    the south of you is a valley.

Of course, if the wrapping text isn't an issue for you, feel free to leave out the
`textwrap` related code completely.

### Back to the game: paths

Now for the paths. We could just print the paths and make the user type in the full 
path to go anywhere, but that would be unkind. What we want is an easy way to show
the list of paths and say "You picked path #1: Go to the mountains".

Python's
[list](https://docs.python.org/2/library/stdtypes.html#sequence-types-str-unicode-list-tuple-bytearray-buffer-xrange) type
is the perfect way to do this. A Python list is a collection of values - they could 
be literals or other variables - that holds each value in order. This lets you ask 
for the third item in a list, or ask for each value in order. Let's start by creating
and displaying the paths.

``` python
# ifiction.py
#  - An interactive fiction game

import textwrap

description = "You are standing in a field. To the north of you are some mountains, " \
              "to the east of you is a forest, to the west of you is a cave, and to " \
              "the south of you is a valley."

print textwrap.fill(description)

# The list of choices available to the user.
paths = [
    "Go to the mountains",
    "Go into the forest",
    "Go into the cave",
    "Go to the valley"
]

for path in paths:
    print path
```

What does it look like now?

    $ python ifiction.py
    You are standing in a field. To the north of you are some mountains,
    to the east of you is a forest, to the west of you is a cave, and to
    the south of you is a valley.
    Go to the mountains
    Go into the forest
    Go into the cave
    Go to the valley

I want to do a bit of formatting to break things up, but you get the idea of what
is going on. We have created a variable called `paths` to hold our list of paths.
What can I say? I like my variable names to be obvious. You can recognize a list 
by the square brackets `[]`. Items in the list are separated by commas. I like to
put each list item on a line by itself, using indentation to show that we are looking
inside the list. Little things like this make your code easier to read, which gets
very important as your program grows.

#### The `for` loop

Okay, I need to take the next few ideas slowly, because I have put a lot of important
new concepts in two lines of code.

[control structures]: /post/2004/07/control-structures/

`for` is one of Python's looping [control structures][]. `for path in paths:` 
is going step to through each item in the list `paths`. That part is straightforward.  
Another nice thing about Python code is that you can usually tell what's going on just by looking at it. 

It also creates a variable called `path` which will hold the value of the current item in the list.
The first time through the list, `path` is set to *"Go to the mountains"*, the second time through
`path` is set to *"Go into the forest"*, and so on.

What is Python going to do with `path`? That is decided in the indented line after the colon `:`
character.

``` python
for path in paths:
    print path
```

I kept it simple for now. All we do is print this path to the screen and move on. Do
you see the extra indentation, though? Python uses indentation to know what code is
supposed to be executed within the loop. If I try to describe it, I'm just going to
make things more confusing than they really are. Just remember this:

* One or more lines at the same indent level are often called a "block"
* Everything right under the `for` statement which is indented belongs to the `for`
  loop.
* If you indent another level, it better be because you're starting a new block
  *inside* the `for` loop.
* If you unindent, it better be because you are done with the loop block.

An indent without a control statement is an error in Python, except for special 
cases like the way I defined `description` and `paths`. It doesn't *really* matter
how much you indent for a block, but it must be consistent throughout your program.
The common standard suggested by Python creator Guido van Rossum is four spaces per
block, with no tab characters used.

`for <item> in <list>` is useful, and it will probably be the most common tool
in your kit for examining every item in a list. It doesn't quite work for our
exact needs today, though. We want to build a menu with an easy value for the user
to enter. This will use the `range()` function combined with the `[]` operator for 
accessing list members.

`range` is a simple function which returns a list of whole numbers in a certain range.
It normally takes a single argument: the upper edge of the range. All the numbers in
the list will be *less than* the upper edge. Here is a simple example:

    >>> range(3)
    [0, 1, 2]

`range` can take additional arguments to set the starting number and the step size,
but this is all we want for now. Oh, notice that the numbering starts at zero. This
is going to be very useful, for reasons which will become clear in a few moments.

I have shown you how to look at a complete list, as well as how to look at each item
in a list one at a time. How do you look at a single item in the list? You use `[]`.
What do they call that, anyways? I can't really tell from the Python docs. Let's call
it the *indexing operation*. Why "operation?" Because we're doing something, but not
with a function. Why "indexing?" Because we will be using a specific value to get at
the item, sort of like using the index or table of contents in a book.

So let's try it out. It is easy to use the indexing operation. Add the left bracket,
the index number of the item you want, and then the right bracket. Go back to the
Python shell and try it out for yourself, getting the value at index 1 of a list:

    >>> items = [ 'apples', 'chocolate bugs', 'bananas']
    >>> items[1]
    'chocolate bugs'

That was a little confusing, wasn't it? We were expecting apples but got chocolate 
bugs instead You would *think* that the index would be easy: the first item would 
be at index 1, the second at index 2, and so on. Unfortunately, that's not the way
indexes work in Python. Numbering starts with the first item being zero.

    >>> items[0]
    'apples'

Zero-based indexing is one of those language features that's there for historical reasons.
It made perfect sense a long time ago in another language, but now it just serves to 
confuse newcomers and create a lot of "off-by-one" errors. You may want to use a mental
trick for reducing confusion: think of the index as the distance from the first item.
The first item *is* the first item, so the distance is zero: `items[0]`. The next item
is one away from the first item, so the distance is one: `items[1]`. And so on.

Or you could just subtract one from the number you're thinking of and get on with it.
Things that are shortcuts for me could just be useless clutter for you. I'm happy
as long as you remember that list index numbers start at zero.

So where do the index numbers stop? You could count the items in the list code by 
hand and work with that number, but that is far too much work. Use Python's built-in
`len` function. `len` is blissfully simple. You hand it a list, and it tells you
how many items are in the list. Try it yourself if you still have that shell open:

    >>> len(items)
    3

There are three items in the list, so the index starts at zero and ends at two. `len`
works perfectly with `range`, which hands you a list of numbers starting at zero and
ending at one less than the upper edge. Back to the shell, where we'll step through
our list using 'len', 'range', and list indexing.

    >>> for index in range(len(items)):
    ...     print index, items[index]
    ...
    0 apples
    1 chocolate bugs
    2 bananas

Oh, I didn't mention blocks in the shell, did I? When Python thinks you are in a block,
it prints `...` instead of `>>>`. Indent by hitting spaces (or I just use the tab key
when I'm in the shell). Hitting Enter on a line with no code tells the Python shell 
that you are done with the block and it's time to execute.

Just so you know - *indexing operation* is just something I came up with after looking
around on the Web a little bit. That is not the official name for `[]`, and I'll be
updating this section as soon as I find out what that name is.

This has been a quick crash course through list handling in Python. Let's apply what 
we've learned about lists to our interactive story.

``` python
# ifiction.py
#  - An interactive fiction game

import textwrap

description = "You are standing in a field. To the north of you are some mountains, " \
              "to the east of you is a forest, to the west of you is a cave, and to " \
              "the south of you is a valley."

print textwrap.fill(description)

# The list of choices available to the user.
paths = [
    "Go to the mountains",
    "Go into the forest",
    "Go into the cave",
    "Go to the valley"
]

for i in range(0, len(paths)):
    path = paths[i]
    menu_item = i + 1
    print "\t", menu_item, path
```

I used `i + 1` instead of `i` because ... well, Python may count from zero but most 
people count from one. We're writing this for people, not for Python.

We didn't *really* need to set up each `path` and `menu_item` as a variable, but 
I thought it would make things easier to read than `print "\t", i+1, paths[i]`.
You want to aim for readabality when you are starting out or you will quickly become
lost. Actually, it's a good idea to aim for readability all the way through your
programming life. It will make your code easier to maintain. Besides, putting these
values in a variable leaves room for us to change our mind about `path` and `menu_item`
are constructed in the future.

Run the script and see what you get.

    You are standing in a field. To the north of you are some mountains,
    to the east of you is a forest, to the west of you is a cave, and to
    the south of you is a valley.
      1 Go to the mountains
      2 Go into the forest
      3 Go into the cave
      4 Go to the valley

It's starting to look like something! Now go take a break for a minute. I threw a
lot of information at you all at once, and you may still need to process it. You at least need
to look at something besides a computer monitor for a few seconds and shake your
fingers loose. It's good for you.

### Getting the user's selection

[Python Babysteps tutorial]: /post/2011/06/python-2.x-babysteps/

I am pleased that we have the scene description code working, but user input is still missing. 
All we need is `raw_input`, which we encountered in the initial [Python Babysteps tutorial][].
Add a line to get user input and another line to show the result.

``` python
# ifiction.py
#  - An interactive fiction game

import textwrap

description = "You are standing in a field. To the north of you are some mountains, " \
              "to the east of you is a forest, to the west of you is a cave, and to " \
              "the south of you is a valley."

print textwrap.fill(description)

# The list of choices available to the user.
paths = [
    "Go to the mountains",
    "Go into the forest",
    "Go into the cave",
    "Go to the valley"
]

for i in range(0, len(paths)):
    path = paths[i]
    menu_item = i + 1
    print "\t", menu_item, path

choice = raw_input("Make a selection: ")
print "Choice", i, "-", paths[i-1]
```

Running this code is very exciting indeed:

    You are standing in a field. To the north of you are some mountains,
    to the east of you is a forest, to the west of you is a cave, and to
    the south of you is a valley.
      1 Go to the mountains
      2 Go into the forest
      3 Go into the cave
      4 Go to the valley
    Make a selection: 3
    Choice 3 - Go into the cave

#### Quitting the game

[control structure]: /post/2004/07/control-structures/

Our specification mentioned that users may quit the game at any point, so we should add the code to make that possible. 
Normal choices are numbers and they start at one, so let's take the easy way out and say that zero quits the game. The
`if` selection [control structure][] can be used to recognize the quit command.

``` python
# ifiction.py
#  - An interactive fiction game

import textwrap

description = "You are standing in a field. To the north of you are some mountains, " \
              "to the east of you is a forest, to the west of you is a cave, and to " \
              "the south of you is a valley."

print textwrap.fill(description)

# The list of choices available to the user.
paths = [
    "Go to the mountains",
    "Go into the forest",
    "Go into the cave",
    "Go to the valley"
]

for i in range(0, len(paths)):
    path = paths[i]
    menu_item = i + 1
    print "\t", menu_item, path

print "\t(0 Quit)"
choice = int( raw_input("Make a selection: ")

if choice == 0:
    print "Good bye!"
else:
    print "Choice", choice, "-", paths[choice-1]
```

A little note about being careful. I spent five minutes debugging the above code. I kept getting `Choice 3 Go into the cave`, for every non-zero
choice I entered. Turns out that I had cut and pasted some debugging code from earlier which was using the `i` variable. `i` was last set to `3`,
so that's what Python kept printing for me. It can be very easy to get distracted while writing code, and although Python can catch a lot of
errors, you must keep an eye out for little mistakes like that. Once I replace `i` with `choice` in the last line, everything was happy.

[type]: /post/2002/06/simple-types-in-python/

Now, why did I use the `int` function on the user input? Keyboard input comes to you in the form of a String, which is a different
[type][] than numbers. If we want to be able to use the input as an index for the `paths` list, we need a way to
turn that String into an integer, or whole number. This is exactly what `int` does. What happens when the user entry can't be turned
into a number? That's part of the next topic.

### Ensuring valid choices

User input needs to be in the form of a number. Not only that, but that number needs to be a valid index for `paths`. If either of these
turns out to be false, Python panics. Let's explore this in the shell. As a special treat, I'll show you a glimpse at making functions
in Python.

    >>> def get_index():
    ...     list = [ 10, 20, 30 ]
    ...     prompt = "Pick a number (0 - 2): "
    ...     index = int( raw_input(prompt) )
    ...     print list[index]
    ...
    >>>

If you make a mistake, hit Enter twice to end the function definition and 
start over. Don't forget your indentation! Incidentally, I chose to put the 
prompt in its own variable because all of those parentheses on the same line 
were making me a little dizzy.

Test `get_index` with a valid number first.

    >>> get_index()
    Pick a number (0 - 2): 0
    10

What happens when you enter a number that's too big? Try it and see.

    >>> get_index()
    Pick a number (0 - 2): 20
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
      File "<stdin>", line 5, in get_index
    IndexError: list index out of range

How about when you enter something that's not a number again? Once again, TIAS *(Try It And See)*.

    >>> get_index()
    Pick a number (0 - 2): banana
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
      File "<stdin>", line 4, in get_index
    ValueError: invalid literal for int(): banana

Python raises an *exception* at you whenever it encounters a situation it can't handle on its own.
An exception is a special type of object that is specially used for errors, accidents, or plain old
weird events in your program. You can plan for them, though, and try to handle them when they happen.
That is going to require a new kind of block: The `try` block. This sort of block
is easier to understand in the context of a full program, so let's go back to `ifiction.py`. We'll start with
catching every kind of exception in one go:

``` python
# ifiction.py
#  - An interactive fiction game

import textwrap

description = "You are standing in a field. To the north of you are some mountains, " \
              "to the east of you is a forest, to the west of you is a cave, and to " \
              "the south of you is a valley."

print textwrap.fill(description)

# The list of choices available to the user.
paths = [
    "Go to the mountains",
    "Go into the forest",
    "Go into the cave",
    "Go to the valley"
]

for i in range(0, len(paths)):
    path = paths[i]
    menu_item = i + 1
    print "\t", menu_item, path

print "\t(0 Quit)"

try:
    choice = int( raw_input("Make a selection: ") )

    if choice == 0:
        print "Good bye!"
    else:
        print "Choice", choice, "-", paths[choice-1]
except:
    print choice, "is not a valid selection!"
```

A `try` block usually has at least 2 parts:

* `try`: The code we think might cause an exception to be raise
* One or more `except` blocks: tells Python what to do when an exception is encountered

We can specify what exceptions we would expect to see, but that is more than I 
want to look at right now. We'll just put up a single `except` block that will 
catch every exception raised within the `try` block.  We can test the code by 
entering a number that is too large.

    You are standing in a field. To the north of you are some mountains,
    to the east of you is a forest, to the west of you is a cave, and to
    the south of you is a valley.
            1 Go to the mountains
            2 Go into the forest
            3 Go into the cave
            4 Go to the valley
            (0 Quit)
    Make a selection: 20
    Choice 20 - 20 is not a valid selection!

This is odd-looking. Our error message prints at exactly the spot where the 
exceptional situation was encountered: trying to access `paths[19]`.  Well, at 
least I've illustrated exactly how dynamic Python is. It doesn't look ahead to 
see if something bad is going to happen, so it has to trust us to know when to 
look for an error. I think it would be a little cleaner to put the choice 
description in its own variable before printing it.  That way we get an 
exception before we try to give normal feedback to the user.

``` python
try:
    choice = int( raw_input("Make a selection: ") )

    if choice == 0:
        print "Good bye!"
    else:
        next_step = paths[choice-1]
        print "Choice", choice, "-", next_step
except:
    print choice, "is not a valid selection!"
```

Our code is starting to get a little long to show the whole thing for every 
little change, so I have decided to focus on the chunk of code that is being 
modified. Anyways, you can see that I have made a new `next_step` variable. 
Python will raise the exception about bad indexing here, instead of in the 
middle of printing out feedback. We have also made the code more readable in 
the process, which is a nice thing.

    You are standing in a field. To the north of you are some mountains,
    to the east of you is a forest, to the west of you is a cave, and to
    the south of you is a valley.
            1 Go to the mountains
            2 Go into the forest
            3 Go into the cave
            4 Go to the valley
            (0 Quit)
    Make a selection: 20
    20 is not a valid selection!

Our input code handles bad indexes. Test the code again by entering a non-number for `choice`.

    You are standing in a field. To the north of you are some mountains,
    to the east of you is a forest, to the west of you is a cave, and to
    the south of you is a valley.
            1 Go to the mountains
            2 Go into the forest
            3 Go into the cave
            4 Go to the valley
            (0 Quit)
    Make a selection: steak and eggs
    Traceback (most recent call last):
      File "ifiction.py", line 35, in ?
        print choice, "is not a valid selection!"
    NameError: name 'choice' is not defined

Oops. I raised a whole new exception because `choice` isn't defined until *after* 
it's converted to a number, but I referred to it in the `except` block. Another 
intermediate variable will save us from that error.

``` python
try:
    choice = raw_input("Make a selection: ")
    menu_selection = int(choice)

    if menu_selection == 0:
        print "Good bye!"
    else:
        index = menu_selection - 1
        next_step = paths[ index ]
        print "Choice", menu_selection, "-", next_step
except:
    print choice, "is not a valid selection!"
```

There are several very small changes here. `choice` now refers only to the raw 
user input, and we have created a new variable `menu_selection` to hold the 
choice converted to an integer. This means we had to adjust the variable names 
where we were really talking about the number the user provided and not the 
keystrokes. You might have noticed that I created an `index` variable in the 
`else` block. This is a personal taste thing. I often start out using a raw 
expression and later replace it with a variable when I think it would make my 
meaning clearer.  The "start sloppy and refine as you go" approach happens to 
work for me, but use whatever tactic you are most comfortable with.

    Make a selection: an iced coffee would good right now
    an iced coffee would good right now is not a valid selection!

Right. We can recognize bad input from the user. What do we want to do about it? 
The best approach may be to continue asking the user for input until we get something 
acceptable for the next step that she wants to take. We can use a simple `while` loop 
[control structure][] to handle this.

``` python
# Keep asking for input until we have a valid choice for the next step
next_step = None
while next_step == None:
    try:
        choice = raw_input("Make a selection: ")
        menu_selection = int(choice)

        if menu_selection == 0:
            next_step = "quit"
        else:
            index = menu_selection - 1
            next_step = paths[ index ]
            print "Choice", choice, "-", next_step
    except:
        print choice, "is not a valid selection!"

print "You decided to:", next_step
```

Now we've given our user endless opportunities to enter a valid choice.

    Make a selection: Rad
    Rad is not a valid selection!
    Make a selection: 42
    42 is not a valid selection!
    Make a selection: 0
    You decided to: quit

What is going on here? We have created a variable `next_step` and assigned it 
the value of .... `None`? We are going to be using `next_step` in the test 
condition of our loop, and Python will complain to us if the variable isn't 
defined before we start testing its value.  Using the `None` value is more 
convenient than arbitrarily declaring a particular value to be invalid and 
using that. `None` is a special value meaning "nothing at all" - not even the 
numeric value of zero. Think of the statement `next_step = None` as our way 
to tell Python "I plan on using a variable called `next_step` but I don't have 
a value for it yet. Just remember that I told you I wanted the variable."

Now for the `while` loop. We specify a condition here, similar to the way we 
did with `if` earlier. The condition is that `next_step` must not be `None`.
It is an easy enough requirement. The test will fail if we successfully assign 
a `next_step` in the loop.

#### Catching specific exceptions

There is one more minor issue to take care of before we wrap up this stage of 
writing the game. It is good that we are handling exceptions raised from user 
input, but we are catching *every* exception that is raised. This doesn't 
sound like a bad thing until you remember that our error message is really 
written for a specific kind of error: the user entered something that can't be 
used by our menu handler. There are [many 
things](https://docs.python.org/2/library/exceptions.html "Python built-in exceptions summary")) 
that can go wrong in a Python code.  We don't want to be handling exceptions 
that we aren't ready for. Why not? The error messages won't make sense, for 
starters. Say you decided to hit `Control-C` in the program to force quit. 
Here's what we end up seeing:

    Make a selection: ^CTraceback (most recent call last):
      File "ifiction.py", line 40, in ?
        print choice, "is not a valid selection!"
    NameError: name 'choice' is not defined

<aside>
Please don't explore this with other types of bad input. 
You could end up with a Python process that won't quit unless you
force it to quit from your task / process manager.
</aside>

The problem is that the original exception was a `KeyboardInterrupt`. We don't 
see that here, because we referred to `choice` which isn't defined until the 
user provides some input. This causes a `NameError` to be raised, which hides 
the original exception. Python usually tells you only about the most recent 
exception that happened. If something truly unexpected happens here, we will 
never know about it. Python normally tells you about the most recent exception 
only.

We caused a `KeyboardInterrupt` by hitting `Control-C`. Python sees our 
catch-all `except` block and hands the `KeyboardInterrupt` exception to that 
block. Inside the block, we try to include the menu choice in our error message.
Unfortunately, `choice` hasn't been defined yet. We never entered a choice! 
This is a whole new exception, and we don't have any code to handle it.
Python's rule is to always stop and inform you of the first unhandled 
exception it encounters. and because of the way we defined and wrote our
`except` block, every exception is treated like bad input - from `Control-C` 
to a missing hard drive. As far as Python is concerned, we've handled the 
`KeyboardInterrupt`. The `NameError` caused by `choice` *in* the exception 
handler is the surprise that makes Python panic.

That is enough of a lecture. I am sure you understand by now that we want to 
be specific about what exceptions we are ready for. It is time to make it
happen. The two exceptions that we care about are:

IndexError
: we tried to use a bad number as a list index

ValueError
: the user input couldn't be converted to a number

Let's add a handler for IndexError.

``` python
while next_step == None:
    try:
        choice = raw_input("Make a selection: ")
        menu_selection = int(choice)

        if menu_selection == 0:
            next_step = "quit"
        else:
            index = menu_selection - 1
            next_step = paths[ index ]
            print "Choice", choice, "-", next_step
    except IndexError:
        print choice, "is not a valid selection!"
```

This change now handles `IndexError` just fine. Look at what happens when we hit `Control-C`.

    Make a selection: ^CTraceback (most recent call last):
      File "ifiction.py", line 30, in ?
        choice = raw_input("Make a selection: ")
    KeyboardInterrupt

Of course, we're only looking for `IndexError`, so look what happens right now 
if we enter something that isn't a number.

    Make a selection: mmm coffee
    Traceback (most recent call last):
      File "ifiction.py", line 31, in ?
        menu_selection = int(choice)
    ValueError: invalid literal for int(): mmm coffee

Now we add the code to handle `ValueError`.

``` python
except IndexError:
    print choice, "is not a valid selection!"
except ValueError:
    print choice, "is not a valid selection!"
```

Yes, Python can handle multiple `except` blocks just fine. This can be very 
handy. A calculator program would want to handle "no input" differently from 
"user tried to divide by zero." What does the program look like with these changes?

    Make a selection: 12
    12 is not a valid selection!
    Make a selection: Can I have a banana?
    Can I have a banana? is not a valid selection!
    Make a selection: ^CTraceback (most recent call last):
      File "ifiction.py", line 30, in ?
        choice = raw_input("Make a selection: ")
    KeyboardInterrupt

Wonderful! Our exception handling code is now behaving politely instead of 
trying to grab every exception that occurs. Now for the style issue. Both of 
our `except` blocks do exactly the same thing. I suppose we could have a 
slightly different error message for each kind of exception, and you are free 
to do exactly that. It's not something I'm concerned about, though. I am 
comfortable with using the same error message. I *would* prefer to cut down on 
the repetition.

``` python
except (IndexError, ValueError):
    print choice, "is not a valid selection!"
```

I would like to look again at this code in the future, but for now it is good enough.

We can handle multiple exceptions in the same `except` block by placing the 
exception types in a special list called a *tuple*.  I am not going to spend 
any time on tuples, because I worry that it would only confuse things. All you 
need to remember right now is that a tuple looks like an ordinary list using `()` 
instead of `[]` to wrap it, and that you should use normal lists unless I tell 
you otherwise.

It looks like we have all the code we need for handling a single round in our game. I had to cover more new concepts than I thought, because
things can become complicated when we start doing things with user input. We dabbled into importing modules thanks to the way
things were printing out in my shell. We looked at the common control structures for selection and repetition, and we
examined `try` for trying out code that we know can misbehave. Here's the full source of what we've done so far, along with a couple
of additional comments intended to clarify what the program is doing.

``` python
# ifiction.py
#  - An interactive fiction game

import textwrap

description = "You are standing in a field. To the north of you are some mountains, " \
              "to the east of you is a forest, to the west of you is a cave, and to " \
              "the south of you is a valley."

print textwrap.fill(description)

# The list of choices available to the user.
paths = [
    "Go to the mountains",
    "Go into the forest",
    "Go into the cave",
    "Go to the valley"
]

# Show the menu for this scene.
for i in range(0, len(paths)):
    path = paths[i]
    menu_item = i + 1
    print "\t", menu_item, path

print "\t(0 Quit)"
next_step = None

# Get the user selection from the menu.
while next_step == None:
    try:
        choice = raw_input("Make a selection: ")
        menu_selection = int(choice)

        if menu_selection == 0:
            next_step = "quit"
        else:
            index = menu_selection - 1
            next_step = paths[ index ]
            print "Choice", choice, "-", next_step
    except (IndexError, ValueError):
        print choice, "is not a valid selection!"

print "You decided to:", next_step
```

Now go take a break. I really mean it this time. We have covered a lot, and 
you need time to process. Listen to some music, have a sandwich, and come 
back when you're ready.