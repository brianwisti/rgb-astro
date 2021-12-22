---
aliases:
- /coolnamehere/2003/06/23_01-first-steps.html
- /post/2003/01-first-steps/
- /2003/06/23/ruby-babysteps-01-first-steps/
category: coolnamehere
date: 2003-06-23 00:00:00
layout: layout:PublishedArticle
slug: ruby-babysteps-01-first-steps
tags:
- ruby
- learn
title: Ruby Babysteps 01 - First Steps
updated: 2017-04-09 00:00:00
uuid: e204315a-eb3f-4b01-9afe-0eba20af8840
---

Ruby is an exciting language with a huge number of features that appeal
to advanced programmers. You should not let that intimidate you, though.
The language is very easy to get started with, and you can work your way
into the more arcane corners.

This page is intended to provide the non-programmer with a gentle
introduction to the Ruby programming language. When you are done with
it, you should feel ready to learn more. You won’t be any kind of
expert, but you will be able find the information you need to go
farther. Beginners and experts alike should feel free to send
suggestions about how to improve this tutorial.

## Installing Ruby

Of course, if you want to use Ruby, you have to install it. To be
honest, installation used to be the trickiest part of dealing with Ruby.
It’s a lot easier to install it these days, depending on your operating
system.

### Linux

As with all things Linux, getting Ruby depends on your distribution. See
if it is already installed on your system. If not, check to see if it’s
available on your distribution discs. If that fails as well, you might
as well move on to the world of compiling software yourself. See a
little further below for details.

### Mac OS X

OS X users have it good. Sort of. A fairly recent Ruby is already
available on the Developer Disk for OS X, so you don’t need to mess with
any of that other stuff to get started. It’s likely that you will want
to later on, but you’ve got enough to get you started. Definitely more
than you’ll be needing with this tutorial\!

See below if you are willing to enter the world of compiling your own
software. It is not as bad as it sounds, trust me.

### Windows

Users of Microsoft Windows are definitely not used to compiling their
own software. Fortunately, the
[RubyInstaller](http://rubyinstaller.org/) project provides an installer
for Windows users.

### Installing From Source

Okay, so there’s no “grab and install” version of Ruby available for
your computer. If you are the adventurous sort, and have a C compiler
handy, you might as well use the traditional UNIX approach: build it
yourself\!

- Download the current stable release of
  [Ruby](http://www.ruby-lang.org/).
- Extract it into a new folder.
- `cd` into the directory with ruby source in it.
- `./configure`
- `make`
- `su` into the root account
- `make install`
- exit the `su` session.
- Start playing with Ruby\!

## Creating Ruby Programs

You’ll probably want to start writing programs at this point. Well, now
that you have installed Ruby, all you need to do is fire up a text
editor and start writing code.

As soon as you’ve been around the programming culture for a while -
sometimes as long as two days - you might notice that some folks have
strong opinions about which is the One True Editor, which you should use
for all of your programming. That’s kind of silly, though. This early,
you can probably make do with almost anything that lets you edit text.
Here are a few of my favorite popular choices:

- [GNU Emacs](/tags/emacs/)
- [Vim](/tags/vim/)

Look around a bit and pick the one that feels most comfortable to you.
If you change your mind later, nobody should hold it against you.

### Hello, World

It is traditional to start programming by creating a program that
displays a simple phrase, such as “Hello, World\!” I am not about to
argue with tradition. Type the following into your text editor:

``` ruby
# hello.rb
#  Displays a warm greeting

puts "Hello, World!"
```

Save the file as `hello.rb`. We’ll be running it in a few moments, but
first - what’s with those first couple of lines?

Well, they’re Ruby *comments*. Comments start from the character `#`,
and extend to the end of the line that you wrote them on. Ruby ignores
comments, which means that you can use them to explain what is going on
in your code. Comments are good. When you come back to look at a complex
script after several months, you might forget what some block of code
does. Having the comments there to remind you will make it that much
easier to sort everything out.

I like to start every one of my scripts off with a quick header to
describe the purpose of the program. Here is the rough template:

``` ruby
# hello.rb
#  Displays a warm greeting
```

Of course, your header can be as complicated as you like:

``` ruby
# hello.rb
#  Displays a warm greeting.
#
# = AUTHOR
#   Brian Wisti (brian@coolnamehere.com)
# = DATE
#   9 March 2009
# = VERSION
#   1.0
# = PURPOSE
#   Demonstration script for my Ruby tutorial at
#   http://www.coolnamehere.com/geekery/ruby/rubytut/
# = USAGE
#   ruby hello.rb
# = LICENSE
#   You may copy and redistribute this program as you see fit, with no
#   restrictions.
# = WARRANTY
#   This program comes with NO warranty, real or implied.
```

Just try to match the header complexity to the program. Using this
header for a program that consists of one line of code might be just a
*little* bit of overkill. I usually start with the two-line header and
expand it as I see fit.

Now you probably would like to know how to actually run a program. Save
the file you have been editing, and switch to a command line. Type the
following at the command prompt:

    $ ruby hello.rb
    Hello, World!

That was kind of cool. It would be nice to customize it a little bit.
Maybe we could change the program so that it says "Hello" to us
personally.

``` ruby
# hello.rb
#  Displays a warm greeting.

name = "Brian"
puts "Hello, #{name}"
```

Save the file, and run it again.

    $ ruby hello.rb
    Hello, Brian!

We stored the string "Brian" in the variable `name`. A *variable* is
basically just something you want the computer to remember so that you
can get to it later. You can get a lot more complicated than that if you
want, and a lot of programmers do. However, this definition should do
for a long time.

The string itself is a special sort of variable called an *object*.
Objects are very powerful things - so powerful that every variable in
Ruby is an object. You can do a lot more with a variable than just ask
the computer what the object’s value is. An object has a set of things
that it knows how to do. For example: a String knows how to ask Ruby to
work out a value when you place some Ruby code - such as a variable name
- inside the string. The code is marked by special characters. Then it
will take the value that Ruby found, and insert it where the special
marker was placed. You could change the value of `name` and rerun the
program. The correct value will be displayed in the greeting string.

``` ruby
name = "Matt"
puts "Hello, #{name}!"
```

See?

    $ ruby hello.rb
    Hello, Matt!

Having a program that displays the exact same message every time you run
it is nice when it comes to being consistent, but not so entertaining as
a program. Let’s make things a little more interesting still. Instead of
changing the value of `name` in the code of the program, we can use the
`gets` method to get a name from the user.

``` ruby
print "What is your name? "
reply = gets
name = reply.chomp
puts "Hello, #{name}!"
```

Running this is a little more fun:

    $ What is your name? Brian
    Hello, Brian!

The `gets` method … wait, I used that word again, “method”. You might be
wondering what that is supposed to be. A *method* is one thing that an
object is capable of. We have to call it by name. You can’t just say
“Ball, do whatever it is you do.” We have to say “Ball, bounce\!” In
the real world, of course, talking to the ball would not be very
helpful. But you get the idea.

`gets` is a method that gets a line of text from the user and *returns*
it to - or hands back to - the program. What do we do with that reply?
We `chomp` it\! `gets` returns *all* of the text it gets, including the
bit that represents the ENTER key you pressed. We don’t want to keep
that, though, so we need a safe way to remove the ENTER character
without doing anything to the rest of the string. `chomp` is a method
associated with Strings of text which asks the string to remove that
rogue ENTER character. A cleaner copy of the string is returned for you
to display.

If you don’t believe me about the ENTER character, you can test it for
yourself. In the string which is printed by `puts`, replace `name` with
`reply`. You’ll see what I am talking about.

``` ruby
puts "Hello, #{reply}!"
```

Generally, you call an object’s methods by tagging a dot and the method
name at the end, like `object.method`. There are lots of things you can
do with methods, and lots of ways to treat them, but that is beyond the
scope of this article.

For now, though, you’ve learned enough to get started, and now I want
you to play around with what you’ve learned and enjoy yourself a little
bit.

## Conclusion

Congratulations\! You have just begun learning Ruby. You just wrote a
complete program which gets input from a user, and prints output which
includes a modified version of their input\! Stop for a minute and think
about that. Of course there’s a lot more to learn, but it’s well within
your abilities. There is an ever-growing abundance of resources for the
“Ruby Newbie”, and you should take advantage of as many of them as
possible\!

- The [Ruby home page](http://www.ruby-lang.org/) is pretty much the
  best place to start, since that is where you’ll find Ruby itself, as
  well as information about user mailing lists that you might be
  interested in subscribing to. Never underestimate the potential help
  that you can get from the rest of the community.
- The [Ruby Forum](https://www.ruby-forum.com/) site provides Web
  access to all of the major Ruby and Rails mailing lists. You can
  check archives, see recent posts, and even post from this interface.