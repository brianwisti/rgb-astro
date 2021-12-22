---
aliases:
- /post/2016/all-the-hugo-themes/
- /2016/01/02/all-the-hugo-themes/
category: Programming
cover_image: cover.png
date: 2016-01-02 00:00:00
description: Using Python to preview my Hugo site with many themes
layout: layout:PublishedArticle
slug: all-the-hugo-themes
tags:
- hugo
- python
title: All The Hugo Themes
updated: 2016-01-04 00:00:00
uuid: a73c90a1-622c-425c-8f11-484dc40aa9b4
---

My site does well enough with [Hugo](http://gohugo.io/) and a custom
theme, but I wanted to explore the [themes
repository](http://themes.gohugo.io/). So I wrote some
[Python](https://python.org/).

<aside class="admonition" markdown="1">
<p class="admonition-title">Updates</p>

2016-01-04
: Added instructions for installing dependencies with Homebrew, and
  clarified some content based on comments from the [Hugo
  community](https://discuss.gohugo.io).

2016-01-03
: My checkout of the themes repository was out of date. I refreshed it
  this morning, resulting in a new GIF.

</aside>

If you followed the [Hugo
Quickstart](https://gohugo.io/overview/quickstart/) then you probably
already have your own copy of the themes to use. Otherwise you might
want to clone the [hugoThemes](https://github.com/spf13/hugoThemes/)
repo with git.

    $ cd mysite/
    $ git clone --depth 1 --recursive https://github.com/spf13/hugoThemes.git themes

## Code

The idea here is to ask Hugo to build and serve the site once for each
theme. For each built theme, ask the browser to load and screenshot the
site with that theme.

I chose Python for this task. No special reason. I was just in a Python
mood that day.

[Splinter](https://splinter.readthedocs.org/en/latest/) provided the
browser controlling API. Since I’m using Chrome for this, I installed
the [Chrome
WebDriver](https://splinter.readthedocs.org/en/latest/drivers/chrome.html).
The [subprocess](https://docs.python.org/3.5/library/subprocess.html)
standard library module allowed me to control Hugo, restarting with a
fresh theme once the browser had enough time to grab a screenshot.

Then I had a last minute idea: use the
[convert](http://imagemagick.org/script/convert.php) utility from
[ImageMagick](http://imagemagick.org/script/index.php) to collect all
the screenshots into an animated GIF.

You may need to install dependencies. Everything you need *should* be
available for your platform, but I still need to double check that. Here
are the steps I followed to get things working with
[Homebrew](https://brew.sh) on my Mac.

    $ brew install python3 imagemagick chromedriver
    $ pip3 install splinter

All right - that’s out of the way. Now for some code.

**`show-themes.py`**

```python
#!/usr/bin/env python3

import os
import os.path
import shutil
import subprocess
import time

from splinter import Browser

def is_theme_dir(folder, item):
    if item[0] == '.':
        return False
    full_path = os.path.join(folder, item)
    if os.path.isfile(full_path):
        return False

    return True

if __name__ == '__main__':
    theme_dir = "themes"
    screenshot_dir = "screenshots"
    url = "http://127.0.0.1:1313"

    # Clean up old screenshots
    for f in os.listdir(screenshot_dir):
        filepath = os.path.join(screenshot_dir, f)
        try:
            if os.path.isfile(filepath):
                os.unlink(filepath)
        except Exception as e:
            print(filepath, e)

    listing = [ item for item in os.listdir(theme_dir)
            if is_theme_dir(theme_dir, item) ]
    browser_name = 'chrome'
    browser = Browser(browser_name)
    browser.visit(url) # visit out here, reload down there because browser cache

    for theme in listing:
        command = [ "/usr/local/bin/hugo", "server", "--theme", theme ]
        hugo = subprocess.Popen(command)
        time.sleep(1) # More than enough time for Hugo to build the site.
        browser.reload()
        time.sleep(2) # Allow browser to get external resources.
        message = "Theme: {}, Status: {}".format(theme, browser.status_code)
        print(message)
        screenshot_name = "{}-{}.".format(browser_name, theme)
        screenshot_file = os.path.join(os.getcwd(), screenshot_dir, screenshot_name)
        browser.screenshot(screenshot_file)
        print("Screenshot saved as: {}".format(screenshot_file))
        hugo.kill()
    browser.quit()

    # Make an animated GIF of the whole thing.
    convert_command = [ "/usr/local/bin/convert",
            "-delay",  '50',
            "-loop",    '0',
            "-scale", '50%',
            "screenshots/*.png",
            "hugo-themes.gif" ]
    subprocess.run(convert_command)
```

## The Result

Aside from a few dozen PNG files? Well, there’s that nifty animation.
Animated GIFs give me a headache sometimes, so I will [link to the
GIF](hugo-themes.gif) instead.

## Observations

I noticed a few things with this experiment.

### Configuration

![Red Lounge theme screenshot](chrome-redlounge-medium.png
  "[Red Lounge](https://themes.gohugo.io/redlounge) theme")

Themes vary significantly in their expected configuration options. Some
want social media links under `author`. Others wanted them in `Params`.
`gravatarHash` and `GravatarHash` are two distinct options. Many have
hard-coded assumptions in their layouts: an image file
`/img/avatar.jpg`, for example. Sometimes it’s called `/media/me.jpg`
though.

This is not an issue if you pick a favorite from the themes repository
and make your site work with your favorite. It *is* an issue if you’re
looking at your site in every theme. I turned my `config.yaml` into sort
of a mess to make it work with more of the themes.

### Layout

Although many themes focus on blog content, some have a different
purpose. Their authors may have created them with project documentation,
portfolios, or company sites in mind. Their structure is more complex or
requires metadata beyond a simple blog.

I like this variety. I find that it’s much easier to create sites with
different purposes using Hugo than when using Jekyll.

![Artists theme screenshot](chrome-artists-medium.png
  "[Artists](https://themes.gohugo.io/artists) theme")

But it does help understand why sometimes the site renders as an
attractive blank space in my preview. Examining the theme README would
be a good next step if a particular theme interested me.

Well - reading documentation for the thing you’re using is generally a
good idea anyways.

### Sections

![Pixyll theme screenshot](chrome-pixyll-medium.png
  "[Pixyll](https://themes.gohugo.io/pixyll) theme")

The themes seemed a little confused by my [craft](/categories/craft/)
section. Some ignored craft projects completely. Others integrated them
with posts on the `index.html` listing. Most at least provided a menu
link to the section. And yes, the theme `README` would likely remove my
confusion.

You will probably need to [customize your
template](http://gohugo.io/themes/customizing/) if you have special
content.

## What Theme Should I Use?

Maybe you were wondering which theme you could use for your new site. I
suggest [Hyde-X](http://themes.gohugo.io/hyde-x/) for blog sites. It has
nice defaults, and provides quality documentation for its many
configuration options. My site started with Hyde-X as a base before
moving in its own direction.

![Hyde-X theme screenshot](chrome-hyde-x-medium.png
  "[Hyde-X](https://themes.gohugo.io/hyde-x) theme")

Hyde-X isn’t the only way to start. There are numerous excellent
blog-focused themes in the repository.

For non-blog sites? I don’t know, to be honest. None of my content
worked well with those. Good luck with your search\!

Anyways, the important thing is to have fun.