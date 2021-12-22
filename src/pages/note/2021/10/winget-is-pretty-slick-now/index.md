---
date: 2021-10-16
format: md
layout: layout:PublishedArticle
tags:
- windows
- package-manager
- respect-the-command-line
title: winget is pretty slick now
---

[looked]: /post/2020/06/winget/
[winget]: https://docs.microsoft.com/en-us/windows/package-manager/winget/

Just updated PowerShell via [winget][], Microsoft's command line package
manager. And Firefox. And Volta. And HeidiSQL. And Alacritty. And Go. And some
other stuff.

[markdown-it-py]: https://markdown-it-py.readthedocs.io/en/latest/index.html

Trying to recover a post about [markdown-it-py][] that I accidentally deleted,
so I won't sidetrack myself with a detailed follow-up on the last time I
really [looked][] at winget.

Instead, here's the <abbr title="Today I Learned">TIL</abbr>:

`winget upgrade`
: shows what's out of date

`winget upgrade --id=<package.id>`
: upgrades a package

`winget upgrade --all`
: upgrades everything.

No "Run As Administrator" needed, though you need to click the
<abbr title="User Access Control">UAC</abbr> dialog. Another caveat: it's
coming from the application's own download servers, not some Azure-backed
central repository. Sometimes the fetching may take a minute.