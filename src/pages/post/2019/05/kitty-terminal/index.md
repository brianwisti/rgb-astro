---
aliases:
- /2019/05/27/kitty-terminal/
category: Tools
cover_image: cover.png
date: 2019-05-27 00:00:00
description: 'I installed kitty for font ligatures in terminals on Linux, but it does
  other stuff too.

  '
layout: layout:PublishedArticle
slug: kitty-terminal
tags:
- shell
- kitty
title: Kitty Terminal
updated: 2019-05-27 00:00:00
uuid: 42abf77c-765b-431b-960e-699845508fdf
---

[kitty](https://sw.kovidgoyal.net/kitty/index.html) is a fast terminal
emulator for Linux and macOS. It includes many features, but the one
that interested me was support for
[ligatures](https://en.wikipedia.org/wiki/Typographic_ligature) in code.
Ligatures *basically* let you combine symbols, characters, or graphemes
to produce a single glyph with compressed meaning.

![Fira Code ligatures](all_ligatures.png)

*via [Github](https://github.com/tonsky/FiraCode/blob/master/showcases/all_ligatures.png)*

Confused yet? Me too. I barely understand what I’m trying to describe
here. Really it’s just that ligatures make your code look cooler than
the plain text most developers enter and read for hours a day. Whether
they improve life in any meaningful fashion is arguable, but "it looks
cooler" is good enough for me today.

By using a special font such as [Fira
Code](https://github.com/tonsky/FiraCode) and a capable terminal, all
sorts of character transformations happen. For example, the `<` and `=`
characters combined as `⇐` — to indicate "less than or equal to" —
displays as `⩽`. It means the same thing, but it says it with a single
visual character.

[Raku]: /tags/raku-lang

We have this rich library of symbols to describe our solutions, but most
programming languages use a tiny subset of those symbols. Except
[Raku][] of course. Raku sort of does everything.

    $ raku -e 'say 1 ≤ 5'
    True

Anyways, back to ligatures. They let you pretend you’re using that rich
library of symbols.

Gnome Terminal does not support ligatures, at least not on my system.
Konsole from the [KDE](https://www.kde.org/) project does, but adds many
KDE-specific dependencies to my system. I wanted to find something a bit
more lightweight.

kitty satisfies that need.

## Installing kitty

kitty runs on both Linux and macOS, but right now I’m concerned with
Linux. I already have [iTerm2](https://iterm2.com/) for ligatures on
macOS.

The [installation
instructions](https://sw.kovidgoyal.net/kitty/binary.html) for *kitty*
follow a familiar pattern of "grab and run the installer script." If you
don’t feel safe with that you can [install from
source](https://sw.kovidgoyal.net/kitty/build.html).

    $ curl -L https://sw.kovidgoyal.net/kitty/installer.sh | sh /dev/stdin

`installer.sh` loads Python to download the latest `kitty` executable to
`~/.local/kitty.app` on Linux.

I followed the installation instructions for desktop integration, making
small adjustments as needed for my own system setup.

    $ ln -s ~/.local/kitty.app/bin/kitty ~/bin/
    $ cp ~/.local/kitty.app/share/applications/kitty.desktop \
      ~/.local/share/applications
    $ sed -i \
      "s/Icon\=kitty/Icon\=\/home\/$USER\/.local\/kitty.app\/share\/icons\/hicolor\/256x256\/apps\/kitty.png/g" \
      ~/.local/share/applications/kitty.desktop
    $ chmod u+x ~/.local/share/applications/kitty.desktop

These steps put *kitty* on my `$PATH` and create a desktop entry
complete with application icon for launching from the GNOME Menu.

My desktop entry file ended up looking like this after a couple edits
(specifying executable path, stuff like that).

**`kitty.desktop`**

```ini
[Desktop Entry]
Version=1.0
Type=Application
Name=kitty
GenericName=Terminal emulator
Comment=A fast, feature full, GPU based terminal emulator
TryExec=/home/randomgeek/bin/kitty
Exec=/home/randomgeek/bin/kitty
Icon=/home/randomgeek/.local/kitty.app/share/icons/hicolor/256x256/apps/kitty.png
Categories=System;TerminalEmulator;
```

Course, I still had to tell GNOME the desktop launcher was trustworthy
but opening `~/.local/share/applications/kitty.desktop` in the GNOME
file manager.

![GNOME trust dialog](gnome-trust.png)

## Font installation

I need a font that supports ligatures now. Fira Code is the one I know
best, though I wouldn’t mind trying others. Fortunately, Fira Code is
available via my system package manager.

    $ sudo apt install fonts-firacode

## kitty configuration

Next step is to define my
[configuration](https://sw.kovidgoyal.net/kitty/conf.html) in
`~/.config/kitty/kitty.conf`. The whole point of this experiment is to
get ligatures, so that’s my first configuration change.

    font_family           Fira Code
    bold_font             auto
    italic_font           auto
    bold_italic_font      auto
    font_size             14.0

Then throw in some window geometry stuff. Normally *kitty* remembers and
applies the last window size you used, but I often don’t want that for
the quick transient terminals I open during my day. Instead I go with a
terminal 110 characters wide and 40 columns tall.

    remember_window_size  no
    initial_window_width  110c
    initial_window_height 40c

*kitty* does not load a login shell by default. I prefer a login shell,
so I specify that in `kitty.conf`.

    shell                 /bin/bash --login

## Using kitty

![Ligatures when looking at Mojolicious source](mojolicious.png)

The ligatures are pretty, of course. But what I really notice? Kitty is
fast. Maybe that’s just because I became accustomed to GNOME Terminal
and its sluggishness. Kitty might not be
[rxvt](http://rxvt.sourceforge.net/) fast, but it’s much quicker than
what I’m used to.

Since kitty is a terminal emulator, most of the functionality is
familiar. The default [keyboard
shortcuts](https://sw.kovidgoyal.net/kitty/index.html#tabs-and-windows)
are similar to those offered by GNOME Terminal, with support for
clipboard access and tabs. *kitty* also supports windows much like panes
in [tmux](https://github.com/tmux/tmux/wiki), but for now I’m sticking
with the familiarity of tmux.

## Speaking of tmux

terminfo should install what’s needed, but if not you will see an
annoying message when you try to start tmux:

    $ tmux
    open terminal failed: missing or unsuitable terminal: xterm-kitty

This works:

    $ TERM="xterm-256color" tmux

But see this
[StackExchange](https://unix.stackexchange.com/questions/470676/tmux-under-kitty-terminal)
item for better instructions. Or at least a pointer to better
instructions.

## kittens

[Kittens](https://sw.kovidgoyal.net/kitty/index.html#kittens) are Python
scripts that take advantage of features provided by kitty. Kitty
includes built-in kittens for handling [handling arbitrary
text](https://sw.kovidgoyal.net/kitty/kittens/hints.html) such as URLs,
working with the
[clipboard](https://sw.kovidgoyal.net/kitty/kittens/clipboard.html), and
viewing [file diffs](https://sw.kovidgoyal.net/kitty/kittens/diff.html).
You can even [write your
own](https://sw.kovidgoyal.net/kitty/kittens/custom.html)\!

Most of the kittens are useful, but a couple also make for great
screenshots. So here they are 😸

### icat

[icat](https://sw.kovidgoyal.net/kitty/kittens/icat.html) shows an image
in the terminal.

    $ kitty +kitten icat cat-fall.jpeg

![classic cat pics in the terminal!](kitty-icat.png)

<aside class="admonition note">
<p class="admonition-title">Note</p>

Over on Twitter, [Yanick Champoux](http://techblog.babyl.ca/) noted that
`icat` does not play well with tmux.

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">Kitty installed and trial started. Alas tmux interferes w/ icat. But the rest is very spiffy. Many thanks for sharing!</p>&mdash; Yanick (@yenzie) <a href="https://twitter.com/yenzie/status/1133131184089681920?ref_src=twsrc%5Etfw">May 27, 2019</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
Confirmed for myself by running icat in a tmux window.

    $ kitty +kitten icat content/post/2019/kitty-terminal/kitty-icat.png
    Terminal does not support reporting screen sizes via the TIOCGWINSZ ioctl

Dang. Thanks, Yanick!

</aside>

### Unicode Input

`Control-Shift-U` lets you enter [Unicode
characters](https://sw.kovidgoyal.net/kitty/kittens/unicode-input.html),
by code or by name.

![Entering a unicode character by name in kitty](unicode-entry.png)

## kitty is fun

Even if I get tired of ligatures — a distinct possibility — I can see
continuing to use kitty for its speed and extensibility. Anyways, it’s
fun to expand my toolkit a little more\!