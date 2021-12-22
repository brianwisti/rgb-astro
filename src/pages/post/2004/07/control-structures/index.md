---
aliases:
- /coolnamehere/2004/07/11_control-structures.html
- /post/2004/control-structures/
- /2004/07/11/control-structures/
category: coolnamehere
date: 2004-07-11 00:00:00
layout: layout:PublishedArticle
slug: control-structures
tags:
- python
- learn
title: Control Structures
updated: 2004-07-11 00:00:00
uuid: e7e03890-f045-462b-a102-23b9c2641b4e
---

There are several different approaches to programming, but the one that
is easiest for me to grasp is *imperative programming*. The imperative
approach allows you to tell the computer exactly what you want it to do
and how you want it done. The best analogy I can think of is a cooking
recipe. You have a list of ingredients and a specific set of
instructions to follow. Veer from the recipe and you may not be happy
with the results. Veer too far from the recipe and your house could burn
down.

Control structures are the basic building blocks of imperative
programming. They describe what kind of instructions the programming
language understands. I will explore control structures, using examples
from both the cooking world - hey, this is a good analagy and I want to
keep using it - and Python, since Python’s syntax is clean enough that
you can see the control structures easily.

I kind of played with the existing names for these structures to give
them what I think is a more poetic quality.

Sequence
--------

The fundamental control structure doesn’t seem like a control structure
at all. *Sequence* refers to the fact that one thing usually happens
after another.

- Beat the eggs and the oil together in a large bowl
- Mix the sugar and vanilla extract into the bowl.

Here’s a simple sequence example.

``` python
name = "Brian"
print "Hello", name
```

You don’t try to beat the eggs in the bowl after you’ve put the sugar
in. I suppose you could, but you are just making your life more
difficult. Similarly, you don’t try to print the name before you’ve
defined it. Bad things will happen if you even try.

Selection
---------

Selection structures allow you to mark some code as optional.

- *(optional)* Mix in walnuts

I like walnuts, but not in cookies. I’m not going to mix them into the
dough. Maybe I’ll just eat them here.

``` python
name = raw_input("Who are you? ")
if name == "Brian":
    print "Hey!", name, "is here!"
```

There are a few refinements to the Selection structure. The main
refinement is the if/else structure. This allows you to perform one
block of code if the test is true, and another block if the test fails.

Instead of:

``` python
if name == "Brian":
    print "Hey! Brian is here!"
if name != "Brian":
    print "What are you doing on Brian's computer?"
```

We can say:

``` python
name = raw_input("Who are you? ")
if name == "Brian":
    print "Hey! Brian is here!"
else:
    print "What are you doing on Brian's computer?"
```

The other main refinement is the if/else-if/else structure, which lets
you chain tests together. Instead of:

``` python
if name == "Brian":
    print "Hey! Brian is here!"
else:
    if name == "Brooke":
        print "This computer is really yours, isn't it?"
    else:
        print "What are you doing on this computer?"
```

… we can say:

``` python
if name == "Brian":
    print "Hey! Brian is here!"
elif name == "Brooke":
    print "This computer is really yours, isn't it?"
else:
    print "What are you doing on this computer?"
```

<aside class="admonition warning">
<p class="admonition-title">Warning</p>

Pay attention to how the else-if refinement is spelled in your favorite
programming language! It’s `elif` in Python, and in other languages
could be `elsif`, `elseif`, `else if`, or something else I haven’t come
across yet.

</aside>

Repetition
----------

The next control structure is *repetition*, which will execute a block
of code repeatedly until some condition is true.

- Cook in a 350 degree preheated oven for 10 minutes

Don’t you hate it when they tell you what temperature the oven is
supposed to be at the last minute? I suppose that’s why we’re suppose to
read the recipe before we start cooking. Anyways, the repetition here is
that you keep on baking until those cookies are done!

Repetition in programming has a very wide range of refinements. I’ll
just look at the major ones.

The first one is the while-loop.

``` python
number = 0
while number < 10:
    print "We have been baking for", number, "minutes"
    number += 1        # The same as saying -> number = number + 1
```

The basic idea of a while-loop is this:

1. We set up a test. We had to create a variable in this case, to make
   sure the test has some meaning the first time through.
2. We apply the test. Is `number` less than `10`?
3. If the test passes, we execute the block.
4. *Hopefully* that block contains some code which affects the test. We
   added one to `number` in our block.
5. We go back to *2*, run this again. In fact, we keep going back to
   *2* until `number` is equal to or greater than `10`.

Generally, any test that your programming language can understand in a
sense of true or false can be used. This applies to *Selection*
structures too, but I forgot to mention it then.

Another kind of repetition structure is the list-loop *(better name?
Somebody? Please?)*. The list-loop steps through each of the values in a
list and executes its block with the current item in the loop.

``` python
breakfast = [ "steak", "eggs", "potatoes" ]
for item in breakfast:
    print "I like", item, "in my breakfast."
```

Some languages won’t let you change the original value of `item` in a
normal list-loop. For example, in Python I can uppercase `item` in my
loop, but the original will still be lowercase. Try it yourself:

``` python
breakfast = [ "steak", "eggs", "potatoes" ]
for item in breakfast:
    item = item.capitalize()  # This is a *method* available to String *objects*
    print "I like", item, "in my breakfast."
for item in breakfast:
    print "Item:", item
```

Replacing the original value of `item` is more of a challenge, and often
not worth the effort involved. You could step through the list using
indexes, and change things that way:

``` python
breakfast = [ "steak", "eggs", "potatoes" ]
for i in range(0, len(breakfast):
    breakfast[i] = breakfast[i].capitalize()
for item in breakfast:
    print "Item:", item
```

I think that approach is unattractive, though. I’ll do it if I have to,
but I will use a prettier and easier tactic if it’s available. A better
way is to build a new list based on a modified version of the old list.
Python makes this easy with a language feature called *list
comprehensions*, which are funny-looking but very easy once you get the
hang of them.

``` python
breakfast = [ "steak", "eggs", "potatoes" ]
capitalized = [ food.capitalize() for food in breakfast ]
for item in capitalized:
    print item, "is a great part of breakfast"
```

Many other languages have similar approaches, such as Perl’s `map`
function.

Remote
------

The last major control structure I am going to look at is *remote code*.
This isn’t technically code on another machine, but I suppose it could
be. Remote code was written outside of the main sequence of the
application, but you can use it (repeatedly) from within the main
sequence. I guess the easiest cooking equivalent would be to hire a
person who makes the cookies for you.

Remote code usually takes the form of functions, classes (the source of
the `capitalize` method used in *Repetition*), and modules (which are
usually collections of classes or functions in a separate file).

``` python
def get_name():
    return raw_prompt("What is your name?")

def greet(name):
    print "Hello", name, "it's good to see you!"

greet( get_name() )
```

That’s it for now.