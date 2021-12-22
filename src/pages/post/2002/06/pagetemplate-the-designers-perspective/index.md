---
aliases:
- /coolnamehere/2002/06/02_the-designers-perspective.html
- /post/2002/the-designers-perspective/
- /2002/06/02/pagetemplate-the-designers-perspective/
category: coolnamehere
date: 2002-06-02 00:00:00
layout: layout:PublishedArticle
slug: pagetemplate-the-designers-perspective
tags:
- pagetemplate
title: PageTemplate - The Designer's Perspective
updated: 2009-07-11 00:00:00
uuid: 5b1d8f88-48dc-4609-8163-86983e6fe51c
---

## Who Are You?

You are the esteemed Web Designer, aesthetically talented and perhaps
artistically inclined. You know what makes a good Web page. You are not
a programmer, though. It’s horrible when you have to go down to the
caves where they keep the developers to explain where a simple login
form belongs. You also don’t want to remember where their odd-looking
programming code is supposed to go in your beautiful page. You want a
simple, clean way of describing the dynamic elements of site pages.

Okay, I’ve had too much coffee. This page explains how templating works,
and how to put PageTemplate to use when laying out the HTML of your
page.

## What’s a Template?

When you are designing pages for a dynamic site or Web application,
there are a lot of details you won’t know in advance. Some examples
might include login information, the contents of a shopping cart, or
maybe even the contents of the page\! Templates allow you to put
placeholders within your HTML to show where that login information is
displayed and how it is formatted. A good template system does not
require you to remember code while you’re designing: you just make the
page, and let programmers worry about filling it with data.

These placeholders are known as *directives* in PageTemplate.

## How Do I Use PageTemplate In My Pages?

PageTemplate uses a very simple language which you can embed in your
page. You should be able to use your favorite design tools to create an
attractive template. My favorite design tool happens to be
[Vim](/tags/vim), but the odds are that the
designers out there lean towards something a little friendlier, like
Adobe Dreamweaver. With the default syntax, all of us can be happy.

PageTemplate directives are indicated by being wrapped in between `[%`
and `%]` characters. If any of those characters are missing,
PageTemplate decides it is not a directive and leaves it alone.