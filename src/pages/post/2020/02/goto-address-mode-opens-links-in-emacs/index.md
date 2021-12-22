---
aliases:
- /2020/02/04/goto-address-mode-opens-links-in-emacs/
category: tools
cover_image: cover.png
date: 2020-02-04 23:27:00
description: Use `goto-address-mode` to make links in Emacs buffers clickable
draft: false
layout: layout:PublishedArticle
slug: goto-address-mode-opens-links-in-emacs
tags:
- emacs
title: Goto Address Mode Opens Links in Emacs
uuid: a032ec14-dceb-45f2-9f7e-a42a1bcba306
---

Org mode has this nice thing where you can click a link in the buffer to
open it in your browser. Turns out that’s not some special org-only
behavior. It’s
[goto-address-mode](https://www.gnu.org/software/emacs/manual/html_node/emacs/Goto-Address-mode.html),
a minor mode that activates URLs and email addresses in the current
buffer.

You can manually launch it with `M-x goto-address-mode`. It might be
easier to automatically enable it for certain modes. You do that with a
[hook](https://www.gnu.org/software/emacs/manual/html_node/emacs/Hooks.html).

I want links to be available when reviewing notes and blog posts. Since
I write those notes in a number of formats, I should add the hook one of
the general [major
modes](https://www.gnu.org/software/emacs/manual/html_node/elisp/Basic-Major-Modes.html#Basic-Major-Modes).
text-mode is a good start.

``` lisp
;; base mode for prose
(add-hook 'text-mode-hook (lambda ()
                           (goto-address-mode)))
```

Now I can open links from my Markdown and [RST](/tags/rst) files with a
click! Or a `C-c <RET>`.

**`goto-address-mode` key bindings**

| Key         | Function                | Action                     |
| ----------- | ----------------------- | -------------------------- |
| `C-c <RET>` | `goto-address-at-point` | Opens the link under point |

I might add the hook for prog-mode later, if I find myself wanting to
click URLs in source code.