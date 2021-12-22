---
aliases:
- /blogspot/2009/06/09_python-blogger-refresh-part-1.html
- /post/2009/python-blogger-refresh-part-1/
- /2009/06/09/python-blogger-refresh-part-1/
category: blogspot
date: 2009-06-09 00:00:00
layout: layout:PublishedArticle
series:
- Python Blogger Refresh
slug: python-blogger-refresh-part-1
tags:
- blogger
- gdata
- markdown
- python
title: Python Blogger Refresh, Part 1
updated: 2009-06-12 00:00:00
uuid: f726a5e8-1e58-474b-b6d6-d257c517e066
---

<!--more-->

## The Idea

[wrote a post]: /post/2007/12/python-loves-blogger-part-1/
[Python]: /tags/python/
[Blogspot]: http://blogspot.com
[Python Markdown]: https://pypi.python.org/pypi/Markdown
[handling metadata]: https://pythonhosted.org/Markdown/extensions/meta_data.html

I [wrote a post][] a while back about using [Python][] to write [Blogspot][] posts
from the command line. It took me about two weeks to completely forget about it. Still, it's one of
the few posts on this blog that gets regular visits, and the code ... well, the code is not great.
It was a fair effort, but it didn't even accomplish the things I had initially set out to do. Account
information is hard-coded into the code, for example. I also blundered along haphazardly with parsing
metadata information myself despite the fact that [Python Markdown][] has an extension which is perfectly
capable of [handling metadata][]. Well, let's look at that code again.
<!--more-->

There's a fresh install of [Ubuntu](http://ubuntu.com) 9.04 on my laptop and I've got projects I feel
like talking about. So let's get started.

The basic flow will be the same. Given a command line that looks like this:

    $ python post-to-blog.py <post.txt>

1. Load settings
2. Create a HTML formatted string based on the Markdown-formatted text found in `post.txt`
3. Request that Blogger store the post using post data and user settings
4. Report the result of the publish request.

I'll be starting from the code that already exists in the earlier posts. We can start this
project with confidence once we have everything set up and we're sure the old code still does
what we expect it to.

## Setup

Ubuntu 9.04 already has a copy of Python 2.6 installed. I suppose I could grab a fresh
copy of the Python source and build it myself, but I don't really feel like it right now.
Sometimes I'm just lazy. Ubuntu's 2.6 will work well enough for my needs.

[GData]: https://github.com/google/gdata-python-client

Modules are a different matter. I want fresh copies of [Python Markdown][] and
[GData][], rather than the somewhat dated modules that are available in the
repository. There are a fair number of bug fixes and new features in the latest versions.

    $ cd ~/src
    $ wget http://gdata-python-client.googlecode.com/files/gdata-1.3.3.tar.gz
    $ tar xfz gdata-1.3.3.tar.gz
    $ cd gdata-1.3.3/
    $ sudo python setup.py install
    $ cd ../
    $ wget http://pypi.python.org/packages/source/M/Markdown/Markdown-2.0.tar.gz
    $ tar xfvz Markdown-2.0.tar.gz
    $ cd Markdown-2.0/
    $ sudo python setup.py install

## The Starting Code

[first]: /post/2007/12/python-loves-blogger-part-1/
[second]: /post/2008/01/adding-categories-to-the-python-blogger-client/

Now that I have the most important dependencies installed, I can revisit the code from
the [first][] and [second][] posts. 
There's no local copy of the code, so I will just copy and paste the original code, run the tests, 
and share the starting code. What could possibly go wrong?

    $ cd ~/Projects/python-blogger
    $ python post-to-blog.py -D
    ...
    ***Test Failed*** 19 failures.

Ouch. Something has gone horribly wrong in copying and pasting the code from the posts, the module
behaviors have changed, or maybe they never worked as well as I thought they did. Either way, 
this is bad. Let me fix these issues and then I'll share the *new* starting code with you.

## The New Starting Code

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

    >>> post = BlogPost('Brian Wisti', 'me@here.com', 'mysecretpassword')
    >>> post.body = 'This is a paragraph'
    >>> print post.body
    <p>This is a paragraph</p>
    """

    def __init__(self, author, account, password):
        self.config = {}
        self.__body = None
        self.__author = author
        self.__account = account
        self.__password = password

    def set_body(self, bodyText):
        """Stores plain text which will be used as the post body

        >>> post = BlogPost('Brian Wisti', 'me@here.com', 'mysecretpassword')
        >>> post.set_body('This is a paragraph')
        >>>
        """
        self.__body = bodyText

    def get_body(self):
        """Access a HTML-formatted version of the post body

        >>> post = BlogPost('Brian Wisti', 'me@here.com', 'mysecretpassword')
        >>> post.set_body('This is a paragraph')
        >>> print post.get_body()
        <p>This is a paragraph</p>
        """
        return markdown.markdown(self.__body)

    body = property(get_body, set_body)

    def parseConfig(self, configText):
        """Reads and stores the directives from the post's config header.

        >>> post = BlogPost('Brian Wisti', 'me@here.com', 'mysecretpassword')
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
        >>> post = BlogPost('Brian Wisti', 'me@here.com', 'mysecretpassword')
        >>> post.parsePost(myText)
        >>> print post.config['title']
        Test
        >>> print post.body
        <p>This is a test</p>
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
      blog_id = feed.entry[0].GetSelfLink().href.split('/')[-1]

      # Create the entry to insert.
      entry = gdata.GDataEntry()
      entry.author.append(atom.Author(atom.Name(text=self.__author)))
      entry.title = atom.Title('xhtml', self.config['title'])
      entry.content = atom.Content(content_type='html', text=self.body)

      # Assemble labels, if any
      if 'tags' in self.config:
          tags = self.config['tags'].split(',')
          for tag in tags:
              category = atom.Category(term=tag, scheme='http://www.blogger.com/atom/ns#')
              entry.category.append(category)

      # Decide whether this is a draft.
      control = atom.Control()
      control.draft = atom.Draft(text='yes')
      entry.control = control

      # Submit it!
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
        post = BlogPost('Brian Wisti', 'me@here.com', 'mysecretpassword')
        postFile = open(options.filename).read()
        post.parsePost(postFile)
        post.sendPost()

if __name__ == '__main__':
    main()
```

## Coming Up Next

[next time]: post/2009/06/python-blogger-refresh-part-2-settings/

These posts will be short, since I want to get *something* up while still getting things done at
work. We have our starting point reestablished, and [next time][] we will be concentrating on loading user
settings rather than embedding those details right in our code.