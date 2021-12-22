---
aliases:
- /note/2020/59/emacs-refresh-package-contents/
date: 2020-02-28 15:23:53
layout: layout:PublishedArticle
slug: emacs-refresh-package-contents
tags:
- emacs
- packages
title: Emacs refresh-package-contents
updated: 2020-04-29T08:52:12-0700
uuid: 2050b0b7-f074-4233-ab88-83a3f6a4cce7
---

Tried adding [Evil](https://www.emacswiki.org/emacs/Evil) with
[use-package](/post/2019/11/emacs-use-package). Didn’t work.

Didn’t write the error message down, of course. Something about MELPA
looking for a package version from two months ago and deciding the
package was "Not Found".

Eventually figured out I need to run `package-refresh-contents`, which
grabs the latest package listings. Might be overkill to run that
automatically in every Emacs session, so I won’t add it to my `.emacs`.

I will add a comment though.

``` elisp
;; Package not installing?
;;  Try 'M-x package-refresh-contents'

(require 'package)
```

Hopefully I remember to read my own comments.

Or the
[documentation](https://evil.readthedocs.io/en/latest/overview.html#installation-via-package-el).

[john sj anderson]: https://genehack.org

<div class="admonition">
<p class="admonition-title">Update</p>

2020-04-29
:  [john sj anderson][] wrote a post
  [expanding](https://genehack.blog/2020/04/a-bit-of-emacs-advice/) on
  a [suggestion](https://mastodon.social/@genehack/103737652356761968)
  to use [advising
  functions](https://www.gnu.org/software/emacs/manual/html_node/elisp/Advising-Functions.html).
  
  </div>