---
aliases:
- /2017/10/01/beets-and-itunes/
category: tools
date: 2017-10-01
description: beets and AppleScript helped me fix my incorrect track information
draft: false
layout: layout:PublishedArticle
slug: beets-and-itunes
tags:
- music
- macOS
- beets
- python
title: Beets and iTunes
updated: 2017-10-02 00:00:00
uuid: 289a21db-bef8-4238-80b0-e2fbf29cafce
---

My macOS iTunes music library includes over 21,000 songs. Some of those tracks
contain the wrong information. Wrong title, wrong album, wrong artist, wrong
year.

## Beets

[Beets]: http://beets.io/

The open source [Beets][] command line tool helps manage your music library.

[MusicBrainz]: https://musicbrainz.org/

> The purpose of beets is to get your music collection right once and for all.
> It catalogs your collection, automatically improving its metadata as it goes
> using the [MusicBrainz][] database. Then it provides a bouquet of tools for
> manipulating and accessing your music.

[Plugins]: http://beets.readthedocs.io/en/v1.4.5/plugins/index.html

[Plugins][] allow beets to perform more than media management. I won’t talk
about most of them today. I don’t want to overwhelm myself. I will keep my focus
on using beets from the command line to help me fix my iTunes library.

### Alternatives

I prefer command line open source tools. It’s a comfortable habit. You have
other options, though.

[Picard]: https://picard.musicbrainz.org
[iTunes guide]: https://musicbrainz.org/doc/iTunes_Guide

If you prefer using a mouse, try out [Picard][] from MusicBrainz. Its manual
includes an [iTunes guide][], so you won’t have to guess your way through the
process.

[TuneUp]: http://www.tuneupmedia.com/

[TuneUp][] is a commercial application that integrates with iTunes. I haven’t
used it, but TuneUp was the first thing that came up in most of my initial
research into fixing my tracks.

## Installation and Configuration

[Python]: https://python.org

beets is written in [Python][]. It works with both Python 2 and 3, but I had
better results with my hooks when using Python 2.

[pyenv]: https://github.com/pyenv/pyenv
[pyenv-virtualenv]: https://github.com/pyenv/pyenv-virtualenv
[Homebrew]: https://brew.sh/

I already installed [pyenv][] and [pyenv-virtualenv][] via [Homebrew][]. They
aren’t strictly needed, but having distinct environments simplifies things when
you have several Python-related projects.

    $ pyenv virtualenv 2.7.14 beets
    $ pyenv shell beets

[pyacoustid]: https://pypi.python.org/pypi/pyacoustid
[Chromaprint]: https://acoustid.org/chromaprint

beets uses [pyacoustid][] for acoustic fingerprinting, which helps identify
tracks by their audio data. pyacoustid needs the [Chromaprint][] library, so I
install that also.

    $ brew install chromaprint
    $ pip install beets pyacoustid

[Google Groups thread]: https://groups.google.com/forum/#!topic/beets-users/yijEk858yiw

This [Google Groups thread][] got me started on configuration. My settings focus
on safely cataloging music rather than organizing it.

**`~/.config/beets/config.yaml`**

```yaml
# using default library ~/.beets/config/library.db
# using default directory ~/Music, but see 'copy'

plugins: chroma edit ftintitle fromfilename importadded hook

import:
  copy: no         # Copy the file to our directory when importing?
  incremental: yes # Skip directories we already imported?
  write: no        # Automatically write the file on library import / update?
  resume: yes      # Resume interrupted imports?
  log: beets.log   # Where should we write what we do?

match:
  strong_rec_thresh: 0.1            # Any difference less than this is a strong recommendation
  preferred:                        # Put these at the top of recommendations
    countries: [US, GB|UK]          # My favorite music publishing countries
    media: [CD, Digital Media|File] # My favorite music sources
    original_year: yes              # entry year is close to entry original_year

# Tell iTunes to add and/or update the track in its library after we write a file.
hook:
  hooks:
    - event: after_write
      command: osascript /Users/brianwisti/bin/iTunesRefresh.scpt "{item.path}"
```

The plugins add important functionality.

[chroma]: http://beets.readthedocs.io/en/v1.4.5/plugins/chroma.html
[edit]: http://beets.readthedocs.io/en/v1.4.5/plugins/edit.html
[ftintitle]: http://beets.readthedocs.io/en/v1.4.5/plugins/ftintitle.html
[fromfilename]: http://beets.readthedocs.io/en/v1.4.5/plugins/fromfilename.html
[importadded]: http://beets.readthedocs.io/en/v1.4.5/plugins/importadded.html
[hook]: http://beets.readthedocs.io/en/v1.4.5/plugins/hook.html

[chroma][]
: Use acoustic fingerprinting to identify songs by their sound. Slower, but helps with tracks that have bad metadata.

[edit][]
: Edit details of your songs after importing

[ftintitle][]
: Puts featured artist information in song title instead of artist.

[fromfilename][]
: Try to guess missing metadata from the filename of a song.

[importadded][]
: Use the file’s modification time to determine when you added it to your library. Useful for importing an existing library.

[hook][]
: Run commands for specific beet events.

<aside class="admonition tip">
<p class="admonition-title">Tip</p>

Oh in iTunes uncheck Preferences > Advanced > "Keep iTunes Media folder organized".
Otherwise you’ll end up deleting and reimporting songs that iTunes moved.

</aside>

Configuration is out of the way. Let’s import music.

    $ beet import ~/Music/iTunes/iTunes Media/Music

Importing a large music library takes time, especially with acoustic
fingerprinting. My music took a full weekend, even with `match` settings giving
it more leeway to automatically use the likeliest matches. But at the end of it
all, here’s what I had.

    $ beet stats
    Tracks: 22112
    Total time: 8.7 weeks
    Approximate total size: 107.8 GiB
    Artists: 2498
    Albums: 2405
    Album artists: 1117

[query support]: http://beets.readthedocs.io/en/v1.4.5/reference/query.html
[format strings]: http://beets.readthedocs.io/en/v1.4.5/reference/pathformat.html

I won’t tell you about all the amazing [query support][] or [format strings][]
in beets. Instead let’s just list matches for a random word.

    $ beet ls pigeon
    Bert - Songs From the Street: 35 Years of Music - Doin' the Pigeon
    Cyndi Lauper - Hat Full of Stars - Sally's Pigeons
    Cyndi Lauper - Twelve Deadly Cyns... and Then Some - Sally's Pigeons
    Tom Lehrer - An Evening Wasted With Tom Lehrer - Poisoning Pigeons in the Park
    Lo Fidelity Allstars - How to Operate With a Blown Mind - Battle Flag feat. Pigeonhed
    RJD2 - Have Mercy - Have Mercy (Remix feat Lyrics Born and Pigeon John)
    RJD2 - Have Mercy - Have Mercy (Remix feat Lyrics Born and Pigeon John)

Looks like I have some duplicates. I can worry about that another day.

### Tell Beets to Tell iTunes to Refresh

Now that beets has imported everything, it’s time to write it all back out and
update the iTunes library.

### Write Some AppleScript

[blog post on JavaScript and iTunes]: https://www.macstories.net/tutorials/getting-started-with-javascript-for-automation-on-yosemite/
[JXA Cookbook page for iTunes]: https://github.com/JXA-Cookbook/JXA-Cookbook/wiki/iTunes

:::note

I spent a full day trying to make JXA work for this. It didn’t. I kept crashing
Script Editor with whimsical directives like `console.log(iTunes)`. If you want
to try JXA, look at this [blog post on JavaScript and iTunes][], or the
[JXA Cookbook page for iTunes][].

:::

[AppleScript]: https://developer.apple.com/library/content/documentation/AppleScript/Conceptual/AppleScriptX/AppleScriptX.html
[This post]: https://dougscripts.com/itunes/2010/12/get-a-track-reference-from-a-file-path/
[Doug’s AppleScripts for iTunes]: https://dougscripts.com/itunes/index.php#whatsnew
[Ask Different answer]: https://apple.stackexchange.com/questions/202504/searching-itunes-library-for-file-location#222834

I rarely use [AppleScript][], so it took a combination of Web searching and
guesswork to come up with this. [This post][] from [Doug's AppleScripts for
iTunes][] blog and this [Ask Different answer][] got me most of the way there.
The guesswork finished it off.

**`~/bin/iTunesRefresh.scpt`**

```applescript
on run (argv)
  tell application "iTunes"
    set filename to POSIX file (argv's item 1 as string) as alias
    try
      set trackRef to (add filename)
      refresh trackRef
    end try
  end tell
end run
```

#### The Beets Hook

`osascript` lets you run AppleScript commands and files from the command line.
This `after_write` hook is only called when song metadata is updated in the file
itself.

Writing every track with the hook after that big import took about four hours —
but I could leave it in the background while I did other stuff.

### After the big import

[Stuck in the Middle With You]: https://youtu.be/DohRa9lsx0Q

Sometimes beets identifies tracks incorrectly. It happens. For example, Bob
Dylan did not sing [Stuck in the Middle With You][].

[modify]: http://beets.readthedocs.io/en/v1.4.5/reference/cli.html#modify
[edit plugin]: http://beets.readthedocs.io/en/v1.4.5/plugins/edit.html

I could [modify][] that song with `beets modify`, but I can also do it with the
[edit plugin][].

    $ beet edit `stuck in the middle`

This pulls up `$EDITOR`, which in my case is Vim.

![Editing a Beets entry in Vim](beet-edit-screen.png)

After the import and update, I saw something else in iTunes that bugged me.
iTunes can sort by `year`, but not by `original_year` — the year an album was
originally released, rather than the year that particular file or CD was
available.

I don’t know how to edit that with beets commands, but I can work directly with
its underlying SQLite database. Maybe I’m being a little bold here, but I can
always spend another weekend reimporting my music.

**`sqlite3 ~/.config/beets/library.db`**

```sql
sqlite> update items set year = original_year where year != original_year and original_year != 0;
sqlite> update albums set year = original_year where year != original_year and original_year != 0;
```

`beet write` finalizes those changes, and updates iTunes again thanks to the
`after_write` hook.

[in real life]: https://xkcd.com/180/

Everything worked out for me this time. But remember, if you change values in
the database, they happen [in real life][] too!

[original date]: http://beets.readthedocs.io/en/v1.4.5/reference/config.html#original-date

:::note

Then somebody mentioned that I could skip this particular mess by setting the
[original date][] option to `yes` in my beets configuration. beets will update a
song’s `year`, `month`, and `day` fields to reflect the values in
`original_date`. Use that setting if you would rather not poke around in the
database.

:::

### What Next?

That’s good enough for today. I’ll correct entries as I see them, but things are
definitely better than when I started.

[plugins]: http://beets.readthedocs.io/en/v1.4.5/plugins/index.html

To see what you can do with beets, check out the [plugins][].

Play with the [query support][] and [format strings][]. Have fun!