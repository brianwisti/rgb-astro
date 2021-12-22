---
aliases:
- /blogspot/2011/04/19_spreadsheet-story-1-general-idea.html
- /post/2011/spreadsheet-story-1-general-idea/
- /2011/04/19/the-spreadsheet-story-1/
category: blogspot
date: 2011-04-19 00:00:00
description: A design experiment figuring out what a local homeless shelter needs
  to track chores.
layout: layout:PublishedArticle
slug: the-spreadsheet-story-1
tags:
- google apps script
- javascript
title: The Spreadsheet Story 1
uuid: c8ca5027-7239-4649-83e9-e9b82322458f
---

<aside class="admonition note">
<p class="admonition-title">Note</p>

We never used the Google Spreadsheet idea, but working on it helped
flesh out the thoughts that went into the Web-based
[marysplace-rails](https://github.com/brianwisti/marysplace-rails)
project.

</aside>

There is this spreadsheet project I have been working on. My wife works
at a day shelter for homeless and formerly homeless women, as well as
their children. At this shelter, they make use of an incentive point
system. The ladies do some chore or favor, and they get points. There
are preset ways to get points, with default values. Helping with the
recycling gets this number of points, while putting chairs up gets that
number of points. The points are just defaults, though. A client can get
more or fewer than the default points depending on the situation. The
staff can also create new chores or reasons for awarding points pretty
much at their whim. A couple of times a week clients get the opportunity
to spend those points in exchange for items.

It’s a very popular program. Clients are constantly looking for ways to
get more points, and asking what their point total is. Over the years,
some clients have accumulated tens of thousands of points.

Tracking incentive points was a very tedious process involving punch
cards, calculators, and the occasional mild profanity. I volunteered my
geekiness to help come up with a better tracking system. I am mostly a
Web programmer, so naturally my first impulse was a full-scale
[Rails](http://rubyonrails.org), [Django](http://www.djangoproject.com),
or maybe even [Catalyst](http://www.catalystframework.org) Web
application. Why not, right? It does sound like the perfect job for a
[CRUD](http://en.wikipedia.org/wiki/Create,_read,_update_and_delete)
framework:

- Add and edit clients
- Add and edit ways to get points
- Log point changes for clients
- Get the point total for any given client

There was just one tiny flaw in my proposal, which my wife was kind
enough to point out: nobody would use it. The staff would prefer to keep
things in a familiar framework, such as a spreadsheet. Spreadsheets are
nice. They may not be the perfect choice for a database, but they do
have a lot of built-in functionality that would take me forever to
implement on my own.

Okay, I’m flexible. I made an
[Excel](http://office.microsoft.com/en-us/excel/) spreadsheet. I learned
enough Excel to add some formulas and data validation rules. I even
learned enough
[VBA](http://en.wikipedia.org/wiki/Visual_Basic_for_Applications) to add
some interactivity, reducing the tediousness a bit more. Well - reducing
the tediousness for them. Not so much for me. Visual Basic is an
interesting language, but I don’t care for it.

What if I could use JavaScript? [Google Apps
Script](http://code.google.com/googleapps/appsscript/) uses JavaScript
to add programming logic to spreadsheets and other documents. I don’t
know if it would be any easier than using VBA in Excel, but I know it
would be more pleasant for me personally.

I have decided to go ahead and try it, now that the dust has settled on
the Excel version. Hey — if it works well enough, they might actually
use it. Regardless of whether it actually gets used, it’ll provide a
reasonable example of adding niftiness to a Google Spreadsheet.
Somebody’s bound to find that useful. Right?

The important thing is that I’ll have some fun.

## The Spreadsheet Itself

I can almost pretend this is an
[MVC](https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller)
application. The spreadsheet itself is the model layer, with each sheet
representing a specific model. My knowledge of spreadsheets is
incomplete at best, but the available formulas don’t seem to provide the
validation constraints that I’m looking for. It looks this will be what
those in the know call a "fat controller" approach, with a
disproportionate amount of the logic going into the scripting layer.
That scripting layer, driven by Google Apps Script, will handle lookup
and validation details. At least, it will until I figure out more about
how Google Spreadsheets works. The scripting layer will also provide a
view, insulating users from the worksheets by presenting dialogs for the
most common tasks.

Yeah, I know. It’s not really MVC. I have made a terrible analogy. But
at least my terrible analogy has helped me divide the thing into logical
components, rather than just looking at it as a spreadsheet with some
scripts.

So. Let’s look at the worksheets. I also made mock ups of the common
task views, just for the fun of it.

### People

Presents information about the clients that take part in the incentive
program.

Name Used
: The most common name used by this person. Must be unique. That’s
  generally handled by including the initial of the last name or a
  nickname.

Full Name
: The full name of the client, if available.

Other Names
: Nicknames and aliases are common. Use this field to list any other
  known names for the client.

Starting Points
: How many points the client had when the spreadsheet started being
  used. Nobody wants to lose their accumulated points, and this
  provides one way to differentiate it from points gained after. Could
  also be handy for importing, such as setting up different workbooks
  for different time periods.

Total Points
: How many points this person has, after gaining and spending is taken
  into account.

![Add Person Dialog](NewPersonDialog.png)

### Categories

The different ways to gain and lose points. Pretty much a list of
predefined chores and a couple of catchall buckets.

Name
: A unique name for this point category, like "Wash breakfast dishes".

Default Points
: Unless the user specifies otherwise, this represents the gain or
  loss in points for the client.

![Add Category Dialog](NewCategoryDialog.png)

### Points Log

This sheet contains records of the actual transactions which affect a
client’s point total. It depends on the other worksheets for some of its
information.

Person
: Who gets the points? *'People'\!'Name Used'*

Points Category
: What are they getting the points for? *'Categories':'Name'*

Points
: How many points are they getting? Based on *'Categories':'Default
  Points'*

Date
: When did they do whatever it was that got (or cost) them points?

![Points Logger Dialog](PointsLoggerDialog.png)

### What’s Missing

There is no sheet to track inventory for items available in the
incentive store. The items and their value vary too much for this to be
a practical feature right now.

### What Do I Have Now?

I have an incredibly dull spreadsheet.

![spreadsheet](spreadsheet-01.png)

## What’s Next?

I plan to spend the next few days — or weeks, depending on how much
bloggy spreadsheet time I have — exploring Google Apps Script,
particularly the
[Spreadsheet](http://code.google.com/googleapps/appsscript/service_spreadsheet.html)
and [UI](http://code.google.com/googleapps/appsscript/service_ui.html)
Services, in order to implement the dialog boxes I have so lovingly
created mockups of. I will be taking it in small steps, depending on
what I can manage in my copious free time. My next post will cover the
simplest dialog: creating new Categories.

<aside class="admonition note">
<p class="admonition-title">Note</p>

I did spent a few days exploring Google Apps Script, but decided that
the Excel spreadsheet was working well enough that I should focus my
effort on the
[marysplace-rails](https://github.com/brianwisti/marysplace-rails)
project.

</aside>