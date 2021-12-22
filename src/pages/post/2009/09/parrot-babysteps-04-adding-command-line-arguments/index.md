---
aliases:
- /coolnamehere/2009/09/17_04-adding-command-line-arguments.html
- /post/2009/04-adding-command-line-arguments/
- /2009/09/17/parrot-babysteps-04-adding-command-line-arguments/
category: coolnamehere
date: 2009-09-17 00:00:00
layout: layout:PublishedArticle
series:
- Parrot Babysteps
slug: parrot-babysteps-04-adding-command-line-arguments
tags:
- parrot
- learn
title: Parrot Babysteps 04 - Adding Command Line Arguments
updated: 2010-07-21 00:00:00
uuid: e154e91e-f0ec-44cc-adbe-a535542cfa15
---

## Introduction

We have learned a reasonable amount so far.
We know how to write fairly trivial applications using Parrot
Intermediate Representation. We could probably write a simple formula
calculator that gets input from the user, ensures that the content is valid,
and presents the results of applying user input to the formula.

It would be nice to write more ambitious programs, though. It would be
painful - maybe even impossible - to create a modern program using only
the tools and opcodes we have learned so far.

[a few steps ago]: /post/2009/07/parrot-babysteps-02-variables-and-types

We can start examining PMCs by writing a version of our hypotenuse calculator
from [a few steps ago][] that has command line
arguments.

## Command Line Arguments

How do we tell Parrot that our program accepts command line arguments, though?
We need some way to show that our `:main` sub is ready to take parameters.
Turns out that's actually pretty easy.

### `.param` directive

The `.param` directive is used at the start of a subroutine to indicate
that the subroutine will accept a parameter and place it in the named
variable.

    # example-04-01.pir

    .sub 'main' :main
        .param pmc argv
    .end

`argv` is a [ResizableStringArray](http://docs.parrot.org/parrot/latest/html/src/pmc/resizablestringarray.pmc.html):
an ordered collection of strings.

We can use the `elements` opcode to find out how many arguments were passed to the file.

    # example-04-02.pir

    .sub 'main' :main
        .param pmc argv
        .local int argument_count
        .local string description

        argument_count = elements argv
        description = "I was called with "
        $S0 = argument_count
        description .= $S0
        description .= " arguments"

        say description
    .end

Try it out.

    $ parrot example-04-02.pir hey there
    I was called with 3 arguments

Three? Let's look at the arguments individually and see if we can figure this out.

### `shift`

The `shift` opcode lets us pull the first item from an array. This shrinks
the `argv` array by one as it shifts the rest of its contents over to fill
the empty space, but it's not a concern for us right now.

    # example-04-03.pir

    .sub 'main' :main
        .param pmc argv
        .local int argument_count
        .local string this_argument
        .local string description

      GET_ARG:
        argument_count = argv
        if argument_count <= 0 goto END
        this_argument = shift argv
        description = "This argument: " . this_argument
        say description
        goto GET_ARG

      END:

    .end

We can use this code to look at our program arguments one at a time.

    bash-3.2$ parrot example-04-03.pir hey there
    This argument: example-04-03.pir
    This argument: hey
    This argument: there

Oh, right. The program name is the first argument. That is not unusual,
especially in some lower level languages. I should have remembered.

### Calculating a Hypotenuse

Let's take what we've learned about handling the command line and apply it to
our hypotenuse calculator.

    # example-04-04.pir

    .sub 'main' :main
        .param pmc argv
        .local int argument_count
        .local string program_name
        .local num a
        .local num b
        .local num c
        .local num a_squared
        .local num b_squared
        .local num c_squared
        .local string error_message

        program_name = shift argv
        argument_count = elements argv
        if argument_count != 2 goto BAD_ARG_COUNT
        a = shift argv
        b = shift argv
        a_squared = a * a
        b_squared = b * b
        say a_squared
        say b_squared
        c_squared = a_squared + b_squared
        c = sqrt c_squared
        say c
        goto END

      BAD_ARG_COUNT:
        error_message = "Exactly two arguments required"
        say error_message
        goto END

      END:
    .end

First we shift the first item off of `argv` because we know for sure that it's
going to be the program name. Then we check to make sure that the user has
provided us with two arguments that we can use for `a` and `b`. Not having two
arguments is an error, so the program branches to displaying an error and 
quitting. When the argument count is right, the program shifts the 
arguments into `a` and `b` then uses them to calculate and display the 
hypotenuse.

Oh yeah - sooner or later you're going to see this error message from Parrot:

    error:imcc:syntax error, unexpected '=', expecting '(' ('=')
            in file 'example-04-04.pir' line 24

What did line 24 look like?

    c_squared = a_squared + b_squared

It toook me a while to realize that I had never
declared `.local num c_squared`. Unfortunately, Parrot's error messages aren't
quite as descriptive as Perl's. Perl has had a lot more time to figure out how
to gently explain a user's error to him, though.

    bash-3.2$ parrot example-04-04.pir 12 23
    144
    529
    25.9422435421457
    bash-3.2$

That worked. 
    
Parrot has many special opcodes [for dealing with 
PMCs](http://docs.parrot.org/parrot/latest/html/src/ops/pmc.ops.html) and soon we'll
be looking at more of them. I am especially interested in the opcodes that allow
us to use arrays and other collection types.

## Summary

Yes, this has been a *very* quick step. Maybe we didn't learn a whole lot, 
but there's a little bit of new stuff in there. We
did learn how to add command line handling by using `.param` to tell Parrot that
our `:main` method accepts parameters. We learned that for `:main`, the parameter
is a particular PMC - something called a ResizableStringArray. The `shift` opcode
removes the first item in a ResizableStringArray and lets us use it in a variable.
We also saw that we can use the `members` opcode to get the number of members in
an array.