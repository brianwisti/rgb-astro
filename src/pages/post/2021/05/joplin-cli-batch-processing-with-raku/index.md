---
caption: don't get excited; these are the only notes I took
category: tools
cover_image: regex-anchors.jpg
date: 2021-05-25 03:00:00
description: In which a minor update veers off on a Raku regex tangent
draft: false
format: md
layout: layout:PublishedArticle
series:
- Journaling in Joplin With Raku
slug: joplin-cli-batch-processing-with-raku
tags:
- joplin
- Raku Lang
- regular expressions
- shell
- oops
- I fixed it!
title: Joplin CLI Batch Processing With Raku
uuid: 6d0be74e-551f-4ec0-9418-7445752164b3
---

:::note

This sidetracks enough for three blog posts, mostly about [Raku][raku].  Sorry
about that.  No time to make it shorter.  You know how it is.  There's a little
[Joplin][joplin] stuff in here.

:::

This is embarrassing.  I fired up the Joplin [desktop app][desktop-app] this
morning and it told me there was an update.  Makes sense.  I haven't loaded the
desktop app in a couple months.

Oh hang on.  What about the [terminal app][terminal-app] which I was just
writing about over the last couple posts?

Yep.  The [Changelog][changelog] shows updates, one of which includes batch
processing.  Batch processing sounds like exactly the thing to address my many
complaints about performance.

## Update Joplin with Volta

I use [Volta][volta] to manage my [Node.js][node-js] resources.  Volta treats
installing and updating as the same action.

    volta install joplin

This is what I have now:

    $ joplin version
    joplin 1.8.1 (prod)

Now I'm up to date.  Let's see what changes I can make to my journaling code.

## Fix the one-liners

The one-liner for adding journal entries works fine as-is.

``` bash
joplin use Journal && joplin edit $(date --iso=minute)
```

Reading the entries needs improvement.

``` bash
raku -e '
  qqx{joplin cat $_}.subst(/^(<[\dT:\-]>+)/, { "# $0" }).say for qx{ joplin ls }.lines.sort
' \
| python -m rich.markdown -
```

Joplin CLI v1.8.1 added a `batch` command, which executes commands from a
text file.  My challenge: `joplin batch` does not appear to have an option
for standard input.  This means I can't casually pipe output from another
process.  Here's what I came up with:

``` bash
joplin batch <(raku -e 'qx{joplin ls}.lines.sort.map({ "cat $_" }).join("\n").say') \
  | raku -ne '.subst(/^(<[\dT:\-]>+)$/, { "# $0" }).say' \
  | python -m rich.markdown -
```

We take advantage of a little shell magic to treat the output of another process as a file.

Don't ask me to understand the shell magic.  In [GNU Bash][bash], `command
<(stuff)` means something along the lines of "evaluate *stuff* and hand the
output of that evaluation to `command` as if it was a file."

It's all a little inside-out and twisty.  It might help if we break up the
chunks.

| Chunk                              | What it does                                           |
| ---------------------------------- | ------------------------------------------------------ |
| `qx{joplin ls}.lines.sort`         | collect the sorted entry list from this notebook       |
| `.map{ "cat $_" }`                 | create a Joplin command to display this entry          |
| `.join("\n").say`                  | print those commands as one multi-line string          |
| `joplin batch <(...)`              | send `raku`'s output to `joplin batch`                 |
| `... \| .subst(...)`               | turn timestamp lines from output into Markdown headers |
| `... \| python -m rich.markdown -` | format the output for terminal display                 |

We pull Raku in twice: once to build the command and again to parse the output.
On the other hand we're only calling Joplin twice instead of forty or so times.

That makes the one-liner downright zippy, all things considered.

    $ time joplin batch <(raku -e 'qx{joplin ls}.lines.sort.map({ "cat $_" }).join("\n").say') \
    | raku -ne '.subst(/^(<[\dT:\-]>+)$/, { "# $0" }).say' \
    | python -m rich.markdown -
    ...
    real    0m1.407s
    user    0m1.608s
    sys     0m0.140s

One and a half seconds for a formatted display of every journal entry.  Not
bad, considering that I'm running on [WSL][wsl].  Plus I don't really know
one-liners, Raku, or Joplin.

:::note

The documentation for `joplin ls` mentions a `--sort` flag, but as of v1.8.1 I
got no difference when using `joplin ls --sort title`. Didn't see a mention of
the specific issue, so I overcame my shyness and filed [#5004][bug-5004].

:::

## Fix the script

Splitting up the Raku script into logical pieces the other day means that today
I only need to fix a single function.  Thank goodness.

```
sub read-entries(@entries) {
  @entries.map({
    qqx{ joplin cat $_}.subst(/^(<[\dT:\-]>+)/, { "# $0" })
  }).join;
}
```

How much does this function need to improve?

    $ time jj today
    ...
    real    0m3.001s
    user    0m3.281s
    sys     0m0.390s

    $ time jj all
    ...
    real    0m31.253s
    user    0m31.779s
    sys     0m4.616s

Lots.  This function needs to be lots quicker.  It took three seconds to
display today's lone entry, and over 30 seconds to display all 40 journal
entries.  Every new entry slows the whole thing down, because every new entry
means a new call to `joplin`.

:::note

I don't jot *that* many notes in a day. Some of that's from reorganizing my
Joplin notebooks, putting daily journals in with the quick entries.

:::

I tried mimicking the shell magic but couldn't figure out how in the time I
allowed myself.  This isn't work code where you have to get things just so.
This is a fun little utility for my own amusement.

`joplin batch` expects a file?  Let's give it a file.  But I want that file
to go away when I'm done, so let's find a module to handle temporary files.

Poking through the directory of [Raku modules][modules] quickly showed me two possibilities:

[`Temp::Path`][temp-path]
: gives you a friendly object you can write to or stringify when you need a filename

[`File::Temp`][file-temp]
: presents a more utilitarian interface, providing filename and filehandle as separate variables

The end result is the same: a file that goes away when you no longer need it.

I like friendly. Let's see how `Temp::Path` does.

### Try `Temp::Path`

Need to install it, of course.  [`zef`][zef] handles Raku modules.  I set that
up a while back with [`rakubrew`][rakubrew].

    zef install Temp::Path

Then we let Raku know we're using the module.  That traditionally goes near the
top of our script.

```
use Temp::Path;
```

More or less following along Temp::Path's sample usage.  [`with`][with] creates
a block for our temporary file.  It even sets the [topic
variable][topic-variable] `$_`.  Don't need to come up with a temporary
variable name for our temporary file.

```
sub read-entries(@entries) {
  with make-temp-path {
    .spurt(@entries.map({ "cat $_" }).join("\n"));
    qqx{ joplin batch $_ }.subst( /^^(<[\dT:\-]>+)$$/, { "# $0" }, :g );
  }
}
```

The regular expression is starting to look interesting.  `joplin batch` hands
everything to us as one string.  We need to adjust the entry-oriented logic we
had before.  Now we find any *line* containing a lone ISO-8601 timestamp, and
convert it to a top-level Markdown header.  The `:g` flag tells `.subst` to
replace every occurrence.

:::admonition{title="`^..$` vs `^^..$$`"}

Regular expressions in other languages treat `^` and `$` differently
depending on whether you're applying the expression in a single-line or
multiple-line context. Raku's [anchors][] treat every expression as multi-line.

That's a nice consistency point in Raku's favor. Instead of memorizing more
flags and contexts, and more special anchors for when the flags and context
make things unclear, we get these two paired anchors.

| Anchor | Where it matches        |
| ------ | ----------------------- |
| `^`    | beginning of the string |
| `$`    | end of the string       |
| `^^`   | beginning of a line     |
| `$$`   | end of a line           |

There are plenty of other things for us to memorize, of course.

If you're more of a visual person, here's a quality page from my extensive
notebook.

#[diagram of multi-line string showing where these anchors match](regex-anchors.jpg)

So what if my Raku notebook only has this one page with this one diagram.
It's a good diagram.  Very professional.  High quality learning aid.

:::

Those few lines don't change anything for me as a user.  Maybe the speed?

    $ time jj today
    ...
    real    0m2.969s
    user    0m3.385s
    sys     0m0.303s

    $ time jj all
    ...
    real    0m3.034s
    user    0m3.328s
    sys     0m0.505s

Huh. It's not any faster than the best case for the initial script, with a
single entry taking roughly the same amount of time to load and display.  Then
again, `batch` is clearly doing its job.  One entry takes almost exactly the
same amount of time as 40.  Since most days I'll have multiple entries, that is
an effective optimization for the common case.

But why is my one-liner twice as fast?  Is it Temp::Path?  Raku?  Joplin?
Something to do with file I/O on WSL 2?  No idea.

Let's find out if File::Temp does any better.

### Try File::Temp

Out comes `zef`…

``` bash
zef install File::Temp
```

…then use File::Temp instead of Temp::Path…

```
use File::Temp;
```

…then rewrite `read-entries` one more time…

```
sub read-entries(@entries) {
  my ($filename, $filehandle) = tempfile;
  $filehandle.spurt( @entries.map({ "cat $_" }).join("\n") );
  qqx{ joplin batch $filename }.subst(/^^ (<[\dT:\-]>+) $$/, { "# $0" }, :g);
}
```

:::admonition

**Space is insignificant in regular expressions**

Did you catch that?  Raku ignores whitespace in regular expressions unless you
say otherwise with [`:sigspace`][sigspace].  Means you can make a regex easier
to read.  This wasn't *much* easier to read, but at least we can tell where the
anchors are and what I hope to find between those anchors.

For Perl folks, this plus the multi-line thing is like giving every regex
`/mx`.  For Python folks, like `re.MULTILINE` and `re.VERBOSE`.  For JavaScript
folks — um — it's like having useful regular expressions.  Okay, it's like
having [XRegExp][xregexp] installed and using `'x'`.

:::

…and try it out.

    $ time jj today
    ...
    real    0m2.502s
    user    0m2.771s
    sys     0m0.326s

    $ time jj all
    ...
    real    0m2.611s
    user    0m2.911s
    sys     0m0.381s

Ran each version a few times, just to be sure.  The version with File::Temp
consistently finished a noticeable fraction of a section quicker than using
Temp::Path.  Still nowhere near the one-liner's performance, but good enough
that I'll stick with File::Temp until I come up with something better.

Do I care enough to reboot into Linux and see how much of a difference that
makes?

Not really.

I can probably optimize this, but it's not urgent or important.  So far I only
skim my entries when I already have a few moments to spare.  Besides, the real
optimizations almost definitely lie with using the Joplin API.

What I'm saying is don't get hung up on trivia.

Speaking of trivia…

## About that regular expression

I need to do something about this.

```
qqx{ ... }.subst(/^^ (<[\dT:\-]>+) $$/, { "# $0" }, :g);
```

We already know that regular expressions are their own little language embedded
in whatever programming language we happen to be getting work done in.  With
Raku, we can treat regular expressions as part of the Raku language itself.

Let's tackle this backwards.  Top-down.  Whatever it is the fancy people say.
I'm going to split it out into its own function.  Makes it easier to think of
this transformation in isolation.

### Hide it in a function

What do I want this function to do?  I want it to give me my *journal text*,
but with *formatted headers* in the right places.

```
sub format-headers($journal-text) {
  $journal-text.subst(
    /^^ (<[\dT:\-]>+) $$/,
    { "# $0" }, :g);
}
```

### Use a named capture

Do I want to format every `$0`? No. I want to format every *entry title*.

```
sub format-journal($journal-text) {
  $journal-text.subst(
    ...,
    { "# $<entry-title>" }, :g
  );
}
```

Of course Raku supports [named captures][named-captures].  The part we care
about is stored in the match object.  Behind the scenes, `$<entry-title>` is
getting the value stored under the key `"entry-title"`.

## An `rx{}` block for legibility

How do I know the *entry title*?  I know the *entry title* because I found a
*lone timestamp*.

```
sub format-journal($journal-text) {
  $journal-text.subst(
    rx{
      $<entry-title> = ( <lone-timestamp> )
    },
    { "# $<entry-title>" }, :g
  );
}
```

`rx{ ... }` indicates an [anonymous regex][anonymous-regex].  "Anonymous" as
opposed to what exactly?  I'm getting there.  As our expressions get more
complex, take advantage of all useful quoting mechanisms.

Notice that instead of a `(?<name> pattern)` approach to named captures, in
Raku it looks a lot more like assigning a pattern to a variable.  Okay fine.
Assigning a pattern to the match object's hash, under the key
`"entry-title"`.  But still.  It looks like a more familiar programming
language assignment.

But rather than the expected elaborate chain of metacharacters, the pattern we
store is — another identifier?

I told you I was getting there.

### Name your regex, not just your capture

What's a *lone timestamp*?
It's a *timestamp* on a line by itself.

```
my regex lone-timestamp {
  ^^ <timestamp> $$
}
```

Now we have a regular expression as its own scoped code object.  The [regex][] is
the rawest component of a family that includes tokens, rules, and entire
[grammars][].  I'm not ready to get into grammars yet, but I am absolutely getting
closer.

### It's not an expression; it's a composition

What does a *timestamp* look like?  Well, a [DateTime String][datetime-str]
holds an *ISO 8601 date*, a *clock time*, and and *offset*, with a `'T'`
between the date and the clock time.

```
my regex timestamp {
  <iso8601-date> 'T' <clock-time> <offset>
}
```

If we're looking for a literal string, it's okay to use a string literal.

Now we have a few regex patterns to define.  An *ISO 8601 date* includes a
*year*, a *month*, and a *day of the month*, separated by '-'`.

```
my regex iso8601-date {
  <year> '-' <month> '-' <day-of-month>
}
```

Playing more with a language gives me a feel for how to use it based on what it
makes easy.  Raku makes it easy to create a program by composing it from small
pieces.  Tiny pieces, even.

Mind you, I have no idea if that's what `raku` the *compiler* likes.  But the
*syntax* loves it.

A *year* is four digits, a *month* is two digits, and the *day of the month* is
two digits.

```
my regex year { \d ** 4 }

my regex month { \d ** 2 }

my regex day-of-month { \d ** 2 }
```

The [general quantifier][general-quantifier] `**` indicates how many times you
expect a chunk to appear.  To this day I can't remember the exact syntax for
quantifiers in old-school regular expressions.  But I can remember the number
4.

:::note

This regex is wrong for verifying real dates. It's not wrong enough to
worry about today. I'm identifying header lines, not validating forms. But
if some day I decide to enforce zero-padded months from `01` to `12`, I
know exactly which block to edit.

:::

Looks like *clock time* gets saved as *hours*, *minutes*, and *seconds*.  In
the interest of time, we'll oversimplify those too.

```
my regex hours { \d ** 2 }

my regex minutes { \d ** 2 }

my regex seconds { \d ** 2 }

my regex clock-time {
  <hours> ':' <minutes> ':' <seconds>
}
```

And my offset holds an indicator, some *hours*, and some *minutes*.  Hey, I can
reuse my existing regex definitions for those!

```
my regex offset {
  <[+-]> <hours> ':' <minutes>
}
```

All right.  I think that covers it.  I enjoyed reusing my expressions for
*hours* and *minutes* like that.  Actual code reuse, in a regular expression.
Who would've thought?

When I take this `lone-timestamp` regex and match it against
`"2021-05-24T08:11:00-07:00"` we can see those named expressions at work.
The potential really starts to sink in for me.

    ｢2021-05-24T08:11:00-07:00｣
    lone-timestamp => ｢2021-05-24T08:11:00-07:00｣
    timestamp => ｢2021-05-24T08:11:00-07:00｣
    iso8601-date => ｢2021-05-24｣
        year => ｢2021｣
        month => ｢05｣
        day-of-month => ｢24｣
    clock-time => ｢08:11:00｣
        hours => ｢08｣
        minutes => ｢11｣
        seconds => ｢00｣
    offset => ｢-07:00｣
        hours => ｢07｣
        minutes => ｢00｣

And this is just me composing regex objects.  Eventually I'm going to try
grammars and then look out world!

:::admonition

**but why?**

This may all seem a little ridiculous, and for this use case — parsing my own
entry titles — it is.  So why am I going through all this work? Aside from it
being fun, of course.

Raku's sibling language Perl got a bad reputation for being dense and
unreadable. Regular expressions factored heavily into that density. By
providing language-level structures for defining our expressions, Raku gives
us an opportunity to use their full power for handling text without resorting
to the infamous density of 1990s regexen.

We should absolutely use that opportunity and encourage new languages to
steal *these* regular expressions rather than the stuff that impressed us
twenty years ago.

:::

### Ship it!

What am I doing on this soapbox? Time to step down.

My script works. It's still not fast, but at least it's never slow. It's
readable. And most important of all, I had fun.

## The complete script

Includes a couple more steps into composition that I didn't feel merited extra
blog post paragraphs.

```
#!/usr/bin/env raku

use File::Temp;

constant $notebook     = "Journal";
constant $entry-window = "minute";

my regex digit { \d }

my regex two-digits { <digit> ** 2 }

my regex year { <digit> ** 4 }

my regex month { <two-digits> }

my regex day-of-month { <two-digits> }

my regex hours { <two-digits> }

my regex minutes { <two-digits> }

my regex seconds { <two-digits> }

my regex iso8601-date {
  <year> '-' <month> '-' <day-of-month>
}

my regex clock-time {
  <hours> ':' <minutes> ':' <seconds>
}

my regex offset {
  <[+-]> <hours> ':' <minutes>
}

my regex timestamp {
  <iso8601-date> 'T' <clock-time> <offset>
}

my regex lone-timestamp {
  ^^ <timestamp> $$
}

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
  my ($filename, $filehandle) = tempfile;
  $filehandle.spurt( @entries.map({ "cat $_" }).join("\n") );
  format-headers( qqx{ joplin batch $filename } );
}

sub format-headers($journal-text) {
  if $journal-text ~~ /<lone-timestamp>/ { $/.say; }

  $journal-text.subst(
    rx{
      $<entry-title> = [ <lone-timestamp> ]
    },
    { "# $<entry-title>" }, :g
  );
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

[joplin]: https://joplinapp.org
[raku]: https://rakulang.org
[desktop-app]: https://joplinapp.org/desktop/
[terminal-app]: https://joplinapp.org/terminal/
[changelog]: https://joplinapp.org/changelog_cli
[volta]: https://volta.sh
[node-js]: https://nodejs.org
[bash]: https://www.gnu.org/software/bash/
[wsl]: https://docs.microsoft.com/en-us/windows/wsl/
[bug-5004]: https://github.com/laurent22/joplin/issues/5004
[modules]: https://modules.raku.org
[temp-path]: https://modules.raku.org/dist/Temp::Path:cpan:UFOBAT
[file-temp]: https://modules.raku.org/dist/File::Temp:cpan:RBT
[zef]: https://github.com/ugexe/zef
[rakubrew]: /bookmark/2021/05/rakubrew-org
[with]: https://docs.raku.org/language/control#index-entry-control_flow_with
[topic-variable]: https://docs.raku.org/language/variables#The_$__variable
[anchors]: https://docs.raku.org/language/regexes#Anchors
[sigspace]: https://docs.raku.org/language/regexes#Sigspace
[xregexp]: https://xregexp.com
[named-captures]: https://docs.raku.org/language/regexes#Named_captures
[anonymous-regex]: https://docs.raku.org/language/regexes#Anonymous_regex_definition_syntax
[regex]: https://docs.raku.org/language/regexes#Named_regex_definition_syntax
[grammars]: https://docs.raku.org/language/grammar_tutorial
[datetime-str]: https://docs.raku.org/type/DateTime#method_Str
[general-quantifier]: https://docs.raku.org/language/regexes#General_quantifier:_**_min..max
