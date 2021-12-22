---
aliases:
- /coolnamehere/2004/12/26_02-getting-started-with-view.html
- /post/2004/02-getting-started-with-view/
- /2004/12/26/rebol-babysteps-02-getting-started-with-view/
category: coolnamehere
date: 2004-12-26 00:00:00
layout: layout:PublishedArticle
series:
- REBOL Babysteps
slug: rebol-babysteps-02-getting-started-with-view
tags:
- rebol
- learn
title: REBOL Babysteps - 02 Getting Started With View
updated: 2009-07-11 00:00:00
uuid: c95bb122-96de-4988-8910-66f2d8fdb68d
---

I’m sure you thought that getting started was fun, but it really didn’t
do anything to show off REBOL. I’d like to go through almost exactly the
same process, but this time focussing my attention on
[REBOL/View](http://www.rebol.com/prod-view.html). So let’s give it a
try!

I’m going to skim through this very quickly. The goal is just for you to
see how much potential there is in the REBOL/View dialect. You want to
see "Hello World"? Here it is.

    >> view layout [ text "Hello World!" ]

![Hello World in REBOL/View](rebol-intro-01.png)

One way to interpret that series of commands is along the lines of: we
want to `view` the `layout` defined as containing the `text` "Hello
World". I’ll be the first to admit that this is not an impressive
demonstration of GUI programming — unless you’ve actually done some,
then you might notice how quick it was to put together compared to using
a lot of other toolkits and platforms.

Still, the whole point of using a GUI is having something to *click*.
Let’s revisit our script from last time and putting some pointy-clicky
goodness into it.

    >> view layout [
    [    text "Enter your name"
    [    field
    [    button "Hi!"
    [    ]

![Asking for a name](rebol-intro-02.png)

Neat. Except that it doesn’t actually do anything if you click the
button. Pretty, but non-functional - sort of like my neighbor’s car.
Let’s give the `button` a block of commands along with the string "Hi!".

    >> view layout [
    [    text "Enter your name"
    [    field
    [    button "Hi!" [
    [        alert "Hello there!"
    [        ]
    [    ]

Sorry, I haven’t gotten a screenshot of the alert just yet. Trust me,
though. It’s pretty standard fare for alert boxes. It still doesn’t have
that personal touch that the script from [last
time](/post/2004/12/rebol-babysteps-01-getting-started/) did, though.
Let’s add a few touches: a little word assignment here, a little
phrase-building there with `rejoin` and some refinements. There, how
about this?

    >> view layout [
    [    text "Enter your name"
    [    name: field
    [    button "Hi!" [
    [        message: rejoin [ "Hello " name/text " - great to see you!" ]
    [        alert message
    [        ]
    [    ]

Hey, that was neat. We’ve got a pointy-clicky version of the "Hello"
script we made last time. We assigned the field to a word and then used
what REBOL calls "refinements" to access the text entered into that
field. You will see a lot about refinements as your knowledge of REBOL
progresses.

Let’s turn this into a script so we can share our newfound REBOL/View
knowledge with our other friends who have REBOL/View installed.

A REBOL/View Script
-------------------

Just rewrite the code in your favorite text editor. Don’t forget the
script header we talked about last time, and the shebang line if you’re
on Linux!

    #!/usr/local/bin/rebview -q

    REBOL [
        Title: "Hello World!"
        File:  %vHello.r
        Author: Brian Wisti
    ]

    view layout [
        text "Enter your name"
        name: field
        button "Hi!" [
            message: join  "Hello " [
                name/text " - great to see you!"
            ]
            alert message
        ]
    ]

You still have the same execution options as before, but REBOL/View
under Windows gives you an additional choice. You can find your View
script via Explorer and double-click. Easy as that!

All Done
--------

This overview didn’t even scratch the surface of REBOL/View. It didn’t
even *touch* the surface, but instead just gave the surface a sideways
glance while hurrying to an urgent appointment. I encourage you to take
a closer look at REBOL/View and its official documentation.