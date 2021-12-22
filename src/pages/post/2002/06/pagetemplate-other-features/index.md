---
aliases:
- /coolnamehere/2002/06/02_other-features.html
- /post/2002/other-features/
- /2002/06/02/pagetemplate-other-features/
category: coolnamehere
date: 2002-06-02 00:00:00
layout: layout:PublishedArticle
slug: pagetemplate-other-features
tags:
- pagetemplate
title: PageTemplate - Other Features
updated: 2009-07-11 00:00:00
uuid: 12b976ca-30f4-4707-b56f-36e2c8fb00ff
---

PageTemplate has a number of other features for the designer, and I
couldn’t figure out where to put them. Let’s just dump them here until
the day I *do* figure out where a good spot for them would be.

## Filter

Filtering seemed so handy with variables that we thought it would be fun
to have filtering as an independent action. All the contents of a
`filter` block are passed through the named filter during output.

### Syntax

### Example

``` html
[%filter :escapeHTML %]
<h1><blink>Some browsers still allow this?</blink></h1>
[%end]
```

## Include

`include` is somewhat tricky. The idea is easy enough. You want to
include the same template fragment in several other templates. A login
form, a stats view, whatever. `include` lets you do that in one of two
ways. First, the developer may have already processed that template
fragment and made it available to you as a sort of variable. The other
is where you request that a specific file be processed. Okay, that
wasn’t so hard after all.

### Syntax

### Example

``` html
[%include login_form %]
[%include fragments/login_form.tmpl %]
```

## Define

Occasionally you will have information that the developer doesn’t. No, I
don’t mean the name of the great Mexican restaurant on the north side of
town. Wait a minute. Sure, why not? You know the name of this great
Mexican restaurant on the north side of town, and the developer doesn’t.
You could just tell him. He could add the name in his code so you can
use it in your template, and then the two of you could go share a tasty
lunch and a few drinks. Then again, he is out with horrible food
poisoning for the whole week because he listened to somebody else’s
great suggestion and went to that restaurant downtown which is so bad it
must be a front for a black market biowaste disposal organization. Maybe
you can just provide the name in the template yourself, and he can add
it to his code when he recovers.

The `define` directive is a helpful tool for adding variables to the
template without waiting for the developers to incorporate them into the
code. It’s kind of a shortcut and only good for simple string values,
but every once in a while a shortcut is exactly what you need.

### Syntax

### Example

``` html
[%define restaurant Jalisco %]
[%define dish Enchilada Combo %]

<p>I really enjoy the [%var dish %] at [%var restaurant%]</p>
```

## Case

The `case` directive is a special extra directive which allows you to
show different content based on the value of a single variable.

### Syntax

### Example

``` html
[%case role %]
[%when admin %]
<a href="abuse.cgi">Abuse Users</a>
[%when user %]
<a href="beg.cgi">Beg For Mercy From Admin</a>
[%else %]
<a href="register.cgi">Register To Get Love And Abuse From Admin</a>
[%end %]
```

You must make sure the developer includes the `PageTemplate/case.rb`
library in his code to use the `case` directive.

## Comments

Comments are useful if you want to make notes to yourself as the
template designer, but you don’t want those comments showing up in the
final template output.

### Syntax

``` html
[%-- Random Commentary %]
```

## Alternate Syntax

One of PageTemplate’s features is the ability to come up with your own
directive syntax. If you feel that the default syntax is less than
ideal, discuss a new system with your developers. If you are the lone
designer/developer, talk to yourself for a bit. We all need some quality
time to ourselves occasionally. Working together, you and the developers —
or you and your split personalities - can come up with a syntax that
is much more comfortable.