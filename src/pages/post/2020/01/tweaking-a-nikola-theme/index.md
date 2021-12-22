---
aliases:
- /2020/01/25/tweaking-a-nikola-theme/
caption: The [/now](/now) page, in Nikola
category: tools
cover_image: cover.png
date: 2020-01-25 20:00:00
draft: false
layout: layout:PublishedArticle
slug: tweaking-a-nikola-theme
tags:
- nikola
- site
title: Tweaking a Nikola Theme
uuid: 1696d39a-5968-44bb-85d9-f8f545631c85
---

I adjusted the default [Nikola](https://getnikola.com) theme to show
cover images!

## Motivation

I am a visual person. You might not know that from all the typing and my
enthusiasm for command line tools. But many of my posts and pages have
cover images. Sometimes the cover images are even relevant to the post.

In the live site, cover images are prominently displayed at the top of
their pages. They get referenced when a post gets shared on social
media. A cropped and adjusted version of the cover image gets displayed
in post summaries.

So if I’m using [Nikola](https://getnikola.com) to build something like
my current site, I need cover images.

Nikola site uses the
[bootblog4](https://themes.getnikola.com/v8/bootblog4/) theme by
default, taking advantage of the [Bootstrap](https://getbootstrap.com/)
toolkit. bootblog4 doesn’t support cover images, so I’ll make a version
that does.

Mind you, I don’t want to build a whole new theme. That can come later.
There’s even a nice tutorial for [creating a
theme](https://getnikola.com/creating-a-theme.html). For now I just want
to tweak the default a little.

## Set up files and metadata

Nikola starts with a few assumptions I can work with. bootblog4 already
looks for `previewimage`
[metadata](https://getnikola.com/handbook.html#metadata-fields) to build
thumbnails for [featured
posts](https://getnikola.com/handbook.html#featured-posts). Nikola also
expects to find image files in your site’s `images/` folder. Makes
sense.

I’ll mirror the content path with images, and add `previewimage`
metadata which points to the right spot.

**`posts/2019/12/again-with-the-manual-symmetry/index.md`**

```yaml
---
date: 2019-12-15 12:37:51-08:00
tags:
- drawing
- Procreate
- symmetry
title: Again with the manual symmetry
category: note
previewimage: /images/2019/12/again-with-the-manual-symmetry/cover.jpg
---
```

<aside class="admonition">

I like how [Hugo](https://gohugo.io/) handles [page
bundles](https://gohugo.io/content-management/page-bundles/). Everything
for your content is in the same folder. Many other static site
generators — including Nikola — keep supplemental content separate from
posts.

</aside>

Hugo uses a powerful but sometimes confusing
[taxonomy](https://gohugo.io/content-management/taxonomies/) system in
layout customization. Nikola prefers a powerful but sometimes confusing
"theme inheritance" system. Look. They’re all confusing. It’s just a
matter of finding the kind of confusing you don’t mind.

With theme inheritance, my tweaks *are* a new theme. But the new theme
basically says "I’m like that theme, except that I changed these
templates."

So let’s inherit a theme.

## Nikola’s `theme` command

| Option                        | Description                                                                                       |
| ----------------------------- | ------------------------------------------------------------------------------------------------- |
| `-i ARG, --install=ARG`       | Install a theme. (config: install)                                                                |
| `-r ARG, --uninstall=ARG`     | Uninstall a theme.  (config: uninstall)                                                           |
| `-l, --list`                  | Show list of available themes. (config: list)                                                     |
| `--list-installed`            | List the installed themes with their location. (config: list_installed)                           |
| `-u ARG, --url=ARG`           | URL for the theme repository (default: https://themes.getnikola.com/v8/themes.json) (config: url) |
| `-g ARG, --get-path=ARG`      | Print the path for installed theme (config: getpath)                                              |
| `-c ARG, --copy-template=ARG` | Copy a built-in template into templates/ or your theme (config: copy-template)                    |
| `-n ARG, --new=ARG`           | Create a new theme (config: new)                                                                  |
| `--engine=ARG`                | Engine to use for new theme (mako or jinja -- default: mako) (config: new_engine)                 |
| `--parent=ARG`                | Parent to use for new theme (default: base) (config: new_parent)                                  |
| `--legacy-meta`               | Create legacy meta files for new theme (config: new_legacy_meta)                                  |

So I ask Nikola for a new theme, using bootblog4 as the parent.

    $ nikola theme --new rgb-bootblog4 --parent bootblog4
    ...
    [2020-01-21T15:35:33Z] NOTICE: theme: Remember to set THEME="rgb-bootblog4" in conf.py to use this theme.

Because I didn’t specify a template engine, rgb-bootblog4 uses
[Mako](https://www.makotemplates.org/).

Let’s remember to update `conf.py` as directed, so we can *see* the
theme as we tweak it. The [theme
tutorial](https://getnikola.com/creating-a-theme.html) also mentions
disabling `USE_BUNDLES` during theme development. I thought they meant
page bundles for a second and got excited, until I realized
[bundles](https://getnikola.com/creating-a-theme.html#bundles) meant
bundled JavaScript and CSS for quicker HTTP/1 downloads.

``` python
# Name of the theme to use.
THEME = "rgb-bootblog4"
USE_BUNDLES = False
```

Sweet. I have a new `themes/rgb-bootblog4` folder. Wait. It has no
templates.

Oh that’s right. This is what they were talking about with *template
inheritance*. The templates are still in the parent. It’s up to me to
copy and change specific templates. That’s both good and a little risky
when the parent theme updates. What if my tweak turns out to be
incompatible? Okay, not going to worry about it today. If you’re going
to veer wildly from the parent, you should probably use
[base](https://themes.getnikola.com/v8/base/) as the parent.

## Editing templates

<aside class="admonition note">
  <p class="admonition-title">Note</p>

The [Mako
extension](https://marketplace.visualstudio.com/items?itemName=tommorris.mako)
for [Visual Studio Code](https://code.visualstudio.com/) associates
itself with `.mako` files. You can add `.tmpl` to that with the
`files.associations`
[setting](https://code.visualstudio.com/docs/getstarted/settings). Might
not want to do that globally though. `.tmpl` could be Mako here, but
[Jinja2](https://jinja.palletsprojects.com/) in another site.

Instead, change it in the workspace file for your Nikola site.

``` json
{
  "folders": [
    {
      "path": "."
    }
  ],
  "settings": {
    "files.associations": {
      "*.tmpl": "mako"
    }
  }
}
```

</aside>

So which of the [built-in
templates](https://getnikola.com/theming.html#built-in-templates) do I
want? Since both posts and pages have cover images on my site, I’ll
start with the most general template. Everything starts with
`base.tmpl`. Let’s look there.

    $ nikola theme -c base.tmpl

Can I find anything interesting in the base template?

```
${template_hooks['page_header']()}
<%block name="extra_header"></%block>
<%block name="content"></%block>
```

Over here on the live site, I put cover images above the main content.
`extra_header` looks promising. Where to set it? I prefer to make my
changes in the most relevant template instead of the most general.

Give me a minute to explore…

Okay. Pages ultimately inherit from posts — Mako supports [template
inheritance](https://docs.makotemplates.org/en/latest/inheritance.html),
letting the parent define some blocks while overriding others. We might
be able to do this with one change.

    $ nikola theme -c post.tmpl

Nikola provides a large number of [template
variables](https://getnikola.com/template-variables.html) to work with,
but today I focus on `post`. How about the preview image? It gets set in
post metadata, so I *could* use `post.meta("previewimage")`. Don’t have
to do that though. `previewimage` metadata is important enough that it
gets promoted to an attribute of the [post
object](https://getnikola.com/template-variables.html#post-object-attributes).

**`post.tmpl`**

```
<%block name="extra_header">
  % if post.previewimage:
      <div class="figure">
          <img src="${post.previewimage}" alt="${post.title}" width="1000">
          <p class="caption">${post.title()}</p>
      </figure>
  % endif
</%block>
```

Keep in mind what I noticed the other day about these [not being real
figures](/post/2020/01/restructuredtext-basics-for-blogging/#images-and-figures)
in reStructuredText. For now I match RST output, as if I’d used a
[figure
directive](https://docutils.sourceforge.io/docs/ref/rst/directives.html#figure).
That way I don’t have to find the CSS for this theme.

![screenshot showing cover image in post](cover-in-post.png "Cover image in post")

It has a cover image, placed right by the title. It doesn’t *quite*
match today’s view of [that
post](/note/2019/12/again-with-the-manual-symmetry/), but this has the
basic idea. And I only had to edit a single template file\!

![screenshot of same page with different style](post-hugo-comparison.png "The same page on the current site")

Looks good for posts that have a cover image. How about pages?

![screenshot of /now page with nikola style](cover-in-page.png "Cover image in a non-post page")

Excellent. I thought that would take much more work.

## Remember Bootstrap?

bootblog4 *is* based off of Bootstrap. I feel compelled to make the
cover image a
[Jumbotron](https://getbootstrap.com/docs/4.4/components/jumbotron/).

```
<%block name="extra_header">
  % if post.previewimage:
      <div class="figure jumbotron">
          <img src="${post.previewimage}" alt="${post.title}" width=1000>
          <p class="caption">${post.title()}</p>
      </div>
  % endif
</%block>
```

![screenshot with large jumbotron element](post-previewimage-jumbotron.png "Cover image in Bootstrap Jumbotron")

Hm. Maybe, maybe not. I’m tempted to tweak it some more, but my task
list is long and my time is short.

## Did I miss anything?

Sort of. On the live site, I let Hugo resize cover images to fit in my
design and avoid large downloads. Nikola has thumbnails, but that’s not
quite the same thing. I’d have to do it myself, maybe with a
[plugin](https://getnikola.com/handbook.html#custom-plugins).
