---
aliases:
- /post/2017/taking-os-x-screenshots/
- /2017/05/26/taking-os-x-screenshots/
category: tools
date: 2017-05-26
draft: false
layout: layout:PublishedArticle
slug: taking-os-x-screenshots
tags:
- os x
title: Taking OS X Screenshots
uuid: b9ec65a1-605c-4f03-8b86-df57a012750c
---

Notes on saving screenshots in OS X, so I don’t have to look it up again.

This started as a search to find how I can set the OS screenshot save location.
[OS X Daily](http://osxdaily.com/) provided that information and much more.
I suggest you check it out for your OS X tips.

## The Shortcuts I Use

My fingers pretty much have these memorized, but it would be nice if my brain knew them too.

| Keys                           | Action
| ------------------------------ | ------
| `⌘ + ⇧ + 3`                    | Save full screen to file
| `⌘ + ⇧ + 4` + select area      | Save selected area to file
| `⌘ + ⇧ + 4` + spacebar + click | Save selected window to file

[several more]: http://osxdaily.com/2010/06/09/screen-capture-in-mac-os-x/
[Emacs]: /tags/emacs/

There are [several more][] that I do not use.
I'm already trying to learn [Emacs][] shortcuts.
I don't feel like cluttering my brain with additional OS X shortcuts I won't use.

## Setting The Save Location

OS X saves these files to `~/Desktop` by default, which results in much visual clutter on my screen desktop.
Eventually I tired of the periodic cleanups and learned how to save in a different folder.

    $ mkdir ~/Pictures/Screenshots
    $ defaults write com.apple.screencapture location ~/Pictures/Screenshots/

[suggested]: http://osxdaily.com/2011/01/26/change-the-screenshot-save-file-location-in-mac-os-x/

OS X Daily [suggested][] changing the setting and running `killall SystemUIServer`.
Somewhere in the years since that post was published, restarting SystemUIServer became unnecessary.