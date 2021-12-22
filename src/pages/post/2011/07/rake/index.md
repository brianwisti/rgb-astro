---
aliases:
- /coolnamehere/2011/07/18_rake.html
- /post/2011/rake/
- /2011/07/18/rake/
category: coolnamehere
date: 2011-07-18 00:00:00
layout: layout:PublishedArticle
slug: rake
tags:
- ruby
- build tools
- site
title: Rake
uuid: 331b8dfb-f3d1-4fdb-b60f-edf47259cf8f
---

[Rake](http://rake.rubyforge.org/) is a simple build program. You can
use it to automate complex or repetitive tasks. It is written in
[Ruby](/tags/ruby/), but is useful in far more than just Ruby projects.

The great news is that if you have Ruby on your system, you *probably*
already have Rake. It has been included as part of the standard Ruby
distribution for a few years.

It is easy to test which version of Rake you have from the command line:

    $ rake --version
    rake, version 0.9.2

If you do not have Rake, then you just need to install a fresh release
of Ruby. Go ahead. I’ll wait.

Rake is driven by a *Rakefile*. A Rakefile is a collection of Ruby
instructions organized into *tasks*.

<aside class="admonition note">
<p class="admonition-title">Note</p>

This is not going to be an in-depth Rake tutorial. I’ve noticed a lack
of simple real-world Rakefile examples, aside from one excellent [Rake
introduction](http://www.stuartellis.eu/articles/rake/). I have a
Rakefile I need to build. That makes this a good opportunity for me to
write a page about Rake.

</aside>

## Building a Simple Rakefile

I have a Web site. You may have noticed that. If you only know me from
my frequent postings on social network sites like
[Plurk](http://plurk.com) or [Google+](http://plus.google.com), I assure
you that I do indeed have a Web site.

The thing about my Web site is that rather than use Drupal or some other
convenient Content Management System, I use a tool that generates static
HTML. The static HTML and associated files like images and stylesheets
are then uploaded to an inexpensive Web host. Hey. It works for me.
Static HTML serves fast, and I don’t change the content on my site
*that* often.

I invoke a simple command to build my site before uploading it.

    $ python site-builder.py

That is not painful, but it does get boring. More importantly, I have
been thinking about how [Compass](https://compass-style.org) would be a
great thing to use for my site. But `site-builder.py` is an ugly, ugly
piece of hackery. It is just coherent enough to build the site you’re
reading. It is *certainly* not up to the job of driving Compass. That’s
where Rake comes in.

### One Task

You might want to use the exact same Rake tasks as me while you read
this. Here is a dummy version of `site-builder.py` that you can use. No,
it does not build a site. It *will* give you something to work with for
demonstrating Rake, though.

``` python
# Imaginary version of site-builder.py
if __name__ == __main__:
    print "Look at me, I'm building a site!"
```

First I will start by creating a Rakefile to handle my current workflow.

``` ruby
# Rakefile for coolnamehere.com
task :html do
  sh "python site-builder.py"
end
```

The simplest Rake `task` command takes two arguments: a name for that
task, and a block of actions to perform when that task is requested. The
name can be written as a String or as a Symbol, but I usually see it
written as a Symbol.

The block can be any valid Ruby code. The `:html` block uses my
shell to run the Python script that builds coolnamehere.com. You ask
Rake to execute a particular task from the command line by using the
task’s name.

    $ rake html
    python site-builder.py
    Look at me, I'm building a site!

How do you find out what tasks are available, aside from reading the
Rakefile? The -T flag will ask Rake to list all of the available tasks.

    $ rake -T

Oh. Hold on a second. Rake will only list the tasks you have described
with the `desc` command.

``` ruby
desc "Generate Web site"
task :html do
  sh "python site-builder.py"
end
```

Let us try that again. The -T flag will ask Rake to list all of the
available *described* tasks.

    $ rake -T
    rake html  # Generate Web site

A Rakefile can have many tasks, but some of them may be
utility tasks which are not expected to be called by the user. That is
why limiting the task list to described tasks is a good idea.

### A Second Task

As I mentioned before, part of the reason I am writing a Rakefile is
because I want to use Compass to define the styles for coolnamehere. I
set up a Compass project parallel to my site sources, including the
blueprint module. The Compass project is called "style". My projects
generally do not have clever names.

<aside class="admonition note">
<p class="admonition-title">Note</p>

If you *really* want to play along, here is how I set up my Compass
project.


    $ gem install compass
    $ compass create style --using blueprint

</aside>

This is another straightforward task.

``` ruby
desc "Generate style sheets"
task :css do
  sh "compass compile style"
end
```

I do not expect anything exciting to happen, since I have not changed
the SCSS files.

    $ rake css
    compass compile style
    unchanged style/sass/ie.scss
    unchanged style/sass/print.scss
    unchanged style/sass/screen.scss

There is still a problem, though. All of the stylesheets are in
`style/stylesheets`, but the working stylesheets have been over in
`site/inc/css`. I need Rake to copy the finished stylesheets to the
expected location. Might as well copy the images that are sitting in the
`style` project while I am at it.

``` ruby
desc "Generate style sheets"
task :css do
  sh "compass compile style"
  cp Dir.glob("style/stylesheets/*"), "source/inc/css", :verbose => true
  cp Dir.glob("style/stylesheets/images/*"), "source/inc/images", :verbose => true
end
```

Rake conveniently imports the FileUtils module. This lets me use Ruby
standard library methods such as `cp` to copy a list of files rather
than relying on platform-specific shell commands.

What does that look like in action?

    $ rake css
    compass compile style
    unchanged style/sass/ie.scss
    unchanged style/sass/print.scss
    unchanged style/sass/screen.scss
    cp -r style/stylesheets/ie.css style/stylesheets/print.css style/stylesheets/screen.css source/inc/css
    cp -r style/images/grid.png source/inc/images

Good enough. Excuse me while I adjust my HTML template to point at the
right stylesheets.

### Setting a Dependency

There are already awkward bits to the Rakefile as it is right now. I
need to run two commands in order to build the site completely. Because
`site-builder.py` also copies the site files to a new location, I must
also remember to run the commands in the correct order. If I don’t, then
the generated CSS will go into my site sources after the HTML has
already been generated and copied.

    $ rake css
    ...
    $ rake html
    ...

What if I made `:css` a *dependency* of `:html`? Rake would make sure
that the `:css` task was executed before it tried to execute the `:html`
task.

A little syntax trickery simplifies the task of describing a task’s
dependencies.

``` ruby
desc "Generate Web site"
task :html => [:css] do
  sh "python site-builder.py"
end
```

Now instead of just a name for the task, we are giving `task` a Hash.
The only key of that Hash is the name of the task, and the value is a
list of tasks which this one depends on.

    $ rake html
    compass compile style
    unchanged style/sass/ie.scss
    unchanged style/sass/print.scss
    unchanged style/sass/screen.scss
    cp -r style/stylesheets/ie.css style/stylesheets/print.css style/stylesheets/screen.css source/inc/css
    cp -r style/images/grid.png source/inc/images
    python site-builder.py
    Look at me, I'm building a site!

Excellent. Now I can generate both CSS and HTML from a single Rake
command. I am going to work a little bit on the styles, and to see if I
notice any other little issues with my Rakefile.

### Setting The Default Task

It has been pretty effective so far. Incidentally, Compass is kind of
awesome. I highly recommend you check it out for your Web design needs.

It would be nice if I could make the `rake` call a little shorter,
though. I have a shortcut set up in [Vim](/tags/vim) that invokes Rake
with a default argument. It would be nice to use that shortcut while I
am working on coolnamehere.

Rake already has rules for default tasks, actually. It looks for a task
named "default" or `:default`. That makes sense. Let me set up a default
task that depends on the `:html` task.

``` ruby
task :default => [:html]
```

That is all I need to do, actually. A task can simply be a name and its
dependencies. You do not *need* to define a block of actions for that
task.

    $ rake
    compass compile style
    unchanged style/sass/ie.scss
    unchanged style/sass/print.scss
    unchanged style/sass/screen.scss
    cp -r style/stylesheets/ie.css style/stylesheets/print.css style/stylesheets/screen.css source/inc/css
    cp -r style/images/grid.png source/inc/images
    python site-builder.py
    Look at me, I'm building a site!

### Something I Have Been Meaning To Get Around To

I have been promising myself for years that I will assemble some sort of
script that would automate the process of uploading my site. I never get
around to it, though. Instead I fire up NCFTP, load the "coolnamehere"
bookmark I’ve had for years, and upload.

It is time to fix that by adding an "upload" task. I will take advantage
of the [syncftp](https://github.com/glejeune/syncftp) Ruby library,
which looks like it will handle all of the little details.

    $ gem install syncftp

For the first test, I will just fill in the blanks using the syncftp
README as a guide.

``` ruby
desc "Transfer site to the remote host"
task :upload => [:html] do
  ftp = SyncFTP.new 'ftp.myhost.com',
    :username => 'me',
    :password => 'supersecret',
  ftp.sync :local => 'build',
    :remote => 'public_html'
end
```

## Conclusion

Here’s the complete Rakefile, with the as-yet untested "upload" task.

``` ruby
task :default => [:html]

desc "Generate Web site"
task :html => [:css] do
  sh "python site-builder.py"
end

desc "Generate style sheets"
task :css do
  sh "compass compile style"
  cp Dir.glob("style/stylesheets/*"), "source/inc/css", :verbose => true
  cp Dir.glob("style/stylesheets/images/*"), "source/inc/images", :verbose => true
end

desc "Transfer site to the remote host"
task :upload => [:html] do
  ftp = SyncFTP.new 'ftp.myhost.com',
    :username => 'me',
    :password => 'supersecret',
  ftp.sync :local => 'build',
    :remote => 'public_html'
end
```

Well, yes. There are differences from the *actual* Rakefile, but this
gets the idea across.

All that I need to do now is test it.

    $ rake upload