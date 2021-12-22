---
aliases:
- /coolnamehere/2009/10/06_07-writing-subroutines.html
- /post/2009/07-writing-subroutines/
- /2009/10/06/parrot-babysteps-07-writing-subroutines/
category: coolnamehere
date: 2009-10-06 00:00:00
layout: layout:PublishedArticle
series:
- Parrot Babysteps
slug: parrot-babysteps-07-writing-subroutines
tags:
- parrot
- learn
title: Parrot Babysteps 07 - Writing Subroutines
updated: 2011-04-12 00:00:00
uuid: 2301daf7-e316-4f85-8736-b57f73edcb33
---

## Introduction

[last step]: /post/2009/10/parrot-babysteps-06-files-and-hashes

We accomplished quite a bit in our [last step][].
We figured out how to parse a 20 MB star catalog and search for information that
we thought could be important. The only problem is that it was turning to
spaghetti. Even though it had barely 100 lines of code, it was becoming a bigger
challenge to figure out what was going on or how to add new features.

Today we're going to streamline the code somewhat by wrapping that complexity
in subroutines.  The Parrot Book has a [sizable chapter discussing
subroutines](http://docs.parrot.org/parrot/latest/html/docs/book/pir/ch06_subroutines.pod.html).
I won't be spending much time exploring the depths of subroutines, because
that would take me far beyond what is appropriate for a babystep. However, a
quick glance at the chapter should suggest that Parrot subroutines are quite 
powerful and worth deeper exploration on your own.

## Subroutines

[the very beginning]: /post/2009/07/parrot-babysteps-01-getting-started

We've been working with subroutines from [the very beginning][].
Every Parrot application has a subroutine tagged as `:main` to show that it contains
the main logic for the program. Let's start adding our own supplementary subroutines.

Our first function will encapsulate the display of star highlights.

    # example-07-01

    .loadlib 'io_ops'

    .sub 'main' :main

        load_bytecode 'String/Utils.pbc'

        .const string DELIMITER  = ','
        .local pmc    chomp
        .local string filename
        .local pmc    data_file
        .local string current_line
        .local pmc    field_names
        .local int    field_count
        .local int    current_field_index
        .local string current_field_name
        .local string current_field_value
        .local pmc    star_data
        .local pmc    star
        .local string star_name
        .local string star_spectrum
        .local pmc    sol
        .local string sol_spectrum
        .local int    matching_count
        .local int    unnamed_match_count

        chomp         = get_global ['String';'Utils'], 'chomp'
        filename      = 'hygxyz.csv'
        data_file     = open filename, 'r'
        current_line  = readline data_file
        current_line  = chomp(current_line)
        field_names   = split DELIMITER, current_line
        field_count   = field_names

        current_line = readline data_file
        current_line = chomp(current_line)
        star_data = split DELIMITER, current_line
        current_field_index = 0
        sol = new 'Hash'

      ASSIGN_NEXT_SOL_FIELD:
        if current_field_index >= field_count goto FIND_MATCHING_STARS
        current_field_name = field_names[current_field_index]
        current_field_value = star_data[current_field_index]
        sol[current_field_name] = current_field_value
        current_field_index += 1
        goto ASSIGN_NEXT_SOL_FIELD

      FIND_MATCHING_STARS:
        sol_spectrum = sol['Spectrum']
        matching_count = 0
        unnamed_match_count = 0
        # We want to show Sol's details as well as other matches.
        say_star_details(sol)

      LOAD_NEXT_STAR:
        unless data_file goto END
        current_line = readline data_file
        current_line = chomp(current_line)
        star_data = split DELIMITER, current_line
        current_field_index = 0
        star = new 'Hash'

      ASSIGN_NEXT_STAR_FIELD:
        if current_field_index >= field_count goto EXAMINE_STAR
        current_field_name = field_names[current_field_index]
        current_field_value = star_data[current_field_index]
        star[current_field_name] = current_field_value
        current_field_index += 1
        goto ASSIGN_NEXT_STAR_FIELD

      EXAMINE_STAR:
        star_spectrum = star['Spectrum']
        if star_spectrum == sol_spectrum goto REMEMBER_MATCH
        goto LOAD_NEXT_STAR

      REMEMBER_MATCH:
        matching_count += 1
        star_name = star['ProperName']
        if star_name goto DISPLAY_STAR_DETAILS
        unnamed_match_count += 1
        goto LOAD_NEXT_STAR

      DISPLAY_STAR_DETAILS:
        say_star_details(star)
        goto LOAD_NEXT_STAR

      END:
        close data_file
        print matching_count
        print " stars exactly matched Sol's spectrum "
        say sol_spectrum
        print unnamed_match_count
        say ' have no proper name'

    .end

    .sub say_star_details
        .param pmc star

        .local string star_name
        .local string star_spectrum
        .local string star_distance

        star_name = star['ProperName']
        star_spectrum = star['Spectrum']
        star_distance = star['Distance']

        print "<Name: "
        print star_name
        print ", Spectrum: "
        print star_spectrum
        print ", Distance: "
        print star_distance
        say ">"
    .end

To create a subroutine that will get used by your `:main` sub, all
you need to do is declare a `.sub`.

    .sub say_star_details
    .end

I like my subroutine names to clearly describe the task being accomplished,
to minimize the guesswork when I come back to code later.

[a few steps ago]: /post/2009/09/parrot-babysteps-04-adding-command-line-arguments

This subroutine accepts a single parameter: a Hash describing the star to be
printed. We learned [a few steps ago][]
that the `.param` directive declares a parameter for your subroutine.

    .sub say_star_details
        .param pmc star
    .end

The subroutine body in this case is going to be a copy and paste of the 
`DISPLAY_STAR_DETAILS` code chunk, along with declarations of `.local`
variables needed to make it work.

    .sub say_star_details
        .param pmc star

        .local string star_name
        .local string star_spectrum
        .local string star_distance

        star_name = star['ProperName']
        star_spectrum = star['Spectrum']
        star_distance = star['Distance']

        print "<Name: "
        print star_name
        print ", Spectrum: "
        print star_spectrum
        print ", Distance: "
        print star_distance
        say ">"
    .end

We no longer care about stellar distances in our main code, so we can safely
remove the `.local string star_distance` directive from `main`.

Now we can rewrite our code to display Sol's details. Remember that subroutines
require that their parameters be wrapped in parentheses.

    # We want to show Sol's details as well as other matches.
    say_star_details(sol)

We could have also wrapped `say_star_details` in quotes, but it's only required
when our subroutines have non-ASCII characters - that is, characters outside the
range of what we consider "normal" characters in the United States. Still, I won't
complain if you're devoted to good form and prefer to show those subroutine calls
as:

    'say_star_details'(sol)

The `DISPLAY_STAR_DETAILS` chunk becomes just a few lines:

    DISPLAY_STAR_DETAILS:
      say_star_details(star) # or 'say_star_details'(star)
      goto LOAD_NEXT_STAR

Does it produce the same result as the code we ran before?

    $ parrot example-07-01.pir 
    <Name: Sol, Spectrum: G2V, Distance: 0.000004848>
    <Name: Rigel Kentaurus A, Spectrum: G2V, Distance: 1.34749097181049>
    568 stars exactly matched Sol's spectrum G2V
    567 have no proper name

It sure does. The code is still rather awkward, though. How about we add a
subroutine for transforming a line from the text file into star data?

## Returning Values

    # example-07-02

    .loadlib 'io_ops'

    .sub 'main' :main

        load_bytecode 'String/Utils.pbc'

        .const string DELIMITER  = ','
        .local pmc    chomp
        .local string filename
        .local pmc    data_file
        .local string current_line
        .local pmc    field_names
        .local pmc    star_data
        .local pmc    star
        .local string star_name
        .local string star_spectrum
        .local pmc    sol
        .local string sol_spectrum
        .local int    matching_count
        .local int    unnamed_match_count

        chomp         = get_global ['String';'Utils'], 'chomp'
        filename      = 'hygxyz.csv'
        data_file     = open filename, 'r'
        current_line  = readline data_file
        current_line  = chomp(current_line)
        field_names   = split DELIMITER, current_line

        current_line = readline data_file
        current_line = chomp(current_line)
        star_data = split DELIMITER, current_line
        sol = extract_star_details(field_names, star_data)

      FIND_MATCHING_STARS:
        sol_spectrum = sol['Spectrum']
        matching_count = 0
        unnamed_match_count = 0
        # We want to show Sol's details as well as other matches.
        say_star_details(sol)

      LOAD_NEXT_STAR:
        unless data_file goto END
        current_line = readline data_file
        current_line = chomp(current_line)
        star_data    = split DELIMITER, current_line
        star         = extract_star_details(field_names, star_data)

      EXAMINE_STAR:
        star_spectrum = star['Spectrum']
        if star_spectrum == sol_spectrum goto REMEMBER_MATCH
        goto LOAD_NEXT_STAR

      REMEMBER_MATCH:
        matching_count += 1
        star_name = star['ProperName']
        unless star_name goto LOAD_NEXT_STAR
        if star_name goto DISPLAY_STAR_DETAILS
        unnamed_match_count += 1
        goto LOAD_NEXT_STAR

      DISPLAY_STAR_DETAILS:
        say_star_details(star)
        goto LOAD_NEXT_STAR

      END:
        close data_file
        print matching_count
        print " stars exactly matched Sol's spectrum "
        say sol_spectrum
        print unnamed_match_count
        say ' have no proper name'

    .end

    .sub extract_star_details
        .param pmc headers
        .param pmc values

        .local pmc star
        .local int header_count
        .local string current_header
        .local string current_value
        .local int current_index

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

    .sub say_star_details
        # ...
    .end

The code is starting to get a little long, so I am adopting the habit
of replacing subroutine blocks with `# ...` when the code is unchanged from
the previous example.

Most of the code in our new `extract_star_details` subroutine looks familiar, but we do
have one noteworthy addition:

    .return(star)

This directive hands the Hash we've just built back to whoever called the function. 

Is our application cleaner? Yes, a little bit. I'm tired of having so many unnamed
stars, though. Let's add a little logic to attempt an alternate name if no proper
name is available.

### Making `say_star_details` Smarter

    # example-07-03
    .sub 'main' :main

        load_bytecode 'String/Utils.pbc'

        .const string DELIMITER  = ','
        .local pmc    chomp
        .local string filename
        .local pmc    data_file
        .local string current_line
        .local pmc    field_names
        .local pmc    star_data
        .local pmc    star
        .local string star_spectrum
        .local pmc    sol
        .local string sol_spectrum
        .local int    matching_count

        chomp         = get_global ['String';'Utils'], 'chomp'
        filename      = 'hygxyz.csv'
        data_file     = open filename, 'r'
        current_line  = readline data_file
        current_line  = chomp(current_line)
        field_names   = split DELIMITER, current_line

        current_line = readline data_file
        current_line = chomp(current_line)
        star_data = split DELIMITER, current_line
        sol = extract_star_details(field_names, star_data)

      FIND_MATCHING_STARS:
        sol_spectrum = sol['Spectrum']
        matching_count = 0
        # We want to show Sol's details as well as other matches.
        say_star_details(sol)

      LOAD_NEXT_STAR:
        unless data_file goto END
        current_line = readline data_file
        current_line = chomp(current_line)
        star_data    = split DELIMITER, current_line
        star         = extract_star_details(field_names, star_data)

      EXAMINE_STAR:
        star_spectrum = star['Spectrum']
        if star_spectrum == sol_spectrum goto REMEMBER_MATCH
        goto LOAD_NEXT_STAR

      REMEMBER_MATCH:
        matching_count += 1
        say_star_details(star)
        goto LOAD_NEXT_STAR

      END:
        close data_file
        print matching_count
        print " stars exactly matched Sol's spectrum "
        say sol_spectrum
    .end

    .sub extract_star_details
        # ...
    .end

    .sub say_star_details
        .param pmc star

        .local string star_name
        .local string star_spectrum
        .local string star_distance

        star_name = star['ProperName']
        star_spectrum = star['Spectrum']
        star_distance = star['Distance']

        if star_name goto DISPLAY_DETAILS

      TRY_GLIESE:
        .local string gliese_number
        gliese_number = star['Gliese']
        unless gliese_number goto TRY_BAYER_FLAMSTEED
        star_name = 'Gliese ' . gliese_number
        goto DISPLAY_DETAILS

      TRY_BAYER_FLAMSTEED:
        .local string bayer_flamsteed
        bayer_flamsteed = star['BayerFlamsteed']
        unless bayer_flamsteed goto TRY_HR
        star_name = "BF " . bayer_flamsteed
        goto DISPLAY_DETAILS

      TRY_HR:
        .local string hr_id
        hr_id = star['HR']
        unless hr_id goto TRY_HD
        star_name = "HR " . hr_id
        goto DISPLAY_DETAILS

      TRY_HD:
        .local string hd_id
        hd_id = star['HD']
        unless hd_id goto USE_STAR_ID
        star_name = "HD " . hd_id
        goto DISPLAY_DETAILS

      TRY_HIP:
        .local string hip_id
        hip_id = star['HIP']
        unless hip_id goto USE_STAR_ID
        star_name = "HIP " . hip_id
        goto DISPLAY_DETAILS

      USE_STAR_ID:
        .local string star_id
        star_id = star['StarID']
        star_name = "HYG " . star_id
        goto DISPLAY_DETAILS

      DISPLAY_DETAILS:
        print "<Name: "
        print star_name
        print ", Spectrum: "
        print star_spectrum
        print ", Distance: "
        print star_distance
        say ">"
    .end

Now *this* version of the app displays everything along with some kind of 
designation. The order I look for names is arbitrary, and is based
roughly in order of how familiar they looked to me. The tediousness of 
determining which reference to use has been hidden away in the `say_star_details`
subroutine, and consists of simply checking each field for a value until
something useful is found. I knew there would be some kind of name to display,
so I removed the name-counting functionality from `main`.

    $ parrot example-07-03.pir | more
    # ... much text omitted
    <Name: HYG 117782, Spectrum: G2V, Distance: 139.275766016713>
    <Name: HD 224693, Spectrum: G2V, Distance: 94.0733772342427>
    568 stars exactly matched Sol's spectrum G2V

## Conclusion

Right. Our script has grown to the point where it shows every `G2V` star
in the HYG database, and some of the complexity of this task has been
tucked away behind subroutines. Is there more to be done? You bet! I would
love to add user search features to the code. That's going to a fair step
on its own, so I think I will close my Vim window and push this page.