---
aliases:
- /coolnamehere/2009/09/11_03-simple-control-structures.html
- /post/2009/03-simple-control-structures/
- /2009/09/11/parrot-babysteps-03-simple-control-structures/
category: coolnamehere
date: 2009-09-11 00:00:00
layout: layout:PublishedArticle
series:
- Parrot Babysteps
slug: parrot-babysteps-03-simple-control-structures
tags:
- parrot
- learn
title: Parrot Babysteps 03 - Simple Control Structures
updated: 2010-02-12 00:00:00
uuid: 1357d622-4869-478e-b9d6-fc90ab141bbb
---

[control structures]: /post/2004/07/control-structures

I've already written a little bit about [control structures][]
on another page. Because of that, I won't spend a whole lot of time on what control
structures *are* and more time on how to implement them in Parrot.

This material follows pretty much the same steps as the Parrot book chapter on [control
structures](http://docs.parrot.org/parrot/latest/html/docs/book/pir/ch05_control_structures.pod.html).
You could follow that chapter and end up with the same knowledge that you would get from
reading today's step. Maybe even a little more.

## Sequence

As usual for many programming languages, the the sequence control structure is 
implemented in Parrot as a pattern of one instruction following another.

    # example-03-01.pir
    .sub main :main
        .const string PROMPT = "What is your name? "
        .local string name
        .local string response
        .local pmc    stdin

        stdin = getstdin
        name = stdin.'readline_interactive'(PROMPT)
        response = "Hello, " . name
        say response
    .end

## Selection

Parrot uses simple mechanisms for building selection and repetition structures. Why is this?
This is because Parrot and PIR are built for designing new programming languages. The
designers opted to have the core control structures be simplistic so you wouldn't be stuck
with what Parrot thinks a repetition loop - as one example - should look like. This does
mean that moderately experienced developers such as myself must release some of our prejudices
about what is "good" or "bad" in code. Very experienced developers and complete newcomers
should have an easier time with Parrot's controls, due to broadened horizons or lack of
preconceptions.

Selection structures are created in Parrot with a combination of labels, `goto`, and `if` test 
instructions. Yes, the [infamous `goto`](http://www.c2.com/cgi/wiki?GotoConsideredHarmful). Let's 
relinquish our [cargo cult](http://en.wikipedia.org/wiki/Cargo_cult_programming) 
habits and start learning how `goto` is used in Parrot.

We'll look at labels first, which are how we tell `goto` where to go.

## Labels

Labels consist of a series of letters, numbers, and underscores followed by a colon `:` character. 
Although it's not strictly required, I use uppercase letters for label identifiers.
You will generally find labels by themselves, outdented from the other instructions around it.

    <IDENTIFIER>:
        # Code following instruction

Again: this is not required. I follow this convention because I believe it makes my
code easier to read. You could just as easily have the following instruction on the same line,
but it has the risk of making your code visually cluttered.

    SET_NAME: $S0 = 'Brian'
    say $S0

Labels serve as markers in your code. They don't accomplish much by themselves, but can
show some of your program structure if named and placed intelligently.

    # example-03-02.pir
    .sub main :main
        .const string PROMPT = "What is your name? "
        .local string name
        .local string response
        .local pmc    stdin

        stdin = getstdin

    GET_NAME:
        name = stdin.'readline_interactive'(PROMPT)

        response = "Hello, " . name
        say response
    .end

### `goto`

A `goto` instruction sends Parrot execution to a specific labelled location
in your code. 

    goto <LABEL_IDENTIFIER>

When it follows a `goto`, Parrot picks up by executing the first
instruction following the label. In this example, it creates an
infinite loop which can only be interrupted by pressing
Control-C.

    # example-03-03.pir
    .sub main :main
        .const string PROMPT = "What is your name? "
        .local string name
        .local string response
        .local pmc    stdin

        stdin = getstdin

    GET_NAME:
        name = stdin.'readline_interactive'(PROMPT)

        goto GET_NAME

        response = "Hello, " . name
        say response
    .end

Infinite loops have their occasional uses, but most of the time they're just
annoying.

    $ parrot example-03-03.pir
    What is your name? Brian
    What is your name? Brian
    What is your name? I said "Brian!"
    What is your name? <Control-C>

### `if`

The `if` operation lets us perform specific instructions when a particular
condition is true by branching control. At our level of expertise, that
branching is performed with `goto`. So for us, the general `if` syntax looks
like this:

    if <conditional> goto <LABEL>

Let's see `if` in action by adding a little control logic to our name
prompt.

    # example-03-04.pir
    .sub 'main' :main
        .const string PROMPT = "What is your name? "
        .local string name
        .local string response
        .local pmc    stdin

        stdin = getstdin

        name = stdin.'readline_interactive'(PROMPT)
        if name == "Brian" goto GREETING_FOR_BRIAN
        response = "Hello, " . name
        goto SAY_IT

      GREETING_FOR_BRIAN:
        response = "Hey, Brian!"

      SAY_IT:
        say response

    .end

I admit it. This example is all about making me feel good. One greeting is prepared for users named Brian, while
another greeting is prepared for everybody else. The program accomplishes this by examining the value of `name`.
If `name` is "Brian", the program is instructed to `goto` the label `GREETING_FOR_BRIAN`. Otherwise it continues
on, preparing a generic response and going to the `SAY_IT` label. `GREETING_FOR_BRIAN` prepares a custom response
and follows up to the next instruction, which happens to be the `SAY_IT` code. Remember that labels are just markers.
They don't cut the labeled code off from the rest of your code.

#### Conditionals

The conditional in an `if` operation is checked to see if it looks false. The
conditional can be a simple variable, in which case the value of the variable
is examined. False looks a little different for each of the types.

For This Type | False looks like this 
--------------|----------------------
Integer       | `0`
Number        | `0.0`
String        | `""`, `"0"`

Anything that doesn't look false is considered true.

You can also use comparison operators to compare two values in your conditional.

    # example-03-05.pir
    .sub main :main
        .local int    a
        .local int    b
        .local pmc    stdin

        stdin = getstdin

        a = stdin.'readline_interactive'('a: ')
        b = stdin.'readline_interactive'('b: ')

        if a > b goto A_IS_GREATER
        if b > a goto B_IS_GREATER
        goto BOTH_EQUAL

    A_IS_GREATER:
        say "a is greater"
        goto END
    B_IS_GREATER:
        say "b is greater"
        goto END
    BOTH_EQUAL:
        say "a and b are the same"
        goto END

    END:
        say "Wasn't that fun?"
    .end

This little script grabs two values from the user and reports which one is greater -
or reports the special case when they are the same.

    $ parrot example-03-05.pir
    a: 5
    b: 10
    b is greater
    Wasn't that fun?

Here are the comparison operators that are available for your conditionals.

Operator   | Tests                                
-----------|-------------------------------------
`a == b`   | Are `a` and `b` the same value?    
`a !== b`  | Are `a` and `b` different values?  
`a > b`    | Is `a` greater than `b`?           
`a < b`    | Is `a` less than `b`?              
`a >= b`   | Is `a` greater than or equal to `b`?
`a <= b`   | Is `a` less than or equal to `b`?   

What about having multiple tests? For example, maybe you will only accept
a number if it's within a certain range. Parrot does not let us chain 
comparisons, but we can still use multiple tests with the `and` and `or`
opcodes.

    # example-03-06.pir
    .sub main :main
        .const int MINIMUM = 10
        .const int MAXIMUM = 100
        .local int input
        .local int input_is_valid
        .local pmc stdin

        stdin = getstdin

    GET_NUMBER:
        print "Enter a number ("
        print MINIMUM
        print " - "
        print MAXIMUM
        print ")"
        input = stdin.'readline_interactive'(': ')
        $I0 = input >= MINIMUM
        $I1 = input <= MAXIMUM
        input_is_valid = and $I0, $I1
        if input_is_valid goto VALID_INPUT
        say "That is not in the acceptable range!"
        goto END_PROGRAM

      VALID_INPUT:
        say "That is in the acceptable range."

      END_PROGRAM:
        say "Thank you!"
    .end

`and` compares its arguments, and returns true if the arguments all look true.
Parrot lets you store test results in a variable, as you can see. Then you can
examine the truthiness of the variable in your `if` condition.

    $ parrot example-03-06.pir
    Enter a number (10 - 100): 990
    That is not in the acceptable range!
    Thank you!
    $ parrot example-03-06.pir
    Enter a number (10 - 100): 82
    That is in the acceptable range.
    Thank you!

This approach looked odd enough to me that I thought I'd show the equivalent
Perl code.

This Parrot code:

      $I0 = input >= MINIMUM
      $I1 = input <= MAXIMUM
      input_is_valid = and $I0, $I1
      if input_is_valid goto VALID_INPUT
      say "That is not in the acceptable range!"
      goto END_PROGRAM

    VALID_INPUT:
      say "That is in the acceptable range."

    END_PROGRAM:
      say "Thank you!"

is roughly equivalent to the following Perl code:

``` perl
if ($input >= $MINIMUM && $input <= $MAXIMUM) {
    say "That is in the acceptable range.";
} else {
    say "That is not in the acceptable range.";
}

say "Thank you!";
```

We could also use `or`, which compares its arguments and returns true if *either*
argument looks true.

    # example-03-07.pir
    .sub 'main' :main
        .const int MINIMUM = 10
        .const int MAXIMUM = 100
        .local int input
        .local int input_is_invalid
        .local pmc stdin

        stdin = getstdin

    GET_NUMBER:
        print "Enter a number ("
        print MINIMUM
        print " - "
        print MAXIMUM
        print ")"
        input = stdin.'readline_interactive'(': ')
        $I0 = input <= MINIMUM
        $I1 = input >= MAXIMUM
        input_is_invalid = or $I0, $I1
        if input_is_invalid goto WARN_USER_ABOUT_INPUT
        goto END_PROGRAM

    WARN_USER_ABOUT_INPUT:
        say "That is not in the acceptable range!"

    END_PROGRAM:
        say "Thank you!"
    .end

### `unless`

Sometimes the normal `if` test does not clearly describe your needs. You 
may only want to branch if a test fails. While you *can* do this with `if`,
Parrot also provides the `unless` test for exactly this situation. `unless`
looks similar to `if`:

    unless <conditional> goto <LABEL>

I can use it in the user prompt program to streamline the description of
the application's response to anyone but me.

    # example-03-08.pir
    .sub main :main
        .const string PROMPT = "What is your name? "
        .local string name
        .local string response
        .local pmc    stdin

        stdin = getstdin

        name = stdin.'readline_interactive'(PROMPT)
        unless name == "Brian" goto GENERIC_GREETING
        response = "Hey, Brian!"
        goto SAY_IT

      GENERIC_GREETING:
        response = "Hello, " . name

      SAY_IT:
        say response
    .end

The program will run the same after this little change. Try it and see.

Usage of `unless` is a personal choice. I like it because it lets me describe
my program a little more concisely. Others don't like to use `unless` because
it adds to the mental load of reading application code: "let's see, `unless` 
means '`if` this is not true." Both points of view are valid, and ultimately
it's up to you whether `unless` belongs in your code.

### Repetition

We saw the infinite loop earlier when we first looked at `goto`. Let's
explore more controlled loops.

Believe it or not, the combination of `if` and `goto` provide us with the
core features we need for a wide range of control structures. Things can
get interesting now that we've added these tools to our kit.

How about a countdown?

    # example-03-09.pir
    .sub 'main' :main
        .const int start = 10
        .const int stop  = 0
        .local int current

        current = start
      COUNTDOWN:
        if current < stop goto LIFTOFF
        say current
        current -= 1
        goto COUNTDOWN

      LIFTOFF:
        say "Liftoff!"
    .end

This presents a simple count-controlled loop. We set a loop counter `current` to a reasonable start value before we
start looping. We check the value of the loop counter each time we start the loop, quitting if `current` is less
than our stopping value. After our check, we display the value, subtract one, and run the loop again.

A condition-controlled loop is easy, too.

    # example-03-10.pir
    .sub main :main
        .const string PROMPT = "What is your name? "
        .local string name
        .local string response
        .local pmc    stdin

        stdin = getstdin

    GET_NAME:
        name = stdin.'readline_interactive'(PROMPT)
        if name goto GREET_USER
        goto GET_NAME

    GREET_USER:
        response = "Hello, " . name
        say response
    .end

Our script will now continue to check to see if the user actually entered
anything for a name. If the user has entered a name, control goes to
the `GREET_USER` label. Otherwise, control is sent backwards to the 
`GET_USER` label.

    $ parrot example-03-10.pir
    What is your name? 
    What is your name? Brian
    Hello, Brian

Collection loops such as list iterators will have to wait until we examine PMCs.

## Summary

Adding `if` and `goto` to our toolkit has given us the means to build fundamental
control structures in our Parrot programs. We know how to use simple conditionals
as well as how to create more complex conditionals using `and` and `or`. We have
`unless` for those situations when `if` doesn't describe our intent clearly 
enough. We can use the simple combination of `if` and `goto` to create counter
and condition controlled loops. A really determined person could create useful 
programs with just this information. However, even simple useful
programs would benefit from using the library of PMCs that are available.