---
aliases:
- /coolnamehere/2004/12/26_rebol-datatypes.html
- /post/2004/rebol-datatypes/
- /2004/12/26/rebol-datatypes/
category: coolnamehere
date: 2004-12-26 00:00:00
layout: layout:PublishedArticle
slug: rebol-datatypes
tags:
- rebol
title: REBOL Datatypes
updated: 2009-07-11 00:00:00
uuid: 93913d58-1657-4572-af16-ae319d3d2f6c
---

One of [REBOL](http://www.rebol.com/)’s strengths is the rich selection
of native datatypes. This selection is part of what makes it so easy to
express solutions to your problems, because there is less \`\`mental
mapping'' to make as you use or create an abstract type to represent an
important concept. Learning this selection is also one of the challenges
for those who are trying to master the language. I am facing that
challenge right now, so I decided to make this table of native REBOL
datatypes and how they are expressed.

You can find the full description of all datatypes, along with detailed
information about usage, at the following url:

> <http://rebol.com/docs/core23/rebolcore-16.html>


| Datatype   | Example                                | Description
| ---------- | -------------------------------------- | -----------
| Decimal    | `1.2`                                  | A number with a fractional component
| Integer    | `4`                                    | A whole number
| Binary     | `#{ccffcc}`                            | Numbers that don’t use a 10-based system (binary, hex, 64-encoded)
| Block      | `[ 1 1.2 "Dude!" ]`                    | A collected group of values and words
| Email      | `dude@sweet.com`                       | An email address
| File       | `%path/to/file.txt`                    | The name of a file or directory
| Hash       | `to-hash [ 1 "uno" 2 "dos" 3 "tres" ]` | A specialized block for quickly finding data - _sort of like dictionaries or associative arrays in other languages_
| Image      | `image: load %logo.jpg`                | A specialized block for holding RGB images - _You can also use binary formatting to describe the image within the document itself, if you want_
| Issue      | `#Pock-Y-STX-5`                        | Handy for phone numbers, serial codes, clone identification, or credit cards
| List       | `to-list[1 2 3]`                       | A specialized block for quickly handling large numbers of insertions and removals
| Paren      | `1 + (2 * 3)`                          | A block that forces immediate evaluation of the values and words it contains
| Path       | `/geekery/rebol/datatypes`             | Used to navigate to or find something. Think of subscripting or object methods, and you’re along the right track.
| String     | `"Dude! What's mine say?"`             | A series of characters. What we humans often use to form words and sentences.
| Tag        | `<img src="slor.jpg" />`               | An HTML tag. Having tags as a native datatype makes parsing and writing Web pages very simple.
| URL        | `http://www.rebol.com/`                | A URL, used for finding stuff on the Internet.
| Character  | `#"Z"`                                 | Not a string, but a single, solitary character.
| Date       | `23-Dec-2004`                          | A single specific calendar date, and sometimes the time to go along with it - _can be created in a dizzying number of ways in REBOL_
| Logic      | `true`                                 | The basic boolean values used for evaluating any yes or no questions.
| Money      | `$8.24`                                | Monetary values. That stuff I never seem to have 2 days after payday.
| None       | `none`                                 | Nothing. No value. Not even zero. Zen, man. - _okay, I’m getting a little goofy now_
| Pair       | `320x200`                              | An (X,Y) ordered pair used for coordinates on a display or sizes.
| Refinement | `system/version`                       | Modifiers used to indicate some variation or extension in the meaning of a value - _Adjectives, basically. Neat, eh?_
| Time       | `16:25`                                | Hours, minutes, and even seconds, if you like. _An entire category of C programming exercises becomes meaningless thanks to this_
| Tuple      | `127.0.0.1`                            | A "dotted series" of integers, often useful for version numbers, net addresses, and color values.
| Words      | `word`                                 | Symbols used by REBOL. Might be a variable - or not, depending on how you use it.

And remember, basically everything is a datatype. Even datatypes.