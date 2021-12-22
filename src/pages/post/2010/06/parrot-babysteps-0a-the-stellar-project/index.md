---
aliases:
- /coolnamehere/2010/06/02_0a-the-stellar-project.html
- /post/2010/0a-the-stellar-project/
- /2010/06/02/parrot-babysteps-0a-the-stellar-project/
category: coolnamehere
date: 2010-06-02 00:00:00
layout: layout:PublishedArticle
series:
- Parrot Babysteps
slug: parrot-babysteps-0a-the-stellar-project
tags:
- parrot
- learn
- space
title: Parrot Babysteps 0a - The Stellar Project
updated: 2011-04-12 00:00:00
uuid: 3925c917-b50b-4d78-9de1-abc7ad87f2b0
---

[simple Parrot projects]: /post/2010/04/parrot-babysteps-09-simple-projects
[been writing]: /post/2009/10/parrot-babysteps-07-writing-subroutines
[Parrot]: /tags/parrot/
[Perl]: /tags/perl/

We just learned how to create and test [simple Parrot projects][]. The next step
is to reexamine the star catalog handler we've [been writing][], and turn it
into a testable project. There will be some changes in how this code gets its
work done, but don't expect any new features. 

I know - you *really* want to start adding features and working on cool new 
stuff. So do I. My workspace is scattered with half-completed steps that talked 
about adding new things and using new [Parrot][] features. They kept breaking, 
though. They kept breaking because I wasn't building from a stable, testable 
foundation. Today we're going to get that step our of the way.

## Set up the project

[larger projects]: /post/2010/04/parrot-babysteps-09-simple-projects

Let's apply what we learned last time putting together [larger projects][], and
set up a project named `stellar`.

    $ mkdir stellar
    $ mkdir stellar/t
    $ mkdir stellar/lib

The `setup.pir` file is copied directly from the previous project. I'm not ready
for anything more elaborate.

    # example-0a-01/setup.pir
    .sub 'main' :main
        .param pmc args
        $S0 = shift args # Ignore my own filename
        load_bytecode 'distutils.pbc'

        # Find out what command the user has issued
        .local string directive
        directive = shift args

        # Used by the test mode
        .local string prove_exec
        prove_exec = get_parrot()

        setup(directive, 'prove_exec' => prove_exec)
    .end

The behavior will be defined in `lib/stellar.pir`, which is initially 
empty. We will steadily build up all of our functionality in the Stellar library
and eventually add a very simple file to act as the face of Stellar for
Parrot. Right now, we just have an empty `lib/stellar.pir`.

## Reimplementing Features

The basic skeleton is in place. Now we can start adding the features we had
written before.

### Extracting Details

It's important to keep test files organized. One helpful approach is to think of
each test as a story. This story describes a single specific thing we want the
Stellar library to accomplish. All of the stories together provide a description
of everything that users should be able to get from the library.

I like to start with the smallest useful test story I can. For this code, I
think that would be extracting the details about a single entry in the HYG
catalog. The whole catalog isn't even needed. We could get away with using the
header line and the line containing a star's details.

Names for test files usually follow a common pattern. They start with a number
and summarize what feature is being tested. What purpose does the number serve?
Well, they are probably executed in the order that Parrot finds them, so that
numbering provides a clue for test order. There are no promises about the order,
though. The system looks at each story individually, and you should too. I like
to think of the numbering as simply presenting the order that I came up with the
stories. It provides a simple history of sorts. First I came up with that test,
and I wrote this test after I was comfortable with the first.

In that spirit, I will name the first test story `01-extract-details.t`.

    # example-0a-01/t/01-extract-details.t
    .include 'lib/stellar.pir'

    .sub 'main' :main
        .include 'test_more.pir'
        .local string header_string
        .local string sol_string
        .local string delimiter
        .local pmc    header_fields
        .local pmc    star_fields
        .local pmc    star

        header_string = "StarID,HIP,HD,HR,Gliese,BayerFlamsteed,ProperName,RA,Dec,Distance,PMRA,PMDec,RV,Mag,AbsMag,Spectrum,ColorIndex,X,Y,Z,VX,VY,VZ"
        sol_string = "0,,,,,,Sol,0,0,0.000004848,0,0,0,-26.73,4.85,G2V,0.656,0,0,0,0,0,0"
        delimiter = ","

        header_fields = split delimiter, header_string
        star_fields = split delimiter, sol_string
        star = extract_star_details(header_fields, star_fields)

        plan(1)

        $S0 = star['Proper Name']
        is($S0, 'Sol', 'ProperName should be Sol')
    .end

Yes, I know that there is a typo in this test code. The key `Proper Name` should be
`ProperName`. We'll come back to that.

What happens if this test is run while `stellar.pir` is still empty? It fails,
of course. It might be useful to look at *how* it fails.

    stellar $ parrot setup.pir test
    t/01-extract-details.t .. Dubious, test returned 1
    Failed 1/1 subtests

    Test Summary Report
    -------------------
    t/01-extract-details.t (Tests: 0 Failed: 0)
    XXX
    Files=1, Tests=0,  0.014 wallclock secs
    Result: FAIL
    test fails
    current instr.: 'setup' pc 883 (runtime/parrot/library/distutils.pir:376)
    called from Sub 'main' pc 29 (setup.pir:17)

`setup` told us something we already know: `extract_star_details` hasn't been
written yet. This is different from a regular test failure, because Parrot
couldn't even get to the tests. I'm showing this so that you recognize what's
going on when you see errors like this in your own library.

Adding `extract_star_details` is easy enough. Just copy the code from the
earlier step.

    # stellar/lib/stellar.pir

    .sub extract_star_details
        .param pmc    headers
        .param pmc    values

        .local pmc    star
        .local int    header_count
        .local string current_header
        .local string current_value
        .local int    current_index

        current_index = 0
        header_count = headers
        star = new 'Hash'

      ASSIGN_NEXT_STAR_FIELD:
        if current_index >= header_count goto RETURN_STAR
        current_header = headers[current_index]
        current_value = values[current_index]
        star[current_header] = current_value
        current_index += 1
        goto ASSIGN_NEXT_STAR_FIELD

      RETURN_STAR:
        .return(star)
    .end

Let's run the test again. 

    $ parrot setup.pir test
    t/01-extract-details.t .. Failed 1/1 subtests

    Test Summary Report
    -------------------
    t/01-extract-details.t (Tests: 1 Failed: 1)
      Failed test:  1
    Files=1, Tests=1,  0.020 wallclock secs
    Result: FAIL
    test fails
    current instr.: 'setup' pc 883 (runtime/parrot/library/distutils.pir:376)
    called from Sub 'main' pc 29 (setup.pir:17)

There's only one assertion, so we already know which one failed. This output is a
little vague for larger test stories, though. Let's run the test file directly.

    #!text
    $ parrot t/01-extract-details.t
    1..1
    not ok 1 - ProperName should be Sol
    # Have:
    # Want: Sol

Okay, *now* we can fix the typo.

    #!parrot
    # t/01-extract-details.t
    .sub 'main' :main
        ...
        $S0 = star['ProperName']
        is($S0, 'Sol', 'ProperName should be Sol')
    .end

The test should pass now that the correction has been made.

    #!text
    $ parrot setup.pir test
    t/01-extract-details.t .. ok
    All tests successful.
    Files=1, Tests=1,  0.014 wallclock secs
    Result: PASS

Don't worry. I won't submit you to this for every test run. It's just important
to know what failure looks like before we can reach success.

What have we accomplished so far? We now have a story in which the user, armed
with a header line and a line describing a star, gets an object that she can
examine and manipulate for her own purposes. If we wanted to be thorough, we
could test every field. I'm not going to do that, though. One thing you want to
avoid when making test stories is predicting the future. It's easy to get
distracted by testing every possible aspect of a single chunk of code when you
could be working on the next story.

These stories aren't static. We will come back and add more when some
detail doesn't work out the way we expect it to.

Our first story is pretty much out of the way. Let's move on to the next one.

### Stringifying Stars

Next up is the string representation of a star. In the original application, we
had the `say_star_details` sub, which printed the star information as soon as it
had been prepared. `Stellar` is more of a library, though. This means that we
can't be completely sure what folks will want to do with the star summary once
they have it. They might want to print it, but they might also want to feed it
to an unmanned orbiter for some reason.

Because we can't predict with certainty what someone will do with the string
summary of a star, this test story will focus on asking for that string.

    # t/02-summarize-star.t
    .sub 'main' :main
        .include 'test_more.pir'
        .local string header_string
        .local string sol_string
        .local string delimiter
        .local pmc    header_fields
        .local pmc    star_fields
        .local pmc    star
        .local string summary

        header_string = "StarID,HIP,HD,HR,Gliese,BayerFlamsteed,ProperName,RA,Dec,Distance,PMRA,PMDec,RV,Mag,AbsMag,Spectrum,ColorIndex,X,Y,Z,VX,VY,VZ"
        sol_string = "0,,,,,,Sol,0,0,0.000004848,0,0,0,-26.73,4.85,G2V,0.656,0,0,0,0,0,0"
        delimiter = ","

        plan(1)

        header_fields = split delimiter, header_string
        star_fields = split delimiter, sol_string
        star = extract_star_details(header_fields, star_fields)

        summary = "<Name: Sol, Spectrum: G2V, Distance: 0.000004848>"
        $S0 = summarize_star(star)
        is($S0, summary, "Sol's summary should include basic details")
    .end

It's not hard to create the code which will make this story true, but it does
involve a little more work than the simple copy and paste for
`extract_star_details`.

    # example-0a-04/lib/stellar.pir

    # ...

    .sub summarize_star
        .param pmc star

        .local string star_name
        .local string star_spectrum
        .local string star_distance
        .local string summary

        star_name = star['ProperName']
        star_spectrum = star['Spectrum']
        star_distance = star['Distance']

        if star_name goto PREPARE_SUMMARY

      TRY_GLIESE:
        .local string gliese_number
        gliese_number = star['Gliese']
        unless gliese_number goto TRY_BAYER_FLAMSTEED
        star_name = 'Gliese ' . gliese_number
        goto PREPARE_SUMMARY

      TRY_BAYER_FLAMSTEED:
        .local string bayer_flamsteed
        bayer_flamsteed = star['BayerFlamsteed']
        unless bayer_flamsteed goto TRY_HR
        star_name = "BF " . bayer_flamsteed
        goto PREPARE_SUMMARY

      TRY_HR:
        .local string hr_id
        hr_id = star['HR']
        unless hr_id goto TRY_HD
        star_name = "HR " . hr_id
        goto PREPARE_SUMMARY

      TRY_HD:
        .local string hd_id
        hd_id = star['HD']
        unless hd_id goto USE_STAR_ID
        star_name = "HD " . hd_id
        goto PREPARE_SUMMARY

      TRY_HIP:
        .local string hip_id
        hip_id = star['HIP']
        unless hip_id goto USE_STAR_ID
        star_name = "HIP " . hip_id
        goto PREPARE_SUMMARY

      USE_STAR_ID:
        .local string star_id
        star_id = star['StarID']
        star_name = "HYG " . star_id
        goto PREPARE_SUMMARY

      PREPARE_SUMMARY:
        summary = "<Name: "
        summary .= star_name
        summary .= ", Spectrum: "
        summary .= star_spectrum
        summary .= ", Distance: "
        summary .= star_distance
        summary .= ">"

        .return(summary)
    .end

Yes, this is mostly a copy and paste of `say_star_details`. The new details
change the focus from displaying the details to returning them as a simple
string.

What's most important is that this test passes when handed Sol. How about some
of those stars that don't have proper names?

    # example-0a-04/t/02-summarize-star.t
    .include 'lib/stellar.pir'

    .sub 'main' :main
        .include 'test_more.pir'
        .local string header_string
        .local string star_string
        .local string delimiter
        .local pmc    header_fields
        .local pmc    star_fields
        .local pmc    star
        .local string summary

        header_string = "StarID,HIP,HD,HR,Gliese,BayerFlamsteed,ProperName,RA,Dec,Distance,PMRA,PMDec,RV,Mag,AbsMag,Spectrum,ColorIndex,X,Y,Z,VX,VY,VZ"
        delimiter = ","

        plan(3)

        header_fields = split delimiter, header_string

        summary = "<Name: Sol, Spectrum: G2V, Distance: 0.000004848>"
        star_string = "0,,,,,,Sol,0,0,0.000004848,0,0,0,-26.73,4.85,G2V,0.656,0,0,0,0,0,0"
        star_fields = split delimiter, star_string
        star = extract_star_details(header_fields, star_fields)
        $S0 = summarize_star(star)
        is($S0, summary, "Sol's summary should include basic details")

        summary = "<Name: HD 224693, Spectrum: G2V, Distance: 94.0733772342427>"
        star_string = "117952,118319,224693,,,,,23.99826083,-22.42818030,94.0733772342427,148.74,27.53,,8.23,3.36266632261649,G2V,0.639,86.95751,-0.03959,-35.89135,4.82e-06,6.7829e-05,1.1605e-05"
        star_fields = split delimiter, star_string
        star = extract_star_details(header_fields, star_fields)
        $S0 = summarize_star(star)
        is($S0, summary, "HD identifier can be used if ProperName is unavailable")

        summary = "<Name: HYG 117782, Spectrum: G2V, Distance: 139.275766016713>"
        star_string = "117782,118149,,,,,,23.96625102,15.95292997,139.275766016713,-46.50,-53.88,,9.59,3.8706222212115,G2V,0.648,133.90672,-1.18315,38.2796,9.72e-06,-3.1482e-05,-3.4977e-05"
        star_fields = split delimiter, star_string
        star = extract_star_details(header_fields, star_fields)
        $S0 = summarize_star(star)
        is($S0, summary, "HYG identifier can be used if ProperName is unavailable")
    .end

It does indeed work.

    $ parrot setup.pir test
    t/01-extract-details.t .. ok
    t/02-summarize-star.t ... ok
    All tests successful.
    Files=2, Tests=4,  0.030 wallclock secs
    Result: PASS

I am concerned about the heft of this test code. The concern is that I 
had to split the CSV text, extract star details, and summarize the star 
manually for each star string. Each of those times is an opportunity for me to
make a mistake. I *think* I would like to have a subroutine which would take the
header fields and a CSV line of star data, and return the extracted details.
Let's make a new test story for that.

    # example-0a-04/t/03-extract-from-csv.t
    .sub 'main' :main
        .include 'test_more.pir'
        .local string header_string
        .local string star_string
        .local string delimiter
        .local pmc    header_fields
        .local pmc    star_fields
        .local pmc    star
        .local string summary

        header_string = "StarID,HIP,HD,HR,Gliese,BayerFlamsteed,ProperName,RA,Dec,Distance,PMRA,PMDec,RV,Mag,AbsMag,Spectrum,ColorIndex,X,Y,Z,VX,VY,VZ"
        delimiter = ","

        plan(3)

        header_fields = split delimiter, header_string

        summary = "<Name: Sol, Spectrum: G2V, Distance: 0.000004848>"
        star_string = "0,,,,,,Sol,0,0,0.000004848,0,0,0,-26.73,4.85,G2V,0.656,0,0,0,0,0,0"
        star = extract_from_csv_line(star_string, header_fields, delimiter)
        $S0 = summarize_star(star)
        is($S0, summary, "Sol's summary should include basic details")

        summary = "<Name: HD 224693, Spectrum: G2V, Distance: 94.0733772342427>"
        star_string = "117952,118319,224693,,,,,23.99826083,-22.42818030,94.0733772342427,148.74,27.53,,8.23,3.36266632261649,G2V,0.639,86.95751,-0.03959,-35.89135,4.82e-06,6.7829e-05,1.1605e-05"
        star = extract_from_csv_line(star_string, header_fields, delimiter)
        $S0 = summarize_star(star)
        is($S0, summary, "HD identifier can be used if ProperName is unavailable")

        summary = "<Name: HYG 117782, Spectrum: G2V, Distance: 139.275766016713>"
        star_string = "117782,118149,,,,,,23.96625102,15.95292997,139.275766016713,-46.50,-53.88,,9.59,3.8706222212115,G2V,0.648,133.90672,-1.18315,38.2796,9.72e-06,-3.1482e-05,-3.4977e-05"
        star = extract_from_csv_line(star_string, header_fields, delimiter)
        $S0 = summarize_star(star)
        is($S0, summary, "HYG identifier can be used if ProperName is unavailable")
    .end

The code to make this work is simple enough.

    # example-0a-04/lib/stellar.pir

    # ...
    
    .sub extract_from_csv_line
        .param string star_string
        .param pmc    header_fields
        .param string delimiter
        .local pmc    star_fields
        .local pmc    star

        star_fields = split delimiter, star_string
        star = extract_star_details(header_fields, star_fields)

        .return(star)
    .end

I do not know if I have saved much work, but it is easier for me to read the
test story. That is important to me, because debugging and improving the code is
easier if I can easily understand what is happening.

## Conclusion


It is time to take a break. The script we wrote a while back is evolving into a
tested library that can be used by others. Now that we have our foundation, we 
can start building up. Our next step will involve adding some simple search
behavior to the library, and that is a significant improvement. For the moment,
take a little time to relax.