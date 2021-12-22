---
aliases:
- /coolnamehere/2009/12/16_08-testing-with-test-more.html
- /post/2009/08-testing-with-test-more/
- /2009/12/16/parrot-babysteps-08-testing-with-testmore/
category: coolnamehere
date: 2009-12-16 00:00:00
layout: layout:PublishedArticle
series:
- Parrot Babysteps
slug: parrot-babysteps-08-testing-with-testmore
tags:
- parrot
- learn
title: Parrot Babysteps 08 - Testing With Test::More
updated: 2011-04-12 00:00:00
uuid: 9007f466-43ed-4da6-a472-17a765881e05
---

[Tapir]: http://github.com/leto/tapir
[Test Anything Protocol]: http://en.wikipedia.org/wiki/Test_Anything_Protocol
[Test::More]: https://github.com/parrot/parrot/blob/RELEASE_3_0_0/runtime/parrot/library/Test/More.pir
[test_more.pir]: https://github.com/parrot/parrot/blob/RELEASE_3_0_0/runtime/parrot/library/Test/More.pir

Co-written by [Jonathan "Duke" Leto](http://leto.net), Parrot core developer
and author of [Tapir][].
<!--more-->

## Introduction

I'll be creating more complex PIR programs soon, but first I want to stop for a minute and look at
testing in Parrot. Why? Code is a weird thing. You need to pin 
down its behavior as specifically as you can, or it'll become 
unreadable before you realize what's going on. Good tests help you describe
how your program should behave. Tests aren't a magic pill that will guarantee 
perfect programs, but they *will* help you check that your program behaves the 
way you claim it does.

There are many testing libraries in the programming world, but I will focus
on [Test::More][] for Parrot.

## Using Test::More to Write Tests

[Test::More][] is more or less an implementation of [Perl's 
Test::More](http://perldoc.perl.org/Test/More.html). It provides a set of simple
assertions such as `ok`, `is`, and `isnt`, along with a few testing-specific
commands like `skip` and `todo`. I'll be looking at some of those simple assertions, but
not spending so much time on the testing commands. This *is* a Babystep, after all.

Test::More is already included in the standard Parrot runtime, so we don't need
to do anything special to install it. Even better - there's a [test_more.pir][] include
file that you can include to import all of the important Test::More subroutines 
automatically.

Let's start writing tests.

### `plan`

Every test needs a plan. The `plan` subroutine in Test::More tells the world
one simple thing: how many tests are in this file. Accuracy is important,
because it's no fun when you are told to expect ten tests but only five run.
The other five might not have run for a number of reasons: the test script failed,
Parrot failed in some mysterious way, or you just forgot to mention that you
removed half of your tests.

We don't plan to have any tests yet, so let's be honest.

    # example-08-01.pir
    .sub 'main' :main
        .include 'test_more.pir'

        plan(0)
    .end

The `.include` directive will insert the contents of `test_more.pir` into the
subroutine, which saves us a lot of namespace wrangling. The testing starts
when a *plan* is declared.

Of course, this is *not* the most exciting test plan in the world to run.

    $ parrot example-08-01.pir
    $

What if we lie?

    # example-08-02.pir
    .sub 'main' :main
        .include 'test_more.pir'

        plan(10)
    .end

Running this is a little different.

    $ parrot example-08-02.pir
    1..10

Now Parrot is telling whoever cares that there will be ten tests in this file.
It's true that nothing exploded. For right now, you're going to have to trust me
when I say that honesty is the best policy. You'll see later that some tools
do care about how many tests you claim to run.

### `diag`

All right. Sometimes we want to make a comment in our test for the world to see.
We could just `say` what we want to say, but Test::More provides the `diag` 
subroutine to produce those comments in a manner that will make testers happy later.

    # example-08-03.pir
    .sub 'main' :main
        .include 'test_more.pir'

        plan(10)
        diag('There are no tests. The plan is a lie.')
    .end

What does this produce?

    $ parrot example-08-03.pir
    1..10
    # There are no tests. The plan is a lie.

See the `#`? That's supposed to make our diagnostic comment stand out from
the test results without confusing anyone. But the diagnostic makes me sad.
Let's write an actual test.

### `ok`

    # example-08-04.pir
    .sub 'main' :main
        .include 'test_more.pir'

        plan(1)
        ok(1, '`ok` tests for simple truth')
    .end

`ok` takes two arguments:

* The value you are testing
* A description of the test

The value being tested is obviously the most important part, but don't underestimate
the helpfulness of those descriptions. They are a form of documentation.

    $ parrot example-08-04.pir
    1..1
    ok 1 - `ok` tests for simple truth

[already saw]: /post/2009/09/parrot-babysteps-03-simple-control-structures

The test in `ok` is one of simple truth as seen by Parrot. We [already saw][]
that anything which looks like `0` or an empty string is considered false by Parrot,
while everything else is considered true.

What happens when we introduce a test that we know will fail?

    # example-08-05.pir
    .sub 'main' :main
        .include 'test_more.pir'

        plan(2)
        ok(1, '`ok` tests for simple truth')
        ok(0, '0 is false, so this should fail.')
    .end

You updated your plan, right? Anyways, let's see what this produces.

    $ parrot example-08-05.pir
    1..2
    ok 1 - `ok` tests for simple truth
    not ok 2 - 0 is false, so this should fail.

Oh hey, this is starting to get interesting! Now we can see clearly that the output
from `ok` is a line split into three parts:

* The result of the test: "`ok`" or "`not ok`"
* The test number
* Our description string

`ok` has shown us what a test result line looks like. Let's look at
some of the other simple assertions.

### `nok`

Sometimes you are more concerned if something is true which shouldn't be. For
example, let's say we have a Web site building script. It builds temporary
cache files to save time when building subpage links, but those cache files
need to go away when it's done. So we would test for existence of a cache file
and fail if the file exists.

    # example-08-06.pir

    .loadlib 'io_ops'

    .sub 'main' :main
        .include 'test_more.pir'

        .local int cache_file_exists

        plan(1)
        cache_file_exists = stat 'subpages.data', 0
        nok(cache_file_exists, 'Cache files should be cleaned up')
    .end

The assertion may be `nok`, but the output is still `ok` or not based on whether
the assertion was true.

    $ parrot example-08-06.pir
    1..1
    ok 1 - Cache files should be cleaned up

What does it look like if we deliberately confuse things?

    $ touch subpages.data
    $ parrot example-08-06.pir
    1..1
    not ok 1 - Cache files should be cleaned up

Yes. That's what I hoped to see. Let's clean up after ourselves to avoid future
confusion.

    $ rm subpages.data

### `is`

There are many times where we want to compare two values. Let's continue with our Web site
building tool. This tool sets the title of a page in metadata. We obviously want to be
certain that it reads the metadata correctly. We would use the `is` assertion for
that kind of test.

    # example-08-07.pir
    .sub 'main' :main
        .include 'test_more.pir'

        .local string expected_title
        .local string actual_title

        expected_title = '08 - Test::More and Tapir'

        plan(1)

        # Okay, let's pretend we got this result by running the builder.
        actual_title = '08 - Test::More and Tapir'
        is(actual_title, expected_title, 'The title should be correct.')
    .end

Anybody know what we should see? 

    $ parrot example-08-07.pir
    1..1
    ok 1 - The title should be correct.

Let's deliberately mess things up again so we know what failure of `is` looks like.

    # example-08-08.pir
    .sub 'main' :main
        .include 'test_more.pir'

        .local string expected_title
        .local string actual_title

        expected_title = '08 - Test::More and Tapir'

        plan(1)

        # Okay, let's pretend we got this result by running the builder.
        actual_title = 'I am a Walrus'
        is(actual_title, expected_title, 'The title should be correct.')
    .end

A failed `is` produces some useful information.

    $ parrot example-08-08.pir
    1..1
    not ok 1 - The title should be correct.
    # Have: I am a Walrus
    # Want: 08 - Test::More and Tapir

There's the test result line, which shows 'not ok', just like we expected.
We also have a couple of diagnostic lines describing what we want and what we
actually have.

`ok` has its opposite assertion `nok`, so there must be an opposite for `is`, right?
There sure is.

### `isnt`

Occasionally we care less about what a value is than making sure it's *not* something
in particular. Maybe we have a user registration process that uses social security numbers
to satisfy an obscure corporate tracking requirement, but can't save them as-is because of 
privacy concerns. In this case we don't care what the stored value is. We want to be certain
that it's not the social security number.

    # example-08-09.pir
    .sub 'main' :main
        .include 'test_more.pir'

        .local string provided_ssn
        .local string stored_ssn

        provided_ssn = '5551234567'

        plan(1)

        # Okay, let's pretend we got this result via user registration
        stored_ssn = 'wxdfk$!'
        isnt(provided_ssn, stored_ssn, 'SSN should not be stored as-is')
    .end

Really, nobody should be surprised by the output at this point.

    1..1
    ok 1 - SSN should not be stored as-is

What does a failed `isnt` look like?

    # example-08-10.pir
    .sub 'main' :main
        .include 'test_more.pir'

        .local string provided_ssn
        .local string stored_ssn

        provided_ssn = '5551234567'

        plan(1)

        # Okay, let's pretend we got this result via user registration
        stored_ssn = provided_ssn
        isnt(provided_ssn, stored_ssn, 'SSN should not be stored as-is')
    .end

The output diagnostic is once again straightforward.

    $ parrot example-08-10.pir
    1..1
    not ok 1 - SSN should not be stored as-is
    # Have: 5551234567
    # Want: not 5551234567

### `is_deeply`

`is` fails us when we need to compare PMCs. Well, it *sort of* works:

    # example-08-11.pir
    .sub 'main' :main
        .include 'test_more.pir'

        .local pmc expected_details
        .local pmc actual_details

        expected_details = new 'Hash'
        expected_details['first'] = 'Super'
        expected_details['last'] = 'Man'

        actual_details = new 'Hash'
        actual_details['first'] = 'Super'
        actual_details['last'] = 'Woman'

        plan(1)

        is(expected_details, actual_details, 'Super Man is not Super Woman')
    .end

The output isn't incredibly useful, though.

    $ parrot example-08-11.pir
    1..1
    not ok 1 - Super Man is not Super Woman
    # Have: Hash[0x25ee84]
    # Want: Hash[0x25ee48]

Thankfully, we have the `is_deeply` assertion to tell use exactly how a test
has failed.

    # example-08-12.pir
    .sub 'main' :main
        .include 'test_more.pir'

        .local pmc expected_details
        .local pmc actual_details

        expected_details = new 'Hash'
        expected_details['first'] = 'Super'
        expected_details['last'] = 'Man'

        actual_details = new 'Hash'
        actual_details['first'] = 'Super'
        actual_details['last'] = 'Woman'

        plan(1)

        is_deeply(expected_details, actual_details, 'Super Man is not Super Woman')
    .end

Now we can see exactly which value in the PMC was different.

    $ parrot example-08-12.pir
    1..1
    not ok 1 - Super Man is not Super Woman
    # Mismatch at [last]: expected Man, received Woman

With `is_deeply` under our belt, we now know enough assertions to get started putting them to use in real
projects.

### What About The Other Assertions and Commands?

We won't be talking about them. I may eventually visit more as we get
the hang of Parrot, but this is a good enough core to start with. Do
you want to dig deeper? Go right ahead. The best resource for the 
moment is the documentation within [Test::More][] itself.

### TAP - The Test Anything Protocol

All of this output has looked remarkably consistent. There's a reason
for that. [Test::More][] formats its result in a format known as TAP - the
[Test Anything Protocol][]. All of the output can be read by another program
to provide you with a summary report. This other program is usually referred
to as a [test harness](http://en.wikipedia.org/wiki/Test_harness). The
test harness runs your tests and then tells you how many of them failed, or
if there were any surprises.

All I need is a test harness. I'll be back to talk about [Tapir][] very soon.

### Conclusion

Hey, we can test now! We learned how to use the [Test::More][] library, making
simple assertions and reporting the results using the [Test Anything Protocol][].
As long as we stay disciplined and run our tests regularly, we will learn
immediately when we have an "inspired" moment that breaks existing code. Since
I'm such a huge fan of Test-Driven Development, you can be assured of seeing many assertions in
future Parrot Babysteps.