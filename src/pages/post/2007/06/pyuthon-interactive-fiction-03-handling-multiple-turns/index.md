---
aliases:
- /coolnamehere/2007/06/14_03-handling-multiple-turns.html
- /post/2007/03-handling-multiple-turns/
- /2007/06/14/python-interactive-fiction-03-handling-multiple-turns/
category: coolnamehere
date: 2007-06-14 00:00:00
layout: layout:PublishedArticle
series:
- Python Interactive Fiction
slug: pyuthon-interactive-fiction-03-handling-multiple-turns
tags:
- python
- ifiction
- learn
title: Python Interactive Fiction - 03 Handling Multiple Turns
description: Letting Python handle more than one round
updated: 2009-07-11 00:00:00
uuid: e6d699a1-f005-4d39-ac23-28c333ba1186
---

[ongoing series]: /post/2007/04/interactive-fiction-with-python/
[Part 2]: /post/2007/04-python-interactive-fiction-02-tying-the-scenes-together/

This is Part 3 of an [ongoing series][] about writing interactive fiction games in Python.
By the end of [Part 2][] we had created a text-based user interface and explored
one way of storing multiple scenes. This part will finally bring the needed glue for the player to
move between all of the scenes in the story. In other words, we'll have a game!
<!--more-->

You're going to be amazed at how simple this is to do. We'll start with a simple, clumsy approach.

``` python
# ifiction.py
#  - An interactive fiction game

import textwrap # For nice formatting of the description
import sys      # For exiting the game

scenes = {
    "field": {
        "description": "You are standing in a field. To the north of you are some mountains, " \
                       "to the east of you is a forest, to the west of you is a cave, and to " \
                       "the south of you is a valley.",
        "paths": [
            { "go_to": "mountains", "phrase": "Go to the mountains" },
            { "go_to": "forest",    "phrase": "Go to the forest" },
            { "go_to": "cave",      "phrase": "Go into the cave" },
            { "go_to": "valley",    "phrase": "Go to the valley" }
        ]
    },
    "mountains": {
        "description": "You are standing at the foot of a mountain range. Huge impassable peaks " \
                       "loom over you. There is a cave to the east, and a field south of you "    \
                       "leading into a valley.",
        "paths": [
            { "go_to": "cave", "phrase": "Go into the cave" },
            { "go_to": "field", "phrase": "Go south into the field" }
        ]
    },
    "forest": {
        "description": "A giant confused bear mistakes your for one of her cubs and takes you "   \
                       "away with her. Although you eventually learn to love your new bear " \
                       "family, your adventuring days are over.",
        "paths": [ ]
    },
    "cave": {
        "description": "You are in a long dark cave. You see points of daylight at either end of " \
                       "the cave, one to the northeast and one to the southwest.",
        "paths": [
            { "go_to": "mountains", "phrase": "Go northwest" },
            { "go_to": "field",     "phrase": "Go southwest" }
        ]
    },
    "valley": {
        "description": "You are standing in the middle of a huge, beautiful valley. Standing right " \
                       "before you is ... whatever it was you were looking for. Success!",
        "paths": [ ]
    }
}

scene = scenes["field"]

while 1 == 1:  # Watch out, could be an infinite loop!
    next_step = None
    description = scene["description"]
    paths = scene["paths"]

    print textwrap.fill(description)

    # Show the menu for this scene.
    for i in range(0, len(paths)):
        path = paths[i]
        menu_item = i + 1
        print "\t", menu_item, path["phrase"]

    print "\t(0 Quit)"

    # Get the user selection from the menu.
    prompt = "Make a selection (0 - %i): " % len(paths)

    while next_step == None:
        try:
            choice = raw_input(prompt)
            menu_selection = int(choice)

            if menu_selection == 0:
                next_step = "quit"
            else:
                index = menu_selection - 1
                next_step = paths[ index ]
        except (IndexError, ValueError):
            print choice, "is not a valid selection!"

    if next_step == "quit":
        print "Good bye!"
        sys.exit()
    else:
        scene = scenes[ next_step["go_to"] ]
        print "You decided to:", next_step["phrase"]
```

The changes really are simple. I decided to put the whole process of describing the scene and getting 
user input into a `while` loop. The loop is basically going to go forever, as our loop test shows. One
always equals one according to my admittedly limited math skills, so this test is always going to return
`true`. That means we have an infinite loop. Infinite loops aren't really a good idea, but they are often
the easiest way to describe what you want the computer to do. However, we do need *some* way to quit the
loop and the game. That is where the `exit` function from the
[`sys`](https://docs.python.org/2/library/sys.html)
module comes in handy. `sys` contains many variables and functions that allow your program to interact 
directly with Python itself and your computer environment. `sys.exit` serves the rather obvious purpose
of exiting the Python system. That's all we need to break out of our loop.

Let's take a look at running the game.

    You are standing in a field. To the north of you are some mountains,
    to the east of you is a forest, to the west of you is a cave, and to
    the south of you is a valley.
            1 Go to the mountains
            2 Go to the forest
            3 Go into the cave
            4 Go to the valley
            (0 Quit)
    Make a selection (0 - 4): 1
    You decided to: Go to the mountains
    You are standing at the foot of a mountain range. Huge impassable
    peaks loom over you. There is a cave to the east, and a field south of
    you leading into a valley.
            1 Go into the cave
            2 Go south into the field
            (0 Quit)
    Make a selection (0 - 2): 2
    You decided to: Go south into the field
    You are standing in a field. To the north of you are some mountains,
    to the east of you is a forest, to the west of you is a cave, and to
    the south of you is a valley.
            1 Go to the mountains
            2 Go to the forest
            3 Go into the cave
            4 Go to the valley
            (0 Quit)
    Make a selection (0 - 4): 4
    You decided to: Go to the valley
    You are standing in the middle of a huge, beautiful valley. Standing
    right before you is ... whatever it was you were looking for. Success!
            (0 Quit)
    Make a selection (0 - 0): 0
    Good bye!

Congratulations, it's a game!

You can stop at this point. The game is complete, and there is nothing more that *needs* to be done.
There are some more things I would like to do with the game before I move on. I invite you to follow
me in the process of making our code more pleasant to read. I will spend time wandering from thought to
thought. You will probably learn less about programming, but quite a bit about how I look at programs.

## Cleaning up

The game works, but it could stand to be cleaned up. *Refactoring* is the practice of examining
your application code and deciding what changes would make the code easier to read, faster, or just plain
better in some way, but *without changing what the program does*. That's the hard part. It is so tempting
to add new features as soon as you think of them. That leads to a pile of unreadable code, sooner or 
later. That pile usually shows up sooner if you don't refactor often enough. Trust me. I am speaking
from years of experience creating huge piles of unreadable code.

Some developers may argue that this program is too small for refactoring to be much use. After all,
my copy is only 87 lines including `scenes`. They can argue all they want, but this is my code, and
I think that some functions would push the more elaborate code into a corner so that the code
which runs the game is easier to read.

It isn't difficult, either. We can start by searching for clumsy-looking blocks of code which make
it harder to figure out what's going on.

This looks like a good candidate right here.

``` python
# Get the user selection from the menu.
prompt = "Make a selection (0 - %i): " % len(paths)

while next_step == None:
    try:
        choice = raw_input(prompt)
        menu_selection = int(choice)

        if menu_selection == 0:
            next_step = "quit"
        else:
            index = menu_selection - 1
            next_step = paths[ index ]
    except (IndexError, ValueError):
        print choice, "is not a valid selection!"
```

What do we want? We want the user to tell us what she wants to do next. The user picks a number which
could lead to another scene or quitting. Let us define it in a function.

``` python
# Scene definitions
# ...

# Function definitions
def select_path(paths):
    next_step = None

    # Show the menu for this scene.
    for i in range(0, len(paths)):
        path = paths[i]
        menu_item = i + 1
        print "\t", menu_item, path["phrase"]

    print "\t(0 Quit)"

    # Get the user selection from the menu.
    prompt = "Make a selection (0 - %i): " % len(paths)
    while next_step == None:
        try:
            choice = raw_input(prompt)
            menu_selection = int(choice)

            if menu_selection == 0:
                next_step = "quit"
            else:
                index = menu_selection - 1
                next_step = paths[ index ]
        except (IndexError, ValueError):
            print choice, "is not a valid selection!"
    return next_step
```

We just moved the code into a function `def` block which we called `select_path`. 
`select_path` needs to know all about the paths for the scene in order to build the prompt, so we indicate that
in the function definition. `next_step` is set to `None` inside the function, since Python doesn't
know about it yet.

The rest of the function block looks like the original chunk of code, until it reaches the end. Instead
of doing something with the selected `next_step`, `select_path` returns it to whoever called it. You
want to limit what your function does to one important thing, and you want to name your function for
the one thing it does. This is one more little thing that makes code easier to handle when you come
back to it later. 

As I was saying - if `select_path` holds the code for getting user input and sends the results to the
caller, what does our main game code look like now?

``` python
# Game starts here.
scene = scenes["field"]

while 1 == 1:  # Watch out, could be an infinite loop!
    description = scene["description"]
    paths = scene["paths"]

    print textwrap.fill(description)
    next_step = select_path(paths)

    if next_step == "quit":
        print "Good bye!"
        sys.exit()
    else:
        scene = scenes[ next_step["go_to"] ]
        print "You decided to:", next_step["phrase"]
```

The original chunk has been replaced by a single line of code. This has made things a little more readable,
but I still see a lot of changes we could make. Yes, I really do program like this. It is a faster process
than you think, especially if you're not narrating as you write code.

What would I like to do next? Well, I don't like the way `select_path` uses a loop to get the path 
selection. There's nothing wrong with that approach, but I don't think it reads clearly:

> While there is not a valid `next_step`, try to get the user selection and use it to pick `next_step`

That is more or less how this reads to me in English. The second part is okay, but the first part is
nonsensical. Let's roll up our sleeves and make some sense out of this.

First off: we know we are going to be working with the user input portion of this function, and maybe
in a big way. Let's protect `select_path` by refactoring user input into its own function. What to name
it? Well, we are showing a prompt and getting user input, so the behavior is similar to `raw_input`. 
This input is relevant to the menu we just displayed, so let's call our new function `menu_input`.
We still need that `paths` data, so it'll be an argument for our new function as well.

Here is a first version of `menu_input`, followed by the modified version of `select_path`.

``` python
# Function definitions
def menu_input(paths):
    next_step = None
    prompt = "Make a selection (0 - %i): " % len(paths)
    while next_step == None:
        try:
            choice = raw_input(prompt)
            menu_selection = int(choice)

            if menu_selection == 0:
                next_step = "quit"
            else:
                index = menu_selection - 1
                next_step = paths[ index ]
        except (IndexError, ValueError):
            print choice, "is not a valid selection!"
    return next_step

def select_path(paths):
    # Show the menu for this scene.
    for i in range(0, len(paths)):
        path = paths[i]
        menu_item = i + 1
        print "\t", menu_item, path["phrase"]

    print "\t(0 Quit)"
    # Get the user selection from the menu.
    next_step = menu_input(paths)
    return next_step
```

The current phrasing of `menu_input` bothers me, but what would be an improvement? Python doesn't
have a convenient way of saying "do this until I have a useful value", but there is another way to
phrase the task:

> Try to get the user selection and use it to pick `next_step`. If something goes wrong, warn the user
> and try again. If nothing goes wrong, return `next_step`.

How do you say that in Python? You say it with *recursion*.

``` python
def menu_input(paths):
    prompt = "Make a selection (0 - %i): " % len(paths)

    try:
        choice = raw_input(prompt)
        menu_selection = int(choice)

        if menu_selection == 0:
            next_step = "quit"
        else:
            index = menu_selection - 1
            next_step = paths[ index ]
    except (IndexError, ValueError):
        print choice, "is not a valid selection!"
        # Try again!
        next_step = menu_input(paths)

    return next_step
```

I have managed to clean up the code merely by changing the way I phrased the task. What does `menu_input` do?
It tries to get a value for `next_step` from user input. What happens if the user input is bad? *It tries again!*
Brilliant in its simplicity! You will find that recursion - the act of calling the current function again - 
can be an easier way to describe your solution to a problem than using a loop. You can even change the arguments 
each time you recurse. Actually, that is encouraged. It just wasn't needed for `menu_input`.

There is one more change I would like to make to `menu_input`. The variable name `next_step` made sense 
when it was being defined in the context of a whole game, but now it is being defined in a much narrower 
context. The variable should have a new name which reflects that we are getting and returning the path
that was selected by the user. `selected_path` ought to do it.

``` python
def menu_input(paths):
    prompt = "Make a selection (0 - %i): " % len(paths)

    try:
        choice = raw_input(prompt)
        menu_selection = int(choice)

        if menu_selection == 0:
            selected_path = "quit"
        else:
            index = menu_selection - 1
            selected_path = paths[ index ]
    except (IndexError, ValueError):
        print choice, "is not a valid selection!"
        # Try again!
        selected_path = menu_input(paths)

    return selected_path
```

Choosing a variable name can be a tricky business. It doesn't have much effect on how the program runs,
but it can have a huge impact on how easy it is for you to read the code. I discuss code reading a lot,
and there is a good reason for that. You will ultimately be spending more time reading code than writing
it. Even if you only work on your own projects, you will have to review the code multiple times. And
program code is not written for the computer. It's written for the programmer. All the computer needs
are the specific machine instructions to perform a task. The reason we don't write much in machine language
these days is simple: we don't have to. Computers are powerful enough to provide layers between us and
the machine language. So, if you are writing code, write for people. You can think of it as a story if you
want to. Try to make it like a story by Ernest Hemingway, a man who was famous for writing simply and
clearly.

> My aim is to put down on paper what I see and what I feel in the best and simplest way. -- *Ernest Hemingway*

My writing is a long way from his, but I keep this goal in my head while I write code.

I am nearly done with refactoring this code. The `while 1 == 1` block still bothers me, though. There
has to be a more graceful way to describe the game loop. Let's look at what we have right now.

``` python
while 1 == 1:  # Watch out, could be an infinite loop!
    description = scene["description"]
    paths = scene["paths"]

    print textwrap.fill(description)
    next_step = select_path(paths)

    if next_step == "quit":
        print "Good bye!"
        sys.exit()
    else:
        scene = scenes[ next_step["go_to"] ]
        print "You decided to:", next_step["phrase"]
```

It is tempting to rewrite this as a recursive function, since it worked so well for menu input. 
Unfortunately, that may not work for a game loop. Python has built-in recursion limits, which you can find
from the library function `sys.getrecursionlimit`. This function returns `1000` on my machine, and it
probably will on yours too. This means that you can recursively call a function no more than one thousand
times. That sounds like a lot, but you will hit that ceiling a lot sooner than you think if you rely 
heavily on recursion.

Oh well, I guess I could put this block into its own function.

``` python
def play_game(start_scene):
    scene = start_scene
    while 1 == 1:  # Watch out, could be an infinite loop!
        description = scene["description"]
        paths = scene["paths"]

        print textwrap.fill(description)
        next_step = select_path(paths)

        if next_step == "quit":
            print "Good bye!"
            sys.exit()
        else:
            scene = scenes[ next_step["go_to"] ]
            print "You decided to:", next_step["phrase"]

# Game starts here.
play_game(scenes["field"])
```

This does make the application code simple. It's just a function call to play the game, starting with
the "field" scene. And really, this is as far as I feel like refactoring the game code. Here is the final
form of our simple interactive fiction game.

``` python
# ifiction.py
#  - An interactive fiction game

import textwrap # For nice formatting of the description
import sys      # For exiting the game

scenes = {
    "field": {
        "description": "You are standing in a field. To the north of you are some mountains, " \
                       "to the east of you is a forest, to the west of you is a cave, and to " \
                       "the south of you is a valley.",
        "paths": [
            { "go_to": "mountains", "phrase": "Go to the mountains" },
            { "go_to": "forest",    "phrase": "Go to the forest" },
            { "go_to": "cave",      "phrase": "Go into the cave" },
            { "go_to": "valley",    "phrase": "Go to the valley" }
        ]
    },
    "mountains": {
        "description": "You are standing at the foot of a mountain range. Huge impassable peaks " \
                       "loom over you. There is a cave to the east, and a field south of you "    \
                       "leading into a valley.",
        "paths": [
            { "go_to": "cave", "phrase": "Go into the cave" },
            { "go_to": "field", "phrase": "Go south into the field" }
        ]
    },
    "forest": {
        "description": "A giant confused bear mistakes your for one of her cubs and takes you "   \
                       "away with her. Although you eventually learn to love your new bear " \
                       "family, your adventuring days are over.",
        "paths": [ ]
    },
    "cave": {
        "description": "You are in a long dark cave. You see points of daylight at either end of " \
                       "the cave, one to the northeast and one to the southwest.",
        "paths": [
            { "go_to": "mountains", "phrase": "Go northwest" },
            { "go_to": "field",     "phrase": "Go southwest" }
        ]
    },
    "valley": {
        "description": "You are standing in the middle of a huge, beautiful valley. Standing right " \
                       "before you is ... whatever it was you were looking for. Success!",
        "paths": [ ]
    }
}

# Function definitions
def menu_input(paths):
    prompt = "Make a selection (0 - %i): " % len(paths)

    try:
        choice = raw_input(prompt)
        menu_selection = int(choice)

        if menu_selection == 0:
            selected_path = "quit"
        else:
            index = menu_selection - 1
            selected_path = paths[ index ]
    except (IndexError, ValueError):
        print choice, "is not a valid selection!"
        # Try again!
        selected_path = menu_input(paths)

    return selected_path

def select_path(paths):
    # Show the menu for this scene.
    for i in range(0, len(paths)):
        path = paths[i]
        menu_item = i + 1
        print "\t", menu_item, path["phrase"]

    print "\t(0 Quit)"
    # Get the user selection from the menu.
    next_step = menu_input(paths)
    return next_step

def play_game(start_scene):
    scene = start_scene
    while 1 == 1:  # Watch out, could be an infinite loop!
        description = scene["description"]
        paths = scene["paths"]

        print textwrap.fill(description)
        next_step = select_path(paths)

        if next_step == "quit":
            print "Good bye!"
            sys.exit()
        else:
            scene = scenes[ next_step["go_to"] ]
            print "You decided to:", next_step["phrase"]

# Game starts here.
play_game(scenes["field"])
```

We are more or less done with this train of thought. I have introduced you to many topics, but I have taken
my own strange path through them. Your next step should be to reexamine the [official Python
tutorial](https://docs.python.org/2/tutorial/index.html)
and see if it makes any more sense than the first time you read it.

## More ideas

Now that you have a complete game, what else can you do? There are many ideas. I may even tackle a few
of them in future installments. You don't have to wait for me, though.

### Different story maps

What happens when you want a different story? Right now, you have to rewrite the `scenes` dictionary within
the program. Wouldn't it be better if you could load a story from another file? It's Python code, so you
could try experimenting with `import`.

### Saving a game

What do you do if you have a very large story map and the player can't handle the whole thing in one
session? Right now, nothing. The user has to restart the game every time. It would be very generous
if you came up with some way to save the key of the current scene to a configuration file, and resume
from that scene when the game restarted. You would have to add a command for saving and quitting instead
of simply quitting.

### Inventory

Would the story go differently if the user had a flashlight in the cave? Adding inventory and letting it
affect the available paths in your story is one way to make your game richer, at the cost of making the
code much more complicated. Still, go ahead and give it a shot if you are interested!

## A Bonus Diversion: Scope

<aside>
This was originally part of the main text, but it didn't really belong anywhere once
I had finished writing. I decided to leave it in as one more bout of insane rambling instead of deleting
it and probably forever forgetting it. At least this way I have something to start from when I *do* feel
like talking about scope.
</aside>

Hey, you may be wondering how I could get away with using the variable `next_step` in so many places. First, let
me make a confession. Reusing the same name like that over and over again is poor form. I should be 
changing the name to reflect how it is being used in its code block, instead of just cutting and pasting
from one block to another. I was in a hurry, though, and being in a hurry can lead to laziness. In my
defense, `next_step` is being properly defined with the same line each step of the way: `next_step = paths[ index ]`.
It doesn't feel like I'm doing any harm, since I *am* effectively referring to the same thing. Still, 
I am making excuses for my laziness.

Another thing I would like to point out is that they are each completely different variables from Python's 
perspective. We use the term *scope* to describe where a particular variable can be seen. First, if a variable
is first defined inside of a function, it is only visible within that function. As soon as the function 
returns, its "local" variables usually cease to exist. *(There are special situations where this is not true,
but I am not going to look at them yet. Look up "closure" on the Internet for more information)*. Variables
that are defined outside of a function are visible from the point where they are defined until the end 
of the file. If you define a value for a local variable with the same name as a global variable, though,
the local variable "masks" the global variable until the end of the function.

It's all fairly confusing, and easiest to demonstrate with another trip to the Python console.

    >>> x = "waffle"
    >>> def foo():
    ...     print x
    ...
    >>> foo()
    waffle
    >>> def bar():
    ...     x = "angry bears!"
    ...     print x
    ...
    >>> bar()
    angry bears!
    >>> print x
    waffle
    >>>  

Are you feeling a little lost? It's okay, variable scope confuses many developers. The scope rule to
remember is that a local definition trumps a global definition. The style rule to remember? Don't use global
variables and you only need to remember about local variables and variables handed to a function as 
part of its arguments.