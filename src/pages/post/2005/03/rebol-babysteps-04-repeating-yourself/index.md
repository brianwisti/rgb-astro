---
aliases:
- /coolnamehere/2005/03/07_04-repeating-yourself.html
- /post/2005/04-repeating-yourself/
- /2005/03/07/rebol-babysteps-04-repeating-yourself/
category: coolnamehere
date: 2005-03-07
layout: layout:PublishedArticle
series:
- REBOL Babysteps
slug: rebol-babysteps-04-repeating-yourself
tags:
- rebol
- learn
title: REBOL Babysteps - 04 Repeating Yourself
updated: 2009-07-11 00:00:00
uuid: 6e55c669-8532-45ba-a3c8-24868eec3d54
---

Now we know how to do things, and we know how to choose whether or not we will do something.
We’re getting close to having some real skills.
We just need to get the understanding of one more concept before we reach the first little plateau of programming knowledge.
We need to learn how to do a task more than once.
Well, besides just running the script again, but that doesn’t really count.

## Simple Loops

The simplest sort of repetition involves doing exactly the same thing again and again.
The simplest sort of repetition involves doing exactly the same thing again and again.
The simplest sort of repetition involves doing exactly the same thing again and again.
The simplest sort of repetition –

Sorry, I got carried away.
Hopefully you get the idea. Sometimes all you need to do is repeat a process a set number of times.

### `loop`

    >> loop 5 [
    [    print "Spam!"
    [    ]
    Spam!
    Spam!
    Spam!
    Spam!
    Spam!

That’s a little boring.
Let’s try something a little more involved.
Maybe we could use `loop` to create a simple math quiz program.

```
REBOL [
    Title: "Simple Math Quiz"
    File: %math.r
]

; Seed the randomizer with the current time to get better random values
random/seed now

correct: 0
questions: 5

loop questions [

    ; Create a simple multiplication problem.
    a: random 10
    b: random 10
    answer: a * b

    ; Get the user's response (converting it to the right datatype)
    response: to-integer ask [ a "x" b "= " ]

    ; Evaluate the response.
    either strict-equal? answer response [
        correct: correct + 1
        print "That's correct!"
    ] [
        print [ "Sorry, it's" answer ]
    ]
]

; Display the final results.
print [ "Out of" questions "questions, you answered" correct "correctly" ]
```

Nothing fancy is going on here.
We just `loop` through the question and answer process a few times, keeping track of the user’s correct answers.
`random/seed now` is necessary to get something close to what we would consider random.
If we don’t provide it, then we get a specific sequence whenever we call `random`.
Try commenting out the `random/seed` line and run the program a few times.
You’ll see what I mean.

You’re right.
A plain old `loop` isn’t very interesting.
Let’s move on.

### Looping `forever`

I’m only telling you this because I can see that one or two of you really want to know.
What if you want to run a loop forever?
Well, you don’t want to.
Maybe you want to run a loop until some signal is received, or the user wants to quit, or something sensible like that.
You don’t want a loop to run forever.
But that doesn’t mean you *can’t* run a loop forever.
REBOL provides us with the `forever` word to let us do exactly that.

    >> forever [ print "spam." ]
    spam.
    spam.
    spam.
    ...

And so on until you hit `Ctrl + C`, or kill the process, or do something to make
the program *stop saying "spam"*!

But please, don’t use `forever` without a mighty good reason.

### `break` out of a loop

Sometimes you’re right in the middle of a loop and you want to break out of it and get back to the rest of the program.
That’s easy enough.

    >> i: 0
    == 0
    >> forever [
    [    prin i
    [    i: i + 1
    [    if equal? i 5 [
    [        print "Augh!"
    [        break
    [        ]
    [    ]
    01234Augh!
    >>

Oh, you noticed that `prin` in there?
That’s a different way of printing.
Each call to `prin` puts its output immediately after the output from the previous `prin`, rather than on a new line.
It’s nothing major, but it is a nice feature to take advantage of every once in a while.

Right.
So we’ve covered simple loops.
Now let’s start getting a little more interesting.

## Monitored Loops

Plain old repetition isn’t actually all that common.
We usually want to do something a little different each time we step through the loop.
REBOL gives us a few words which help us in that situation.

### `repeat`

`repeat` works almost exactly the same as `loop`.
The main difference is that it stores the number of trips you’ve taken through the loop in a variable that you can get to from inside the loop.
The variable has a value of `1` on the first trip through, `2` on the second trip through, and so on.

    >> repeat count 9 [
    [    print [ "3 x" count "is" 3 * count ]
    [    ]
    3 x 1 is 3
    3 x 2 is 6
    3 x 3 is 9
    3 x 4 is 12
    3 x 5 is 15
    3 x 6 is 18
    3 x 7 is 21
    3 x 8 is 24
    3 x 9 is 27

### `for`

The next sort of repetition structure is `for`, which adds a starting point, stopping point, and step size to the `repeat` loop.
`for` is useful for producing very specific loops.
It might be a little wordy for simple loops which can be handled by the `repeat` word:

    >> for num 1 9 1 [ print ["3 x" num "is" 3 * num] ]

[datatypes]: /post/2004/12/rebol-datatypes

We have a loop variable, `num`, which starts at `1` and goes up to `9` `1` number at a time.
Of course, `repeat num 9` does exactly the same thing.
`for` tends to be more useful in loops for "real-world" code, though, where you need more control over what’s being looped.
You want some real world code?
Hmm.
Oh, I know.
Let’s answer the age-old question, "How much should I tip?
That way we can play a little bit with some [datatypes][] while helping out our friends in the food service industry.
Hey, what do you expect from me?
I was a waiter for ten years, so this is the sort of stuff that pops into my head!

    >> for bill $10 $20 $1 [
    [    tip: bill * .15
    [    print ["Bill:" bill "-- Tip:" tip]
    [    ]
    Bill: $10.00 -- Tip: $1.50
    Bill: $11.00 -- Tip: $1.65
    Bill: $12.00 -- Tip: $1.80
    Bill: $13.00 -- Tip: $1.95
    Bill: $14.00 -- Tip: $2.10
    Bill: $15.00 -- Tip: $2.25
    Bill: $16.00 -- Tip: $2.40
    Bill: $17.00 -- Tip: $2.55
    Bill: $18.00 -- Tip: $2.70
    Bill: $19.00 -- Tip: $2.85
    Bill: $20.00 -- Tip: $3.00

We can’t do *that* with a `repeat` loop.
At least, I don’t think we can.
We set the starting bill at `$10`, and moved up to `$20` by `$1` at a time, showing the bill and corresponding average tip.
It’s still a very small thing.
The fact that it recognizes the values as money and treats it appropriately is a special thrill for me.
If you haven’t programmed before, then you might just assume that things are supposed to work like this.
You would be right.
Things *should* work like this: transparent, and the obvious stuff should do the obvious.
But in C, there would be all sorts of chaos and `printf` madness and general ugliness that would get you so angry that you might not even bother leaving a tip.

And that would be bad, my friends.
Very bad indeed.

As long as I’m looking at datatypes in `for` loops, let’s look at another example.
Starting from Saturday, January 3 2009, what is the calendar date of each following Saturday until March 7 2009?

    >> for day 3-jan-2009 7-mar-2009 7 [ print day ]
    3-Jan-2009
    10-Jan-2009
    17-Jan-2009
    24-Jan-2009
    31-Jan-2009
    7-Feb-2009
    14-Feb-2009
    21-Feb-2009
    28-Feb-2009
    7-Mar-2009

Start on January 3, step 7 days at a time until we reach March 7, and print the calendar date at each step.
Not bad, eh?
I know that these all occured on a Saturday, but you’ll have to wait until later for me to explain it.
You want a clue?
Oh, all right.
I used `day/weekday`, got `6`, and figured out that the sixth day of the week is Saturday.

Or maybe I looked at a calendar.
I’ll never tell.

## Conditional Loops

Then there are the times when you aren’t sure exactly when you’ll need to stop.
You need to keep going until it’s time to stop, basically.
Now, you could use a `forever` loop and `break` whenever you need to stop.
But I don’t want you to do that.
Why am I so opposed to an approach like that?
It comes down to clarity.
Somebody will be reading your code a few weeks, months, or even years after you write it.
That person could be you.

Don’t laugh - I’m still haunted by a script that I wrote years ago when I was first learning Perl.
I thought I’d just be throwing that script away, but I still use it.
I still cringe every time I have to read it, too.
And yes, it had a couple of `forever`-style loops.
I want to save you from the embarassment of bad code whenever possible.

But I digress.
Let’s look at the conditional loops.
There are two main conditional loops, `until` and `while`.
The difference between the two from our perspective is when they test to see whether it’s time to quit the loop.

### Keep going `until` something is true

[selection structures]: /post/2005/02/rebol-babysteps-03-making-decisions

The `until` loop tests at the end of each step of the loop.
If the block returns true, then it’s time to quit.
How do you know if the block returns `true`?
Because the block returns the value of the last statement in the block.
This means that we could put a simple test as the last statement, using the guidelines from the chapter on [selection structures][].

    >> until [
    [    print "Spam"
    [    response: ask "? "
    [    equal? response "Bloody Vikings!"
    [    ]
    Spam
    ? Spam
    Spam
    ? Bacon Eggs and Spam
    Spam
    ? I don't like Spam!
    Spam
    ? Bloody Vikings!
    == true

Because it doesn’t test until the end of the loop, `until` will step through the loop at least once.

### Keep going `while` something is true

`while` takes a test block and a loop block.
There’s all sorts of clever things we can do in the test block, but for now we’ll just put simple tests in it.
If the test comes up false, then `while` doesn’t bother running through the loop.
If it’s true, then it runs through the loop and tests again.

Hrm, I need to think of a decent example of `while`.
For now, let’s just make a variation of what we might do with an `until` loop.

    >> response: none
    == none
    >> while [ not-equal? response "Bloody Vikings!" ] [
    [    print "Spam."
    [    response: ask "? "
    [    ]
    Spam.
    ? flerg
    Spam.
    ? flop
    Spam.
    ? Bloody Vikings!
    == "Bloody Vikings!"

`while` will not run at all if the condition isn’t true at the start of the loop, because it tests the condition before beginning each step.

## Stepping Through a List

The last form of repetition is iterating through a list.
A copy of each item in the list is passed to a temporary variable that you can play with in the loop block.
I will only look briefly at this form of repetition in this chapter, because list manipulation and iteration is a big topic in its own right.
Nevertheless, many of you will want to do *something* with lists before I get around to writing that next chapter.

### `foreach`

The basic list iteration function is `foreach`.
It takes a name, a list variable, and a block.
`foreach` repeats the loop once for each item in the list.
The name is set to the value of the current item in the list.
It is easier to demonstrate a `foreach` loop than it is to describe one.
Here’s a quick example.

    >> colors: to-list [ "red" "green" "blue" ]
    == make list! ["red" "green" "blue"]
    >> foreach color colors [ print color ]
    red
    green
    blue

I would like to close this chapter with something a little meatier than that example, though.
Let’s write a script that takes a list of dates and tells us how far from today each of those dates are.

```
REBOL [
    file: %days.r
    purpose: { Simple demonstration of iterating through a list }
]

; Feel free to create your own list of days
days: to-list [
    23-Jan-2009 24-Feb-2009 13-Mar-2009 30-Apr-2009 31-Oct-2009 5-Jan-2010
]

foreach day days [
    ; Determine how many days we are from 'day'
    day-span: day - now

    ; 'day_span' will be negative for days in the past, and we need a
    ; positive number for our phrase below
    absolute-span: abs day-span

    ; Make sure that our phrase uses the correct form of the word 'day'
    day-string: either absolute-span > 1 [ "days" ] [ "day" ]

    either day-span > 0 [
        ; 'day' is in the future.
        print [ day "is in" day-span day-string ]
    ] [
        either day-span < 0 [
            ; 'day' is in the past.
            print [ day "was" absolute-span day-string "ago" ]
        ] [
            print [ day "is today!" ]
        ]
    ]
]
```

Now that we’ve written the code, let’s run the script:

    23-Jan-2009 was 32 days ago
    24-Feb-2009 is today!
    13-Mar-2009 is in 17 days
    30-Apr-2009 is in 65 days
    31-Oct-2009 is in 249 days
    5-Jan-2010 is in 315 days

Naturally, your results may vary.
In fact, they will almost definitely vary unless you read this article the day I updated it or your clock is set wrong.
I encourage you to play with this script and come up with your own variations.
How about a script that asks the user for a date and tells how far that day is from today?
You’ll probably need to use `to-date` on the user input.

## Conclusion and Congratulations

Completing this chapter means you have hit a significant milestone in programming by learning all of the basic elements of something called "Structured Programming".
It is now possible for you to build non-trivial, "real-world" programs using REBOL.
I will try to keep this in mind when putting together future chapters in this tutorial.
