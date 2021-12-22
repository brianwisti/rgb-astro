---
aliases:
- /emacs/2014/10/21_blog-writing-in-org-mode.html
- /post/2014/blog-writing-in-org-mode.html
- /2014/10/21/blog-writing-in-org-mode/
category: tools
date: 2014-10-21
description: An experiment with using Org mode to write Jekyll blog posts.
layout: layout:PublishedArticle
slug: blog-writing-in-org-mode
tags:
- emacs
- OrgMode
- jekyll
title: Blog Writing in Org Mode
uuid: eab5b774-32a0-44d8-a62d-009143aa051d
---

## Introduction

Much of what I’ve read about [Org mode](http://orgmode.org) has focused
on its utility as a task management tool. That’s great. I wouldn’t mind
spending some time on that aspect. Mostly I’ve been focused on its
usefulness for note-taking and writing.

Org mode includes features which make it attractive for blogging and
journaling. It has a relatively simple set of markup rules for common
constructs such as paragraphs,
[lists](http://orgmode.org/manual/Plain-lists.html), [source
code](http://orgmode.org/manual/Working-With-Source-Code.html), and
[tables](http://orgmode.org/manual/Tables.html). The mode itself
provides an editing interface which simplifies creating and managing
those constructs. Most importantly for the blogger, org files can be
exported to a range of formats including Markdown and HTML.

Why not use that functionality for my own site? Random Geekery is built
with [Jekyll](http://jekyllrb.com), and there are already
[instructions](http://orgmode.org/worg/org-tutorials/org-jekyll.html)
available for using the two together. I can use those as a starting
point.

## Organize Directories

When I’m using Org mode to write the blog pages, Jekyll becomes an
implementation detail specific to publishing the blog. One folder
contains all of the Jekyll project files, and an `org` folder mirrors
the content-specific structure of the `jekyll` tree.

```
+jekyll
+- css
+- _data
+- _drafts
+- img
+- _includes
+- _layouts
+- pages
+- _plugins
+- _posts
+- _sass
+- _scripts
+- _site
+org
    +- _drafts
    +- _posts
    +- pages
```

I use `_drafts` because I don’t always know when I will be publishing a
post, and `pages` because I have legacy content that will get rewritten
in Org format as it gets updated.

## Front Matter

The [front matter](http://jekyllrb.com/docs/frontmatter/) used by Jekyll
and other engines to determine content metadata requires some special
handling to get exported correctly by Org mode. The most straightforward
thing is to use the suggestion from the instructions mentioned earlier.
Put your front matter in a HTML block right at the top of the file.

```
#+BEGIN_HTML
---
title: Blog Writing in Org Mode
layout: post
category: Emacs
tags: org jekyll
---
#+END_HTML
```

Okay, it’s not HTML. But Org mode doesn’t really care. It will get
passed through untouched when you export.

## Configure HTML Export

HTML and other output needs to be placed correctly within the Jekyll
layout conventions. A proper `org-publish-project-alist` will take care
of this.

``` elisp
(setq org-publish-project-alist
      '(
        ("org-randomgeekery"
         ;; Location of org files
         :base-directory "~/Projects/randomgeekery.org/org/"
         :base-extension "org"

         ;; Location of Jekyll files
         :publishing-directory "~/Projects/randomgeekery.org/jekyll/"
         :recursive t
         :publishing-function org-publish-org-to-html
         :headline-levels 4
         :html-extension "html"

         ;; Only export section between <body></body>
         :body-only t)

        ("org-static-randomgeekery"
         :base-directory "~/Projects/randomgeekery.org/org/"
         :base-extension "css\\|js\\|png\\|jpg\\|gif\\|pdf\\|mp3\\|ogg"
         :publishing-directory "~/Projects/randomgeekery.org/"
         :recursive t
         :publishing-function org-publish-attachment)

        ("rg" :components ("org-randomgeekery" "org-static-randomgeekery"))
        ))
```

Now when I export the project with `org-mode-export (C-c C-e X) rg`, all
of my org content for the project gets put in the correct spot. I even
get a table of contents, which is not such a bad thing.

## Publishing A Post

So when you’ve been editing a draft long enough and you’re ready to make
it a real live post, you need to move the file from `_drafts` to
`_posts`, with the publish date prefixing the filename.

I could do that manually, but it’s tedious to do that for every blog
post.

I experiment with my rudimentary Emacs Lisp skills to create a new
filename that looks about right.

``` elisp
(defun post-it ()
  "Write current draft file as a Jekyll post file"
  (interactive)
  (if
      (string-match "_drafts" buffer-file-name)
      (let ((draft-copy buffer-file-name)
            (post-copy
             ;; _drafts/<stub>.org
             ;; becomes
             ;; _posts/yyyy-mm-dd-<stub>.org
             (concat
              (replace-regexp-in-string "_drafts" "_posts"
                                        (file-name-directory buffer-file-name))
              (format-time-string "%Y-%m-%d")
              "-"
              (file-name-nondirectory buffer-file-name)
              )
             ))
        (write-file post-copy)
        )
    (message "%s is not in _drafts!" (file-name-nondirectory buffer-file-name))
      )
  )
```

Awkward, but it works. It worked at least once, anyways. Should manually
remove the original `_draft` file until I know what I’m doing a little
more.

<aside class="admonition warning">
<p class="admonition-title">Warning</p>

See that Lisp I wrote? It’s probably wrong in some horrible way. It’s
the most complex Elisp I’ve ever managed. Look at it for interesting
ideas, but please don’t just copy and paste.

</aside>

## Followup

I wonder if maybe this isn’t the best approach, since it seems to
confuse the heck out of Org mode. My lone org file just would not
republish until I found [this
post](http://lists.gnu.org/archive/html/emacs-orgmode/2009-05/msg00285.html)
for a similar situation. If it’s just not rebuilding, force it with a
numeric argument: <kbd>C-u 0 C-c e</kbd>.

This works well enough to get one post published, anyways. I’m sure to
revisit this topic as I continue to learn more about Org mode and Emacs.
