---
aliases:
- /blogspot/2007/12/28_python-loves-blogger.html
- /post/2007/python-loves-blogger/
- /2007/12/28/python-loves-blogger-part-1/
category: blogspot
date: 2007-12-28 00:00:00
layout: layout:PublishedArticle
slug: python-loves-blogger-part-1
description: Posting to Blogger with Python
tags:
- blogger
- python
title: Python Loves Blogger (Part 1)
updated: 2015-03-28 00:00:00
uuid: a17f7ee9-4274-4000-be86-65985560479b
---

[here]: /post/2009/06/python-blogger-refresh-part-1/

I've revisited the code for Blogger posting with Python. Start [here][] to see the new starting point.
<!--more-->

## The Original Tale

I want the ability to post to my blogs from the command line. That's because
I prefer to do *everything* from the command line, but that's not really the
point. The point is that I want an excuse to write a new quick script and
satisfy that constant urge to gain some new superpower. Okay, so blogging's
not a superpower. Hush.

I'm writing this into a text file via [vim](http://www.vim.org). It is written
in a format known as [Markdown](http://daringfireball.net/projects/markdown/),
because I hate writing HTML by hand these days. It will eventually manifest as
an HTML formatted post on my
Blogger account.

[Python]: http://python.org
[Google Blogger API]: https://developers.google.com/blogger/
[GData Python Client]: https://github.com/google/gdata-python-client

All of the hard work is going to be done with [Python][]. Why
Python? Mainly because the [Google Blogger API][] is supported rather well by Python.
They love their snake-based languages at Google, and it shows in the [GData Python Client][] library.

I could just as easily have used Perl or Ruby for this project. Heck, I could
have used REBOL for this project if I was willing to craft some of the
library by hand. All of these things are possibilities for the future. One
thing I love to do is reimplement applications in various languages. It's a
sickness.

## The Application Skeleton

Basic usage will be `python post-to-blog.py post.txt`. `post.txt` is a text
file containing details like title or tags and the post body.

Here's the basic pseudo-code that will work fine for simple posts.

1. Load global settings such as login and account URL
2. Create a local blog post based on the configuration and body from contents of `post.txt`
3. Request that Blogger publish this post.
4. Report the results of the request.

It's fairly straightforward, but already shows me one class I'll be using to mask the details:

``` python
# post-to-blog.py

class BlogPost(object):
    """A single posting for a blog owned by a Blogger account"""

if __name__ == '__main__':
   import doctest
   doctest.testmod()
```

[doctest]: https://docs.python.org/2/library/doctest.html

I plan to use the [doctest][] module
to incorporate tests as I write this. It'll get invoked if the script is run
directly. I'll put in some command line parsing later so that the tests can still
be run but it doesn't have to be the default behavior.

I already know what libraries I'm going to use, so let's install those.


## Installing Dependencies

I need a few things to make this work:

[Python Markdown]: https://pypi.python.org/pypi/Markdown

* [ActiveState Python 2.5.1](http://activestate.com/Products/activepython/), because I am not in the mood to compile anything today.
* The [Python Markdown][] library, to handle the formatting.
* The [GData Python Client][], because that's the whole *reason* I'm starting with Python instead of another language.
* A Blogger account. Seemed obvious, but I thought I'd mention it.

I already have Python installed, so let's move on to Markdown. It's simple
enough to install and verify.

    ~/src/pymods brian$ unzip ~/python_markdown-1.7.rc1.zip
    ~/src/pymods brian$ cd python_markdown-1.7/
    ~/src/pymods/python_markdown-1.7 brian$ sudo python setup.py install
    ~/src/pymods/python_markdown-1.7 brian$ python
    ActivePython 2.5.1.1 (ActiveState Software Inc.) based on
    Python 2.5.1 (r251:54863, May  1 2007, 17:40:00)
    [GCC 4.0.1 (Apple Computer, Inc. build 5250)] on darwin
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import markdown
    >>> markdown.markdown("# Hello")
    u'<h1>Hello</h1>'
    >>>

Next I'll install GData.

    ~/src/pymods brian$ tar xfvz ~/gdata.py-1.0.10.latest.tar.gz
    ~/src/pymods/gdata.py-1.0.10.1 brian$ cd gdata.py-1.0.10.1/
    ~/src/pymods/gdata.py-1.0.10.1 brian$ sudo python setup.py install

What can I do to verify this one? Let's just run the provided sample Blogger code.

    $ cd samples/blogger
    $ python BloggerExample.py --email [email] --password [password]

There's a bunch of spew, and posts are made and deleted along with comments. Looks like it works.


## Posting Formats

[Emacs]: /tags/emacs/

My blog post files will have a fairly straightforward layout, with a head
section and a body section. It'll look ... well, it'll look a lot like the
`lj-compose` buffer in [Emacs][] for composing Livejournal posts, now that I think about it.

``` markdown
title: Python Loves Blogger
tags: python,gdata,project,blogger
--
I want the ability to post to my blogs from the command line. That's because
I prefer to do *everything* from the command line, but that's not really the
point. The point is that I want an excuse to write a new quick script and
satisfy that constant urge to gain some new superpower. Okay, so blogging's
not a superpower. Hush.
```

The two sections are separated by a line containing only the characters `--`.

The head section uses a common format where each line contains a key and its
value, with a colon and space combo `:` separating them. The keys and values
in a blog posting contain details that are important to Blogger and unique to
this particular file. Right now that means I'm only using *title* and *tags*.

I'll just use commas for now when listing multiple values for a single key,
such as with tags.

    key1: value1
    key2: value2,value3,value4,value5

The body section is just Markdown-formatted text, including extensions that
are available in the Python Markdown library.


### Parsing the Config Header

[ConfigParser]: https://docs.python.org/2/library/configparser.html

There is a very handy [ConfigParser][] class
available in the Python standard libs, but it's actually a little more than I
need in a single post file. I just want to examine each line for key/value
pairings without worrying about providing sections or a filehandle-like object
to make ConfigParser happy.

``` python
class BlogPost(object):
   """A single posting for a blog owned by a Blogger account
   """

   def __init__(self):
       self.__config = {}

   def parseConfig(self, configText):
       """Reads and stores the directives from the post's config header.

       >>> post = BlogPost()
       >>> import os
       >>> myConfig = os.linesep.join(["key1: value1", "key2: value2"])
       >>> post.parseConfig(myConfig)
       >>> post.getConfig('key1')
       'value1'
       >>> post.getConfig('key2')
       'value2'
       """
       textLines = configText.splitlines()
       for line in textLines:
           key, value = line.split(': ')
           self.__config[key] = value

   def getConfig(self, key):
   """Fetch the value of a config directive"""
       return self.__config[key]

if __name__ == '__main__':
   import doctest
   doctest.testmod()
```

That was pretty easy, although I did have to do a little thinking to work around the
fact that newline escapes tend to be read before `doctest` can get to them. Anyways,
config lines are split on the `: ` pair of characters. A regular expression might be
better for general use but I'm still going for quick, dirty, and exactly what *I* want.


### Parsing the Post Body

Now let's get some HTML out of a block of Markdown-formatted text.

``` python
import markdown

class BlogPost(object):
   """A single posting for a blog owned by a Blogger account
   """

   def __init__(self):
       self.__config = {}
       self.__body = None

   def parseBody(self, bodyText):
       """Generates HTML from Markdown-formatted text.

       >>> post = BlogPost()
       >>> post.parseBody('This is a paragraph')
       >>> post.getBody().find('<p>This is a paragraph')
       0
       """
       self.__body = markdown.markdown(bodyText)

   def parseConfig(self, configText):
       """Reads and stores the directives from the post's config header.

       >>> post = BlogPost()
       >>> import os
       >>> myConfig = os.linesep.join(["key1: value1", "key2: value2"])
       >>> post.parseConfig(myConfig)
       >>> post.getConfig('key1')
       'value1'
       >>> post.getConfig('key2')
       'value2'
       """
       textLines = configText.splitlines()
       for line in textLines:
           key, value = line.split(': ')
           self.__config[key] = value

   def getBody(self):
       """Fetch the HTML body of this post."""
       return self.__body

   def getConfig(self, key):
       """Fetch the value of a config directive"""
       return self.__config[key]

if __name__ == '__main__':
   import doctest
   doctest.testmod()
```

Those `doctest` tests are starting to look a little contorted.
`BlogPost.__config` is really just a dictionary, and I don't really care whether
it is private to the object. Let's make the adjustments in `__init__` and
`parseConfig`. We don't need `getConfig` now that we have direct access to
the dictionary.

As long as we're refactoring, I'd prefer it if the message body could be
treated as a property. Setting it would store the string, while getting it
would invoke markup and return the result.

``` python
import markdown

class BlogPost(object):
   """A single posting for a blog owned by a Blogger account

   >>> post = BlogPost()
   >>> post.body = 'This is a paragraph'
   >>> print post.body
   <p>This is a paragraph
   </p>
   """

   def __init__(self):
       self.config = {}
       self.__body = None

   def set_body(self, bodyText):
       """Stores plain text which will be used as the post body

       >>> post = BlogPost()
       >>> post.set_body('This is a paragraph')
       >>>
       """
       self.__body = bodyText

   def get_body(self):
       """Access a HTML-formatted version of the post body

       >>> post = BlogPost()
       >>> post.set_body('This is a paragraph')
       >>> print post.get_body()
       <p>This is a paragraph
       </p>
       """
       return markdown.markdown(self.__body)

   body = property(get_body, set_body)

   def parseConfig(self, configText):
       """Reads and stores the directives from the post's config header.

       >>> post = BlogPost()
       >>> import os
       >>> myConfig = os.linesep.join(["key1: value1", "key2: value2"])
       >>> post.parseConfig(myConfig)
       >>> post.config['key1']
       'value1'
       >>> post.config['key2']
       'value2'
       """
       textLines = configText.splitlines()
       for line in textLines:
           key, value = line.split(': ')
           self.config[key] = value

if __name__ == '__main__':
   import doctest
   doctest.testmod()
```

## Command Line Options

[optparse]: https://docs.python.org/2/library/optparse.html

Before I get too carried away, I want to make sure that there are no ugly
surprises in the formatting of my posts. Let's do the heavy lifting with
[optparse][].

``` python
import markdown

class BlogPost(object):
   """A single posting for a blog owned by a Blogger account

   >>> post = BlogPost()
   >>> post.body = 'This is a paragraph'
   >>> print post.body
   <p>This is a paragraph
   </p>
   """

   def __init__(self):
       self.config = {}
       self.__body = None

   def set_body(self, bodyText):
       """Stores plain text which will be used as the post body

       >>> post = BlogPost()
       >>> post.set_body('This is a paragraph')
       >>>
       """
       self.__body = bodyText

   def get_body(self):
       """Access a HTML-formatted version of the post body

       >>> post = BlogPost()
       >>> post.set_body('This is a paragraph')
       >>> print post.get_body()
       <p>This is a paragraph
       </p>
       """
       return markdown.markdown(self.__body)

   body = property(get_body, set_body)

   def parseConfig(self, configText):
       """Reads and stores the directives from the post's config header.

       >>> post = BlogPost()
       >>> import os
       >>> myConfig = os.linesep.join(["key1: value1", "key2: value2"])
       >>> post.parseConfig(myConfig)
       >>> post.config['key1']
       'value1'
       >>> post.config['key2']
       'value2'
       """
       textLines = configText.splitlines()
       for line in textLines:
           key, value = line.split(': ')
           self.config[key] = value

   def parsePost(self, postText):
       """Parses the contents of a full post, including header and body.

       >>> import os
       >>> myText = os.linesep.join(["title: Test", "--", "This is a test"])
       >>> post = BlogPost()
       >>> post.parsePost(myText)
       >>> print post.config['title']
       Test
       >>> print post.body
       <p>This is a test
       </p>
       """

       header, body = postText.split('--', 1)
       self.parseConfig(header)
       self.body = body

def runTests():
   import doctest
   doctest.testmod()

def main():
   from optparse import OptionParser
   parser = OptionParser()
   parser.add_option("-D", "--do-tests", action="store_true", dest="doTests",
                     help="Run built-in doctests")
   parser.add_option("-f", "--file", dest="filename",
                     help="Specify source file for post")
   (options, args) = parser.parse_args()

   if options.doTests:
       runTests()

   post = BlogPost()

   if options.filename:
       postFile = open(options.filename).read()
       post.parsePost(postFile)
       print post.body

if __name__ == '__main__':
   main()
```

You'll have to just take my word for it that I wrote tests for each stage.
Well, except for verifying that the final output looked roughly like what I
hoped for. I'm not 100% sure how Markdown is going to place its newlines, so
I am looking at the output via STDOUT:

    $ ./post-to-blog.py -f post.txt | more
    <p>I want the ability to post to my blogs from the command line. That's because
      I prefer to do <em>everything</em> from the command line, but that's not really the
      point. The point is that I want an excuse to write a new quick script and
      satisfy that constant urge to gain some new superpower. Okay, so blogging's
      not a superpower. Hush.
    </p>
    ...

I'll save you the details of the full output. It looked about right, though.

Enough stalling. It's time to login and post this article.


## Interacting with Blogger

[the official guide]: https://developers.google.com/blogger/docs/3.0/getting_started

I'll be using [the official guide][]
for Python and Blogger to choose my steps. You aren't likely to find anything
here that isn't already there.

<aside>
<h3>Update 2015-03-28</h3>

The "official guide" link is newer than this post, and you should favor its lessons over these.
</aside>

``` python
import markdown
from xml.etree import ElementTree
from gdata import service
import gdata
import atom
import sys

class BlogPost(object):
   """A single posting for a blog owned by a Blogger account

   >>> post = BlogPost()
   >>> post.body = 'This is a paragraph'
   >>> print post.body
   <p>This is a paragraph
   </p>
   """

   def __init__(self):
       self.config = {}
       self.__body = None

   def set_body(self, bodyText):
       """Stores plain text which will be used as the post body

       >>> post = BlogPost()
       >>> post.set_body('This is a paragraph')
       >>>
       """
       self.__body = bodyText

   def get_body(self):
       """Access a HTML-formatted version of the post body

       >>> post = BlogPost()
       >>> post.set_body('This is a paragraph')
       >>> print post.get_body()
       <p>This is a paragraph
       </p>
       """
       return markdown.markdown(self.__body)

   body = property(get_body, set_body)

   def parseConfig(self, configText):
       """Reads and stores the directives from the post's config header.

       >>> post = BlogPost()
       >>> import os
       >>> myConfig = os.linesep.join(["key1: value1", "key2: value2"])
       >>> post.parseConfig(myConfig)
       >>> post.config['key1']
       'value1'
       >>> post.config['key2']
       'value2'
       """
       textLines = configText.splitlines()
       for line in textLines:
           key, value = line.split(': ')
           self.config[key] = value

   def parsePost(self, postText):
       """Parses the contents of a full post, including header and body.

       >>> import os
       >>> myText = os.linesep.join(["title: Test", "--", "This is a test"])
       >>> post = BlogPost()
       >>> post.parsePost(myText)
       >>> print post.config['title']
       Test
       >>> print post.body
       <p>This is a test
       </p>
       """

       header, body = postText.split('--', 1)
       self.parseConfig(header)
       self.body = body

   def sendPost(self, username, password):
       """Log into Blogger and submit my already parsed post"""
       blogger = service.GDataService(username, password)
       blogger.source = 'post-to-blog.py_v01.0'
       blogger.service = 'blogger'
       blogger.server = 'www.blogger.com'
       blogger.ProgrammaticLogin()

       query = service.Query()
       query.feed = '/feeds/default/blogs'
       feed = blogger.Get(query.ToUri())
       blog_id = feed.entry[0].GetSelfLink().href.split("/")[-1]

       entry = gdata.GDataEntry()
       entry.author.append(atom.Author(atom.Name(text=username)))
       entry.title = self.config['title']
       entry.content = atom.Content('html', '', self.body)
       blogger.Post(entry, '/feeds/' + blog_id + '/posts/default')

def runTests():
   import doctest
   doctest.testmod()

def main():
   from optparse import OptionParser
   parser = OptionParser()
   parser.add_option("-D", "--do-tests", action="store_true", dest="doTests",
                     help="Run built-in doctests")
   parser.add_option("-f", "--file", dest="filename",
                     help="Specify source file for post")
   parser.add_option("-u", "--user", dest="username",
                     help="Blogger account name")
   parser.add_option("-p", "--password", dest="password",
                     help="Blogger account password")
   (options, args) = parser.parse_args()

   if options.doTests:
       runTests()

   post = BlogPost()

   if options.filename and options.username and options.password:
       postFile = open(options.filename).read()
       post.parsePost(postFile)
       post.sendPost(options.username, options.password)

if __name__ == '__main__':
   main()
```

I haven't figured out tags/labels yet, but let's see how well this works. If
you see this post, then I'll know that Part 1 of my little quest is complete!

Um ... okay, no. That didn't work. I got a couple syntax and library errors, but
after fixing those I still got an error code `bX-y33b4h`. [This thread](http://groups.google.com/group/bloggerDev/browse_thread/thread/5788317a11c21268)
showed me that I wasn't alone, but didn't do much to solve my problem. I'll
have to look at the sample code that is in the python gdata distribution.

... later ...

That posted, but I lost all the line breaks in my `pre` blocks. I decided to pick a new template, and that seemed to do the trick. I will *definitely* be fine tuning that template as I move along.

At some point I'll figure out how to add labels.

## The Code So Far

This is the code I used to publish this post. Definitely a work in progress - this version will submit your post as a draft, for example.

``` python
# post-to-blog.py

import markdown
from xml.etree import ElementTree
from gdata import service
import gdata
import atom
import sys

class BlogPost(object):
    """A single posting for a blog owned by a Blogger account

    >>> post = BlogPost()
    >>> post.body = 'This is a paragraph'
    >>> print post.body
    This is a paragraph
    
    """

    def __init__(self, author, account, password):
        self.config = {}
        self.__body = None
        self.__author = author
        self.__account = account
        self.__password = password

    def set_body(self, bodyText):
        """Stores plain text which will be used as the post body

        >>> post = BlogPost()
        >>> post.set_body('This is a paragraph')
        >>>
        """
        self.__body = bodyText

    def get_body(self):
        """Access a HTML-formatted version of the post body

        >>> post = BlogPost()
        >>> post.set_body('This is a paragraph')
        >>> print post.get_body()
        This is a paragraph
        
        """
        return markdown.markdown(self.__body)

    body = property(get_body, set_body)
    
    def parseConfig(self, configText):
        """Reads and stores the directives from the post's config header.

        >>> post = BlogPost()
        >>> import os
        >>> myConfig = os.linesep.join(["key1: value1", "key2: value2"])
        >>> post.parseConfig(myConfig)
        >>> post.config['key1']
        'value1'
        >>> post.config['key2']
        'value2'
        """
        textLines = configText.splitlines()
        for line in textLines:
            key, value = line.split(': ')
            self.config[key] = value

    def parsePost(self, postText):
        """Parses the contents of a full post, including header and body.

        >>> import os
        >>> myText = os.linesep.join(["title: Test", "--", "This is a test"])
        >>> post = BlogPost()
        >>> post.parsePost(myText)
        >>> print post.config['title']
        Test
        >>> print post.body
        This is a test
        
        """
        
        header, body = postText.split('--', 1)
        self.parseConfig(header)
        self.body = body

    def sendPost(self):
        """Log into Blogger and submit my already parsed post"""

        # Authenticate using ClientLogin
        blogger = service.GDataService(self.__account, self.__password)
        blogger.source = 'post-to-blog.py_v01.0'
        blogger.service = 'blogger'
        blogger.server = 'www.blogger.com'
        blogger.ProgrammaticLogin()

        # Get the blog ID
        query = service.Query()
        query.feed = '/feeds/default/blogs'
        feed = blogger.Get(query.ToUri())
        blog_id = feed.entry[0].GetSelfLink().href.split("/")[-1]

        # Create the entry to insert.
        entry = gdata.GDataEntry()
        entry.author.append(atom.Author(atom.Name(text=self.__author)))
        entry.title = atom.Title('xhtml', self.config['title'])
        entry.content = atom.Content(content_type='html', text=self.body)
        control = atom.Control()
        control.draft = atom.Draft(text='yes')
        entry.control = control
        blogger.Post(entry, '/feeds/' + blog_id + '/posts/default')

def runTests():
    import doctest
    doctest.testmod()

def main():
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-D", "--do-tests", action="store_true", dest="doTests",
                      help="Run built-in doctests")
    parser.add_option("-f", "--file", dest="filename",
                      help="Specify source file for post")
    (options, args) = parser.parse_args()

    if options.doTests:
        runTests()

    if options.filename:
        post = BlogPost('Brian Wisti', 'brian.wisti@gmail.com', 'mypassword')
        postFile = open(options.filename).read()
        post.parsePost(postFile)
        post.sendPost()
        
if __name__ == '__main__':
    main()
```