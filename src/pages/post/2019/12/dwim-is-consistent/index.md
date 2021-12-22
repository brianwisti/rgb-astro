---
aliases:
- /2019/12/27/dwim-is-consistent/
category: Programming
date: 2019-12-27
draft: false
layout: layout:PublishedArticle
slug: dwim-is-consistent
tags:
- perl
- python
- DWIM
title: DWIM is consistent
uuid: 9c017b12-39ab-4f8e-8825-6e0752e9d5e3
---

Moshe Zadka has been [writing](https://opensource.com/users/moshez) a
mostly excellent exploration of the [Zen of
Python](https://www.python.org/dev/peps/pep-0020/) for
[Opensource.com](https://opensource.com). Not sure I approve of this
take on guessing, from [The importance of consistency in your Python
code](https://opensource.com/article/19/12/zen-python-consistency):

> What should the result of `1 + "1"` be? Both `"11"` and `2` would be
> valid guesses. This expression is ambiguous: there is no single thing
> it can do that would not be a surprise to at least some people.
>
> Some languages choose to guess. In JavaScript, the result is `"11"`.
> In Perl, the result is 2. In `C`, naturally, the result is the empty
> string. In the face of ambiguity, JavaScript, Perl, and C all guess.

I can’t speak for the other languages, but Perl isn’t guessing. It’s
adding these two values as numbers because we *told it to* by using the
numeric `+` operator. If we wanted a string, we would tell Perl, by
using the `.` concatenation operator.

Let’s fire up
[tinyrepl](https://metacpan.org/pod/distribution/Eval-WithLexicals/bin/tinyrepl)
for a quick demonstration.

    $ tinyrepl
    re.pl$ 1 + "1"
    2
    re.pl$ 1 . "1"
    11

Perl
[operators](https://perldoc.perl.org/perlop.html#Additive-Operators) do
the type casting for you. This is
[DWIM](https://en.wikipedia.org/wiki/DWIM) — “Do What I Mean” — in
action. You say you want numbers? Perl gives you numbers. You say you
want strings? Perl gives you strings.

Are `1 + "1"` and `1 . "1"` better than `1 + int("1")` and `str(1) +
"1"`? I don’t know. Perl was born for text processing. Most of its
[affordances](https://en.wikipedia.org/wiki/Affordance) make the most
sense in that context.

DWIM can be surprising to those unfamiliar with this approach. But it’s
not guessing.

The points about consistency and ambiguity are solid. The Zen of Python
can be applied with slight modifications to all programming. Just
remember that "obvious" is different in different languages.