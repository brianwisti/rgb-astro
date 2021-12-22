---
aliases:
- /blogspot/2008/01/02_adding-categories-to-python-blogger.html
- /post/2008/adding-categories-to-python-blogger/
- /2008/01/02/adding-categories-to-the-python-blogger-client/
category: blogspot
date: 2008-01-02 00:00:00
layout: layout:PublishedArticle
slug: adding-categories-to-the-python-blogger-client
tags:
- blogger
- gdata
- python
title: Adding Categories to the Python Blogger Client
updated: 2009-06-09
uuid: 1638f948-df3f-4a4d-bd5d-e826664876d4
---

[Python Blogger refresh]: /post/2009/06/python-blogger-refresh-part-1/

## Update 2009-06-09

I've revisited the code for Blogger posting with Python. Start with the [Python Blogger refresh][] to see the new starting point.
<!--more-->

<h2>The Original Tale</h2>

[Python Blogger client]: /post/2007/12/python-loves-blogger-part-1/

I've already used my [Python Blogger client][] for a couple
of postings, and I've been pretty happy with it so far. It still desperately needs
tags, though. Actually, Blogger calls them "labels." Actually actually, the Atom API calls
them "categories." Well, whatever they are called it looks like they are pretty easy to add.

You already know that tags are defined in my config header, and are simply a comma-delimited list like so:

    tags: python,gdata,blogger

Here's the new `sendPost` method:

``` python
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

    # Assemble labels, if any
    if 'tags' in self.config:
        tags = self.config['tags'].split(',')
        for tag in tags:
            category = atom.Category(term=tag, scheme="http://www.blogger.com/atom/ns#")
            entry.category.append(category)

    # Decide whether this is a draft.
    control = atom.Control()
    control.draft = atom.Draft(text='yes')
    entry.control = control

    # Submit it!
    blogger.Post(entry, '/feeds/' + blog_id + '/posts/default')
```

I hope this works. If it does work, then I am going to do a little refactoring
 as time allows to make this mess a little cleaner. If it doesn't work, then I
 guess I'll have to ... you know ... *fix it*.