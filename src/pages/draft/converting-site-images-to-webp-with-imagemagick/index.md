---
caption: null
category: Tools
description: null
draft: true
layout: layout:Article
slug: converting-site-images-to-webp-with-imagemagick
tags:
- images
- shell
- perl
- crystal
- site
title: Converting Site Images to Webp with ImageMagick
uuid: 3f6568e9-bd1f-4244-a6e9-0dbc83f19ee8
---

## What I'm trying to do

Convert all the images in my site to Webp while still leaving the originals in there for browsers that don't support it.
We won't name names.
Safari knows what it's done.

### Why

Reduce image sizes for quicker download of pages in supported browsers.

### Why in three different ways?

It's Friday and I'm bored.
And ImageMagick can be linked to almost anything.
I wanted to show that off.

### Set the scene

[libPixel]: https://www.libpixel.com/

Today my platform of choice is Ubuntu 20.04 on WSL.

I want this all local.
[libPixel][] looks cool, but I don't like calling out to external services when I don't need to.

## Shell

* `find`
* `convert`

Finding images with `find`?
Super easy.

Hang on.
I forgot a backslash.
*There* we go.

```
find -type f -iregex "^.*\.\(png\|jpe?g\)$"

./content/note/2019/06/karabiner/cover.png
./content/note/2019/06/chicken-for-lunch/cover.jpg
./content/note/2019/06/internet-connected/cover.png
./content/note/2019/07/charming-victorian-also-means-creepy-as-hell/cover.jpg
./content/note/2019/07/home/cover.jpg
⋮
and so on, for 3296 rows
```

Converting images with `convert`?

```
brew tap linuxbrew/xorg
```

```
brew install imagemagick
```

Easy peasy.

```
time find content -type f -iregex "^.*\.\(png\|jpe?g\)$" -exec mogrify -verbose -format webp {} \;

find content -type f -iregex "^.*\.\(png\|jpe?g\)$" -exec mogrify -verbose
227.45s user 9.40s system 120% cpu 3:17.11 total
```

Well that does take a bit, doesn't it?

What about the variant that hands all the filenames over at once?

```
time find content -type f -iregex "^.*\.\(png\|jpe?g\)$" -exec mogrify -verbose -format webp {} \+

find content -type f -iregex "^.*\.\(png\|jpe?g\)$" -exec mogrify -verbose
228.39s user 5.13s system 124% cpu 3:08.09 total
```

Um.
Anyways.
We'll get back to this.

Next we need to figure out how much work is needed to use Webp images in my Hugo site.

Hang on.
Jpeg images should convert to lossy Webp.
PNG images should convert to lossless.

TODO

## Perl

* Mojolicious
    * Mojo::File
* Image::Magick

## Crystal
