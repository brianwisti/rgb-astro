---
aliases:
- /coolnamehere/2010/07/15_0c-the-stellar-app.html
- /post/2010/0c-the-stellar-app/
- /2010/07/15/parrot-babysteps-0c-the-stellar-app/
category: coolnamehere
date: 2010-07-15 00:00:00
layout: layout:PublishedArticle
series:
- Parrot Babysteps
slug: parrot-babysteps-0x-the-stellar-app
tags:
- parrot
- learn
- space
title: Parrot Babysteps 0c - The Stellar App
updated: 2010-07-15 00:00:00
uuid: cf10771e-0bb2-47e6-9d16-7ed18405945d
---

[step 07]: /post/2009/10/parrot-babysteps-07-writing-subroutines
[checking a single star]: /post/2010/06/parrot-babysteps-0b-subroutine-params
[HYG Catalog]: http://www.astronexus.com

Our search journey continues. We have accomplished the hard 
part: [checking a single star][] to see if it has the traits we're looking for.
Today we just have to use that logic to search a set of stars. First we'll
examine a handpicked selection. Guess what happens after that? We finally get
back into the full [HYG Catalog][] and search for stars from the command line.
That's right. After all this work, `stellar` grows up and becomes an
application.

[Perl]: /tags/perl/
[Python]: /tags/python/
[Parrot]: /tags/parrot/
[SQLite]: http://sqlite.org

### Note

There are easier ways to get searches out of a large CSV file. If
that was really all I wanted to do, I could use a higher level language like
[Perl][] or [Python][] to feed the CSV into a [SQLite][] database and directly
query the database. However, we are not building a SQL database. We are learning
how to do interesting things with [Parrot][].

## Building a Catalog and Searching It

The first thing that's tripping me up is how to set up the catalog itself. You
know the "set of stars" I was talking about? The easy way to do this from a test
is to have a few CSV strings for some sample stars, apply `extract_from_csv` to
each of them, push each star into an array, then search through the array. Thing 
is, I *know* that this is not going to be acceptable when I get to the real data.
I expect this application to be one where you run it from the command line,
using your search conditions as command line arguments. Loading all the data
before searching it takes time. I should write this code so that it searches
while reading in data. That would be much faster.

On the other hand, what if I add an interactive prompt to this application later?
Loading the full catalog into memory before applying searches could be
faster in the long run compared to reading the data file for every search.

That is trying to predict the future, though. I know how I want to use this
catalog today. I want to run a search and see the results as soon as the
application knows about them.

<aside>
I will share a secret. I spent a day writing the "load then
search" approach to building the catalog. Guess what? It is unbearably slow at
my current Parrot skill level. I am confident that this is only
slow because my code overall is simplistic. Maybe I can revisit this idea after
learning more about Parrot.
</aside>

### Searching The Catalog

I do not want to dig right into searching the full 119,617 entries of the real
catalog. Instead, let's set up a small test catalog and write some tests.

Where you put your test data is a matter of taste. I will be keeping my data in
a folder named `data`. That seems reasonable.

    $ mkdir data

Only a few entries are needed in the test catalog. We just need to be sure that
the code works with a CSV file with the same structure as the HYG database.
I'll grab Sol, another G2V spectrum star, and a K3V star.

    # example-0c-01/data/test-catalog.csv
    StarID,HIP,HD,HR,Gliese,BayerFlamsteed,ProperName,RA,Dec,Distance,PMRA,PMDec,RV,Mag,AbsMag,Spectrum,ColorIndex,X,Y,Z,VX,VY,VZ
    0,,,,,,Sol,0,0,0.000004848,0,0,0,-26.73,4.85,G2V,0.656,0,0,0,0,0,0
    80,80,224817,,,,,0.01611947,-11.82353722,64.143681847338,419.04,-82.83,,8.40,4.36423057594421,G2V,0.566,62.7822,0.26494,-13.14292,-5.827e-06,0.000130277,-2.5209e-05
    7358,7372,9770,,Gl  60 A,,,1.58359898,-29.91056753,23.6462520690471,85.56,96.58,34.2,7.11,5.2411884257345,K3V,0.909,18.76027,8.25627,-11.79114,2.8852e-05,2.3413e-05,-7.844e-06

The test data is out of the way, so now I feel comfortable writing the tests
that use it.

    # example-0c-01/t/05-search-catalog.t
    .include 'lib/stellar.pir'

    .sub 'main' :main
        .include 'test_more.pir'

        plan(5)

        .local string csv_filename 
        .local pmc    matches
        .local pmc    star
        
        csv_filename = 'data/test-catalog.csv'
        matches = search_catalog(csv_filename, 'ProperName', 'Sol')
        is(matches, 1, 'There should be one star named "Sol"')
        star = matches[0]
        $S0 = star['ProperName']
        is($S0, 'Sol', 'That star should be Sol')

        matches = search_catalog(csv_filename, 'Spectrum', 'G2V')
        is(matches, 2, 'There are two G2V stars in the test catalog')

        matches = search_catalog(csv_filename, 'Spectrum', 'K3V')
        is(matches, 1, 'There should be one K3V star in the test catalog')

        matches = search_catalog(csv_filename, 'Spectrum', 'G2V', 'ColorIndex', '0.566')
        is(matches, 1, 'There should be one G2V star with Spectrum G2V and ColorIndex 0.566')
    .end

I am deliberately keeping the tests simple right now. The goal is to make sure
the basic functionality works rather than to guarantee behavior for every little
detail. Tests can be added for those details as they become important.

The actual `search_catalog` sub borrows quite a bit from [step 07][]. 

    # example-0c-01/lib/stellar.pir

    .loadlib 'io_ops'

    # ...
    .sub search_catalog
        .param string filename
        .param pmc    conditions :slurpy
        .local pmc    chomp
        .local pmc    matches
        .local pmc    catalog
        .local string current_line
        .local pmc    current_star
        .local pmc    is_match

        load_bytecode 'String/Utils.pbc'
        chomp = get_global ['String';'Utils'], 'chomp'

        matches = new 'ResizablePMCArray'

        catalog = open filename, 'r'
        current_line = readline catalog # Ignore header line

      READ_LINE:
        unless catalog goto RETURN_MATCHES
        current_line = readline catalog
        current_line = chomp(current_line)
        current_star = extract_from_csv_line(current_line)
        is_match = check_star(current_star, conditions :flat)
        if is_match goto REMEMBER_MATCH
        goto READ_LINE

      REMEMBER_MATCH:
        push matches, current_star
        goto READ_LINE

      RETURN_MATCHES:
        close catalog
        .return(matches)
    .end

`search_catalog` will handle the task of reading the file and looking for
stars that match the search conditions it has been given. After it defines
a star from the current line, it asks `check_star` to compare that star
to the set of conditions it has been given. It remembers the stars that
match, and returns them once it has reached the end of the file. It is not
the fastest approach, but it works.

It works well enough that I am ready to add real data and some way for people
to use it!

### Searching From The Command Line

Now that we know `stellar` can read a CSV and return results, it's time to work
on that empty `main` that has been sitting in `stellar.pir`. Oh yeah - we will
want to make `hygxyz.csv` available now. I will be pushing my copy into the
`data` folder, next to `test-catalog.csv`. You can place your copy wherever you
like, but make sure that you set the path appropriately in `main`.

    # example-0c-02/lib/stellar.pir
    
    .loadlib 'io_ops'

    .sub 'main' :main
        .param pmc    conditions
        .local string csv_file
        .local pmc    matches
        .local pmc    matches_iter
        .local pmc    star
        .local string summary
        .local int    match_count

        $S0 = shift conditions # ignore my own filename
        csv_file = 'data/hygxyz.csv'
        matches = search_catalog(csv_file, conditions :flat)
        matches_iter = iter matches

      NEXT_MATCH:
        star = shift matches_iter
        summary = summarize_star(star)
        say summary
        if matches_iter goto NEXT_MATCH

        match_count = matches
        print match_count
        say " matches."
    .end

Here is the result of all that work we have done setting up the project and 
support code. The main subroutine in `stellar` is downright civilized 
compared to what we had for [step 07][]. All we do is search based on the
command line parameters and display each of the matches.

    $ parrot lib/stellar.pir Spectrum G2V ColorIndex 0.656
    <Name: Sol, Spectrum: G2V, Distance: 0.000004848>
    <Name: HD 7186, Spectrum: G2V, Distance: 112.359550561798>
    <Name: HD 140235, Spectrum: G2V, Distance: 60.1684717208183>
    <Name: HD 169019, Spectrum: G2V, Distance: 108.108108108108>
    4 matches.

Hey, this thing is almost useful!

## Conclusion

[HYG Database]: http://astronexus.com/node/34

`stellar` has reached a major milestone. When I started fiddling with the [HYG
Database][], I wanted to write a command-line Parrot tool that could look up
stars based on specific fields. This step gives us that ability. I admit that
a lot more could be done. For example, it only does exact matches. You can
easily find a star that is `108.108108108108` light years away, but not
stars that are roughly `108` light years away. And forget about finding
stars within 20 light years.

[Rakudo Star]: http://rakudo.org

I am going to take a little break from the `stellar` project, though. 
[Rakudo Star][] is almost out, and I want to play with that.

[David Nash]: http://astronexus.com/node/10

You can add to `stellar` yourself. Make it faster. Make it
object-oriented. Make it a library. Rewrite it in LOLCODE. Have fun. Just
remember to give [David Nash][] credit for creating the HYG Database. 
We have been having all of this fun because he took the time to put that
catalog together.

Enjoy yourself!