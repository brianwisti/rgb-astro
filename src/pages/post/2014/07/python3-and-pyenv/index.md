---
aliases:
- /tools/2014/07/04_python3-venv.html
- /post/2014/python3-venv/
- /2014/07/04/python3-and-pyvenv/
category: tools
date: 2014-07-04 00:00:00
layout: layout:PublishedArticle
slug: python3-and-pyenv
tags:
- python
title: Python3 and pyvenv
uuid: e7c99e93-1f57-4c5d-8149-db721b459654
---

[Python]: http://python.org
[Pelican]: http://blog.getpelican.com/
[Google App Engine]: https://developers.google.com/appengine/docs/python/
[Python 3]: https://wiki.python.org/moin/Python2orPython3
I have been spending much of my coding time in [Python][]
recently. This site is built in [Pelican][]. Many lines of Python have
been written for work. I have even been poking at
[Google App Engine][] in what spare time is available. The only
disappointment is that all of these have been in Python 2. I would
prefer to be using [Python 3][]. There is a little free time today, so
I will set up a nice Python 3 workspace.
<!--more-->

[rbenv]: http://rbenv.org/
[perlbrew]: http://perlbrew.pl/
[Bundler]: http://bundler.io/
[pip]: http://pip.readthedocs.org/en/latest/

One of the interesting things about Python is how it handles personal
workspaces. Popular tools in other languages, such as [rbenv][] for
Ruby and [perlbrew][] for Perl, focus on a complete localized
installation for any version you care to use. Python tools assume a
system standard version, and focus on making a snapshot for your
projects. That works *sort of* like [Bundler][]. Once you have your
snapshot loaded, you use [pip][] to install the exact libraries needed
by your projects. That works very much like Bundler.

[pyvenv]: https://docs.python.org/dev/library/venv.html
[virtualenv]: http://virtualenv.readthedocs.org/en/latest/

The tool of choice for making virtual environments in Python 3 is
[pyvenv][]. pyvenv actually comes with the standard installation of
Python 3.3 or greater. That is good news. Python 2's [virtualenv][]
was not hard to install, but it was not available by default. You
still had to *install* it.

[introduction]: https://packaging.python.org/en/latest/tutorial.html#creating-and-using-virtual-environments

There is already an excellent [introduction][] to using pyvenv. That
tells most of what you need to know.

    $ pyvenv my-project
    $ source my-project/bin/activate
    (my-project) $

Now `my-project` holds the default Python interpreter until you exit
that particular shell or activate a different virtual environment.

That is good enough to get started, but I often have several projects
going. Each project gets its own virtual environment. Having my
environment files just sitting there in my project folder bothers me,
though.

[virtualenvwrapper]: http://virtualenvwrapper.readthedocs.org/en/latest/index.html
[instructions]: http://virtualenvwrapper.readthedocs.org/en/latest/install.html

I like things tidy, so I use [virtualenvwrapper][]. virtualenvwrapper
creates a single folder to hold your virtual environments and provides
you with a couple of shell commands to manage those environments. It's
easy if you're only using a single system Python. Just follow their
installation [instructions][]. After that, `mkvirtualenv` and `workon`
are your friends.

    $ mkvirtualenv mypy3
    (mypy3) $
    # later, in another shell
    $ workon mypy3
    (mypy3) $

[Vagrant]: http://www.vagrantup.com/

What if I wanted to use both Python 2 and Python 3 virtual environments?
Well, the virtual environments I already had set up for work function
without any problem. Thank goodness. If I wanted to do new Python 2
work - well, that may be a good time to pull up a *real* virtual
environment with a tool like [Vagrant][]. I may come back to that
later.
