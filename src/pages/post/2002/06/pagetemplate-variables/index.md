---
aliases:
- /coolnamehere/2002/06/02_variables.html
- /post/2002/variables/
- /2002/06/02/pagetemplate-variables/
category: coolnamehere
date: 2002-06-02 00:00:00
layout: layout:PublishedArticle
slug: pagetemplate-variables
tags:
- pagetemplate
title: PageTemplate - Variables
updated: 2009-11-11 00:00:00
uuid: f6809302-e970-4877-8565-76518f13ecf1
---

The major directives require *variables*, which are just names for the
value your want inserted, checked, or otherwise accessed. It’s a good
idea to use variable names that make sense(`name` for a person’s name,
`title` for the title of the page, etc.).

## Value Substitution

Substitution is the easiest concept to master. When PageTemplate comes
across a value directive, it replaces that directive with some text.

### Syntax

### Example

``` html
<h1>Hello, [%var name%]</h1>
```

Every time that PageTemplate sees `[%var name%]` in your template, it
will replace that directive with the text associated with `name`.

The programmer works his magic, and the visitor “Frank” sees this
greeting:

``` html
<h1>Hello, Frank</h1>
```

If `name` is not set, nothing is inserted. The greeting header would end
up looking like this:

``` html
<h1>Hello,</h1>
```

## Filters

Text on the Web is a funny thing. Your page can be unreadable if you
forget to escape a few `<` characters. You could rely on your
programmers to take care of the necessary escapes, but there is always
the chance that they may forget it. Sometimes it is just easier to take
care of these things yourself, and that’s where *preprocessors* come in.
They take the contents of a variable and reformat it according to
specific rules.

### Syntax

### Example

``` html
<p>You have received a message on the Wensleydale Advocacy Forum.</p>
<div class="message">
[%var message.contents :escapeHTML %]
</div>
<p>You can also view this comment <a href="[%var message.url :escapeURL %]">here</a></p>
<p>Thank You,</p>
<p>WAF Management</p>
```

That might end up looking like this:

``` html
<p>You received a message on the Wensleydale Advocacy Forum.</p>
<div class="message">
&lt;span style='font-size: 250%'&gt;&lt;blink&gt;Wenzleedale suks! Cheddr 4evar!!1!&lt;/blink&gt;&lt;/span&gt;
</div>
<p>You can also view this comment <a href="http://wensleydaleforum.net/messages/view/Wenzlee+Sucks%21">here</a></p>
<p>Thank You,</p>
<p>WAF Management</p>
```

## Dots, Objects, and Traits

What? Oh, some of you might have noticed that little dot in the variable
names for the last example. This is a little bit of geek code getting
into the template. Lots of information in a Ruby program is divided into
*objects*, each of which has special traits unique to that object. In
this example, you have a message with both a URL and some contents.
Rather than make you try to remember some contorted syntax in order to
get the information you need, we just borrow the Ruby syntax. Confer
with your developers for more details as they are needed, and make sure
they give you objects with traits that make sense in a template. It also
helps if they let you know what traits you need to use for the
information you want.

Well, we call traits “fields”, “methods”, or maybe “messages” in our
code. PageTemplate is a little more flexible in how it gets an object’s
details, so a more general name seemed appropriate. You can call them
“Waffle Monkeys of the Yukon” if you like.

### Syntax

    variable.trait