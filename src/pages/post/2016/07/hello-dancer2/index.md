---
aliases:
- /post/2016/dancer2-hello/
- /2016/07/11/hello-dancer2/
category: Programming
date: 2016-07-11 00:00:00
description: Some simple first steps with the Perl 5 Dancer2 web framework
draft: false
layout: layout:PublishedArticle
slug: hello-dancer2
tags:
- perl
- dancer
- learn
title: Hello Dancer2
uuid: 9b5b99c2-cbce-48da-8ea5-f217d146097a
---

The [PerlDancer](https://github.com/PerlDancer/) team’s
[Dancer2](https://metacpan.org/pod/Dancer2) project is a Perl framework
for writing Web applications with less [boilerplate
code](https://en.wikipedia.org/wiki/Boilerplate_code) than other Web
frameworks. I am slowly exploring what it offers. Feel free to follow
along.

This is sort of a tutorial. I assume you know Perl and maybe a bit about
Web server programming, but not that you have mastered either. My pace
may annoy you if you *have* mastered Perl, Web programming, or Dancer2.

## Installation

I use Perl 5.24.0 and [cpanm](https://metacpan.org/pod/App::cpanminus)
via [Perlbrew](http://perlbrew.pl/). Installation of Dancer2 and its
dependencies requires a single command.

    $ cpanm Dancer2

## Hey

You do not need much code to create a Dancer2 application.

``` perl
use Dancer2;     # Load Dancer2 and its keywords

get '/hey' => sub { # Define some routes
  return 'Hey!';
};

start;           # Run the application
```

Even better: you can hand this code to Perl and it starts a server\!

    $ perl hey.pl
    >> Dancer2 v0.200002 server 15388 listening on http://0.0.0.0:3000

Loading `http://localhost:3000/hey` in a browser shows our simple
message.

![Hey from Dancer2](dancer2-hey.png "Hey from Dancer2!")

Dancer2 gives you a
[DSL](https://en.wikipedia.org/wiki/Domain-specific_language) —
Domain-Specific Language — to describe your application. These DSL
[keywords](https://metacpan.org/pod/distribution/Dancer2/lib/Dancer2/Manual.pod#DSL-KEYWORDS)
cut down the boilerplate code common in some Web development frameworks.

### `get`

The
[get](https://metacpan.org/pod/distribution/Dancer2/lib/Dancer2/Manual.pod#get)
keyword defines a [route](https://metacpan.org/pod/Dancer2::Core::Route)
for Dancer2. Routes tell Dancer2 how to respond when someone requests a
path — the /hey bit — from your application. `get` is also a method from
[HTTP](https://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol). Use
it when you only want to "get" something from the application. Dancer2
has keywords for more HTTP methods, but `get` is fine for now.

What happens if someone requests a path that you did not define?

Your Dancer2 application returns an error page informing them that the
path does not exist.

With the HTTP method and path defined, the last important part of our
route is the code. Your application runs that code and sends its return
value to the visitor. Our first route code example is an anonymous
subroutine that returns the text "Hello\!", but they can be as
complicated as you need.

### `start`

[start](https://metacpan.org/pod/distribution/Dancer2/lib/Dancer2/Manual.pod#start)
tells Dancer2 that you finished defining your application and it can
begin serving to the world.

DSL = Keywords + Sugar

Keywords make the Dancer2 DSL work, but the code style takes advantage
of Perl’s flexible syntax. Our route looks like this with less
[syntactic sugar](https://en.wikipedia.org/wiki/Syntactic_sugar).

``` perl
get('/hey', sub { return 'Hey!'; });
```

## Hey You

How about greeting the visitor by name? Since form processing involves
more steps than I want to think about today, we use route parameters
instead.

Dancer2 allows placeholders in route paths. The simplest placeholders
are tokens prefixed with a colon, such as `:name` or `:id`. When you
make a request that matches, such as `/hey/brian`, Dancer2 saves the
matching path part. Here, look at some code.

``` perl
use Dancer2;

# A simple greeting: /hey
get '/hey' => sub {
  return 'Hey!';
  };

# A personalized greeting: /hey/Brian
get '/hey/:name' => sub {
  my $name = route_parameters->get('name');
  return "Hey $name!";
};

start;
```

Route handlers can get [much more
complicated](https://metacpan.org/pod/distribution/Dancer2/lib/Dancer2/Manual.pod#Route-Handlers),
but not today. Our application treats a general greeting and a greeting
with a distinct name at two different actions, so we use two different
routes.

In order to use the new code, we need to stop the Perl process.
`Control-C` should do it. Then launch it again, and the new code will be
loaded.

    $ perl hey.pl
    >> Dancer2 v0.200002 server 31385 listening on http://0.0.0.0:3000

Now we should be able to see <http://localhost:3000/hey/Brian> — or
whatever name you prefer.

!["Hey Brian\!" in Dancer2](dancer2-hey-brian.png)

### `route_parameters`

[route\_parameters](https://metacpan.org/pod/distribution/Dancer2/lib/Dancer2/Manual.pod#route_parameters)
returns a [hash-like object](https://metacpan.org/pod/Hash::MultiValue)
which stores tokens and their values from a route match. Use the `get`
method when you need those values in your route code.

## Wrap It Up

We installed Dancer2, made just about the simplest Web application I
could think of, and explored a little bit about declaring routes.

What’s next? I plan to look at using template files to produce real Web
pages.