---
aliases:
- /coolnamehere/2009/07/11_02-variables-and-types.html
- /post/2009/02-variables-and-types/
- /2009/07/11/parrot-babysteps-02-variables-and-types/
category: coolnamehere
date: 2009-07-11 00:00:00
layout: layout:PublishedArticle
series:
- Parrot Babysteps
slug: parrot-babysteps-02-variables-and-types
tags:
- parrot
- learn
title: Parrot Babysteps 02 - Variables and Types
updated: 2010-07-21 00:00:00
uuid: 8c69f18c-a428-41d0-b222-4980788db1ad
---

I've always felt that learning the core types of a platform is boring.
Once you've learned a few languages, you know the difference between an integer and a floating
point number, what a string is, and have a general idea for how you work with each of them. You
mainly care about the details of how you work with them in your new platform. It
is important to learn these details, though.

[the last step]: /post/2009/07/parrot-babysteps-01-getting-started

We already looked at variables when we wrote the simple "Hello, World" program 
in [the last step][].  We looked at the different variable 
types and the registers that Parrot uses to hold them. Today we're going to dive a 
little deeper into variables and types so that you can get the basic idea of what 
you can do with variables in Parrot. I won't be digging *too* deep, though.
In particular, I will be talking as little about PMCs as I can. It's just too much for where
we're at today.

## Variable Names

Names become important when you're using variables. Good names add documentation by
telling people who look at your code what a given variable is going to be used for. Parrot
has two naming schemes: one for register variables, and another for everything else.

### Register Variable Names

Register variable rules are easy to remember. First comes the register being used, then one or more
digits. 

    <register><identifier>

The registers are named with a dollar sign (`$`), then an upper case letter indicating what types are
held in that register:

Register | Type
---------|-------------------------
$I       | Integers
$N       | Numbers (decimal values)
$S       | Strings
$P       | Polymorphic Containers

I thought that the number after the register identifier was something that tells Parrot something
especially meaningful, like which slot it's using or something. Turns out that's not the case,
or at least not in quite the way I thought it was.

    #!parrot
    # example-02-01.pir
    .sub main :main
      $I01 = 10
      $I1  = 20
      say $I01
      say $I1
    .end

`01` and `1` are the same number according to the numbering systems that I'm familiar with.
Look what happens when you run it, though.

    $ parrot example-02-01.pir
    10
    20

So the numbers are just a sequence of characters identifying the variable for the register. They
don't indicate order or anything else. The register takes care of storing variables and lets you
use those numbers however you want. But if I see you `$I01` and `$I1` in your code without a good
reason I might have to slap you. Well, no. I will be disappointed, though.

I've already said that I prefer `.local` variables. They're more explicit than using the
register, and I've generally found that more explicit code is easier to read and maintain.
Nevertheless, register variables have a certain charm. You don't have to declare them, for starters.
Just say "Hey, set `$I1` to `10`" and move on to the next instruction. You also don't have to spend
any time coming up with a clever name. As long as *you* remember what the numbers mean
and document it somewhere, it's all good. That makes register variables ideal for short chunks of
code.

It does get confusing as your program grows larger or if you are like me and can quickly forget
what you were using a variable for. That's when `.local` variables become valuable.

### `.local` Variable Names

Local variables are more complicated than register variables, but they have additional features
which make them useful. I've already talked about how the names can be made meaningful. They
also only exist in the subroutine where they are defined, which is a lifesaver in large programs.
The format of a local variable declaration makes it easy to understand when you will be using
it and what you plan to use it for.

Local variables are declared with the `.local` directive, followed by a type identifier and finally
the name of the variable.

    .local <type-identifier> <name>

[previous step]: /post/2009/07/parrot-babysteps-01-getting-started

I briefly described the type identifiers in the [previous step][], but here they are again.

Identifier | Type
-----------|------------------------
`int`      | integer
`num`      | number (decimal values)
`string`   | string
`pmc`      | Polymorphic container

Now for the name. It needs to start with a letter or underscore (`_`) character, and the rest
must only contain letters, digits, or underscores. Variable names are case sensitive, so
`year`, `YEAR`, and `Year` all describe different variables. A variable name may have any length, but
keep it reasonable. 

The only other rule to remember about variable names is that they may not be *reserved
words*. Reserved words have special meaning to Parrot, and it will complain
if you use one of them for your own nefarious ends. The list of reserved words is 
delightfully small.

* `goto`
* `if`
* `int`
* `null`
* `num`
* `pmc`
* `string`
* `unless`

[myself]: /post/2002/06/simple-types-in-python

I think I'll plagiarize [myself][] and reiterate
some of my old guidelines for variable names.

* Use descriptive names rather than abbreviations or inside jokes. 
  When you are naming a variable that holds the radius of a circle, 
  it is usually better to use `radius` than `r` or `halfway_there`
* Use a name that indicates what the variable will be used for. 
  `radius` is much better than `fnord` for describing the radius of a 
  circle. *(plus, `fnord` breaks the "no inside jokes" guideline)*
* Constant variables are often indicated by having the name be in
  all upper case letters.
* Find a balance between names that are too long or too short.
      * *Too short* might be `n`
      * *Too long* might be `name_of_my_favorite_customer_in_walla_walla_washington`
      * *Just right* might be `name` or `customer_name`
* Then again, it's okay to bend the guidelines in favor of common terms. If 
  you are writing code to figure out the distance between two points, 
  then `x1, y1, x2,` and `y2` are perfectly sensible identifiers. And maybe `r`
  isn't always a bad idea for `radius`. Use your own judgment.

I break these guidelines sometimes, but at least I think about it before I do.

#### Assignment

Remember that declaring a local variable and assigning a value to it are two different actions, and
require two separate instructions.

    #!parrot
    # example-02-02.pir
    .sub main :main
      .local int year
      year = 2010
      say year
    .end

## `.const` Variables

Actually, that earlier guideline about constant variables reminded me: Parrot has a directive
for declaring and assigning a value for a local constant variable. Use the `.const` 
directive when you want a variable that won't somehow change in value after you've 
created it.

    .const <type-identifier> <name> = <value>

Here's an example of `.const` in action: calculating the area of a circle with
a radius of 10 units.

    #!parrot
    # example-02-03.pir
    .sub main :main
      .const num PI     = 3.14159
      .const num RADIUS = 10
      .local num area

      print "Radius: "
      say RADIUS

      # Area of a circle: PI * RADIUS * RADIUS
      area  = PI
      area *= RADIUS
      area *= RADIUS
      print "Area: "
      say area
    .end

`PI` and `RADIUS` are the constants in this program. We define them once and never
need to change them again. Area, on the other hand, is a local because it needs 
to be touched several times to get the final value.

    $ parrot example-02-03.pir
    Radius: 10
    Area: 314.159

<aside markdown="1">

This is where developers experienced with other languages should see the
low-level nature of PIR. Those operators correspond to opcodes, and PIR only wants
to see one opcode per statement. That's why the formula is broken down into distinct
steps.

</aside>

I think we've got a solid grip on declaration and basic usage of both local and
register variables. On to the types.

## Variable Types

You know what the types are: integers, numbers, strings, and polymorphic containers.
You also know the rough outline of what they look like.

### Numeric Types

When you need to do math, it's time for integers and numbers. 

#### Integers

Integers are whole numbers such as `3`, `94`, and `-48183`. They are signed, which 
means that you can create positive or negative values. Each integer takes up the same
amount of memory. How much memory do they take up? Well, that depends on your system and
how Parrot was compiled. 32-bit Parrot uses 4 bytes for integers, while it's 
presumably 8 bytes on 64-bit Parrot. The 
[`sysinfo`](http://docs.parrot.org/parrot/latest/html/src/dynoplibs/sys.ops.html) opcode can tell us for sure.

    #!parrot
    # example-02-04.pir
    .loadlib 'sys_ops'
    .include 'sysinfo.pasm'

    .sub 'main' :main
        $I0 = sysinfo .SYSINFO_PARROT_INTSIZE
        print $I0
        say " bytes in an integer on this machine"
    .end

Parrot keeps only the most important opcodes in its core. A question like "how many bytes are in an integer?"
is just not considered all that important most of the time. The `.loadlib` directive allows us to load
special Parrot bytecode libraries that have been compiled so that they are more efficient on the virtual
machine. The `.include` directive lets us use code that is written in PIR but has not been compiled or
otherwise treated in any special way. There are fine differences between them, but I think that's the
important one. We will often use the `.loadlib` and `.include` directives to grab functionality that is not 
available in core Parrot. 

What does this code tell us?

    $ parrot example-02-04.pir
    4 bytes in an integer on this machine

I'm using a 32-bit Parrot, which gives my integers a range of `-2,147,483,648` to `2,147,483,647`.
That will be more than sufficient for our purposes, and there's the [`BigInt` 
PMC](http://docs.parrot.org/parrot/latest/html/src/pmc/bigint.pmc.html) for those days when
we need truly huge integers.

Most often you'll create integers using the 10-based system, but every once in a while it will
be more informative to use base 8, base 16, or even binary. Parrot supports that.

    #!parrot
    # example-02-05.pir
    .sub main :main
        $I0 = 10   # decimal (base 10)
        say $I0
        $I0 = 0o10 # octal (base 8)
        say $I0
        $I0 = 0x10 # hexadecimal (base 16)
        say $I0
        $I0 = 0b10 # binary (base 2)
        say $I0
    .end

Now I can see the value described by `10` in decimal, octal, hex, and binary. My life
is complete.

    $ parrot example-02-05.pir
    10
    8
    16
    2

That wasn't as fulfilling as I'd hoped. Perhaps my life is not complete after all.
I might as well move on to floating point numbers.

#### Numbers

The Number type is used by Parrot to represent [floating point 
values](http://en.wikipedia.org/wiki/Floating_point). These are
more or less the same as the decimal numbers you may be more familiar with. 

Like integers, numbers may be positive or negative and have a range that depends on their
size. `sysinfo` can get that size for us.

    #!parrot
    # example-02-06.pir
    .loadlib 'sys_ops'
    .include 'sysinfo.pasm'

    .sub 'main' :main
        $I0 = sysinfo .SYSINFO_PARROT_FLOATSIZE
        print $I0
        say " bytes in a number on this machine"
    .end

Now we know how much space is used for a number in Parrot.

    $ parrot example-02-06.pir
    8 bytes in a number on this machine

What does that mean, though? Integers are easy: 4 bytes is 32 bits is somewhere over 4 billion
possible values. With numbers - well, I have no idea really. The range is "some insanely small
value" to "some insanely big value". Look at Wikipedia's entry on [double precision
floating point](http://en.wikipedia.org/wiki/Double_precision) if you really want to know.

You can use ordinary decimal values or scientific notation for number values.

    #!parrot
    $N0 = 3.1415926
    $N1 = 6.0221415e+23

What can you do with numbers?

#### Numeric Operators and Opcodes

Operators in PIR provide a convenient and fairly readable shorthand for opcode instructions. It's
generally easier for me to remember `sum = a + b` than `add sum, a, b`. If the second option is
more readable for you, that's great! It's not for me.

There are many operators, but here are what I think of as the core operators for dealing with numbers.

Operator | Opcode | Action
---------|--------|---------------------
`=`      | `set`  | assign a value
`*`      | `mul`  | multiply
`/`      | `div`  | divide
`+`      | `add`  | add
`-`      | `sub`  | subtract
`*=`     | `mul`  | multiply and assign
`/=`     | `div`  | divide and assign
`+=`     | `add`  | add and assign
`-=`     | `sub`  | subtract and assign

Just for laughs - and to see how the operators fill in for opcodes - let's rewrite the 
area program using opcodes and register variables instead of operators, local variables,
and constants.

    #!parrot
    # example-02-07.pir
    .sub main :main
        set $N0, 3.14159
        set $N1, 10

        print "Radius is "
        say $N1

        # Calculate the area.
        set $N2, $N0
        mul $N2, $N1
        mul $N2, $N1
        print "Area is "
        say $N2
    .end

Actually, this isn't all that hard to read. Still, the operators are more 
familiar to me and I'm more comfortable with variables that have names. I'll
continue using them. Parrot doesn't care.

Let's have a little fun and add interaction to our original area calculator.

    #!parrot
    # example-02-08.pir
    .sub main :main
        .const num PI = 3.1415926
        .const string PROMPT = "Radius: "

        .local num radius
        .local num area
        .local pmc stdin

        stdin = getstdin
        radius = stdin.'readline_interactive'(PROMPT)
        area = PI
        area *= radius
        area *= radius
        print "Area: "
        say area
    .end

For some reason, adding user interaction always makes a program seem more entertaining to me. Even
a silly program that figures out something you could use a calculator for.

    $ parrot example-02-08.pir
    Radius: 10
    Area: 314.15926

#### Type Conversion

I'm not sure if you noticed, but I didn't bother converting the user input to a number
before assigning it to `radius`. Oh, you noticed? You get a gold star.

The `=` operator takes care of such conversions automatically, allowing you to do things like
get a string of input text from the user and treat it as the radius of a circle without having
an intermediate step of using a temporary string variable to hold the user input. Actually, the
more I think about what it would take to convert a string to an integer or floating point
number, the happier I am that Parrot does it for me. PIR isn't exactly a [low level
language](http://en.wikipedia.org/wiki/Low-level_programming_language), even though it is
lower than what I'm used to.

#### Opcodes For Integers

I won't be playing with them much today, but I thought you should know that there are [many 
math-related opcodes](http://docs.parrot.org/parrot/latest/html/src/ops/math.ops.html).

#### Hypotenuse Finder

Here's a little program to find the hypotenuse of a triangle. Maybe you remember the 
[Pythagorean theorem](http://en.wikipedia.org/wiki/Pythagorean_theorem) from school:

> In any right triangle, the area of the square whose side is the hypotenuse (the 
> side opposite the right angle) is equal to the sum of the areas of the squares 
> whose sides are the two legs (the two sides that meet at a right angle).

The formula looks like this:

> c&sup2; = a&sup2; + b&sup2;

Calculating the hypotenuse is easy once we notice that there is a `sqrt` opcode for
finding the square root of a number.

    #!parrot
    # example-02-09.pir
    .sub main :main
        .local num a
        .local num b
        .local num c
        .local num a_squared
        .local num b_squared
        .local num c_squared
        .local pmc stdin

        stdin = getstdin
        a = stdin.'readline_interactive'('A: ')
        b = stdin.'readline_interactive'('B: ')
        a_squared = a * a
        b_squared = b * b
        c_squared = a_squared + b_squared
        c = sqrt c_squared
        print "Hypotenuse: "
        say c
    .end

Don't look at me like that. Using a letter for a variable name makes perfect sense if you're
writing code that follows a well-established formula.

I did have to add specific variables to hold the squared values, because as far as I
can tell PIR does not support chained math operations. On the other hand, I did get to
save a lot of effort with the `sqrt` opcode. I didn't even have to import a library. 

    $ parrot example-02-09.pir
    A: 1
    B: 1
    Hypotenuse: 1.4142135623731

We've learned a lot about how math works in Parrot. We've seen some operators and even
looked at the math opcodes. Okay, a few. Okay, one. At least it's a start.

Let's move on from numbers to take a closer look at strings.

### Strings

We have been using [strings](http://en.wikipedia.org/wiki/String_%28computer_science%29) since
the first step, but I haven't spent much time describing them. That is because I have found them 
a little hard to explain. I can't stall any longer, though.

#### Basics

A string is basically a sequence of characters tied together and treated like a single thing.
There is [a *lot* more](http://en.wikipedia.org/wiki/String_%28computer_science%29) to strings.

Let's take the string "Hello". I see that as a word, but of course the computer doesn't understand
words the way we do. The computer sees a chain of symbols: "H", "e", "l", "l", and "o". Really, it
doesn't even see that. It sees a chain of integers that can be displayed as the phrase "Hello".

You know what? It doesn't really matter. Remember that strings are basically text, but the fact
that they aren't really text means we treat them in all sorts of strange ways later. We don't need
to worry about those strange treatments today. It's fine to say that a string is quoted text.

There are three ways to wrap your strings when assigning them:

* single quotes
* double quotes
* heredocs

Single-quoted strings are simple. Parrot assumes they are [ASCII 
encoded](http://en.wikipedia.org/wiki/ASCII), and very little magic happens when
processing them.

    #!parrot
    $S0 = 'Hello World!'

Double-quoted strings are a little more complex. Parrot assumes they are ASCII, but allows you
to set the encoding yourself. Double-quoted strings also handle several backslash escapes.
Encoding is easy in Parrot but I'm having a heck of a time getting Unicode to display on
my machines, so I'll skip encoding. I will talk about escapes in a few minutes.

    #!parrot
    $S1 = "Hello World!\n"

Heredocs are multi-line, which is a great convenience for larger strings. They can
act like single-quoted strings or double-quoted strings, depending on the way
they are created.

    #!parrot
      $S2 =<<"EndS2"
    Hello, World!
    Isn't it a lovely day?
    EndS2

If you like, we can whip up some quick code to show these string quoting methods in action.

    #!parrot
    # example-02-10.pir
    .sub main :main
        $S0 = 'Hello World!'
        $S1 = "Hello World!\n"
        $S2 =<<"EndS2"
    Hello, World!
    Isn't it a lovely day?
    EndS2

        say $S0
        say $S1
        say $S2
    .end

I don't think there are any surprises in this code.

    $ parrot example-02-10.pir
    Hello World!
    Hello World!

    Hello, World!
    Isn't it a lovely day?

So that's the basics of quoting. Now what about escapes?

#### Backslash Escapes

Backslash escapes make it possible for you to include normally unprintable characters
in a string. For example, they allow tabs and quotation marks to be part of your string:

    #!parrot
    # example-02-11.pir
    .sub main :main
        $S0 = "Question:\tAren't you sick of \"Hello World\"?\n"
        print $S0
    .end

See?

    $ parrot example-02-11.pir
    Question:  Aren't you sick of "Hello World"?

Here are my favorite backslash escapes:

Escape       | Description
-------------|------------
`\t`         | Inserts a tab
`\n`         | Inserts a newline
`\\`         | Inserts a backslash
`\"`         | Inserts a double quote in double-quoted strings
`\'`         | Inserts a single quote in single-quoted strings
`\a`         | Rings an alarm
`\xhh`       | Inserts character corresponding to the 2 byte hexadecimal value indicated by `hh`
`\uhhhh`     | Inserts character corresponding to the 4 byte hexadecimal value indicated by `hhhh`

There are more escape sequences, but I tend to ignore them.

Single quoted strings only escape `\\` and `\'`. Everything else is passed through unchanged.

#### String Operators

We've already worked with the major string operators, but here they are to review.

Operator | Opcode   | Action
---------|----------|---------------------
`=`      | `set`    | assign a value
`.`      | `concat` | concatenate two strings
`.=`     | `concat` | concatenate and assign

#### Opcodes For Strings

You will almost definitely want to explore the [string
opcodes](http://docs.parrot.org/parrot/latest/html/src/ops/string.ops.html).

#### Playing With String

We have already been doing some interesting things with strings. Well *I* think getting user
input and converting it to numbers is interesting. The opcodes open up the possibilities for
some more interesting statistics and transformations. 

    #!parrot
    # example-02-12.pir
    .sub main :main
        .const string PROMPT = "Enter some text: "
        .local string text
        .local int    text_length
        .local string transformed
        .local pmc    stdin

        stdin = getstdin
        text = stdin.'readline_interactive'(PROMPT)
        print "Number of characters: "
        text_length = length text
        say text_length
        print "Uppercase: "
        transformed = upcase text
        say transformed
        print "Lowercase: "
        transformed = downcase text
        say transformed
        print "Title case: "
        transformed = titlecase text
        say transformed
    .end

Granted, it doesn't do a whole lot.

    $ parrot example-02-12.pir
    Enter some text: BRian
    Number of characters: 5
    Uppercase: BRIAN
    Lowercase: brian
    Title case: Brian

Still, I think this shows that there is good reason to study those [string 
opcodes](http://docs.parrot.org/parrot/latest/html/src/ops/string.ops.html).

### PMCs

Uh, no. I'm not ready to describe polymorphic containers yet. You've already been using a PMC to
get user input, and that's quite complex enough for the moment. Eventually we'll explore the
[PMCs](http://docs.parrot.org/parrot/latest/html/pmc.html) - what's already available, how to 
use them, and how to define our own. Right now we're just getting into the basics of how to make
code run. As always, I encourage you to strike out on your own and explore the Parrot
documentation if you want to get ahead of what I've covered. I won't be offended. I'll be quite
pleased, in fact.

## Summary

We got the basics of variable handling and simple types out of the way. Thank goodness. Types can
be confusing, but now you know about integers, floating point numbers,
and strings. You understand the differences between them. You know how you would use them in your
own programs. If you use the opcodes available, you can get an incredible amount of power in
your Parrot programs. But so far, Parrot is nothing more than an awkward calculator for you.
You will want to look at labels and branching statements to start getting something interesting
out of Parrot.