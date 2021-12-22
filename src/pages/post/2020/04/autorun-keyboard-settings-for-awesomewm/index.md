---
aliases:
- /2020/04/12/autorun-keyboard-settings-for-awesomewm/
category: tools
date: 2020-04-12 20:40:03
description: Getting Control and Escape keys where I want them
draft: false
layout: layout:PublishedArticle
slug: autorun-keyboard-settings-for-awesomewm
tags:
- linux
- settings
- awesomewm
title: Autorun Keyboard Settings for Awesomewm
uuid: f3f318ba-dea5-4276-9471-83663ff0bf52
---

I like my Caps Lock key to not be a Caps Lock key. Act as Escape when I
tap on it. Act as Control when I press it with another key. And never
ever enable SHOUT MODE.

This is the third time I’ve done this. This is also the third time I had
to look up how to do this. Better save it on the site.

[setxcbmap](https://linux.die.net/man/1/setxkbmap) takes care of adding
Control functionality and removing Caps Lock behavior. I need
[xcape](https://github.com/alols/xcape) for Escape key behavior. Since
I’m running [Manjaro](https://manjaro.org/) on my Linux partition this
week, I’ll use [pamac](https://wiki.manjaro.org/index.php?title=Pamac)
to install.

    $ pamac install xcape

I set up an
[autostart](https://wiki.archlinux.org/index.php/Awesome#Autostart)
script to get this in every Awesomewm session.

**`~/.config/awesome/autorun.sh`**

```bash
#!/usr/bin/env bash

function run {
  if ! pgrep -f $1 ;
  then
    $@&
  fi
}

run setxkbmap -option ctrl:nocaps
run xcape -e 'Control_L=Escape'
```

It’s a script, so make sure it’s executable.

    $ chmod 755 ~/.config/awesome/autorun.sh

Add one line of code to my `rc.lua` to make sure `autorun.sh` gets
spawned on startup.

**`~/.config/awesome/rc.lua`**

```lua
-- {{{ Autorun
awful.spawn.with_shell("~/.config/awesome/autorun.sh")
-- }}}
```

And that’s it!