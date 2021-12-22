---
aliases:
- /blogspot/2008/01/30_php-extract-and-compact-functions.html
- /post/2008/php-extract-and-compact-functions/
- /2008/01/30/phps-extract-and-compact-functions/
category: blogspot
date: 2008-01-30 00:00:00
layout: layout:PublishedArticle
slug: phps-extract-and-compact-functions
tags:
- php
title: PHP's extract and compact functions
uuid: 47e4d9ef-c5aa-4bcd-a673-09b5380a8b84
---

[PHP]: http://php.net

I've been brushing up on my PHP basics lately. Why? Well, it never hurts to 
revisit things you think you already know. There is a good chance you will
discover something you didn't know after all. For example: this time I
learned about [PHP][]'s `extract` and `compact` functions.
<!--more-->

[`extract`]: http://us3.php.net/manual/en/function.extract.php
[`compact`]: http://us3.php.net/manual/en/function.compact.php

[`extract`][] takes an associative array and creates local variables on the
fly, named for the keys in the array and with the corresponding values
matched up. [`compact`][] is the corresponding function for taking a
collection of variables and stuffing them into an associative array.

``` php
<?php
  $book = array(
      "title"     => "Dad's Own Cookbook",
      "author"    => "Bob Sloan",
  );

  extract($book);
  echo $title . " was written by " . $author . "\n";

  $first = "Brian";
  $last  = "Wisti";
  $keys  = array("first", "last");
  $my_name = compact($keys);
  print_r($my_name);
?>
```

Running this code:

    $ php -f extract-compact.php
    Dad's Own Cookbook was written by Bob Sloan
    Array
    (
        [first] => Brian
        [last] => Wisti
    )

`extract` is the more immediately useful of the two for my purposes, because
it simplifies a common tactic I use for creating local variables based on 
database lookups.

Instead of manually creating local variables, like this:

``` php
<?php
    # ...
    while ($row = mysql_fetch_array($result, MYSQL_ASSOC)) {
        $author = $row["author"];
        $title  = $row["title"];
        # ...
    }
?>
```

I can save myself a little effort with `extract`.

``` php
<?php
    # ...
    while ($row = mysql_fetch_array($result, MYSQL_ASSOC)) {
        extract($row);
        # ...
    }
?>
```

I realize that there may be an even easier way to do it, but just this will
make my life noticeably easier as long as I don't abuse it. I would mainly
tuck a call like this off in a function and probably use it in conjunction with
a SQL query or something else where I knew exactly what names I would end up with.

Why didn't I know about this before? Well, the manual approach was good enough.
And since what I had was good enough, I didn't think of looking for a better 
approach. Then again, finds like this are exactly why I *do* go back and review
what I thought I already knew.