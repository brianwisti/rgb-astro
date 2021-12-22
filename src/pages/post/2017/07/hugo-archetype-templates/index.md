---
aliases:
- /post/2017/hugo-archetype-templates/
- /2017/07/01/hugo-archetype-templates/
category: tools
cover_image: cover.png
date: 2017-07-01
draft: false
layout: layout:PublishedArticle
slug: hugo-archetype-templates
tags:
- hugo
- site
- bash
title: Hugo Archetype Templates
uuid: 88777d98-385e-4584-bec6-bfad1d9179f5
---

I try out archetype templates from the Hugo static site generator, smoothing the
whole thing into my workflow with a bash script.

## Hugo Archetypes

[Hugo archetypes]: http://gohugo.io/content/archetypes/
[section]: http://gohugo.io/content/archetypes/#section-archetypes

[Hugo archetypes][] are templates that Hugo uses when you tell it to create new
content. Hugo allows both default archetypes and [section archetypes][] for
content that belongs in a particular section (such as Posts or Crafts).

[v0.24]: https://github.com/gohugoio/hugo/releases/tag/v0.24
[variables]: http://gohugo.io/templates/variables/
[functions]: http://gohugo.io/templates/functions/

As of release [v0.24][], archetypes are full templates. You can use
[variables][] and [functions][]  to fine-tune details of your archetype. This
gives me a chance to simplify my content creation workflow.

### My Default Archetype Template

[front matter]: http://gohugo.io/content/front-matter/

My archetype focuses on [front matter][]. Since the site sections share taxonomy
rules, I use a single default archetype.

**`archetypes/default.md`**

```markdown
---
title: "{{ replace .TranslationBaseName "-" " " | title }}"
date: {{ dateFormat "2006-01-02" .Date }}
year: "{{ dateFormat "2006" .Date }}"
draft: true
tags:
-
categories:
-
---
tl;dr
<!-- more -->
```

### Notes

* Hugo provides `title` and `date` if you leave them out. My `title` looks the
  same as the default, but I add it to the template to remember what
  transformations are being done.
* I prefer a specific format for date in my front matter, so I add my own
  version.
* I use a `year` taxonomy for archives.
* Everything is a `draft` until I specify otherwise.
* All my content should be tagged and categorized.
* I try to summarize the post in an initial paragraph that gets shown in list
  views.
* That last line is really <code>&#60;&#33;&#45;&#45;more&#45;&#45;&#62;</code>
  with no spaces, but if I skip the spaces here Hugo thinks I want another
  summary block in this post.

[YAML]: http://yaml.org/
[config]: http://gohugo.io/overview/configuration/

That's good enough for `hugo new`. Since I have `newContentEditor` set to "vim"
in my [config][], Hugo opens the new file in my editor after creating it.

    $ hugo new post/2017/23-things-i-hate-about-lists.md

My workflow is a little more complicated than "create a draft and edit it"
though.

## My Workflow

I create and edit site content in its own git branch. With multiple drafts going
at any one time, using separate branches lets me focus on the current content.

I follow these steps every time I add a new post.

1. Create a branch
2. Add a draft content file
3. Start editing the draft file!

[AWS S3]: https://aws.amazon.com/s3/

I can ignore the publishing part of the workflow for today, which involves
running some tests and pushing to [AWS S3][]. That deserves its own post.

[Bash]: https://www.gnu.org/software/bash/

I originally automated this with a small Ruby script which would create the
branch and generate a content file for me. The file generating code is not
needed now that Hugo archetypes are templates. My small, slightly clunky Ruby
script can be replaced with a smaller, hopefully less clunky [Bash][] script.

**`scripts/add`**

```bash
#!/usr/bin/env bash

# stricter bash
#  see http://redsymbol.net/articles/unofficial-bash-strict-mode/
set -euo pipefail
IFS=$'\n\t'

SECTION=${1:-}
TITLE=${2:-}

if [[ -z "$SECTION" || -z "$TITLE" ]]; then
  echo "Usage: $0 SECTION TITLE"
  exit 1
fi

TITLE_SLUG="$(echo -n "$TITLE" | sed -e 's/[^[:alnum:]]/-/g' | tr -s '-' | tr A-Z a-z)"
YEAR="$(date +"%Y")"
STUB="$SECTION/$YEAR/$TITLE_SLUG"

git checkout -b "$STUB"
hugo new "$STUB.md"
# newContentEditor set in Hugo config, expect Vim here.
```

### Notes

[unofficial strict mode]: http://redsymbol.net/articles/unofficial-bash-strict-mode/
[The Imposter's Handbook]: https://bigmachine.io/products/the-imposters-handbook/
[`date`]: https://www.gnu.org/software/coreutils/manual/html_node/date-invocation.html#date-invocation
[GNU Coreutils]: https://www.gnu.org/software/coreutils/manual/html_node/index.html#Top

Applying details like [unofficial strict mode][] is part my process for
getting more comfortable scripting Bash. The bit that's important to me: this
script fails loudly on encountering bad variables and bad processes.

The fun little slug-generating `sed` and `tr` pipe came directly from [The
Imposter's Handbook][]. I know that I will lose punctuation and unusual
capitalization between this and Hugo's manipulation of `.TranslationBaseName`.
It encourages me to keep titles simple. The title can edited in the front
matter later if it is that important to me.

[`date`][] comes from [GNU Coreutils][]. I knew I could use `date` to get a
simple description of the date. I recently discovered that it also accepts a
format string! Turns out that GNU Coreutils gives the shell quite a bit of
functionality that I usually ran to some programming language and its
libraries for. Being self-taught produces weird gaps in my knowledge.


    $ ./script/add post "23 Things I Hate About Lists"
    Switched to a new branch 'post/2017/23-things-i-hate-about-lists'
    /home/brian/Sites/rgb-hugo/content/post/2017/23-things-i-hate-about-lists.md created

Excuse me while I go write my masterpiece. Have fun!