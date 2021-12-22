---
caption: the formatted output of my journal-reading one-liner
category: tools
cover_image: cover.png
date: 2021-05-21
description: I sure do use a lot of words to justify my one-liners
draft: false
format: md
layout: layout:PublishedArticle
series:
- Journaling in Joplin With Raku
slug: cli-journaling-in-joplin-with-raku
tags:
- shell
- joplin
- Raku Lang
- second brain
title: CLI Journaling in Joplin with Raku
uuid: 5ea23b58-22c2-43d0-ac4a-e5d03a7edbc0
---

Let's write a couple one-liners so I can journal in [Joplin][joplin] from the command
line!

## But why?

Journaling is great.  Now I'm not talking about big name [Bujo][bujo] bullet
journaling process.  I mean getting a thought down quick before I lose it.
Even better if I can get that thought down in a place where I can find it
later.

I know there are loads of great journaling applications.  And lots of great
applications that support journaling generally.  But I love my command line.
Too many distractions in those apps.

Command line options exist.  I could use one of the bazillion command line
journaling tools.  Okay.  Maybe not a bazillion.  A couple dozen, at least.

Those apps and tools are yet another interface, another set of rules.  I
already have Joplin handy.  Besides desktop, mobile, and terminal applications,
Joplin has a CLI.  And an API, but I suspect I'll get to that later.

With uncharacteristic restraint, today I choose to get better at the tools I
have rather than installing a new one.

## Adding a journal entry

```bash
joplin use Journal && joplin edit $(date --iso=minute)
```

[GNU Date][gnu-date] — from GNU Coreutils — gets us consistent timestamps,
which simplify searching and filtering.  `--iso` produces an [ISO
8601][iso-8601] timestamp.  Very handy.  By default it prints the `YYYY-MM-DD`
version of today's date, but you can opt for more granularity.

    $ date --iso=minute
    2021-05-20T08:26-07:00

I plan to make frequent small notes, so `minute` feels like a good choice.

:::admonition

**`use Journal`?**

Yes, this came up.  Had the Joplin terminal app open in one terminal while I
added a journal entry in another terminal.  Terminal app did some sort of
state maintenance thing.  Next thing I know I'm adding journal entries to
"Nerd Notes."

:::

Since it doesn't exist, `joplin` will ask for confirmation before creating
it.

    $ joplin use Journal && joplin edit $(date --iso=minute)
    Note does not exist: "2021-05-20T08:26-07:00". Create it? (Y/n)

I'm okay with the confirmation request for now.
That way I have fewer moments of accidentally creating entries.

#[Editing a journal entry](editing-note.png)

### What about more of a diary?

Leave `minute` off the `--iso` argument if you prefer a tidy collection of
daily pages to my big stack of notes.

``` bash
joplin edit $(date --iso)
```

Now you'll be editing the single entry for today's date.

## Reading journal entries

The best review path will be via the Joplin app itself.  That way you can tag
and edit.

*But* – if you just want a quick view of recent thoughts?  That is something we
can do from the command line.

This next bit gets a little fancy.

``` bash
joplin use Journal \
  && raku -e '
    for qx{ joplin ls }.lines.sort {
      qqx{ joplin cat $_ }.subst(
        /^(<[\dT:\-]>+)/, { "# $0" }
      ).say
    }' \
  | python -m rich.markdown -
```

Let me stall for a second.

### Pretty print with Rich

We already talked about `joplin use Journal`. [Rich Markdown][rich-md] formats
Markdown — Joplin's default format — for rich display in a terminal.  It can
even run as a standalone application.  I take advantage of that here to get a
pretty view of my Joplin entries:

<pre class="rich">╔══════════════════════════════════════════════════════════════════════════════╗
║                            <span style="font-weight: bold">2021-05-20T08:26-07:00</span>                            ║
╚══════════════════════════════════════════════════════════════════════════════╝


Getting an idea for a CLI journaling tool using Joplin as the backend

The logic would look something like this:

<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">┌──────────────────────────────────────────────────────────────────────────────┐</span>
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span> <span style="color: #f8f8f2; text-decoration-color: #f8f8f2; background-color: #272822">joplin use Journal</span><span style="background-color: #272822">                                                          </span> <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span> <span style="color: #f8f8f2; text-decoration-color: #f8f8f2; background-color: #272822">joplin edit </span><span style="color: #66d9ef; text-decoration-color: #66d9ef; background-color: #272822">$(</span><span style="color: #f8f8f2; text-decoration-color: #f8f8f2; background-color: #272822">date --iso</span><span style="color: #66d9ef; text-decoration-color: #66d9ef; background-color: #272822">)</span><span style="background-color: #272822">                                                   </span> <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span> <span style="color: #75715e; text-decoration-color: #75715e; background-color: #272822"># append "## $(date --iso=minute)"</span><span style="background-color: #272822">                                          </span> <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">└──────────────────────────────────────────────────────────────────────────────┘</span>

That's it, basically. There could be more functionality, such as reviewing the
log.

╔══════════════════════════════════════════════════════════════════════════════╗
║                            <span style="font-weight: bold">2021-05-21T09:00-07:00</span>                            ║
╚══════════════════════════════════════════════════════════════════════════════╝

Alarm 07:00, stayed in bed as long as I could. Thanks to the dogs, that was 15
minutes. Oh well.

Got the Raspberry Pi 4 set up with Raspbian, and the 500GB external drive
attached. Thinking about package managers. I know <span style="color: #0000ff; text-decoration-color: #0000ff"><a href="https://brew.sh">Homebrew</a></span> but I could maybe try
<span style="color: #0000ff; text-decoration-color: #0000ff"><a href="https://nixos.org/">Nix</a></span>. There's a post about <span style="color: #0000ff; text-decoration-color: #0000ff"><a href="https://ariya.io/2020/05/nix-package-manager-on-ubuntu-or-debian">using Nix on Debian</a></span>.

╔══════════════════════════════════════════════════════════════════════════════╗
║                          <span style="font-weight: bold">2021-05-21T14:01:00-07:00</span>                           ║
╚══════════════════════════════════════════════════════════════════════════════╝

Resuming productivity, or something like it.

╔══════════════════════════════════════════════════════════════════════════════╗
║                          <span style="font-weight: bold">2021-05-21T20:20:00-07:00</span>                           ║
╚══════════════════════════════════════════════════════════════════════════════╝

I keep forgetting <span style="color: #ffffff; text-decoration-color: #ffffff; background-color: #000000">-sel clip</span> when using xclip. Without that it doesn't go into
the easy copy buffer.

<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">┌──────────────────────────────────────────────────────────────────────────────┐</span>
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span> <span style="color: #f92672; text-decoration-color: #f92672; background-color: #272822; font-weight: bold">$ </span><span style="color: #f8f8f2; text-decoration-color: #f8f8f2; background-color: #272822">my-command | xclip -sel clip</span><span style="background-color: #272822">                                              </span> <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">└──────────────────────────────────────────────────────────────────────────────┘</span>
</pre>

You can also use [Glow][glow] if you want a standalone Markdown pretty printer.
It works.  Rich is already part of my toolkit, so I'll keep using it.

### Am I ready to explain myself?

Okay, I think I've stalled enough.  That middle bit.  That's [Raku][raku].

```
for qx{ joplin ls }.lines.sort {
  qqx{ joplin cat $_ }.subst(
    /^(<[\dT:\-]>+)/,
    { "# $0" }
  ).say
}
```

I don't often do one-liners. We'll have to break it down into tiny pieces.

First, we need a sorted list of journal entries.

```
qx{ joplin ls }  # ask `joplin` to print note titles, saving the output
  .lines         # Split that output into lines, one per note
  .sort          # Sort those lines by note title
```

Things get unpredictable if I don't sort notes myself.  Joplin tends to sort
notes by last activity.  Thank goodness for ISO 8601, which is easily sorted:

    2021-05-20T08:26-07:00
    2021-05-21T09:00-07:00
    2021-05-21T14:01-07:00
    2021-05-21T20:20-07:00

Next, we need to do something with each of those note titles.

```
for qx{ joplin ls }.lines.sort { ... }
```

Well? The content of each note is important.

```
qqx{ joplin cat $_ }
```

`qqx` interpolates variables before asking the system to run your command.
The variable being interpolated is our old friend `$_`, this time around
standing in for whichever of those sorted lines we reached.

```` markdown
2021-05-20T08:26-07:00

Getting an idea for a CLI journaling tool using Joplin as the backend

The logic would look something like this:

```bash
joplin use Journal
joplin edit $(date --iso)
# append "## $(date --iso=minute)"
```

That's it, basically. There could be more functionality, such as reviewing
the log.
````

I want to print this out in the terminal.  I need to massage it a little first.
Even though the file is Markdown, the first line is the note's unformatted
title.  It makes quick one-line notes easier.

But it also means if *I* want that first line to look significant, I need to do
something with this:

    2021-05-20T08:26-07:00

The most obvious fix to me? Turn it into a level one Markdown header.

```markdown
# 2021-05-20T08:26-07:00
```

[`subst`]]: https://docs.raku.org/routine/subst

That's a single [`.subst`][] transformation.

```
qqx{ joplin cat $_ }.subst(  # in printed note
  /^(<[\dT:\-]>+)/,          # find the first line that looks like a timestamp
  { "# $0" }                 # and turn it into a Markdown header
)
```

Okay, I got a little lazy with the regular expression.  But my brain was in
one-liner mode.  For a full script I'd probably spell it out more clearly.

The last step is to display the transformed note contents.

```
qqx{ joplin cat $_ }.subst(...).say
```

Or ask them to display themselves.  However you want to think of it.

This whole thing would be rather clunky as a shell alias.  I could add it as a
function to my `.bashrc`.

``` bash
jread() {
  joplin use Journal \
    && raku -e '
      qqx{joplin cat $_}.subst(/^(<[\dT:\-]>+)/, { "# $0" }).say for qx{ joplin ls }.lines.sort
    ' \
    | python -m rich.markdown -
}
```

Then again, maybe not.  This should probably be a script.  Check back in a few
days.

:::admonition

**Oooh a cliffhanger!**

I have a working script already.  What I don't have much of is unallocated
time.  But hopefully yes!  Soon.  I did some cool stuff with `multi MAIN`
in Raku that I'm desperate to show off.

:::

[joplin]: https://joplinapp.org
[bujo]: https://bulletjournal.com/
[iso-8601]: https://en.wikipedia.org/wiki/ISO_8601
[gnu-date]: https://www.gnu.org/software/coreutils/manual/html_node/date-invocation.html#date-invocation
[rich-md]: https://rich.readthedocs.io/en/stable/markdown.html
[glow]: https://github.com/charmbracelet/glow
[raku]: https://raku.org
