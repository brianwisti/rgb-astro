---
aliases:
- /blogspot/2009/06/12_python-blogger-refresh-part-2-settings.html
- /post/2009/python-blogger-refresh-part-2-settings/
- /2009/06/12/python-blogger-refresh-part-2-settings/
category: blogspot
date: 2009-06-12 00:00:00
layout: layout:PublishedArticle
series:
- Python Blogger Refresh
slug: python-blogger-refresh-part-2-settings
tags:
- blogger
- gdata
- python
title: Python Blogger Refresh Part 2 - Settings
uuid: 4235a7b0-4fc9-4d10-8bac-dee2aa86fd89
---

<!--more-->

## The Idea

[last time]: /post/2009/06/python-blogger-refresh-part-1

I had to focus my efforts [last time][] on restoring the original functionality
of my Python Blogger script. That's out of the way. I can now start looking at
enhancements. The first annoyance - of many - is the fact that Blogger connection
settings are hard-coded into the script. Do you want to post to a different blog?
That's going to require editing the source.
<!--more-->

Let's fix that three ways:

1. Adding the ability to define connection details from the command line
2. Adding the ability to define connection details from a config file.
3. Adding the ability to interactively request connection details when they
   have not been specified on the command line or in a config file.

### From the Command Line

We're already using [optparse](http://docs.python.org/library/optparse.html), so adding
the ability to define connection settings from the command line won't be difficult. Three
options are needed:

* Author Name
* Email
* Password

Add those options in `main` with `parser.add_option`.

``` python
def main():
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-D", "--do-tests", action="store_true", dest="doTests",
                      help="Run built-in doctests")
    parser.add_option("-f", "--file", dest="filename",
                      help="Specify source file for post")
    parser.add_option("-a", "--author", dest="author",
                      help="The author for this post")
    parser.add_option("-e", "--email", dest="email",
                      help="The email of the blog owner")
    parser.add_option("-p", "--password", dest="password",
                      help="The password of the blog owner")
    (options, args) = parser.parse_args()

    if options.doTests:
        runTests()

    # Only process post options if user specified a file to post.
    if options.filename:
        try:
            if not options.author:
                raise NameError("Author required. --help for usage")
            if not options.email:
                raise NameError("Email required. --help for usage")
            if not options.password:
                raise NameError("Password required. --help for usage")
        except NameError as e:
            parser.print_help()
            print e
            sys.exit(1)

        author = options.author
        email = options.email
        password = options.password
        post = BlogPost(author, email, password)
        postFile = open(options.filename).read()
        post.parsePost(postFile)
        post.sendPost()
```

Let's see how that behaves. First I'll try using the old way, which is now the
wrong way.

    $ python post-to-blog.py -f python-blogger-part-2-settings.mkd
    /usr/local/lib/python2.6/dist-packages/gdata/tlslite/utils/cryptomath.py:9: \
    DeprecationWarning: the sha module is deprecated; use the hashlib module instead
      import sha
    Usage: post-to-blog.py [options]

    Options:
      -h, --help            show this help message and exit
      -D, --do-tests        Run built-in doctests
      -f FILENAME, --file=FILENAME
                            Specify source file for post
      -a AUTHOR, --author=AUTHOR
                            The author for this post
      -e EMAIL, --email=EMAIL
                            The email of the blog owner
      -p PASSWORD, --password=PASSWORD
                            The password of the blog owner
    Author required. --help for usage

That `DeprecationWarning` is coming from inside GData. I won't worry about it for the moment, but
I *will* keep my eyes open for new releases.

Anyways, how about when running it correctly?

    $ python post-to-blog.py -f python-blogger-part-2-settings.mkd -a "Brian Wisti" \
    -e "me@here.com" -p "mysecretpassword"
    /usr/local/lib/python2.6/dist-packages/gdata/tlslite/utils/cryptomath.py:9:     \
    DeprecationWarning: the sha module is deprecated; use the hashlib module instead
      import sha

A quick look at the drafts in my Blogspot dashboard confirms that the code works.
That command line has gotten a bit long, though. How about adding a config file?

### From a Config File

It's good to have a configuration file holding most of your details. We can keep
sensitive information out of the application code, and not have to remember them 
on the command line every time we run the script.

I am going to make a separate `config` directory to hold my config. Why? This
makes it easier for me to expand my definition of what a configuration *is*.
If I want to use non-core Markdown extensions later - and I will - I can
place them here rather than dirtying my Python `site-packages` folder. 
Or `dist-packages`, in Ubuntu's case. Why do they always have to be different?

The actual config file will be a simple ini-style file spiked with *key*=*value* lines.
Here's mine:

``` ini
# config/blog.cfg
[connection]
author=Brian Wisti
email=me@here.com
password=mysecretpassword
```

The [ConfigParser](http://docs.python.org/library/configparser.html) library will be used to handle opening and reading in these
options. Using both a config file and command line parsing is going to require
poking a little bit at everything, so I'm going to move along slowly.

In `main`, I'll set up the ConfigParser.

``` python
def main():
    from optparse import OptionParser
    import ConfigParser

    config_file = "config/blog.cfg"
    config = ConfigParser.ConfigParser()
    config.read(config_file)

    parser = OptionParser()
    parser.add_option("-D", "--do-tests", action="store_true", dest="doTests",
                      help="Run built-in doctests")
    parser.add_option("-f", "--file", dest="filename",
                      help="Specify source file for post")
    parser.add_option("-a", "--author", dest="author",
                      help="The author for this post")
    parser.add_option("-e", "--email", dest="email",
                      help="The email of the blog owner")
    parser.add_option("-p", "--password", dest="password",
                      help="The password of the blog owner")
    (options, args) = parser.parse_args()

    if options.doTests:
        runTests()

    # Allow command line options to overwrite config settings
    if options.author:
        config.set("connection", "author", options.author)

    if options.email:
        config.set("connection", "email", options.email)

    if options.password:
        config.set("connection", "password", options.password)

    if options.filename:
        try:
            author = config.get("connection", "author")
            email = config.get("connection", "email")
            password = config.get("connection", "password")
        except ConfigParser.NoSectionError:
            print "%s is missing the [connection] section!" % config_file
            sys.exit(1)
        except ConfigParser.NoOptionError as e:
            parser.print_help()
            print e
            print "Options can be defined in %s or on command line" % config_file
            sys.exit(1)

        post = BlogPost(author, email, password)
        postFile = open(options.filename).read()
        post.parsePost(postFile)
        post.sendPost()
```

The application reads the configuration file before handling the command line to set up
the normal behavior. It still processes the command line, though. Maybe I don't want to
keep all of my information in the config, or maybe I'm posting to a completely
different blog.

It's nice to get the settings both ways, but I think we can be a little nicer still.

### Interactively

What if there's no config file, or the config file is incomplete, and there are still missing
pieces even after parsing the command line? The behavior I would hope for in an app like this 
is that it would ask me to fill in the missing blanks. Might as well allow the post filename
to be one of the blanks.

``` python
def main():
    # ...
    if options.password:
        config.set("connection", "password", options.password)

    if options.filename:
        config.set("connection", "filename", options.filename)

    for option in [ "author", "email", "password", "filename" ]:
        try:
            value = config.get("connection", option)
        except ConfigParser.NoOptionError, NameError:
            value = raw_input("%s: " % option)
            config.set("connection", option, value)
```

Hey, it works and I don't even have to use a config file if I don't want to!

The only problem is that now I've messed up the way testing behaves.

    $ python post-to-blog.py -D
    /usr/local/lib/python2.6/dist-packages/gdata/tlslite/utils/cryptomath.py:\
    9: DeprecationWarning: the sha module is deprecated; use the hashlib modu\
    le instead
      import sha
    filename:

That's easy enough to fix. I'll just exit after running the tests. You would think I would have
noticed that before. Why would I? I never used the `-f` flag at the same time as
the `-D` flag, so this issue wouldn't have come up.

``` python
def main():
# ...
if options.doTests:
    runTests()
    sys.exit(0)
# ...
```

Let's stop here and get ready for the next leg.

### What Was Accomplished

At the start of this post, we had a script which would submit a blog posting
based on a filename command parameter, using connection settings that were
hard-coded into the script. After a little fiddling around, we've added the 
ability to get all connection details from the command line, from a configuration
file, from interactive input, or some combination of all three. That's a pretty
big step in making this blog post code more useful for people who aren't me.

## Next Time

This code gets the job done, but I will freely admit that this code is getting ugly.
Half the application has tests, and the other half is in `main`. Next time I 
visit this code I'll have to take a long hard look at refactoring and maybe
adding some tests for the stuff that is currently in `main`. I should also look at packaging the whole thing up with [distutils](http://docs.python.org/library/distutils.html). The next post is going to be a long one, isn't it?

## Getting The Code

Although it's still small enough to reasonably paste the code into this blog posting,
I think it might be a little easier for folks to work with if they just had an
archive of what's been done so far.  I'm going to start making it available directly 
from coolnamehere.

*** Update 2015-03-28

Oh, *that's* what that zipfile was for. No, it's long gone now.

I might come up with a better system later, but this will do today. Trust me:
I'll get better at this.