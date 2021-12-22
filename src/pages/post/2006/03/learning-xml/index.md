---
aliases:
- /coolnamehere/2006/03/17_learning-xml.html
- /post/2006/learning-xml/
- /2006/03/17/learning-xml/
category: coolnamehere
date: 2006-03-17 00:00:00
layout: layout:PublishedArticle
slug: learning-xml
tags:
- xml
- learn
title: Learning XML
updated: 2009-07-11 00:00:00
uuid: 9dffaa2a-3ef3-4507-a133-82f3f6f6364c
---

A mountain of standards and specifications have piled on top of XML over the 
years, but the core language is still pretty easy to get started in. Because it 
is a markup language rather than a programming language, there aren't as many 
new concepts to learn. If you've learned HTML in the past, then XML will be 
familiar.
<!--more-->

I usually try to scatter my "Learning" sections across several pages, so that 
each major idea can get its own space. XML is different, though. Core XML 
really is a simple creature, and I think I can get the most important ideas 
out in one page. Let's see if that will happen.

## What You Need

[text editor]: /tags/editors/
A [text editor][] is all you need to get started in 
XML. However, you will probably want to look at your XML as something besides 
markup. The best solution for that would be a Web browser that understands 
XML. Both Internet Explorer and [Mozilla 
Firefox](http://www.mozilla.com/) can read and display XML documents in a 
pleasant format. I strongly prefer Firefox because its XML capabilities are 
very strong.

## The Skeleton of an XML Document

A simple XML document is indeed very simple. All you need is a prolog and a 
root element.

``` xml
<?xml version="1.0" ?>
<greeting>Hello, World!</greeting>
```

The very first line is called the *prolog*. The browser relies on the presence 
of that prolog to recognize an XML file. Later, you may learn how to add 
information in the prolog, providing details like character set. For now, just 
starting every XML document out with that line is good enough.

<aside>
Browser, parser, interpreter, whatever. It's a piece of software that will 
look at your XML file and need to be reassured that is in fact looking at an 
XML file.
</aside>

The document itself consists of the *root element*. If you've ever written 
HTML, then this "element" business will be no problem for you. `<html>` is the 
root element of a HTML file, and the rest of your page goes inside. If you 
haven't written HTML, then elements can look a little intimidating. Let's talk 
about them in a little more detail.

### Elements

Elements are what give an XML document its structure. They have three parts: a 
beginning, an end, and everything in between. The beginning consists of a name 
and maybe some *attributes* wrapped in `<` and `>` characters. The end is the 
name prefixed by the / character and wrapped in `<` and `>` characters. The 
beginning and end are often referred to as the *opening tag* and the *closing tag*. 
In between them, you can find anything: text, *entities*, *comments*, 
*processing instructions*, *non-parsed data*, and more *elements*.

``` xml
<element>Stuff in between</element>
```

Even though you *can* find anything inside an element, the XML language you 
are using probably has specific rules for what can be contained inside each 
particular element. For example, in XHTML `<body>` should only be inside of 
the `<html>` element.

#### Attributes

Attributes often serve the purpose of providing additional information about an 
element. They consist of a name followed by an equals (=) sign and a value. 
The value is usually in quotation marks.

``` xml
<element attribute="value">...</element>
```

Elements may have any number of elements, depending on the rules defined in the 
XML language you are using.

#### Empty Elements

Sometimes there is no "in-between" content for an element. The creators of the 
XML specification realized that it would get tiring to enter `<element></element>` 
all the time. Those extra characters can also add up, taking up precious 
bandwidth when sending large XML documents to large numbers of machines. So, 
they added a special rule. If the element is empty, you can suffix the opening 
tag with a / character, and leave off the closing tag.

``` xml
<element attribute="value" />
```

You might have noticed that I put a space in between the last character of the 
opening tag and the / character. You don't need to do that, but I think that 
it makes the markup for an empty element a little easier to read.

### Plain Old Text

Elements may contain text. In fact, text is usually the actual content which 
is being marked up. It's easy to lose sight of that when your text is drowning 
in a sea of elements. 

Plain old text is pretty straightforward: you're reading some right now. There 
is one little quirk that you need to deal with, though. What do you do when 
you want to display a less-than or greater-than symbol in your text? Well, 
that's where *entity references* come in.

### Entity References

Entity references allow you to display characters that are either already being 
used in XML, or just flat out unprintable with the keyboard you are using.

Using an entity reference is a little more complicated than what you've dealt 
with so far, but let's get into it. An entity is either a special name or a 
numeric value. You reference the entiy by prefixing it with the `&` character 
and suffixing it with the `;` character. If your entity is a numeric value, it 
must be prefixed with the # character befor referencing it.

``` xml
<element>1 &lt; 2</element>
```

Of course, now you need a special entity for the & character. In fact, there is 
a small set of predefined entities which are valid in any XML document. Let's 
just stuff them into a table rather than reviewing them one by one.

### Common XML Entities

Entity   | Represents
---------|-----------
`&lt;`   | `<`
`&gt;`   | `>`
`&amp;`  | `&`
`&apos;` | `'`
`&quot;` | `"`

Numeric entity references are a whole different can of worms, and frankly I'd 
rather not get into them in such a high-level overview of XML. Still, here's 
what they look like so you can recognize them:

``` xml
<element>&#62; should be the same as &gt;</element>
```

Stick to named entities for now, and be sure to look up what is available for 
you. XHTML has a particularly rich set of named entities that you can use in 
your Web pages.

### Comments

XML authors need a way to add information that will be completely ignored by 
the computer. XML comments provide the ability to do just that. A comment is 
prefixed by `<!--` and ends with `-->`.

``` xml
<!-- Some scandalously clever comment -->
```

### Processing Instructions

Processing Instructions are special instructions to the browser which are not 
considered part of the document itself. They are indicated with a question 
mark and an indicator of the application used for the processing.

``` xml
<?lang directives ... ?>
```

Did you notice how similar this is to the prolog mentioned above? That's 
because the prolog is a processing instruction letting the browser know that 
it's time to fire up the ol' XML processing code.

### Non-Parsed Data

[Python]: /tags/python/

You probably won't see this much when you're getting started, but I thought 
I would mention it anyways. Non-Parsed Data is content that ... well ... you 
don't want parsed. It can hold anything, including XML. I've used it to hold 
[Python][] code for projects. It doesn't matter what 
the section holds, because the browser will ignore it unless told to do 
otherwise.

``` xml
<![CDATA[Clever code that saves the world. ]]>
```

### DTD Declarations

I was going to ignore these, since they are a relic of XML's SGML history. The 
truth is that you are going to see these a lot when editing XML documents. Web 
browsers in particular often rely on the DTD when deciding how to interpret an 
XHTML file. DTD declarations are used to define the rules of the XML language 
you are using or to point to the location of these rules. Here's a sample DTD 
declaration, which is pointing to the Transitional XHTML rules.

``` xml
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
```

Using a DTD declaration in your XML is - at this stage in your knowledge - just 
a matter of copying and pasting a sample. You can always pursue DTD mastery 
yourself if you like.

## The Importance of Good Form

If you are used to HTML, then you may also be used to seeing some sloppy 
markup. Authors used opening tags with no closing tag, or mixed up the order 
that tags were closed. HTML browsers were forgiving, but XML is not. All 
elements must be opened and closed or shown to be empty. Elements always 
contain elements. You must close your elements in the opposite order you 
opened them.

Bad!                            | Good!
--------------------------------|---------------------------------------
`<br>`                          | `<br />`
`<li>...<li>...<li>`            | `<li>...</li><li>...</li><li>...</li>`
`<em><strong>...</em></strong>` | `<em><strong>...</strong></em>`

## Conclusion

You've just dipped your toes in the deep and murky waters of XML. There is 
still *so* much more to discover. I wanted you to be able to recognize an XML 
document in the wild, and know enough to create your own simple documents. You 
still need to learn how to create your own language so that your XML is 
completely valid. Both of us need to study XPath, XML-Schema, and the many 
other standards which have evolved over the years.

The best resource for additional information is the [World Wide Web 
Consortium](http://www.w3.org/). But if standards and specifications aren't 
your cup of tea, there are also a number of good tutorial sites, such as 
[XML.com](http://www.xml.com/) and [W3 Schools](http://www.w3schools.com/).