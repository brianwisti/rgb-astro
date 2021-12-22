---
aliases:
- /coolnamehere/2009/05/05_02-user-input.html
- /post/2009/02-user-input/
- /2009/05/05/perl-5-babysteps-02-user-input/
category: coolnamehere
date: 2009-05-05 00:00:00
layout: layout:PublishedArticle
slug: perl-5-babysteps-02-user-input
tags:
- perl
- learn
title: Perl 5 Babysteps 02 - User Input
updated: 2009-07-11 00:00:00
uuid: 7eeacafa-7996-4abf-ae30-291cc0d5f6d7
---

Having a program that displays the exact same message every time you
run is nice when it comes to being consistent, but not so entertaining
as a program. "What does it do?" "It prints out my name." "Oh."
Let's make things a little more interesting. We could change the value 
of `$name` in the code, but it might be a little tiresome to do this before 
showing it to each new person. How about making the program ask for a name? 
User interaction - a neat idea.
<!--more-->

It's so neat that I'm going to show you two ways to do it.

## Traditional

Here's how I got user input before Perl 5.10. You'll find a lot of code
that looks like this.

``` perl
=pod

=head1 hello.pl

Displays a warm message.

=cut

# Follow some common-sense guidelines for Perl coding.
use Modern::Perl;

print "What is your name? ";
my $name = <STDIN>;
chomp($name);
say "Hello, $name!";
```

Why don't we run this before we start trying to decipher it?

    $ perl hello.pl
    What is your name? Brian[ENTER]
    Hello, Brian!

There is a lot going on in the few lines we added. Let's look at them one by one.

``` perl
print "What is your name? ";
```

`print` is how we used to get messages displayed on the console. It's still
useful when you want to say something but you don't want to start a whole new
line when it's done. We use `print` so that our answer to the question will
display on the same line as the question itself. That is a common approach
to user prompts.

``` perl
my $name = <STDIN>;
```

We've got some funny-looking thing instead of "Brian". What is it?  Here's the 
short explanation:

> `<STDIN>` gets input from the user that you can save in a variable.

There's also a long version. Feel free to skip it if you just want to get on 
with it. The long version works out like this:

> The scalar `$name` is assigned the value of `<STDIN>`. `<...>` tells Perl
> that we want it to read a *filehandle* and hand the results back to us. A
> *filehandle* is a source of information. It could be an open file, but in
> this case it is `STDIN`. *`STDIN`* is the *standard input stream* - geek talk
> for "wherever we expect user input to be coming from." `STDIN` usually just
> means "keys the user enters from the keyboard." The result of reading from
> the filehandle - which is `STDIN` in this case, which is the keys you entered
> from the keyboard in this case - is stored in `$name`.

There's a really long version, but I'm getting bored so we'll skip it.

``` perl
chomp($name);
```


`chomp` removes the last character from a string if that character is 
a newline - whatever a newline is defined as on your platform. Why do we need 
that? Well, when Perl reads with the `<...>` operator, it gives 
you *everything*. That includes the `[ENTER]` key that you pressed to send your 
name to the program. What that ENTER actually looks like depends on your platform:
but the end result is a line break in the text. Sometimes we like that, but not
today. Here's what you would see if you left out `chomp`:

    $ perl hello.pl
    What is your name? Brian[ENTER]
    Hello, Brian
    !
    $

You can see that you're going to use `chomp` a lot when getting user input. But
what if there were an easier way? There is ... sort of.

## A new way

The new way looks better to my eyes, but I'm willing to admit that there's a lot
going on for a beginner. You can feel free to ignore this section if you like,
and my feelings won't be hurt at all.

``` perl
=pod

=head1 hello.pl

Displays a warm message.

=cut

# Follow some common-sense guidelines for Perl coding.
use Modern::Perl;

use Term::UI;
use Term::ReadLine;

my $console = Term::ReadLine->new();
my $name    = $console->get_reply( prompt => "What is your name? " );
say "Hello, $name!";
```

The program is doing nearly the same thing as before, but the code looks a 
lot different. We `use` some new stuff, added a new variable, and have changed
the way we get the user's name. On the other hand, we don't have to `chomp`
anything.

### Looking at the changes

``` perl
use Term::UI;
use Term::ReadLine;
```

These lines tell Perl to load a couple of modules for some additional
functionality. This is different from when we called `use` before. With
Modern::Perl we were giving Perl a new personality. This
time we're just making some new functions available. Module names are usually
capitalized like proper names, and that `::` is conventionally used to indicate
related modules within a category.

Why do we want those modules? So we can create an object that reads user input.

``` perl
my $console = Term::ReadLine->new();
my $name    = $console->get_reply( prompt => "What is your name? " );
```

There are a lot of things to learn in these two lines of code, so please
forgive me if I rush through them too quickly.

What's an object? Oh boy. That is a tricky question for a beginner tutorial.
It's so tricky that I've decided to skip it completely. Almost completely.
Objects are basically magic scalar variables that hold extra information
such as data (the *fields*) and subroutines (the *methods*). Intelligent
use of objects allow you to quickly write powerful programs while hiding the
complexity of what's going on behind a sweet and smiling face.

*Classes* define the structure of a particular type of object. You create an
object with a *constructor* method defined in the class. The constructor is
usually called `new`, and you access it with the `->` operator. The same
operator is used to access the methods of your `$console` object.

The last source of confusion in this new example is the way we asked `$console`
to present its prompt to the user. The quick way to think of it is that we are
giving a dictionary to `get_reply`. `get_reply` looks at this dictionary for
keywords that are important to it, such as `prompt`. We use that `=>` operator
to tell `$console->get_reply` that we want the `prompt` to be "What is 
your name? "

I'll get more into dictionaries later, but that's the basic idea for now. Wait,
one more thing. It's helpful to think of those special keyword lookup collections
as dictionaries, but they're really called *hashes*.

Enough babbling. Let's run it.

<pre>
$ perl hello.pl
<u>What is your name?</u> <b>Brian</b>
Hello, Brian!
</pre>

Nice, it adds some formatting to the process! Well, it does for me. You might 
not get the formatting if your console doesn't support it.

We only added a few lines to our program, but it made a significant difference
in the end. Maybe you don't understand what is going on behind those changes.
That's okay. Perl is a strange language, full of things that are very easy and
fairly challenging at the same time. Give yourself time to learn the language
and explore its features. Definitely explore the available libraries,
because you will be amazed by how much you can improve your programs. And
I don't forget to explore [CPAN](http://www.cpan.org/), the gigantic repository
of libraries for Perl.