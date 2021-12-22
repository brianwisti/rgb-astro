---
aliases:
- /coolnamehere/2005/02/27_03-making-decisions.html
- /post/2005/03-making-decisions/
- /2005/02/27/rebol-babysteps-03-making-decisions/
category: coolnamehere
date: 2005-02-27
layout: layout:PublishedArticle
series:
- REBOL Babysteps
slug: rebol-babysteps-03-making-decisions
tags:
- rebol
- learn
title: REBOL Babysteps - 03 Making Decisions
updated: 2009-07-11 00:00:00
uuid: 82c23b5e-444d-482f-8f8d-280cefab908d
---

[part 1]: /post/2004/12/rebol-babysteps-01-getting-started/
[REBOL]: http://www.rebol.com
[part 2]: /post/2004/12/rebol-babysteps-02-getting-started-with-view/

In [part 1][] I gave you a first cautious glance at the [REBOL][] programming language.
In [part 2][] I extended that glance to a peek at the excellent REBOL/View GUI library.
Let’s continue learning how to program with Rebol.
Today I want to get you started with some structured programming by introducing you to selection structures.
Selection structures make it possible to decide whether or not to do something based on a test.
Here are a few uses for a simple selection structure.

* Tell me if a file exists.
* Stop me from continuing the program if I give the wrong password.
* Tell me if a new item on [Carl's blog](http://www.rebol.com/cgi-bin/blog.r) has been posted.

## Simple Tests

### `if`

The simplest selection structure is `if`.
You give it a *test expression* and a *block*.
If the test expression turns out to be true, then REBOL runs the block.
Otherwise, it ignores the block and moves on to the next statement.

```
REBOL []
if equal? name "Zim" [ print "Reporting for duty sir!" ]
```

| if   | Test Expression     | Block
| ---- | ------------------- | -----
| `if` | `equal? name "Zim"` | `[ print "Reporting for duty sir!" ]`


You can choose between using the `equal?` function or the *equality* operator.

```
REBOL []
if name == "Zim" [ print "Reporting for duty sir!" ]
```

Those two equal signs in there combine to make a special *operator* that REBOL uses to test for strict equality --
making sure that the thing on the left has exactly the same value as the thing on the right.
There are a number of comparison functions and operators in REBOL.
It's up to you whether you prefer to use the function approach or the operator approach.
My own preference varies according to my mood and the things being compared.
Numbers and strings often get the operator treatment, while I lean towards using the functions for more complex things.
I'll stick to using the functions today, because that's the sort of mood I'm in.

| Function            | Operator | Checks For
| ------------------- | -------- | ----------
| `equal?`            | `=`      | Equality
| `strict-equal?`     | `==`     | Strict Equality
| `not-equal?`        | `<>`     | Inequality
| `strict-not-equal?` | *none*   |  Strict Inequality
| `greater?`          | `>`      | Greater Than
| `lesser?`           | `<`      | Less Than
| `greater-or-equal?` | `>=`     | Equality or Greater Than
| `lesser-or-equal?`  | `<=`     | Equality or Lesser Than

`equal?` doesn't care about case.
"abc" and "ABC" are the same, according to these tests.
So are `1` and `1.0`.
This is the way most of us think about comparisons, but programs sometimes need more careful comparisons in situations where case matters.
One example that immediately comes to mind is login and password entry.
You need to use `strict-equal?` or `strict-not-equal?` if you need an exact test.

### `either`

What happens if you want to do one thing if a test is true, but a *different* thing if the test is false?
Let's say, for example, we want to print out one message if we recognize the user as a master,
and print out another message if the user is not a master.
Well, I suppose you could have two `if` statements, like this:

```
REBOL []
if equal? name "Zim" [ print "Reporting for duty sir!" ]
if not-equal? name "Zim" [ print "Meow!" ]
```

This can obviously get ugly very quickly.
REBOL gives us the `either` statement to simplify situations like this.

```
REBOL []
either equal? name "Zim" [ print "Reporting for duty sir!" ] [ print "Meow!" ]
```

The `either` command requires a test expressions and two blocks.
Either the test is true and the first block is executed, or the test is false and the second block is executed.
That makes sense, doesn't it?
Here's how that example breaks down.

| `either` | Test                | Do this if True                       | Or do this if False
| -------- | ------------------- | ------------------------------------- | -------------------
| `either` | `equal? name "Zim"` | `[ print "Reporting for duty sir!" ]` | `[ print "Meow!" ]`

Now is a good time to point out how flexible REBOL can be.
Let's reexamine our code and see what we are trying to do.
We are printing a message, right?
The only thing that is different is *which* message we are printing.
We could hand the entire `if` statement directly to the print command like this:

```
REBOL []
print either equal? name "Zim" [ "Reporting for duty sir!" ] [ "Meow!" ]
```

It accomplishes the exact same thing as we did with the original `either` statement, but removes a little bit of repetition.
Some folks think that steps like this do a lot to make program code more readable.
Another approach might be to assign the result of the `either` statement to a variable and then print the variable.
I like this approach, because my program might grow later on.
I might decide that I want the program to *speak* the response rather than print it out to the screen.

```
REBOL []
response: either equal? name "Zim" [ "Yes master I obey!" ] [ "Meow!" ]
print response
```

I don't want to overwhelm anybody right now, and you can ignore options like these until you are much more comfortable with REBOL.
I just wanted you to see how REBOL will let you describe your program in the style that you like best.

Yes, `either` is a variation of the `if/else` construct that you find in many other languages.

## Having Multiple Tests

### `any`

```
REBOL []
response: ask "What's your favorite snack? "
if any [
	equal? response "tacos"
	equal? response "waffles"
] [
	print "Me too!"
]
```

There will be times that you want to check several things, and execute if any of them are true.
Fortunately REBOL is there to help us with the `any` function.
`any` takes a block of tests and returns true if any of those tests are true.
This is another one of those definitions that just repeats the obvious, isn't it?
Well, a lot of predefined words in REBOL work like that.

Yes, this does sound like the `or` logical operator from other languages.
Also known as `||` in C-derived languages.
I don't know about you, but I like `any` better than `||`.

### `all`

What if you only want to execute the block if *all* tests are true?
It shouldn't surprise you by this point to find out that REBOL is right there waiting for us with the `all` statement.

```
REBOL []
name: ask "Name: "
password: ask "Password: "
if all [
	strict-equal? name "Brian"
	strict-equal? password "Pretty Please?"
] [
	print "Login accepted!"
]
```

Yes, this does sound like the `and` logical operator from other languages.
Also known as `&&` in C-derived languages.
I don't know about you, but I like `all` better than `&&`.

## Conclusion

Now that you have worked with selection structures, you have a major building block for writing useful programs.
Next time around we will take a look at a few of REBOL's many repetition and iteration structures.
Then maybe we can sit down and write a *real* program!

## Changes

### 24 Feb 2009

* General cleanup

### 27 Feb 2005

* Initial release into the wild.
* Corrected some inaccuracies about `equal?` and `=` and `==`, pointed out by [Graham Chiu](http://www.compkarori.com/vanilla)
