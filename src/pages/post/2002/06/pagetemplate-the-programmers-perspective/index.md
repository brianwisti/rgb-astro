---
aliases:
- /coolnamehere/2002/06/02_the-programmers-perspective.html
- /post/2002/the-programmers-perspective/
- /2002/06/02/pagetemplate-the-programmers-perspective/
category: coolnamehere
date: 2002-06-02 00:00:00
layout: layout:PublishedArticle
slug: pagetemplate-the-programmers-perspective
tags:
- pagetemplate
title: PageTemplate - The Programmer's Perspective
updated: 2009-07-11 00:00:00
uuid: f8101496-6c7d-48f1-b42c-07fd07110330
---

## Getting Started

Before you dig into the code, you might want to take a look at the
[designer’s](/post/2002/06/pagetemplate-the-designers-perspective/)
perspective of PageTemplate.

## Using PageTemplate In Your Ruby Code

This is a *very* quick overview, because I just spent hours going over
the designer documents and I’m a little tired.

First, of course, you’ll want to
[install](/post/2002/07/pagetemplate-getting-it/) the PageTemplate
package. Once that’s done, `require` the package.

``` ruby
require 'PageTemplate'
```

You’ll need a PageTemplate object to hold values and parse template
files.

``` ruby
template = PageTemplate.new()
```

At some point, you will want the PageTemplate object to load a template
text file, bristling with directives. The template file should be
readable by the script, and the path must be either absolute or relative
to the script’s working directory.

``` ruby
template.load('/var/www/templates/template.txt')
```

To assign a value for use by PageTemplate, use hash-style assignment,
with the name to be used by the template as the key, and the value
assigned as — well — the value. The only rule is that the value must
evaluate to a String. Either it *is* a String or it has a `to_s`
method). Page designers would probably be grateful if the key was a
string, too. Much easier to type it into a text template that way.

``` ruby
template['title'] = 'My PageTemplate Script'
```

The easiest way to handle flags used in `if` directives is to take
advantage of Ruby’s boolean values.

``` ruby
template['flag'] = true
template['shovel'] = false
```

You can use the truth of a regular variable or loop variable in an `if`
directive, but remember that Ruby is more specific about `false` than
other languages you might be used to. For example, the number zero is
not false. It’s just zero. Same with empty strings. If you want a
variable to be interpreted as `false`, you should explicitly set it.

PageTemplate uses arrays of objects for lists. Each object provides a
local namespace which lasts only for the current iteration through the
chunk of content. Otherwise, you’d have to manually set loop variables,
and I don’t like that idea\!

The classic approach is to borrow from
[HTML::Template](http://html-template.sourceforge.net/) and use a list
of hashes for your namespaces.

``` ruby
listing = [
  { 'name'   => 'Swordfishtrombones',
    'artist' => 'Tom Waits' },
  { 'name'   => 'Dirt Track Date',
    'artist' => 'Southern Culture On The Skids' },
  { 'name'   => 'The Craft',
    'artist' => 'Blackalicious' }
]
template['albums'] = listing
```

What about nested lists? They are handled the same way. One of the keys
in your item hash points to another array of hashes, which will be used
for the inner loop.

``` ruby
favorites = [
  { "topic"  => "Interesting Comic Books",
    "items"    => [
    { "title"   => "Dropsie Avenue",
      "creator" => "Will Eisner"},
    { "title"   => "Cerebus",
      "creator" => "Dave Sim"},
    { "title"   => "Jar Of Fools",
      "creator" => "Jason Lutes"}
  ]},
  { "topic"  => "Old Favorites",
    "items"    => [
    { "title"   => "Amnesiac",
      "creator" => "Radiohead"},
    { "title"   => "The Moon and Antarctica",
      "creator" => "Modest Mouse"},
    { "title"   => "Dirt Track Date",
      "creator" => "Southern Culture On The Skids"},
    { "title"   => "My Motor",
      "creator" => "Dorkweed"},
    { "title"   => "Swordfishtrombones",
      "creator" => "Tom Waits"}
  ]}
]
```

Using objects in a list requires a little more research, but it’s still
a practical solution. Say you’re trying to figure out how to use
PageTemplate in an image gallery. You might have an Image class with
accessors that look something like this:

``` ruby
class Image
  attr_reader :url, :height, :width, :caption
end
```

You can build your template armed with this knowledge.

``` html
[%loop images %]
<td>
  <img src="[%var url%]"
    height="[%var height%]" width="[%var width%]"
    alt="[%var caption %]" /><br />
  <strong>[%var caption %]</strong>
</td>
[%end loop %]
```

Then, rather than waste precious minutes altering class `Image` to
respond to hash-based access, you can assign a list of `Image` objects
to the template list.

``` ruby
galleryPage['images'] = gallery.current.images
```

This approach definitely encourages maintaining a consistent interface.
I wouldn’t want to go altering my template files (or telling the
designer to alter her files) every time I get a bright idea for how
`Image` should work.

You can also refer to public methods of the object in your template, but
that’s still a bit shaky. The methods have to accept calls with no
arguments or blocks (Ex: `image.thumbnail()` would be referenced as
`[%var thumbnail%]`).

Once you’ve told your PageTemplate object which file to load and what
values to remember, you’ll probably want to display the neat custom
page.

``` ruby
output = template.output
print output
```

Of course, if you do things this way you’ll have to remember all of the
HTTP header information. Life will be much easier for you if you just
use the functionality provided by the standard CGI module for ruby.

``` ruby
cgi.out { template.output }
```

I’m not a [Rails](http://rubyonrails.com/) person, so I really don’t
know how well PageTemplate works with Rails these days. Definitely send
reports if you have any troubles, though. See the [front
page](/post/2002/06/pagetemplate/) for links to bug filing and the
forum.

### Digging Deeper

The stuff covered in this tutorial should remain pretty consistent
through future versions. If you’re curious to see inside
PageTemplate.rb, you will definitely want to go over the [reference
section](/tags/pagetemplate/). It describes PageTemplate and the classes
that back it up. Be warned, though: anything not described in this page
is definitely subject to change, so your clever hack might be useless
with the next release. Then again - that never stopped me. Go, have
fun\!

### Caching Templates

PageTemplate has some support for saving template information to disk.
This means that your application needs less time to prepare its
templates. You still need to provide a Namespace when you need output,
though.

Two steps are required to take advantage of PageTemplate’s cache
capabilities. First, make sure that your script has write permissions to
the directory or directories that contain your template source. Next,
call the PageTemplate constructor with the `use_cache` flag set to
`true`.

``` ruby
template = PageTemplate.new(
  'use_cache' => true
)
```

### Creating Your Own Syntax

For now, use the source as your guides.