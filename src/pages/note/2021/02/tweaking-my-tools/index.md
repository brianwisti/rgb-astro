---
date: 2021-02-16 22:40:03.058286
layout: layout:PublishedArticle
slug: tweaking-my-tools
tags:
- ruby
- site
title: Tweaking my tools
uuid: d89a79ca-bdee-43ec-8da9-b439f13d1ab1
---

[TTY Toolkit]: https://ttytoolkit.org

Playing a little more with [TTY Toolkit][] for the site workflow.
I wanted to say I'm tightening focus, but with a `require` list like this for one tool?

```ruby
require 'pastel'
require 'ruby-slugify'
require 'tty-editor'
require 'tty-exit'
require 'tty-logger'
require 'tty-option'
require 'tty-prompt'
require 'tty-screen'
```

"Tightening focus" would be a lie.

Anyways, it seems to function correctly. Huzzah! Now back to work.