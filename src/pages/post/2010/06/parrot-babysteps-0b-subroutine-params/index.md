---
aliases:
- /coolnamehere/2010/06/15_0b-subroutine-params.html
- /post/2010/0b-subroutine-params/
- /2010/06/15/parrot-babysteps-0b-subroutine-params/
category: coolnamehere
date: 2010-06-15 00:00:00
layout: layout:PublishedArticle
series:
- Parrot Babysteps
slug: parrot-babysteps-0b-subroutine-params
tags:
- parrot
- learn
title: Parrot Babysteps 0b - Subroutine Params
updated: 2011-04-11 00:00:00
uuid: 0971c043-f2ff-44cf-a018-92c12ce2ff51
---

[Subroutines chapter]: http://docs.parrot.org/parrot/latest/html/docs/book/pir/ch06_subroutines.pod.html
[First]: /post/2009/10/parrot-babysteps-06-files-and-hashes
[Second]: /post/2009/10/parrot-babysteps-07-writing-subroutines
[testing]: /post/2009/12/parrot-babysteps-08-testing-with-testmore
[larger projects]: /post/2010/04/parrot-babysteps-09-simple-projects
[Parrot]: /tags/parrot/
[Perl]: /tags/perl/
[Stellar project]: /post/2010/06/parrot-babysteps-0a-the-stellar-project

It's time to treat the star database like a database. Well, it's time to treat
it like something we can search, anyways. I know this is not a trivial task in
Parrot, so the Babysteps have been building up to it slowly. [First][], we
figured out how to read from the database file and display its contents in a
meaningful fashion. [Second][], we added subroutines to massage the data a
little and produce some usable names for the thousands of stars in the database
that do not have proper names. Then we suddenly spun off in a seemingly random
direction, talking about [testing][] and setting up [larger projects][]. That
was intentional, though. This sort of project requires more work in [Parrot][] than in
a language like [Perl][], due to Parrot's lower-level nature. I wanted to be
sure we could test this application as we add search functionality. We just
pushed our script into the [Stellar project][] to get that testing foundation.

First I am going to describe what is being built, then I'm going to work on the
very important detail of examining a single star. We'll have to wait until the
next Baby Step before we start searching the catalog.

## Thinking Through The Problem

We could start by creating a simple search function, testing every line in the
HYG Catalog and verifying the results by hand. That will obviously not work.
Part of the reason we have been writing this is because the catalog is not
easily read without a little computer help.

It might be a better idea to take a smaller set and search against it. How small
is good enough? A thousand? A hundred? Ten? We could reasonably start
by searching a set of one star. It is certainly easy to manage. Okay, so we'll
start with a set of one star.

What do I mean when I talk about searching through the catalog? The basic idea
is that we have a catalog of stars and some conditions, like "the ProperName
is 'Sol'." We build a list of matches by examining each star, seeing if the
conditions are true for that star. If they are, then that star goes in the list
of matches. Either way, we then move on to the next star.

How do we determine if a single star is a match? Okay, we have a single star and
some conditions. We determine if the star is a match by testing each condition.
We can stop testing when we find a condition that is not true or we have run out
of conditions to test. We know that this star is a match if every condition we
tested was true.

There are a lot of technical details that we would think about if this code was
intended for use in the real world. Large match lists could use a lot of memory.
The conditions would need to allow for ranges or approximate matches.
Luckily, this code is not indented for use in the real world. I can be as clumsy
as I want, as long as my program gives the right answer.

## Writing Code

Now we're ready to go back to the `stellar` project and write some code.

### Testing a Condition

Our first approach to checking a star's details will be to check a single field.
The star `ProperName` is a good field to start with:

    # example-0b-01/t/04-check-star.t
    .include 'lib/stellar.pir'

    .sub 'main' :main
        .include 'test_more.pir'
        .local string header_string
        .local string star_string
        .local string delimiter
        .local pmc    header_fields
        .local pmc    star

        header_string = "StarID,HIP,HD,HR,Gliese,BayerFlamsteed,ProperName,RA,Dec,Distance,PMRA,PMDec,RV,Mag,AbsMag,Spectrum,ColorIndex,X,Y,Z,VX,VY,VZ"
        delimiter = ","
        star_string = "0,,,,,,Sol,0,0,0.000004848,0,0,0,-26.73,4.85,G2V,0.656,0,0,0,0,0,0"

        plan(2)

        header_fields = split delimiter, header_string
        star = extract_from_csv_line(star_string, header_fields, delimiter)
        $S0 = 'Sol'

        $I0 = check_star_proper_name(star, 'Sol')
        ok($I0, 'Sol should have ProperName of "Sol"')
        $I0 = check_star_proper_name(star, 'Arcturus')
        nok($I0, 'Sol should not have ProperName of "Arcturus"')
    .end

`check_star_proper_name` is an easy sub to write. My version is more verbose
than necessary, to be honest:

    # example-0b-01/lib/stellar.pir

    # ...

    .sub check_star_proper_name
        .param pmc    star
        .param string desired_value
        .local string actual_value
        .local int    check_result

        actual_value = star['ProperName']
        check_result = desired_value == actual_value
        .return(check_result)
    .end

[Remember]: /post/2009/07/parrot-babysteps-02-variables-and-types

The sub returns the result of comparing our desired `ProperName` with the actual
value held in the `star`. I rely on Parrot to do the right thing when comparing
`desired_value` with `actual_value`. [Remember][] that Parrot automatically
handles any type conversions, so we can ignore type for now.

### Revisiting the `header_string`

I want to stop for a moment and look at my tests. One annoying fact is that
every single test file includes the full `header_string` and `delimiter`. That
is explicit behavior, which I like. Then again, it is also cluttering up my
tests. The headers never change, yet I always include them. What if I could make
the header string and delimiter optional?

I *can* make those parameters optional. Let's reopen the test file `03-extract-from-csv.t`.

    # example-0b-02/03-extract-from-csv.t
    .sub main ':main'
        # ...
        plan(4)
        # ...
        star = extract_from_csv_line(star_string, header_fields)
        $S0 = summarize_star(star)
        is($S0, summary, "delimiter should be optional")

        star = extract_from_csv_line(star_string)
        $S0 = summarize_star(star)
        is($S0, summary, "header_fields should be optional")
    .end

How do we make those fields optional? We use the parameter modifiers `:optional`
and `:opt_flag`.

    .sub extract_from_csv_line
        .param string star_string
        .param pmc    header_fields     :optional
        .param int    has_header_fields :opt_flag
        .param string delimiter         :optional
        .param int    has_delimiter     :opt_flag

        if has_delimiter goto CHECK_HEADER_FIELDS
        delimiter = ','
      CHECK_HEADER_FIELDS:
        if has_header_fields goto BEGIN_EXTRACTING
        .local string header_string
        header_string = "StarID,HIP,HD,HR,Gliese,BayerFlamsteed,ProperName,RA,Dec,Distance,PMRA,PMDec,RV,Mag,AbsMag,Spectrum,ColorIndex,X,Y,Z,VX,VY,VZ"
        header_fields = split delimiter, header_string

      BEGIN_EXTRACTING:
        .local pmc    star_fields
        .local pmc    star

        star_fields = split delimiter, star_string
        star = extract_star_details(header_fields, star_fields)

        .return(star)
    .end

The `:optional` modifier makes sense. Use it to tell Parrot that a particular
parameter is not required for the sub to perform its duties. `:opt_flag` might
require a little bit of explanation, though. It is a bookkeeping parameter
provided by Parrot to let you know whether or not the preceding optional
parameter was provided by the caller. You test the flag to see if the optional
parameter was set. The name of the flag doesn't matter.

    # example-0b-03.pir
    .sub 'main' :main
        .local string eggs
        .local string topping 
        .local string order

        eggs = 'over easy'
        topping = "Frank's RedHot"

        order = breakfast(eggs, topping)
        say order

        order = breakfast(eggs)
        say order
    .end

    .sub breakfast
        .param string eggs
        .param string topping   :optional
        .param int    has_stuff :opt_flag

        .local string breakfast_order
        breakfast_order = 'Eggs cooked ' . eggs

        unless has_stuff goto SERVE_BREAKFAST
        breakfast_order .= ' topped with '
        breakfast_order .= topping

      SERVE_BREAKFAST:
        .return(breakfast_order)
    .end

This program executes without a hitch. There is nothing important about the name
of the flag.

    $ parrot example-0b-03.pir
    Eggs cooked over easy topped with Frank's RedHot
    Eggs cooked over easy
 
Order *does* matter, though. You always want to put the flag after the optional
parameter in your `.param` directives, or bad things will happen.

    # example-0b-04.pir
    .sub 'main' :main
        .local string eggs
        .local string topping 
        .local string order

        eggs = 'over easy'
        topping = "Frank's RedHot"

        order = breakfast(eggs, topping)
        say order

        order = breakfast(eggs)
        say order
    .end

    .sub breakfast
        .param string eggs
        .param int    has_stuff :opt_flag
        .param string topping   :optional

        .local string breakfast_order
        breakfast_order = 'Eggs cooked ' . eggs

        unless has_stuff goto SERVE_BREAKFAST
        breakfast_order .= ' topped with '
        breakfast_order .= topping

      SERVE_BREAKFAST:
        .return(breakfast_order)
    .end

See?

    $ parrot example-0b-04.pir
    Eggs cooked over easy
    too few positional arguments: 1 passed, 2 (or more) expected
    current instr.: 'breakfast' pc 34 (example-0b-04.pir:19)
    called from Sub 'main' pc 26 (example-0b-04.pir:15)

Back to `stellar`. `extract_from_csv_line` can work the headers out for itself now. Let's clean up
our test code.

    # example-0b-05/t/04-check-star.t
    .sub 'main' :main
        .include 'test_more.pir'
        .local string header_string
        .local string star_string
        .local string delimiter
        .local pmc    header_fields
        .local pmc    star

        star_string = "0,,,,,,Sol,0,0,0.000004848,0,0,0,-26.73,4.85,G2V,0.656,0,0,0,0,0,0"
        star = extract_from_csv_line(star_string)

        plan(2)

        $I0 = check_star_proper_name(star, 'Sol')
        ok($I0, 'Sol should have ProperName of "Sol"')
        $I0 = check_star_proper_name(star, 'Arcturus')
        nok($I0, 'Sol should not have ProperName of "Arcturus"')
    .end

It is a little easier now to tell what I am actually testing in this code. Good.
I know I should be all methodical and orderly about checking my star fields, but
I have not had enough sleep for that to be practical. Let's check `Spectrum`.

    # example-0b-06/t/04-check-star.t

    .sub 'main' :main
        # ...
        plan(4)
        # ...
        $I0 = check_star_spectrum(star, 'G2V')
        ok($I0, 'Sol should have Spectrum of "G2V"')
        $I0 = check_star_spectrum(star, 'K3V')
        nok($I0, 'Sol should not have Spectrum of "K3V"')
    .end

Meanwhile, in `stellar.pir`:

    # example-0b-06/lib/stellar.pir
    .sub check_star_spectrum
        .param pmc star
        .param string desired_value
        .local string actual_value
        .local int check_result

        actual_value = star['Spectrum']
        check_result = desired_value == actual_value
        .return(check_result)
    .end

This works perfectly, but compare `check_star_spectrum` to
`check_star_proper_name`. They are almost identical. In fact, the only difference between
the code for the two subs is which field gets grabbed for `actual_value`.
It seems to me that the same behavior could be described by a single sub.

    # example-0b-06/t/04-check-star.t
    .sub 'main' :main
        # ...

        plan(8)

        # ...

        $I0 = check_star_field(star, 'ProperName', 'Sol')
        ok($I0, 'Sol should have ProperName of "Sol"')
        $I0 = check_star_field(star, 'ProperName', 'Arcturus')
        nok($I0, 'Sol should not have ProperName of "Arcturus"')
        $I0 = check_star_field(star, 'Spectrum', 'G2V')
        ok($I0, 'Sol should have Spectrum of "G2V"')
        $I0 = check_star_field(star, 'Spectrum', 'K3V')
        nok($I0, 'Sol should not have Spectrum of "K3V"')
    .end

`check_star_field` looks like a generic version of `check_star_proper_name` and
`check_star_spectrum`.

    # example-0b-06/lib/stellar.pir

    # ...

    .sub check_star_field
        .param pmc star
        .param string field
        .param string desired_value
        .local string actual_value
        .local int check_result

        actual_value = star[field]
        check_result = desired_value == actual_value
        .return(check_result)
    .end

All tests are still passing. You *are* working along with me and running tests,
right? It's time to decide what to do with those specific subs now that we have
a nice general purpose field checker. You could argue that those subs should
stick around but as wrappers that call `check_star_field`. That is entirely
reasonable. I am comfortable using the general purpose sub as my main checker,
though. I will delete the specific subs and their tests in my code.

### Testing Multiple Conditions

`stellar` does a convincing job of checking a single field in a star. The next
step is figuring out how to check multiple fields.

    # example-0b-07/t/04-check-star.t
    .include 'lib/stellar.pir'

    .sub 'main' :main
        .include 'test_more.pir'
        .local string header_string
        .local string star_string
        .local string delimiter
        .local pmc    header_fields
        .local pmc    star

        star_string = "0,,,,,,Sol,0,0,0.000004848,0,0,0,-26.73,4.85,G2V,0.656,0,0,0,0,0,0"
        star = extract_from_csv_line(star_string)

        plan(9)

        $I0 = check_star_field(star, 'ProperName', 'Sol')
        ok($I0, 'Sol should have ProperName of "Sol"')
        $I0 = check_star_field(star, 'ProperName', 'Arcturus')
        nok($I0, 'Sol should not have ProperName of "Arcturus"')
        $I0 = check_star_field(star, 'Spectrum', 'G2V')
        ok($I0, 'Sol should have Spectrum of "G2V"')
        $I0 = check_star_field(star, 'Spectrum', 'K3V')
        nok($I0, 'Sol should not have Spectrum of "K3V"')

        $I0 = check_star(star, 'ProperName', 'Sol')
        ok($I0, 'Sol should have ProperName "Sol"')
        $I0 = check_star(star, 'ProperName', 'Sol', 'Spectrum', 'G2V')
        ok($I0, 'Sol should have ProperName "Sol" and Spectrum "G2V"')
        $I0 = check_star(star, 'ProperName', 'Arcturus', 'Spectrum', 'G2V')
        nok($I0, 'Sol should not have ProperName "Arcturus" and Spectrum "G2V"')
        $I0 = check_star(star, 'ProperName', 'Sol', 'Spectrum', 'K3V')
        nok($I0, 'Sol should not have ProperName "Sol" and Spectrum "K3V"')
        $I0 = check_star(star, 'ProperName', 'Arcturus', 'Spectrum', 'K3V')
        nok($I0, 'Sol should not have ProperName "Arcturus" and Spectrum "K3V"')
    .end

Yes, I did go through several variations on testing multiple fields. I wanted to
make sure that `check_star` behaved *exactly* the way I expected. How am I going
to make those tests succeed?

#### `:slurpy` and `:flat` Save the Day

Parrot gives us two excellent modifiers that simplify the job of checking
multiple fields. The `:slurpy` param modifier to effectively say "Oh,
there might be some other params. Just put them in an array." The flip side of
that is the `:flat` modifier in subroutine calls, which lets us say "Oh, I have
this array of stuff. Just tack its elements to the param list for the sub I'm
about to call."

Enough imaginary dialog. Here's what `check_star` looks like.

    # example-0b-07/lib/stellar.pir
    .sub check_star
        .param pmc    star
        .param string field
        .param string desired_value
        .param pmc    extra_fields :slurpy
        .local int    match_result
        .local int    extra_field_count

        match_result = check_star_field(star, field, desired_value)

        # We're done if this match fails.
        unless match_result goto RETURN_RESULT

        extra_field_count = extra_fields
        # We're done if there are no extra fields.
        unless extra_field_count goto RETURN_RESULT

        # Grab the result of checking the extra fields.
        match_result = check_star(star, extra_fields :flat)

      RETURN_RESULT:
        .return(match_result)
    .end

I tried to make it clear what was going on the comments. `check_star` is given a
star and a handful of conditions. It only cares about the first condition, and
stuffs the rest into `extra_fields`. If the first condition fails, we're done.
There's no point in checking any more fields, so jump down to return the failure. 
If there are no other conditions to check - which we determine by looking at 
the size of `extra_fields` - we return the result, which should be a success.

If there *are* more conditions to check, we call `check_star` again, using the
star and the conditions we had stuffed into `extra_fields`. That goes through
the same process of testing and looking for extra conditions until it has
completed the last test. The result of all the completed tests is handed back to
`check_star`, which then hands it back to us. 

[recursion]: http://en.wikipedia.org/wiki/Recursion_(computer_science)

This process of [recursion][] -
solving a complex problem by breaking it down into small problems - is common in
many programming languages, so it is supported by Parrot. After all, Parrot is
supposed to be used for creating new languages. It is not just for
browsing some guy's star catalog.

[tail call]: http://en.wikipedia.org/wiki/Tail_call

The "[tail call][]" pattern of evaluating a sub and immediately returning its result is so
common that Parrot provides the `.tailcall` directive to optimize its
behavior. `.tailcall` essentially tells Parrot to immediately return the result
of evaluating the sub rather than storing it in memory. It may not do much in a
case like `check_star`, but you should see a difference in complex problems.

Then again, it might help `check_star` immensely. I don't really know about 
Parrot optimization effects yet.

    # example-0b-08/lib/stellar.pir
    .sub 'main' :main
        # ...

        # Return the result of checking the extra fields.
        .tailcall check_star(star, extra_fields :flat)

      RETURN_RESULT:
        .return(match_result)
    .end

## Conclusion

We can now examine multiple fields to determine if a star matches a description
we've provided. Along the way, we explored subroutine parameters. We learned how
to make a parameter optional. We learned how to grab all of a subroutine's
params and stuff them into a list. We also learned how to paste the contents of
a list onto the parameters of a subroutine call. We even dabbled in
[recursion][], the fine art of breaking a big problem down with small solutions.

In our next step, we will use `check_star` to search through sets of stars.
That's the part I've been looking forward to for a while! 

In the meantime, continue your own [Parrot][] exploration. You might review the 
Parrot [Subroutines chapter][] a little more. I hardly left that page while 
working through this step. Whatever you do, remember to have fun!