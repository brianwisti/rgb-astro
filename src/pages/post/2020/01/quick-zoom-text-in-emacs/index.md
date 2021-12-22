---
aliases:
- /2020/01/01/quick-zoom-text-in-emacs/
category: Tools
cover_image: cover.png
date: 2020-01-01
draft: false
layout: layout:PublishedArticle
slug: quick-zoom-text-in-emacs
tags:
- emacs
title: Quick Zoom Text in Emacs
uuid: bb7362ba-5086-4f46-8f10-c9053a5d0ec9
---

<aside class="admonition tldr">
  <p class="admonition-title">.tl;dr</p>

Use `C-x C-=`, `C-x C--`, and `C-x C-0` to scale text on the fly in your
Emacs buffer.

</aside>

Hey, happy new year!

Okay quick scenario: you are at your desk working through some problem
in Emacs. This problem is a little tricky, so you call your friend or
coworker for advice. They take one look at your screen. They immediately
walk away, eyelids twitching. Their old eyes cannot cope with your eight
point font on a 4k screen.

If only you could have prevented this tragedy.

You could have, with `text-scale-adjust`\! This built-in function
adjusts font size in your current buffer by whatever you have
`text-scale-mode-step` set to.

**Emacs text scale adjustment key bindings**

| Function                 | Keys                   | Description                    |
| ------------------------ | ---------------------- | ------------------------------ |
| `(text-scale-adjust 1)`  | `C-x C-=` or `C-x C-+` | Increase text size by one step |
| `(text-scale-adjust -1)` | `C-x C--`              | Decrease text-size by one step |
| `(text-scale-adjust 0)`  | `C-x C-0`              | Reset text size to default     |

On my system, `text-scale-mode-step` is 1.2. I set default height of
`fixed-pitch` fonts to 120, or 12 points. Increasing the scale by one
step makes the default height for that buffer 144 — 14 point, more or
less. Again? 172. Again? 207.

You get the point.

`text-scale-adjust` leaves your other buffers and frame fonts alone.
Maybe you prefer adjusting everything at once. I will not judge. Try the
[default-text-scale](https://github.com/purcell/default-text-scale)
package if you want to adjust global font sizes.

Call your friend back over to help on that code problem. Their eyes have
probably stopped twitching by now.

And when they go you can get your eight point font back with `C-x C-0`.