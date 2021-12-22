---
category: programming
cover_image: cover.png
date: 2021-05-22
description: Why mess with getopt when I can just use multi-dispatch?
draft: false
format: md
layout: layout:PublishedArticle
series:
- Journaling in Joplin With Raku
slug: my-raku-script-for-journaling-in-joplin
tags:
- Raku Lang
- joplin
- shell
title: My Raku script for Journaling in Joplin
updated: 2021-05-24
uuid: fdc4f584-94fe-4f58-a384-9600267c7731
---

## Setting the scene

So yesterday I wrote a couple of [one-liners][] for managing journal entries in
the [Joplin][joplin] note-taking application, with help from [Raku][raku].

I made one for writing:

``` bash
joplin use Journal && joplin edit $(date --iso=minute)
```

I made one for reading:

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

They work.  That's great.

They don't work great, though.  Mainly the one-liner for reading.  It dumps
every journal entry, which is both overwhelming and slow.  Overwhelming because
I only want to see today's journal entries most of the time.  Slow because
every one of those entries requires a separate call to `joplin`.  Joplin is
lovely, but it expects to be used as a persistent application.  The command
line functionality is optimized for convenience.  It is *not* optimized for
being hammered repeatedly by an overenthusiastic command line script.

I can fix the overwhelming.  I can't properly fix the slow until I learn more
about the [Joplin API][joplin-api].  At least I can make the experience less
awful.

## Make it less awful

### Less hard-coding please

First things first.  I might change the name of my journal notebook.  You might
want a daily diary rather than a giant stack of entries.

```
constant $notebook     = "Journal";
constant $entry-window = "minute";
```

Focusing on daily journals? Set `$entry-window` to `"day"`.

### Adding an entry

```
sub add-entry() {
  my $timestamp = DateTime.now.truncated-to($entry-window);
  my $command = "joplin use $notebook && joplin edit $timestamp";
  shell( $command );
}
```

Raku's [DateTime][datetime] classes provide the gist of what we got with GNU Date.
[`truncated-to`][truncated-to] rounds our current timestamp — [`now`][now] — down to the minute.

    $ raku -e 'DateTime.now.say'
    2021-05-22T11:52:28.380996-07:00

    $ raku -e 'DateTime.now.truncated-to("minute").say'
    2021-05-22T11:52:00-07:00

It doesn't print exactly the same as `date`:

    $ date --iso=minute
    2021-05-22T11:52-07:00

It wouldn't take excessive effort to make them match, but I'm just not
concerned about it at the moment.

#### Use a ``MAIN`` sub

Well, we went and put the logic for adding an entry into a function.  We want
to call that function at some point, right?

```
sub MAIN() {
  add-entry;
}
```

We don't need [`MAIN`][main-sub] yet.  If present, it's your Raku script's
official entry point.  If not, you have a plain old script.  You're good either
way.  Having that entry point will make things easier to manage in a minute,
though.

If we run this as-is, it adds a new entry.

    $ raku journal
    Note does not exist: "2021-05-22T12:18:00-07:00". Create it? (Y/n) y
    ...
    Note has been saved.

Okay, fine.  It works.  So far it's neither tidier nor more readable than the
initial one-liner.  But writing an entry was never the problem.

The problem was reading the entries.

### Read all the entries?

Back in our one-liner, collecting entries and reading them got smushed
together.  They're two distinct actions, though.

```
sub all-entries() {
  qqx{joplin use $notebook && joplin ls}.lines.sort;
}

sub read-entries(@entries) {
  @entries.map({
    qqx{ joplin cat $_}.subst(/^(<[\dT:\-]>+)/, { "# $0" })
  }).join;
}
```

Right.  Now we have subs for writing, and subs for reading.  How do we want to
get at them?  Maybe a callback table with action keywords? Maybe a fancy
[module][]?

Nope!  Well — we *could*.  But we don't need to.  Raku has [multi-dispatch][]!

#### Use multiple `MAIN` subs!

We replace the initial `MAIN` definition with these:

```
multi sub MAIN("add") {   #= Add an entry
  add-entry;
}

multi sub MAIN("read") {  #= Read all entries
  say read-entries(all-entries);
}
```

`multi` tells Raku to expect multiple definitions for this sub.  Without it,
the compiler gets annoyed.

[Multiple dispatch][multiple-dispatch] means a few things depending on which
language you're using — or which computer scientist you're asking.  Basically
it lets you avoid having one giant glob of a function with all sorts of special
logic.  You do that by having a different version of the function for different
situations.

Where I got surprised?  Most of the tiny amount I've read out there for
multiple dispatch talks about basing on types or pattern matching against
variables.  You could absolutely do that with Raku.

```
multi sub MAIN(Str $action where { $action == "add" }) { ... }

multi sub MAIN(Str $action where { $action == "read" }) { ... }
```

Thing is, we're not doing anything with `$action`.  We *read* if the first
command line argument is `read`.  We *add* if it's `add`.  Raku is happy
enough matching that first argument against literal strings.  I assume other
multi-dispatch languages can to the same, but nobody's been uncouth enough to
bring it up in polite company.  It's always "this type" and "that pattern" or
"this enum."

What happens if we try to run the script with no arguments?  Well, if we didn't
remove that initial version of `MAIN` we get a compiler error about
redefining the sub.  But once that's out of the way, we no longer have a
default path into the application!

No worries.  Raku's special handling of the entry point sub shows us the
accepted usage.

    $ raku journal.raku
    Usage:
    journal.raku add -- Add an entry
    journal.raku read -- Read all entries

And that's where those `#=` comments come in.  They provide extra detail for
the usage message displayed.

Let's try them out.  We'll `add` an entry and then make sure it shows up when
we `read` them.

    $ raku journal.raku add
    Note does not exist: "2021-05-22T12:55:00-07:00". Create it? (Y/n)
    ...
    Note has been saved.
    $ raku journal.raku read
    ...
    # 2021-05-22T12:55:00-07:00

    [multi-dispatch]: https://docs.raku.org/language/functions#Multi-dispatch

    Raku Joplin journaling script, now with [multi-dispatch][]!

Nice.  Of course, at this point I'm being handed 142 lines of text, and it's
taking about 12 seconds to do it.  All that work and we finally reached the
full "overwhelming and slow" point we were at this morning.

Things are about to improve!

### I just want today

I've been carefully using [ISO 8601][iso-8601] format for my entries.  That
means I can filter to a specific date — or year, month, hour, etc — by
constructing a date fragment and grabbing each entry that starts with the
fragment.

```
sub filtered-entries(Str $date-funnel) {
  all-entries.grep({ .starts-with($date-funnel) });
}
```

Getting today's entries then becomes a matter of extracting a yyyy-mm-dd`
string from the ever-so-helpful DateTime.

```
sub entries-for-today() {
  filtered-entries DateTime.now.yyyy-mm-dd
}
```

:::note

**2021-05-24**

[@b2gills][b2gills] mentioned that I could also use [`Date.today`][date-today]
here!

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">Why didn&#39;t you use Date.​today?<br><br>If you had a coercive parameter, you wouldn&#39;t even need to do anything more than Date.​today.<br><br> sub filtered-entries(Str(Date) $​date-funnel) &#123;…}<br><br> sub entries-for-today() &#123;<br> filtered-entries Date.​today<br> }</p>&mdash; Brad Gilbert (@b2gills) <a href="https://twitter.com/b2gills/status/1397038905405452296?ref_src=twsrc%5Etfw">May 25, 2021</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

I haven't messed with [parameter coercion][parameter-coercion] yet, but that
looks like it will come in handy.

:::

Need to touch up my reading `MAIN` definition, though.

```
multi sub MAIN("read") {  #= Read today's entries
  say read-entries( entries-for-today );
}
```

Does it work?  Is it fast?

    $ time raku journal.raku read
    # 2021-05-22T08:12:00-07:00

    Millie let me sleep in until 7:54. How gracious.

    [@liztormato]: https://twitter.com/liztormato
    [Reddit]: https://www.reddit.com/r/rakulang/comments/nif2sf/cli_journaling_in_joplin_with_raku_brian_wisti/

    Oh and last night's Joplin / Raku post got some legs. [@liztormato][] even
    shared it on [Reddit][]. That's cool. I always hope they like it when I post
    something about #RakuLang.

    # 2021-05-22T10:43:00-07:00

    My note script needs an option for "read yesterday's notes."

    # 2021-05-22T12:18:00-07:00 Making sure that my Raku Joplin journaling script lets me add an entry.

    # 2021-05-22T12:55:00-07:00

    [multi-dispatch]: https://docs.raku.org/language/functions#Multi-dispatch

    Raku Joplin journaling script, now with [multi-dispatch][]!

    real    0m3.815s
    user    0m3.966s
    sys     0m0.502s

It works.  It's — it's not *fast* by any means, but 3.8 seconds is much faster
than 12.  Again, there's an API waiting for when I'm bored of abusing Joplin's
command line conveniences.

### And maybe yesterday

Most of my deep dives into the journal will be from inside the Joplin app.  A
quick glance at yesterday's notes could still be useful.

Of course a DateTime lets me ask for an [`earlier`][earlier] DateTime.

```
sub entries-for-yesterday() {
  my $yesterday = DateTime.now.earlier(days => 1);  # or :1day for the terse
  filtered-entries $yesterday.yyyy-mm-dd;
}
```

For `MAIN` I *could* add and match against a subcommand.  I think instead I
will adjust my top-level commands to reflect the most common cases.

```
multi sub MAIN("today") {  #= Read today's entries
  say read-entries( entries-for-today );
}

multi sub MAIN("yesterday") { #= Read yesterday's entries
  say read-entries( entries-for-yesterday );
}
```

And it works!

    $ raku journal.raku yesterday
    # 2021-05-21T09:00-07:00

    Alarm 07:00, stayed in bed as long as I could. Thanks to the dogs, that was 15
    minutes. Oh well.

    [Homebrew]: https://brew.sh
    [Nix]: https://nixos.org/
    [using Nix on Debian]: https://ariya.io/2020/05/nix-package-manager-on-ubuntu-or-debian

    Got the Raspberry Pi 4 set up with Raspbian, and the 500GB external drive
    attached. Thinking about package managers. I know [Homebrew][] but I could
    maybe try [Nix][]. There's a post about [using Nix on Debian][].
    ...
    # 2021-05-21T21:29:00-07:00

    Just about to post my Raku Joplin Journaling One-liners, but maybe a couple
    screenshots? People love screenshots.

    Maybe they do. Maybe they don't. *I* love screenshots.

### What about formatting?

Honestly?  I'm not going to worry about it right now.  Piping to [Rich][rich]
or [Glow][glow] suffices when I want it pretty.

<pre class="rich">╔══════════════════════════════════════════════════════════════════════════════╗
║                          <span style="font-weight: bold">2021-05-22T08:12:00-07:00</span>                           ║
╚══════════════════════════════════════════════════════════════════════════════╝

Millie let me sleep in until 7:54. How gracious.

Oh and last night's Joplin / Raku post got some legs. <span style="color: #0000ff; text-decoration-color: #0000ff"><a href="https://twitter.com/liztormato">@liztormato</a></span> even shared it
on <span style="color: #0000ff; text-decoration-color: #0000ff"><a href="https://www.reddit.com/r/rakulang/comments/nif2sf/cli_journaling_in_joplin_with_raku_brian_wisti/">Reddit</a></span>. That's cool. I always hope they like it when I post something about
#RakuLang.

╔══════════════════════════════════════════════════════════════════════════════╗
║                          <span style="font-weight: bold">2021-05-22T10:43:00-07:00</span>                           ║
╚══════════════════════════════════════════════════════════════════════════════╝

My note script needs an option for "read yesterday's notes."

╔══════════════════════════════════════════════════════════════════════════════╗
║                          <span style="font-weight: bold">2021-05-22T12:18:00-07:00</span>                           ║
╚══════════════════════════════════════════════════════════════════════════════╝

Making sure that my Raku Joplin journaling script lets me add an entry.

╔══════════════════════════════════════════════════════════════════════════════╗
║                          <span style="font-weight: bold">2021-05-22T12:55:00-07:00</span>                           ║
╚══════════════════════════════════════════════════════════════════════════════╝

Raku Joplin journaling script, now with <span style="color: #0000ff; text-decoration-color: #0000ff"><a href="https://docs.raku.org/language/functions#Multi-dispatch">multi-dispatch</a></span>!

╔══════════════════════════════════════════════════════════════════════════════╗
║                          <span style="font-weight: bold">2021-05-22T14:05:00-07:00</span>                           ║
╚══════════════════════════════════════════════════════════════════════════════╝

Guess I'm about ready to post the second Raku Joplin journaling post. Ah, the
joys of hyperfocus.

Better stretch my legs and get back to the official task list after.
</pre>

## The complete script

```
#!/usr/bin/env raku

constant $notebook     = "Journal";
constant $entry-window = "minute";

sub add-entry() {
  my $timestamp = DateTime.now.truncated-to($entry-window);
  my $command = "joplin use $notebook && joplin edit $timestamp";
  shell( $command );
}

sub all-entries() {
  qqx{joplin use $notebook && joplin ls}.lines.sort;
}

sub filtered-entries(Str $date-funnel) {
  all-entries.grep({ .starts-with($date-funnel) });
}

sub entries-for-today() {
  filtered-entries DateTime.now.yyyy-mm-dd;
}

sub entries-for-yesterday() {
  my $yesterday = DateTime.now.earlier(days => 1);  # or :1day for the terse
  filtered-entries $yesterday.yyyy-mm-dd;
}

sub read-entries(@entries) {
  @entries.map({
    qqx{ joplin cat $_}.subst(/^(<[\dT:\-]>+)/, { "# $0" })
  }).join;
}

multi sub MAIN("add") {   #= Add an entry
  add-entry;
}

multi sub MAIN("today") {  #= Read today's entries
  say read-entries( entries-for-today );
}

multi sub MAIN("yesterday") { #= Read yesterday's entries
  say read-entries( entries-for-yesterday );
}

multi sub MAIN("all") { #= Read all entries (SLOW!)
  say read-entries( all-entries );
}
```

[one-liners]: /post/2021/05/cli-journaling-in-joplin-with-raku/
[joplin]: https://joplinapp.org
[raku]: https://raku.org
[datetime]: https://docs.raku.org/type/DateTime
[now]: https://docs.raku.org/type/DateTime#method_now
[truncated-to]: https://docs.raku.org/type/DateTime#method_truncated-to
[module]: https://modules.raku.org
[multi-dispatch]: https://docs.raku.org/language/functions#Multi-dispatch
[multiple-dispatch]: https://en.wikipedia.org/wiki/Multiple_dispatch
[iso-8601]: https://en.wikipedia.org/wiki/ISO_8601
[b2gills]: https://twitter.com/b2gills
[date-today]: https://docs.raku.org/type/Date#method_today[Date.today]
[parameter-coercion]: https://docs.raku.org/syntax/Coercion%20type
[earlier]: https://docs.raku.org/type/DateTime#(Dateish)_method_earlier
[rich]: https://rich.readthedocs.io/en/stable/markdown.html
[glow]: https://github.com/charmbracelet/glow
[joplin-api]: https://joplinapp.org/api/overview/
[main-sub]: https://docs.raku.org/routine/MAIN
