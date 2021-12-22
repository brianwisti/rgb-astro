---
aliases:
- /2019/09/08/colorized-my-go-output-with-grc/
category: Tools
cover_image: cover.png
date: 2019-09-08
description: In which I spent Sunday having fun learning stuff
format: md
layout: layout:PublishedArticle
slug: colorized-my-go-output-with-grc
tags:
- go
- shell
title: Colorized my go output with grc
uuid: 9cff48b0-9ca3-416b-a52d-a1c2f377d21e
---

Enjoying myself as I go through [Learn Go with Tests][go-with-tests] by [Chris
James][chris-james].

I didn’t enjoy myself on the [official tour][official-tour], or with whatever
LinkedIn course it was that I took. The structure and flow of the
learn-by-testing piece gives me a familiar context and the pace seems just
about right. It’s giving me ideas where I might enjoy Go for my own projects.

So yeah I like it.

Still having some *tiny* issues with the output of ``go test``.

#[normal `go test` output](plain.png)

Part of it’s that my brain hasn’t gotten used to how Go displays its errors.
Some of it’s that my brain always has — and always will — panic at random
symbols without context.

I figured I wasn’t the first with this problem, so I went looking. Found a
[Stack Overflow answer][stackoverflow] pointing me to [grc][]. Installed via
[Homebrew][homebrew], then followed directions from Stack Overflow to configure
grc, with a slight tweak to `~/.grc/conf.gotest`.

grc needs an entry in `~/.grc/grc.conf` for Go test runs.

``` text
 # Go
 \bgo.* test\b
 conf.gotest
```

I did make a slight tweak to the suggested `~/.grc/conf.gotest`, so that
"panic" lines get highlighted as failures.

``` text
regexp==== RUN .*
colour=blue
-
regexp=--- PASS: .*
colour=green
-
regexp=^PASS$
colour=green
-
regexp=^(ok|\?) .*
colour=magenta
-
regexp=^\s*panic: .*
colour=red
-
regexp=--- FAIL: .*
colour=red
-
regexp=[^\s]+\.go(:\d+)?
colour=cyan
```

Now when I run tests through `grc go test`, output is colorized and I can
track it more easily!

#[colorized by `grc go test`](cover.png)

Of course I’ll probably get used to how Go presents errors and then forget all
about `grc`, but it’s great for today. Might be more generally useful too, if
I want colorized output that my tools don’t already provide!

[go-with-tests]: https://github.com/quii/learn-go-with-tests
[chris-james]: https://quii.dev/
[official-tour]: https://tour.golang.org/welcome/1
[stackoverflow]: https://stackoverflow.com/a/40160711
[grc]: https://github.com/garabik/grc
[homebrew]: https://brew.sh/