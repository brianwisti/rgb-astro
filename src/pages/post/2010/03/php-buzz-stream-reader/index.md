---
aliases:
- /coolnamehere/2010/03/12_php-buzz-stream-reader.html
- /post/2010/php-buzz-stream-reader/
- /2010/03/12/php-buzz-stream-reader/
category: coolnamehere
date: 2010-03-12 00:00:00
layout: layout:PublishedArticle
slug: php-buzz-stream-reader
tags:
- php
title: PHP Buzz Stream Reader
description: Does anyone even remember Google Buzz anymore?
updated: 2020-03-13
uuid: a4cb7096-e105-4173-a78a-9be6a97f7c4f
---

::: note 2020-03-13

Of course, Google long ago turned Buzz into
[Plus](https://plus.google.com/), then abandoned *that*. Keeping the
content here in case some fragment of it can be useful to others.

:::

## Why and What?

Recently I updated the site so that it would summarize the latest posts
from my blog. The motive is simple: my site does not get updated often,
so data should be piped in from elsewhere to reassure people that I have
not died in the middle of writing Parrot Babystep 09.

The blog summary works. It’s nice. It’s pretty. Well, it’s pretty enough
for me. The problem is that I am not the world’s most prolific blogger.
I can write a lot, and I can write a little. The in-between world of
blogs is uncomfortable territory for me. As a result, that nifty little
summary only makes me look a little bit less dead than the old static
update system I used.

What about a [Twitter](http://twitter.com) feed? That is easy enough,
but the problem with Twitter feeds is that you get no context. I might
be teasing a fellow Tweeter with [foursquare](http://foursquare.com)
jokes, but if you don’t know him and his seething hatred of all things
foursquare then my commentary will seem nonsensical at best.

Besides, I haven’t been using Twitter quite as much recently. I’m on to
the next shiny thing: [Google
Buzz](https://en.wikipedia.org/wiki/Google_Buzz). It provides the
instant gratification of Twitter, along with a system for commenting,
liking, geolocation, sharing links, and more. It’s sort of like
[Facebook](http://facebook.com), except that it’s embedded into GMail
and there’s no Mafia Wars yet.

I’ve been [buzzing rather
frequently](http://www.google.com/profiles/brian.wisti#buzz). I even
have my blog and [Flickr](http://www.flickr.com/photos/brianwisti/)
activity fed into Buzz, so my Buzz stream includes anything from either
of those.

## How?

Let me throw an immediate disclaimer by saying that 80% of what I want
is already implemented in the [Google Buzz
Widget](http://www.moretechtips.net/2010/02/google-buzz-widget-jquery-plugin.html),
a jQuery plugin which displays the contents of your Buzz stream. I tried
it out, and it worked like a charm.

``` html
<script type="text/javascript"
    src="http://ajax.googleapis.com/ajax/libs/jquery/1.3.2/jquery.min.js"></script>
<script type="text/javascript"
    src="http://google-buzz-widget.googlecode.com/files/jquery.google-buzz-1.0.min.js"></script>
<script type="text/javascript">
    $(document).ready(function(){
        $('div.my-buzz').googleBuzz({
            username:'brian.wisti',
            n: 8,
            show_n:0
        });
    });
</script>

<div class="my-buzz">loading..</div>
```

A little CSS fiddling, and voila\!

![Google Buzz Widget Image](buzz-widget.png "Google Buzz Widget Image")

The only thing is that some stuff I really want sits in the other 20%:

- the (admittedly lightweight) formatting from the original Buzz
- the links I share
- the images I post to Flickr.

I don’t blame the Google Buzz Widget for not having that information. It
uses a Google service which does not yet provide those details. To get
at that information *today* I’ll need to directly access the original
feed, not the feed as translated by a service. Since I’m the sort of guy
that enjoys reinventing wheels, I’ll put something together myself.

My site runs on a shared host, and the freshest language available to me
on that host is [PHP](http://php.net). I’m not a huge fan of the
language, but I am pragmatic. If the most convenient tool available is
PHP, then that’s what I’ll use.

If they had [mod\_perlite](http://modperlite.org), it would be a
significantly different story. Oh well. Let’s begin.

## Start\!

The initial local development will be on the home Mac, running OS X 10.5
and PHP 5.2.11. My Web host supports newer versions of PHP - all the way
up to 6 -but I’m not going to worry about it today.

### Grab my own copy of the feed

All right. I know for a fact that I’m going to be loading and
manipulating this data a *lot* during the initial stage of development.
I might as well grab a copy of the Buzz XML feed and work with it
locally. That will save a bit of time and network load. Hey, every
second counts.

Buzz feed URLs follow a simple pattern, with your username inserted at
the approproate place.

> `http://buzz.googleapis.com/feeds/username/public/posted`

    $ wget http://buzz.googleapis.com/feeds/brian.wisti/public/posted -O buzz.xml
    ...
    2010-03-11 18:48:44 (754 KB/s) - `buzz.xml` saved [92972]

### Parse and Print

The first task is to parse the XML and display the results. I enjoy
[SimpleXML](http://php.net/manual/en/book.simplexml.php) when handling
XML in PHP-land, since it hands back a reasonable data structure without
any fuss from me.

``` php
<?php

function dump($variable) {
    $output = htmlentities(print_r($variable, TRUE));
    return "<pre>$output</pre>";
}

$source = 'buzz.xml';
$buzz = simplexml_load_file($source);

// Printing this, because PHP chokes on the '<?xml' Processing Instruction
print '<?xml version="1.0"?>';
?>
<!DOCTYPE html
    PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
    <head>
        <title>Buzz Stream Test</title>
    </head>
    <body>
        <h1>Buzz Stream Test</h1>
        <?php echo dump($buzz) ?>
    </body>
</html>
```

The result is not exciting, but it does show that the XML is being
parsed. I have created a simple `dump` function which will come in handy
as I examine the information being displayed.

![Google Buzz dumped image](buzz-dump.png "Google Buzz dumped image")

### Show Entries

Now I want to display the entries. How about I start by dumping them?

``` php
<?php

function dump($variable) {
    $output = htmlentities(print_r($variable, TRUE));
    return "<pre>$output</pre>";
}

$source = 'buzz.xml';
$buzz = simplexml_load_file($source);

// Printing this, because PHP chokes on the '<?xml' Processing Instruction
print '<?xml version="1.0"?>';
?>
<!DOCTYPE html
    PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
    <head>
        <title>Buzz Stream Test</title>
    </head>
    <body>
        <h1>Buzz Stream Test</h1>
        <?php foreach($buzz->entry as $entry): ?>
        <?php echo dump($entry) ?>
        <hr />
        <?php endforeach ?>
    </body>
</html>
```

This lets me focus on the structure of an entry, at least as far as
SimpleXML perceives it.

    SimpleXMLElement Object
    (
        [title] => Buzz by Brian Wisti from Buzz
        [summary] => Right. I set up a basic Buzz feed on my site using the jQuery Google Buzz Widget. It'll do while I'm hacking together one of my own for a new PHP project page on coolnamehere. That section's been a bit neglected.
        [published] => 2010-03-11T08:04:37.000Z
        [updated] => 2010-03-11T08:04:37.626Z
        [id] => tag:google.com,2009:buzz/z135dd3bwnadctqp404cd1tqkrqpyjgrmtg0k
        [link] => Array
            (
                [0] => SimpleXMLElement Object
                    (
                        [@attributes] => Array
                            (
                                [rel] => alternate
                                [type] => text/html
                                [href] => http://www.google.com/buzz/108694322269563399860/UYqMxptshCD/Right-I-set-up-a-basic-Buzz-feed-on-my-site-using
                            )

                    )

                [1] => SimpleXMLElement Object
                    (
                        [@attributes] => Array
                            (
                                [rel] => replies
                                [type] => application/atom+xml
                                [href] => http://buzz.googleapis.com/feeds/108694322269563399860/comments/z135dd3bwnadctqp404cd1tqkrqpyjgrmtg0k
                            )

                    )

            )

        [author] => SimpleXMLElement Object
            (
                [name] => Brian Wisti
                [uri] => http://www.google.com/profiles/brian.wisti
            )

        [content] => <div>Right. I set up a basic Buzz feed on my site using the jQuery Google Buzz Widget. It&#39;ll do while I&#39;m hacking together one of my own for a new PHP project page on coolnamehere. That section&#39;s been a bit neglected.</div>
    )

Quite a few details are being missed because SimpleXML has its own
special tricks for handling namespaces, but a lot can be done before
that is a concern. Let’s look at the information that *is* readily
accessible and figure out what I can do with it.

title
: The posting source is shown here (Buzz, Flickr, Mobile, etc.)

published
: When the Buzz was posted

link
: A collection of links associated with the buzz (the buzz itself,
  posted links, images, replies, etc.)

content
: The Buzz, formatted as an HTML fragment

Let’s do some simple formatting. I’m not sure what to do with the links
yet, so I’ll just `dump` them.

``` php
<body>
    <h1>Buzz Stream Test</h1>
    <?php foreach ($buzz->entry as $entry): ?>
        <?php echo $entry->content ?>
        <p><?php echo $entry->published ?></p>
        <p><?php echo $entry->title ?></p>
        <?php foreach ($entry->link as $link): ?>
            <?php echo dump($link) ?>
        <?php endforeach ?>
    <?php endforeach ?>
</body>
```

So what does that get us?

:::note

Oh that’s right. At one point this was a sort of cool direct embedding
of my Buzz debug run into the page. Wonder if I could find a capture at
<https://archive.org>

:::

``` html
<div class="example">
<div>The sock begins</div>
<p>2010-03-10T07:22:09.000Z</p>
<p>Buzz by Brian Wisti from Flickr</p>
<pre>SimpleXMLElement Object
(
    [@attributes] => Array
        (
            [rel]  => alternate
            [type] => text/html
            [href] => http://www.google.com/buzz/108694322269563399860/PaTypwpxCkH/The-sock-begins
        )

)
</pre>
<pre>SimpleXMLElement Object
(
    [@attributes] => Array
        (
            [rel]   => enclosure
            [href]  => http://www.flickr.com/photos/20592809@N00/4422058708
            [type]  => image/jpeg
            [title] => The sock begins
        )

)
</pre>
<pre>SimpleXMLElement Object
(
    [@attributes] => Array
        (
            [rel]  => replies
            [type] => application/atom+xml
            [href] => http://buzz.googleapis.com/feeds/108694322269563399860/comments/z13lhl3xavv4ujzga04cd1tqkrqpyjgrmtg0k
        )

)
</pre>
</div>
```

This particular example has three links.

- An HTML "alternate" link that goes to the original Buzz post.
- An image "enclosure" link that leads to the [Flickr
  photo](http://www.flickr.com/photos/20592809@N00/4422058708).
- An Atom "replies" link that leads to a feed of replies for the
  original post.

I care about the alternate and enclosure links, but not about the
replies. Now, every entry has an alternate link, but not all of them
have enclosure links. I will need to do a little processing to display
those links properly, but I don’t want that processing to occur down
there in the display section. I like to keep my displays as simple as
possible. I’m going to create a Buzz\_Entry class to handle the hard
work.

The first stab at this class is going to be simple, just adding clearly
defined links for the Buzz and any enclosure.

``` php
<?php

// Buzz/Entry.class.php
class Buzz_Entry
{

    function __construct($xml_node) {
        $this->title = $xml_node->title;
        $this->content = $xml_node->content;
        $this->published = $xml_node->published;
        $this->link = null;
        $this->enclosure = array();

        foreach($xml_node->link as $link) {
            switch($link['rel']) {
            case 'alternate':
                $this->link = $link['href'];
                break;
            case 'enclosure':
                $this->enclosure = $link;
                break;
            default:
                break;
            }
        }
    }
}

?>
```

The newest iteration of the main file builds a collection of Buzz\_Entry
objects and takes advantage of the new attributes.

``` php
<?php

require 'Buzz/Entry.class.php';

function dump($variable) {
    $output = htmlentities(print_r($variable, TRUE));
    return "<pre>$output</pre>";
}

$source = 'buzz.xml';
$buzz = simplexml_load_file($source);
$entries = array();

foreach($buzz->entry as $entry_node) {
    $entry = new Buzz_Entry($entry_node);
    array_push($entries, $entry);
}

// Printing this, because PHP chokes on the '<?xml' Processing Instruction
print '<?xml version="1.0"?>';
?>
<!DOCTYPE html
    PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
    <head>
        <title>Buzz Stream Test</title>
    </head>
    <body>
        <h1>Buzz Stream Test</h1>
        <?php foreach ($entries as $entry): ?>
            <?php echo $entry->content ?>
            <p><a href="<?php echo $entry->link ?>"><?php echo $entry->published ?></a></p>
            <p><?php echo $entry->title ?></p>
            <?php if ($entry->enclosure): ?>
                <p><a href="<?php echo $entry->enclosure['href']?>"><?php echo $entry->enclosure['title'] ?></a></p>
            <?php endif ?>
        <?php endforeach ?>
    </body>
</html>
```

Hey look\! Now there’s stuff you can click\!

I want to refactor a little bit now, and put that initial logic into a
separate file. It’s nice to keep your workplace tidy.

``` php
<?php

// Buzz.inc.php

require 'Buzz/Entry.class.php';

/**
 * Prints the guts of a variable as preformatted text.
 */
function dump($variable) {
    $output = htmlentities(print_r($variable, TRUE));
    return "<pre>$output</pre>";
}

/**
 * Creates a collection of Buzz_Entry objects by
 * parsing the Buzz feed found in $source.
 */
function load_buzz($source) {
    $buzz = simplexml_load_file($source);
    $entries = array();

    foreach($buzz->entry as $entry_node) {
        $entry = new Buzz_Entry($entry_node);
        array_push($entries, $entry);
    }

    return $entries;
}

?>
```

This makes the initial PHP block of the main file simple.

``` php
<?php

require 'Buzz.inc.php';
$source = 'buzz.xml';
$entries = load_buzz($source);

// Printing this, because PHP chokes on the '<?xml' Processing Instruction
print '<?xml version="1.0"?>';
?>
⋮
```

Now that I’ve satisfied my general sense of tidiness for the moment, I
want to make the "published" timestamp into something normal people can
read.

``` php
<?php

class Buzz_Entry
{

    function __construct($xml_node) {
        $this->title = $xml_node->title;
        $this->content = $xml_node->content;

        // For your own formatting options, see:
        //   http://www.php.net/manual/en/function.date.php
        $this->published = date('g:i a, F jS', strtotime($xml_node->published));

        // ...
    }
}

?>
```

It’s a good idea to set the time zone, especially if your "published"
format includes the time. I set mine in Buzz.inc.php.

``` php
<?php

// Buzz.inc.php

date_default_timezone_set('America/Los_Angeles');

require 'Buzz/Entry.class.php';
// ...
```

Now I don’t have to work so hard to figure out when a particular Buzz
was posted.

``` html
<div class="example">
<div>The sock begins</div>
<p><a href="http://www.google.com/buzz/108694322269563399860/PaTypwpxCkH/The-sock-begins">11:22 pm, March 9th</a></p>
<p>Buzz by Brian Wisti from Flickr</p>
<p><a href="http://www.flickr.com/photos/20592809@N00/4422058708">The sock begins</a></p>
</div>
```

I want to make one more adjustment to the output. The phrase "Buzz by
Brian Wisti from X" in every title is redundant. "X" is the important
part. Let’s get rid of the title, and replace it with a source.

``` php
<?php

// Buzz/Entry.class.php

class Buzz_Entry
{

    function __construct($xml_node) {
        $this->source = str_replace('Buzz by Brian Wisti from ', '', $xml_node->title);
        $this->content = $xml_node->content;
        // ...
```

I can’t forget to change the reference in the main PHP file.

``` php
// ...
<?php foreach ($entries as $entry): ?>
    <?php echo $entry->content ?>
    <p><a href="<?php echo $entry->link ?>"><?php echo $entry->published ?></a></p>
    <p><?php echo $entry->source ?></p>
// ...
```

Better?

``` html
<div class="example">
<div>The sock begins</div>
<p><a href="http://www.google.com/buzz/108694322269563399860/PaTypwpxCkH/The-sock-begins">11:22 pm, March 9th</a></p>
<p>Flickr</p>
<p><a href="http://www.flickr.com/photos/20592809@N00/4422058708">The sock begins</a></p>
</div>
```

Yes. Each entry now has what I consider a comfortable amount of
information. Sure, I would love to embed the image into the entry, but
that can wait. At least the link to the image is being displayed.

Besides, if I wait too long the Buzz API will cover all of this. I want
something up *today*.

Now that I have the information I want, it’s time to make the entries
pretty with a little shuffling and some CSS.

``` php
<?php foreach ($entries as $entry): ?>
    <div class="entry">
        <?php echo $entry->content ?>
        <?php if ($entry->enclosure): ?>
            <p class="enclosure">
                <a href="<?php echo $entry->enclosure['href']?>"><?php echo $entry->enclosure['title'] ?></a>
            </p>
        <?php endif ?>
        <p class="published">
            <a href="<?php echo $entry->link ?>"><?php echo $entry->published ?></a>
            (via <?php echo $entry->source ?>)
        </p>
    </div>
<?php endforeach ?>
```

Here are the style rules that I used.

``` css
.entry {
    border: thin solid black;
    padding: 0.5em;
    margin: 0.5em;
}

.entry a {
    text-decoration: none;
}

.entry p.published {
    text-align: right;
    font-size: 75%;
    margin: 0;
}

.entry p.enclosure {
    margin-left: 1em;
}
```

And the result may not be pretty, but it’s definitely better looking
than it was before.

### Live Data

Most of my fiddling is done. It is time to use live data. On the home
machine, I only need to change the value of $source, because I have
[allow\_url\_fopen](http://us2.php.net/manual/en/filesystem.configuration.php#ini.allow-url-fopen)
enabled.

``` php
<?php
require 'Buzz.inc.php';

// Remember to replace 'brian.wisti' with your username
$source = 'http://buzz.googleapis.com/feeds/brian.wisti/public/posted';
$entries = load_buzz($source);
# ...
```

However, more is needed for this to work on the shared host.
allow\_url\_fopen is not available, but the [PHP cURL
functions](http://us2.php.net/manual/en/ref.curl.php) are. Well, we work
with what we have.

``` php
<?php

// Buzz.inc.php

// ...

function load_buzz($source) {
    if (ini_get('allow_url_fopen') == 'waffles') {
        $buzz = simplexml_load_file($source);
    } elseif (function_exists('curl_init')) {
        $curl = curl_init();
        curl_setopt($curl, CURLOPT_URL, $source);
        curl_setopt($curl, CURLOPT_HEADER, 0);
        curl_setopt($curl, CURLOPT_RETURNTRANSFER, 1);
        $raw_xml = curl_exec($curl);
        curl_close($curl);
        $buzz = new SimpleXMLElement($raw_xml);
    } else {
        throw new Exception("No reasonable fetching function available");
    }

    $entries = array();

    foreach($buzz->entry as $entry_node) {

        $entry = new Buzz_Entry($entry_node);
        array_push($entries, $entry);
    }

    return $entries;
}
```

Most of you can stop right here, but I need to do one more step. This
site is actually a bunch of static HTML content, with no server side
interaction. Well, almost static. I give myself permission to include
content feeds from supplemental files and sites via JavaScript.

It’s my site, and I go by my own strange rules. At least I try to be
consistent.

I’m going to do some quick and dirty
[AJAX](http://en.wikipedia.org/wiki/Ajax_\(programming\)). Very quick,
and very dirty. Let’s change the main buzz.php file so that it generates
an HTML fragment rather than a whole valid page.

``` php
<?php

require 'Buzz.inc.php';
$source = 'http://buzz.googleapis.com/feeds/brian.wisti/public/posted';
$entries = load_buzz($source);
?>
<?php foreach ($entries as $entry): ?>
    <div class="entry">
        <?php echo $entry->content ?>
        <?php if ($entry->enclosure): ?>
            <p class="enclosure">
                <a href="<?php echo $entry->enclosure['href']?>"><?php echo $entry->enclosure['title'] ?></a>
            </p>
        <?php endif ?>
        <p class="published">
            <a href="<?php echo $entry->link ?>"><?php echo $entry->published ?></a>
            (via <?php echo $entry->source ?>)
        </p>
    </div>
<?php endforeach ?>
```

I will continue using [jQuery](http://jquery.com) as the framework for
JavaScript interaction at this site, because it’s familiar to me.

``` html
<script type="text/javascript" src="inc/js/jquery-1.4.2.js"></script>
<script type="text/javascript" src="inc/js/cnh.js"></script>
```

Off in my site JavaScript file cnh.js, I set up the buzz-loading
function. All it does is grab the output from buzz.php and insert it
into the document.

``` javascript
function get_buzz(div) {
    $.ajax({
        url: "/buzz/buzz.php",
        cache: false,
        success: function(summary) {
            div.append(summary);
        }
    });
}
```

Finally, I add the function call to my site index:

``` html
<div id="buzz"></div>

<script type="text/javascript">
$(document).ready(function(){ get_buzz($('#my-buzz')); })
</script>
<noscript>
<p>See my latest updates on <a
href="http://www.google.com/profiles/brian.wisti#buzz">Google Buzz</a>.</p>
</noscript>
```

Hopefully you can now go to the [home page](/) and see a Buzz feed\!

:::note

Well, you could have if it was 2010 and Google Buzz was still a thing.
Oh well.

:::

Okay, one issue. It’s showing the *whole* feed. Let’s throw in a limit
to the number of entries returned. I don’t feel like messing with the
calling code right now, so let’s have a reasonable default.

``` php
<?php

// Buzz.inc.php

// ...

function load_buzz($source, $limit = 10) {
    if (ini_get('allow_url_fopen') == 'waffles') {
        $buzz = simplexml_load_file($source);
    } elseif (function_exists('curl_init')) {
        $curl = curl_init();
        curl_setopt($curl, CURLOPT_URL, $source);
        curl_setopt($curl, CURLOPT_HEADER, 0);
        curl_setopt($curl, CURLOPT_RETURNTRANSFER, 1);
        $raw_xml = curl_exec($curl);
        curl_close($curl);
        $buzz = new SimpleXMLElement($raw_xml);
    } else {
        throw new Exception("No reasonable fetching function available");
    }

    $entries = array();

    foreach($buzz->entry as $entry_node) {
        if ($limit <= 0) { break; }

        $entry = new Buzz_Entry($entry_node);
        array_push($entries, $entry);
        $limit--;
    }

    return $entries;
}
```

Okay. That’s a good enough hack for a low-traffic site like mine.

### Cache the Output

What would happen if I got twelve million hits per minute because the
world had suddenly become obsessed over whether I would ever finish
knitting those socks?

Well, my educated guess is that coolnamehere.com would be hosed. I have
a good host for the price, but I think that is more traffic than your
average shared host would be prepared for.

I can take precautions to reduce the load, though. One that comes to
mind is caching the HTML output to a file, and only checking for updates
every 30 minutes or so. That will involve using PHP’s [output control
functions](http://www.php.net/manual/en/ref.outcontrol.php) to store the
output which would normally be printed.

I’m putting the display block into a template file, to make the
application flow a little easier to understand. The display block does
get an additional item to tell me *when* the cache was last built.

``` php
<?php /* Buzz/Template.inc.php */ ?>
<p class="generated">Generated at <?php echo $build_time ?></p>

<?php foreach ($entries as $entry): ?>
    <div class="entry">
        <?php echo $entry->content ?>
        <?php if ($entry->enclosure): ?>
            <p class="enclosure">
                <a href="<?php echo $entry->enclosure['href']?>"><?php echo $entry->enclosure['title'] ?></a>
            </p>
        <?php endif ?>
        <p class="published">
            <a href="<?php echo $entry->link ?>"><?php echo $entry->published ?></a>
            (via <?php echo $entry->source ?>)
        </p>
    </div>
<?php endforeach ?>
```

The main `buzz.php` looks a bit different now. Instead of jumping
straight to the display, it looks for a cache file. If the cache file is
new enough -defined here as less than 30 minutes old - then the script
goes the easy way out and loads the cache. Otherwise, it buffers the
output into a string, which is then saved to the cache file.

``` php
<?php

require 'Buzz.inc.php';
$source = 'http://buzz.googleapis.com/feeds/brian.wisti/public/posted';
$html_cache = "/tmp/buzz.html";
$cache_limit = 30 * 60; // Maximum allowed age for cache, in seconds

// Load the cache if it exists and is new enough.
if (file_exists($html_cache)) {
    $cache_age = time() - filemtime($html_cache);

    if ($cache_age < $cache_limit) {
        $output = file_get_contents($html_cache);
    }
}

// Build the cache if it is not loaded.
if (!$output) {
    $entries = load_buzz($source);
    $build_time = date('g:i a, F jS', time());
    ob_start();
    require('Buzz/Template.inc.php');
    $output = ob_get_contents();
    file_put_contents($html_cache, $output);
}

echo $output;

?>
```

Oh right. Whatever the output was gets sent to the browser. Don’t want
to forget about that.

Sweet. It worked. I make a couple minor adjustments relevant to my
shared host settings, upload what I have, and hope for the best.

### A Quick Bug Fix

One issue is that the output gets displayed twice when the cache is
first built.

The problem is that I’m building `$output` by capturing standard output,
and then printing out `$output`. What I didn’t stop to think about is
the fact that standard output still gets displayed when the script is
done running.

Okay, so a quick fix is to only display output when it’s loaded from the
cache file.

``` php
<?php

require 'Buzz.inc.php';
$source = 'http://buzz.googleapis.com/feeds/brian.wisti/public/posted';
$production_temp = '/home/bwisti/tmp';

if (file_exists($production_temp)) {
    $html_cache = "$production_temp/buzz.html";
} else {
    $html_cache = "/tmp/buzz.html";
}

$cache_limit = 30 * 60; // Maximum allowed age for cache, in seconds

// Load the cache if it exists and is new enough.
if (file_exists($html_cache)) {
    $cache_age = time() - filemtime($html_cache);

    if ($cache_age < $cache_limit) {
        $output = file_get_contents($html_cache);
        echo $output;
    }
}

// Build the cache if it is not loaded.
if (!isset($output)) {
    $entries = load_buzz($source);
    $build_time = date('g:i a, F jS', time());
    ob_start();
    require('Buzz/Template.inc.php');
    $output = ob_get_contents();
    file_put_contents($html_cache, $output);
}

?>
```

## Next Steps

There is a lot more information in the XML that I haven’t used with my
naive application of SimpleXML. Once my eyes have uncrossed from this
quick burst of activity, I’ll want to figure out how to get at those
details and incorporate them into the feed.