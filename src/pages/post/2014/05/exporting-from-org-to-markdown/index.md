---
aliases:
- /emacs/2014/05/16_exporting-from-org-to-markdown.html
- /post/2014/exporting-from-org-to-markdown/
- /2014/05/16/exporting-from-org-to-markdown/
category: tools
date: 2014-05-16 00:00:00
layout: layout:PublishedArticle
slug: exporting-from-org-to-markdown
tags:
- emacs
- OrgMode
- markdown
title: Exporting From Org to Markdown
uuid: 1a44a1aa-27cc-4099-832d-d25d7e4717ea
---

<aside class="admonition tldr">
<p class="admonition-title">tl;dr</p>

`C-h v org-export-backends` to ensure that Markdown export is available.
`C-c C-e m m` invokes `org-md-export-to-markdown`. You may need to
update Org Mode, which could be a fussy process.

</aside>

Let’s say that I am supposed to be writing a blog post. Not this one,
another one. I have spent a lot of time learning about [Org
mode](http://orgmode.org), and I’m not ready to leave it just yet.
There’s a problem, though. The blog that I’m supposed to be
contributing to looks a bit like [Jekyll](http://jekyllrb.com).
Specifically, it uses
[Markdown](http://daringfireball.net/projects/markdown) formatting.
That’s nice, but I *really* like Org mode formatting this week.

No problem!

According to the [Org Markdown export
page](http://orgmode.org/manual/Markdown-export.html), `C-c C-e` opens an
Export view. `m m` then triggers `(org-md-export-to-markdown)`, which
produces `post.md` from `post.org`.

Except that `C-c C-e m m` just exported the post to a [FreeMind mind
map](http://freemind.sourceforge.net/wiki/index.php/Main_Page). Cool,
but not Markdown. `org-md-export-to-markdown` isn’t even available.

Problem.

Apparently I have `org-mode` 7.9.3f installed. The documentation on the
Org Mode site is for the newest version: 8.2.6. How do I get the new
version? The [installation
instructions](http://orgmode.org/manual/Installation.html) suggest it
can be done with `package-install` before you’ve loaded any org files.

    package-install RET org

And now I have 8.2.6.

No problem. Except now I’m getting an error with `C-c C-e m`. Oh, I see
the problem. There are only a few [export
backends](http://orgmode.org/manual/Export-back_002dends.html#Export-back_002dends)
enabled by default.

- ascii
- html
- icalendar
- latex

I need to set `org-export-backends`. The documentation specifies that I
should use the Emacs customization interface. All righty.

    C-h v org-export-backends

I end up with this in my `.init.el`

```elisp
(custom-set-variables
 ;; custom-set-variables was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 '(org-export-backends (quote (ascii html icalendar latex md))))
```

The export interface is better, but now I get a **different** error.

    org-refresh-category-properties: Invalid function: org-with-silent-modifications

This [Markdown Export on
Aquamacs](http://www.benjaminmgross.com/markdown-export-on-aquamacs/)
post by Benjamin M. Gross was particularly helpful. He suggests you use
the package manager to remove and reinstall the `org` package.

So I did. There was a confusing moment where the package manager didn’t
seem to realize that a Org Mode was installed. Just turns out that a
newer version was available. I installed the newer version and restarted
emacs.

Trying `C-c C-e m m` one more time before I give up for now.

``` md
# Exporting From Org to Markdown

Let's say that I am supposed to be writing a blog post. Not this
one, another one. I have spent a lot of time learning about
[Org mode](http://orgmode.org), and I'm not ready to leave it just yet.
There's a problem, though. The blog that I'm supposed to be contributing
to looks a bit like [Jekyll](http://jekyllrb.com/). Specifically, it uses
[Markdown](http://daringfireball.net/projects/markdown/)
formatting. That's nice, but I *really* like `org-mode` formatting
this week.
```

See? No problem!

Now I just need to *write* the post. Not this one. The other one.