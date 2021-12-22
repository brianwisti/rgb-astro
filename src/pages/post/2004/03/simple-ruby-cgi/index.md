---
aliases:
- /coolnamehere/2004/03/10_simple-ruby-cgi.html
- /post/2004/simple-ruby-cgi/
- /2004/03/10/simple-ruby-cgi/
category: coolnamehere
date: 2004-03-10 00:00:00
layout: layout:PublishedArticle
slug: simple-ruby-cgi
tags:
- ruby
- web
- learn
title: Simple Ruby CGI
updated: 2009-07-11 00:00:00
uuid: 9ff8b133-27a3-4d65-b004-aedb75f93f28
---

This article is intended to provide a casual introduction the CGI
programming with the [Ruby](/tags/ruby/) language. You won’t be an
expert when you are done, but you will certainly be ready to explore
more on your own, and maybe delve into becoming a Ruby/CGI expert.

## Why Are You Reading This?

There are a couple of possibilities, other than the obvious “I have
nothing better to do”. That’s my excuse, incidentally, so you better
pick another. Perhaps you have been using Ruby for a little while, and
you want to learn how to use this curious language as a Web programming
tool. There is also the possibility that you are a grizzled Perl/CGI
veteran of many years, and you are interested in learning how this
curious language handles tasks that you do every day with CGI.pm.
Hopefully neither of you will be too disappointed by my efforts.

## Why Ruby?

Even though I hesitate to call it my favorite language, I definitely
prefer to do most of my coding in Ruby these days. It is similar to my
other favorite, [Perl](/tags/perl/), because it is put together in such
a way that programs are easy to write. I must admit that large programs
are easier to manage in Ruby, though. I use object-oriented programming
techniques to abstract and tame the complexity of particularly
challenging projects. Support for object-oriented programming is built
into the Ruby language, so extremely large and complex applications are
relatively simple to build and maintain.

## Why CGI?

I’ll give you the easy answer first: I chose to write an article on CGI
programming with Ruby because CGI programming is what I know best. I’ve
been doing CGI for nearly ten years now, and can comfortably answer (or
find the answer to) most questions on the subject. “Write about what you
know” and all that.

The longer answer is that CGI is an established standard, and many of
the more powerful Web development tools use CGI concepts as their basis.
You will be able to create some impressive Web applications using CGI.
CGI is easy to set up on a Web server, and this means that CGI has the
lowest barrier to entry. I think that’s the term - I never have been up
on my buzzwords. Even if you move on to something else later, knowing a
little bit about how CGI works will give you a better appreciation for
the other tools that are available for you.

## Preparation

CGI is a standard part of the Ruby library. All you need to create a CGI
application with Ruby is a standard installation of Ruby and a server
capable of processing CGI requests. This includes nearly every Web
server in existence, but I will focus my attention on the [Apache Web
server](http://httpd.apache.org/). Apache is freely available for most
operating systems, and should be very easy to install from the
directions at the Apache web site.

So let’s say you’ve got a Web server with Ruby installed on it. Add a
text editor such as [Vim](/tags/perl/) or [Emacs](/tags/emacs/), and you
are ready to go!

## CGI Programming

CGI programs are so easy because they are basically just a bunch of
`print` statements chained together. You are usually generating HTML for
the browser to read, but you could also use CGI to generate PDF files,
images, or even interactive Flash! You really have a lot of power and
flexibility, since all you have to do is generate content and tell the
browser what sort of content it is. Anything the browser can’t handle
will be handed off to a plugin.

### “Hello World” The CGI Way

Let’s start with a basic task, pushing some plain old HTML out to the
browser. It isn’t fancy, but it’ll do to help us get a feel for things.

**`hello1.cgi`**

```ruby
#!/usr/bin/ruby

puts "Content-Type: text/html"
puts
puts "<html>"
puts "<body>"
puts "<h1>Hello Ruby!</h1>"
puts "</body>"
puts "</html>"
```

#### Running The CGI Script

Now is the time to upload `hello1.cgi` to the Web server if it’s not
already in place. You’ll also need to make the file executable. If your
FTP application or site management tool supports it, you can use those.
Otherwise, you’ll need to rely on the `chmod` command:

    $ chmod 755 hello1.cgi

Direct your browser to the appropriate URL, and you should see that
basic "Hello Ruby!" message. Simple, but at least we’ve gotten some
of the boring setup out of the way. Now we can start looking at Ruby’s
special touches.

### A Better Way

For our first venture into the `CGI` library, let’s work with the HTML
generating features. This script will produce the same overall output as
the first example, but the code to do it looks a little different. Give
it a try for yourself.

**`hello2.cgi`**

```ruby
#!/usr/bin/ruby

require 'cgi'

# Create a cgi object, with HTML 4 generation methods.
cgi = CGI.new('html4')

# Ask the cgi object to send some text out to the browser.
cgi.out {
 cgi.html {
   cgi.body {
     cgi.h1 { 'Hello Ruby!' }
   }
 }
}
```

This version is functionally the same as the first version, but it takes
advantage of the HTML generating methods available in the CGI object.
The style you use is completely up to you. I generally lean towards a
template-based approach, but we can get into that in a different
article. I’ll alternate between `puts` and using the object-oriented
style as the whim strikes me.