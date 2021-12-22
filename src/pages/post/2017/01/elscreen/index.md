---
aliases:
- /post/2017/elscreen/
- /2017/01/11/elscreen/
category: tools
cover_image: cover.png
date: 2017-01-11
draft: false
layout: layout:PublishedArticle
slug: elscreen
tags:
- emacs
- elscreen
title: elscreen
uuid: 07380976-b527-46ff-b398-cfe9e5670290
---

[ElScreen]: https://github.com/knu/elscreen/

I use [ElScreen][] every time I open Emacs.
May as well make a quick note about it.

[Vim]: http://www.vim.org/
[tmux]: https://tmux.github.io/

I admit it.
I’m still more of a [Vim][] user.
The workflow I’m used to is Vim with some tabs, usually sitting in a [tmux][] session.
When in Emacs I use ElScreen, which basically gives me tmux inside Emacs.

If you know what that means, great.
If not, then pretend ElScreen is a weird way to make emacs a tabbed editor.

## Install It

[ErgoEmacs]: http://ergoemacs.org/
[guide]: http://ergoemacs.org/emacs/emacs_package_system.html
[elscreen package]: https://melpa.org/#/elscreen
[MELPA]: https://melpa.org/

[ErgoEmacs][] has a nice [guide][] to using the Emacs package manager.
With that as your guide, find and install the [elscreen package][] from [MELPA][].

Start ElScreen in your init file.

```elisp
(elscreen-start)
```

Now the elscreen commands are available throughout your Emacs session.

## Use It

[ElScreen Usage]: https://github.com/knu/elscreen#usage

[ElScreen Usage][] shows *many* commands for ElScreen.
I manage with just a few.

| Function            | Keys       | Description
| ------------------- | ---------- | -----------
| `elscreen-create`   | `Ctrl+z c` | Create a new screen and switch to it.
| `elscreen-next`     | `Ctrl+z n` | Cycle to the next screen
| `elscreen-previous` | `Ctrl+z p` | Cycle to the previous screen
| `elscreen-kill`     | `Ctrl+z k` | Kill the current screen
| `elscreen-help`     | `Ctrl+z ?` | Show ElScreen key bindings

I know.
A tutorial or something would be nice.
But every time I start to write a tutorial for something,
I think of one more detail that hasn't been covered and the cycle starts all over again on the new detail.
Just needed *something* here so I could shut my brain up about "why don't you mention ElScreen?"