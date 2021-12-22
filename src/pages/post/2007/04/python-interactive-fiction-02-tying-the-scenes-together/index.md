---
aliases:
- /coolnamehere/2007/04/19_02-tying-the-scenes-together.html
- /post/2007/02-tying-the-scenes-together/
- /2007/04/20/python-interactive-fiction-02-tying-the-scenes-together/
category: coolnamehere
date: 2007-04-20 00:00:00
layout: layout:PublishedArticle
series:
- Python Interactive Fiction
slug: python-interactive-fiction-02-tying-the-scenes-together
tags:
- python
- ifiction
- learn
title: Python Interactive Fiction - 02 Tying the Scenes Together
updated: 2009-07-11 00:00:00
uuid: 878d0f7e-1ee4-4989-975b-2f14f19151b6
---

[ongoing series]: /post/2007/04/interactive-fiction-with-python/
[started]: /post/2007/04/interactive-fiction-with-python/
[Next]: /post/2007/04/python-interactive-fiction-01-handling-a-single-round/

This is the second part of an [ongoing series][] about using 
Python to create interactive fiction.  I hope to show you one fun use of 
Python while teaching you more about the basics of this language.  We [started][]
by defining how our game was going to work and creating a 
set of scenes for play. [Next][] we wrote the code to handle 
a single round of the game. Today we are going to tie all of our scenes 
together to make a complete, playable game of interactive fiction. We are 
going to approach it from an experimental view, playing with different 
approaches until we find one that makes us happy. Well, one that makes *me* 
happy.
<!--more-->

## Specifying a scene

`ifiction.py` already does a good job of describing a scene, but we want to 
describe any one of several scenes. That won't happen unless we have an 
effective way to store all of the scenes and get at a specific one.  It's 
immediately obvious that we can't have a separate variable for each scene
along with a separate list for each scene's available actions. That will 
become clumsy far too quickly. Let's think this through.

We are tracking two items for each scene.

1. The scene's description
2. A list of actions the user can take, leading to other scenes.

We need both of these items any time we deal with a scene. It makes sense to 
store them together. The easiest way to do that with our current knowledge
would be to use a list, and grab `description` and `paths` from that list.

``` python
# ifiction.py
#  - An interactive fiction game

import textwrap

scene = [
    # description
    "You are standing in a field. To the north of you are some mountains, " \
    "to the east of you is a forest, to the west of you is a cave, and to " \
    "the south of you is a valley.",
    # paths
    [
        "Go to the mountains",
        "Go into the forest",
        "Go into the cave",
        "Go to the valley"
    ]

]

description = scene[0]
paths = scene[1]

print textwrap.fill(description)

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

Did you see that array just sitting there in the middle of `scene`? Arrays can 
hold anything, even other arrays. But why didn't I declare an array variable 
to hold the paths? Well, the answer boils down to "why bother?" The array of 
paths doesn't really have a meaning outside of the scene, so I don't want to 
clutter up the names by adding a variable I will only use once. Why do I then 
go and declare a `path` array later on? To make it easier to use the paths 
of different scenes when that becomes an issue for me.

Go ahead and try that code out. It still functions exactly the same. That's good. 
You don't want the whole thing collapsing just because you made one change. So, why 
did I keep `description` and `paths` instead of referring to `scene[0]` and `scene[1]` 
in this version? The answer is as easy as you think it is. No way am I going to 
remember that `scene[1]` refers to the paths for that scene. I kept the variable name
because it's easy to remember, and works the same regardless of what scene I use.

Don't believe me? Here, let's add another scene.

``` python
# ifiction.py
#  - An interactive fiction game

import textwrap

field_scene = [
    # description
    "You are standing in a field. To the north of you are some mountains, " \
    "to the east of you is a forest, to the west of you is a cave, and to " \
    "the south of you is a valley.",
    # paths
    [
        "Go to the mountains",
        "Go into the forest",
        "Go into the cave",
        "Go to the valley"
    ]

]

mountain_scene = [
    # description
    "You are standing at the foot of a mountain range. Huge impassable peaks " \
    "loom over you. There is a cave to the east, and a field south of you "    \
    "leading into a valley.",
    # paths
    [
        "Go into the cave",
        "Go south into the field"
    ]
]

scene = mountain_scene
description = scene[0]
paths = scene[1]
```

Hey, we have two scenes! Did you notice that I added yet another variable layer, 
by remembering one of the scenes in `scene`? I am very lazy, and will work extremely 
hard to avoid extra work. We still haven't had to do anything to the logic of our 
application, and we didn't even have to change how `description` and `paths` get 
assigned.

Oh, did you run it?

    $ python ifiction.py
    You are standing at the foot of a mountain range. Huge impassable
    peaks loom over you. There is a cave to the east, and a field south of
    you leading into a valley.
            1 Go into the cave
            2 Go south into the field
            (0 Quit)
    Make a selection: 2
    Choice 2 - Go south into the field
    You decided to: Go south into the field

We have confirmed that our code works equally well regardless of which scene we use. 
It is time to start tying all the scenes together. First, let's get all the scenes
into the code.

``` python
field_scene = [
    # description
    "You are standing in a field. To the north of you are some mountains, " \
    "to the east of you is a forest, to the west of you is a cave, and to " \
    "the south of you is a valley.",
    # paths
    [
        "Go to the mountains",
        "Go into the forest",
        "Go into the cave",
        "Go to the valley"
    ]

]

mountain_scene = [
    # description
    "You are standing at the foot of a mountain range. Huge impassable peaks " \
    "loom over you. There is a cave to the east, and a field south of you "    \
    "leading into a valley.",
    # paths
    [
        "Go into the cave",
        "Go south into the field"
    ]
]

forest_scene = [
    # description
    "A giant confused bear mistakes your for one of her cubs and takes you " \
    "away with her. Although you eventually learn to love your " \
    "new bear family, your adventuring days are over.",
    # paths
    # No paths - this is a story ending
    [ ]
]

cave_scene = [
    # description
    "You are in a long dark cave. You see points of daylight at either end of " \
    "the cave, one to the northeast and one to the southwest.",
    # paths
    [
        "Go northwest",
        "Go southwest"
    ]
]

valley_scene = [
    # description
    "You are standing in the middle of a huge, beautiful valley. Standing right " \
    "before you is ... whatever it was you were looking for. Success!",
    # paths
    # No paths - this is a game ending
    [ ]
]

scene = valley_scene
```

Experiment with using different scenes for `scene` in the game, just to make sure 
everything works.

    You are standing in the middle of a huge, beautiful valley. Standing
    right before you is ... whatever it was you were looking for. Success!
            (0 Quit)
    Make a selection: 0
    You decided to: quit

How do we go from selecting a path to describing the selected scene? The 
easiest way to do that right now is to expand the list of paths for each 
list, turning a path into a list holding the string describing the path and 
the name of the scene which the path points to. Another one which is easier to 
show than to describe.

``` python
field_scene = [
    # description
    "You are standing in a field. To the north of you are some mountains, " \
    "to the east of you is a forest, to the west of you is a cave, and to " \
    "the south of you is a valley.",
    # paths
    [
        [ "Go to the mountains", mountain_scene ],
        [ "Go into the forest",  forest_scene   ],
        [ "Go into the cave",    cave_scene     ],
        [ "Go to the valley",    valley_scene   ]
    ]

]

mountain_scene = [
    # description
    "You are standing at the foot of a mountain range. Huge impassable peaks " \
    "loom over you. There is a cave to the east, and a field south of you "    \
    "leading into a valley.",
    # paths
    [
        [ "Go into the cave",        cave_scene  ],
        [ "Go south into the field", field_scene ]
    ]
]

forest_scene = [
    # description
    "A giant confused bear mistakes your for one of her cubs and takes you " \
    "away with her. Although you eventually learn to love your " \
    "new bear family, your adventuring days are over.",
    # paths
    # No paths - this is a story ending
    [ ]
]

cave_scene = [
    # description
    "You are in a long dark cave. You see points of daylight at either end of " \
    "the cave, one to the northeast and one to the southwest.",
    # paths
    [
        [ "Go northwest", mountain_scene ],
        [ "Go southwest", field_scene    ]
    ]
]

valley_scene = [
    # description
    "You are standing in the middle of a huge, beautiful valley. Standing right " \
    "before you is ... whatever it was you were loking for. Success!",
    # paths
    # No paths - this is a game ending
    [ ]
]

scene = field_scene
```

Of course, my changes broke our code.

    $ python ifiction.py
    Traceback (most recent call last):
      File "ifiction.py", line 6, in ?
        field_scene = [
    NameError: name 'mountain_scene' is not defined

Oh, that's no good at all. Of course we can't use `mountain_scene` before we tell Python what `mountain_scene` 
actually *is*. What are we going to do? We could make a handful of `None` assignments at the beginning 
of the code, but that fights against the flexibility of a language like Python. We could also create a 
big list called `scenes` and use the index of each scene instead of a variable name. That *would* work, 
but it's inconvenient. Everything could break again if we change the number of scenes. We'll also have 
to keep good notes in order to remember that `scenes[0]` is the "field scene", `scenes[1]` is the "mountain 
scene," and so on. Besides, do we really care what order the scenes are stored in? Everything should 
fall into place automatically once we decide what the starting scene is.

Python has a wonderful type for collecting things where the order doesn't matter. That type is called 
a *dictionary*, and it will be the subject of the next section.

### Dictionaries

A dictionary is also the most perfectly named type. We have to think about what strings, integers, 
and arrays are, but a *dictionary* is easy.  You know how to use a dictionary, right? You want to 
know the meaning of a word, so you look it up by name, and there is the definition. The dictionary
type works the same way. It uses *keys* instead of indexes. You look up values in a dictionary 
using their keys. Hey, we haven't gone to the console recently, and now's the perfect time.

    >>> letters = {
    ...     "a": "The first letter in the alphabet",
    ...     "b": "The second letter in the alphabet",
    ...     "banana pancakes": "A tasty and nutritious breakfast treat"
    ... }

Python recognizes that you are creating a hash when you use the curly brackets `{}`. Your initial 
keys and values will go within those brackets, much like when creating a list. The items in a hash -
sorry, they're called dictionaries in Python, but hashes in many other languages. Dictionary is a
much more sensible name, since it describes how you use it. Still, I do occasionally use the word
"hash" instead of dictionary because I'm so used to it from other languages. I could have corrected
myself and you never need know, but I thought it seemed nice to take a second and point it out. Now
when you hear somebody talking about hashes in Perl or Ruby, you will already know that they are
describing what you know as dictionaries.

What was I saying? Oh, right. The items in a *dictionary* are pairs of keys and values. The bit on
the left of the `:` character is the *key*, and that's what we use to look up a value. The *value*
is the item on the right, and that's the bit you'll usually cared about. The values are strings in
this case, but they can be anything. Actually, the same thing is true for the keys, but string keys
are the most common. I will definitely be sticking with string keys in the near future.

Once you've defined your dictionary, use square brackets `[]` to get to individual values. This is
similar to the way you get at values in a list. This little bit of consistency is provided because
both lists and dictionaries are *collection* types, and it's important to provide a consistent 
interface for similar tasks. The task in this case is accessing individual items in the collection.

    >>> letters["a"]
    "The first letter in the alphabet"
    >>> letters["b"]
    "The second letter in the alphabet"
    >>> letters["banana pancakes"]
    'A tasty and nutritious breakfast treat'

Oh yeah, our keys are strings, so we need to remember the quotes when using them to access a value.

The logic here is straightforward. Again, think of a dictionary. You flip through the pages to look
up "banana pancakes" and you find "A tasty and nutritious breakfast treat".

What happens when you try to use a key that doesn't exist? TIAS! *(Try It And See, for those of you
who don't turn every phrase into an acronym)*

    >>> letters["c"]
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
    KeyError: 'c'

Python won't try to do anything clever when you use a key that hasn't been defined. It simply raises a 
`KeyError` exception.

Using a dictionary is straightforward, as you can see. There is one quirk you need to be aware of, 
though. Remember how I said that dictionaries were a good collection type for those situations where
the order of things collected doesn't matter? That's because you cannot assume that the keys in a 
dictionary have any kind of order.

See for yourself with the dictionary method `keys`.

    >>> letters.keys()
    ['a', 'banana pancakes', 'b']
    >>>               

You can see that the keys are not in the alphabetical order you might expect. The reason is a little
technical for my mood right now, but basically Python does a little preparation which makes it easier
to store and access the keys later. The cost for us is that the keys look unsorted. It's a small cost,
and one that we can work around easily if it's that important.

Okay, fine. But what was I saying earlier about *methods*, and why does it look like I have a function
call pressed up against `letters`? That is our first peek at Object Oriented Programming, a popular
approach which makes a lot of programs easier to describe.

I am having a hard time coming up with a description for objects, even though the basic idea is easy.
You have been dealing so far with simple values for variables, like the number `3` or the string 
`"bananagram"`. Well, an object is *like* a simple value, but you can ask it to do things. Take a 
dictionary for example. You can ask it for its keys, you can ask it if it has a particular key, and
a few other things. Many of those requests are done with *methods*. A method looks like an ordinary
function, but it is associated with a particular type of object. 

I have been lying a little bit about strings, actually. They are objects, not simple values.

    >>> "surprise".upper()
    'SURPRISE'

An easy way to get at all of the values in a dictionary is to get the list of keys and iterate through
the list with `for`.

    >>> keys = letters.keys()
    >>> for key in keys:
    ...     print key, "is", letters[key]
    ...
    a is The first letter in the alphabet
    banana pancakes is A tasty and nutritious breakfast treat
    b is The second letter in the alphabet

And if the order is important to us, we can sort the list of keys with the `sort` method common to all
lists. See, you have been using objects quite a bit already!

    >>> keys.sort()
    >>> for key in keys:
    ...     print key, "is", letters[key]
    ...
    a is The first letter in the alphabet
    b is The second letter in the alphabet
    banana pancakes is A tasty and nutritious breakfast treat

I think it's been too long since we worked on our game. Let's put everything in a dictionary and make 
our game code work with that. Some big changes are coming to the code, so prepare yourself.

``` python
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
                       "away with her. Although you eventually learn to love your " \
                       "new bear family, your adventuring days are over.",
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
```

We are now using key names instead of variable names. This makes Python happier, since we aren't using
variable names that haven't been defined yet. There is a pleasant side effect, too. Instead of having
half a dozen different `scene` variables, we have contained all of them in a single `scenes` dictionary.
I like to think that this makes the code a little cleaner. We use a convenient name as the key for
each scene. Each scene is a dictionary as well, containing the description and paths for that scene.
And then the paths collection for each scene is an array of dictionaries. Each element of the `paths`
list contains the destination and a phrase describing the command. *(I'm not comfortable with the
names I used for the path dictionaries. Let's revisit that later.)*

It all sounds a little confusing, and eventually I'll come up with a better way to explain it. I think 
you'll find that dictionaries provide an incredibly convenient way to store information that is more 
complicated than a simple string or number as you get comfortable with them.

Now we need to fix our scene handling code so that it works with our new dictionary-based scenes.

``` python
scene = scenes["field"]
description = scene["description"]
paths = scene["paths"]

print textwrap.fill(description)
```

I used an array *(right name for a list -- search and replace through text)* for a scene's paths because 
I still want to use numbers in our menu listing. This means that order is important, which is the 
best time to use an array.

Printing the menu is easy. We adjust the `print` statement so that it prints the value associated with
the "phrase" key of `path`. You know what? That is too much of a mouthful. How about I start saying
"the 'phrase' for this `path`" or something like that? It means the same thing, and is probably easier
to understand since it is so much shorter.

``` python
# Show the menu for this scene.
for i in range(0, len(paths)):
    path = paths[i]
    menu_item = i + 1
    print "\t", menu_item, path["phrase"]

print "\t(0 Quit)"
next_step = None
```

Processing the input is going to be a little trickier. We need to get the right assignment for `next_step`,
but we also need to correctly handle a user decision to quit.

``` python
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
    except (IndexError, ValueError):
        print choice, "is not a valid selection!"

if next_step == "quit":
    print "Good bye!"
else:
    print "You decided to:", next_step["phrase"]
```

That exception handling code is starting to bother me. It catches errors well enough, but it doesn't
give any useful information to the user. We have provided the user with a menu and some numbers, but
we are assuming that she knows what she is supposed to enter. Our user needs to know what we expect
from her so that she can enjoy the game. Please remember: we are *not* going to assume that the user is
stupid, but we *are* going to assume that she has better things to do with her time than decipher our
menu.

I think we'll be safe by adding a little bit of direction as part of our input prompt.

``` python
prompt = "Make a selection (0 - %i): " % len(paths)

while next_step == None:
    try:
        choice = raw_input(prompt)
```

Our prompt message is a little more complicated now, so we put it into its own variable. And I have
introduced yet another way to construct strings.

String formatting
gives us a mini-language for exact control over the contents of a string. It is a fairly simple language,
consisting of placeholders marked with `%` and a conversion rule. I want to display the length of `paths`
as an integer number, so my conversion rule is `i`. The string is followed by another `%` symbol and the
value you want converted and placed in the string. Use a tuple after the `%` if you have more than one
conversion to handle in your string:

    >>> str = "%s are better for you than %s, but I don't care" % ("apples", "pancakes")
    >>> str
    'apples are better for you than pancakes'

Your rules can become very elaborate, and I encourage you to play with them more. I've rambled enough 
and there is a lot more to cover. Let's move on.

Guess what? It's time to create the game loop, which means that we are about to have a playable version
of our interactive fiction game! Take another break. Shake your fingers out. Have a taste of coffee,
juice, or whatever your beverage of choice is. We'll pick this up again soon.