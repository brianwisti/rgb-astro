---
aliases:
- /coolnamehere/2006/04/30_reduce-reuse-recycle.html
- /post/2006/reduce-reuse-recycle/
- /2006/04/30/reduce-reuse-recycle-in-rebol/
category: coolnamehere
date: 2006-04-30 00:00:00
layout: layout:PublishedArticle
slug: reduce-reuse-recycle-in-rebol
tags:
- rebol
title: Reduce, Reuse, Recycle in REBOL
updated: 2009-07-11 00:00:00
uuid: 5970a2e0-434e-4128-b8ac-cf36b0264b7d
---

I had to share a "Eureka!" moment that I recently experienced about REBOL. I 
never did get around to refining it, but it stands here as a rambling 
testament of - well, as a testament of my ability to ramble.  I might end up 
refining it later, or I might not. I just didn't want the thoughts to 
disappear in air as thoughts are sometimes known to do.
<!--more-->

## My Baffling Issue

There are a lot of `re-` words in Rebol.

* reduce
* reform
* rejoin
* remold
* repend

There are others, but they make sense to people who are comfortable with the 
English language. I won't spend too much time with them.

* recycle
* remove
* rename
* repeat
* replace
* request
* resend

These do more or less what you would expect them to. `remove` will remove an 
item from a series, `rename` renames a file, `request` requests console input 
from the user. Try `help _word_` to get the specifics on the others. Like I 
said, I'm not worrying about them right now.

That first list of `re-` words was really standing in the way of understanding 
Rebol. That's because the prefix `re-` doesn't quite mean what you would 
expect in an English language context. I'm used to the meaning "do this thing 
again," and that's the way it gets used in words like `resend` and `repeat`. 
What about `repend` and those others?

## `reduce`

The key for those words is in understanding `reduce`. `reduce` takes a series 
and evaluates every expression in that series. When it's done, it hands you a 
new list consisting of the results of those evaluations. It's easier to show 
than explain:

    >> example: [
    [    2 + 3
    [    4 * 6
    [    4 / 2
    [    ]
    == [
        2 + 3
        4 * 6
        4 / 2
      ]
    >> reduce example
    == [5 24 2]

It gets more interesting when your expressions are a little more interesting, 
but I'm keeping it simple so I don't get distracted.

Those other four words which have been confusing me for months suddenly make a 
lot more sense when I realize that the prefix `re-` means "`reduce` these 
values before doing this other thing."

## `reform`

`form` takes a value and returns a stringified version of the value.

    >> form example
    == "2 + 3 4 * 6 4 / 2"

Now that we know what `reduce` does, we have a good idea what to expect out of `reform`.

    >> reform example
    == "5 24 2"

It will `reduce` the series, and then `form` a string from the values in the 
new series.

## `rejoin`

`join` is a little funky. Now that I understand what `rejoin` does, I usually 
end up using it directly. Here's a breakdown just the same.

`join` takes two arguments: a value and a series. It will reduce the value and 
the series, and then glue the results tightly into a string. Sounds a little 
bit like `form`, doesn't it? Unlike `form`, `join` will not provide spaces in 
between the values.

    >> join 3 + 2 example
    == "55242"

`rejoin` effectively does the same thing, but it doesn't need the first value. 
You can `rejoin` your series directly.

    >> rejoin example
    == "5242"

## `remold`

`mold` is somewhat nifty. It will transform its argument into a string that 
Rebol can evaluate later. Pretty handy for generating code while the program
is running!

    >> mold example
    == {[
          2 + 3
          4 * 6
          4 / 2
    ]}

`remold` will `reduce` the argument and then `mold` the results.

    >> remold example
    == "[5 24 2]"

## `repend`

    >> append example [2 + 3]
    == [
        2 + 3
        4 * 6
        4 / 2 2 + 3
    ]

Be careful, `append` actually does append the value to your original series. 
You may want to work on a `copy` if you want to leave your original series alone.

    >> append copy example [2 + 3]
    == [ 2 + 3 
         4 * 6 
         4 / 2 
         2 + 3
    ]
    >> example
    == [2 + 3 4 * 6 4 / 2]

Let's look at `repend` now that we've got the `append` warning out of the way. 
Easy enough. `repend` will `reduce` the extra value before appending. I 
haven't gotten far enough along to see why this is better or even different 
from just appending the raw expression:

    >> append copy example 2 + 3
    == [2 + 3 4 * 6 4 / 2 5]

I do feel a little smarter than I did 20 minutes ago, though. If nothing else, 
I feel good.

Great, now I think I've got a little bit better understanding of Rebol. Let's 
see if I've gotten far enough to make truly useful programs.