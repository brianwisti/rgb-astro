---
category: tools
draft: true
layout: layout:Article
tags:
- music
- python
title: Managing My Music With Beets
uuid: 0a1b4c7d-d96b-4bbc-8395-2ec7c9107f09
---

Watch me explore my music library with [beets](http://beets.io), "the
media library management system for obsessive-compulsive music geeks"!

<aside class="admonition">
<p class="admonition-title">originally started 2017-05-19</p>

BTW, don’t be like me. Install the acousticbrainz, lastgenre, and chroma
plugins before you start importing.

</aside>

## TODO

  - Update system description

  - Rerun stats

## Introduction

[using beets]: /post/2017/10/beets-and-itunes/

Remember a couple years back when I talked about [using beets][] to fix
track information in my iTunes library? Well, I still use
[beets](http://beets.io) to manage my music library, even though I’m on
[Manjaro](https://manjaro.org) Linux these days.

<aside class="admonition">

WHO? Who suggested?

</aside>

I complained about trying to manage music in general purpose music
players like iTunes and Rhythmbox. A friend suggested that I try the
beets music manager. beets focuses on helping you identify and organize
your music collection. It also provides a rich selection of
[plugins](http://beets.readthedocs.io/en/v1.4.3/plugins/index.html) to
give it new features.

## Installing

I use [pyenv](https://github.com/pyenv/pyenv) on an
[openSUSE](https://www.opensuse.org/) Tumbleweed setup that already had
all the dependencies I needed. All I did was enable my preferred python
environment and install with `pip`.

To install beets yourself, check the [Getting
Started](http://beets.readthedocs.io/en/v1.4.3/guides/main.html) guide.

    $ pip install beets
    $ pip install requests pyacoustid pylast flask

## Importing

I like to keep my music in `~/Sync/Music` so that Syncthing can do its
thing. During a normal import, beets copies files into that folder.
However, since all I’m doing today is importing the library into exactly
the same location, I’ll skip copying. And writing.

    $ beet import -CWA ~/Sync/Music

Importing took about ten hours from start to finish, but that included
me responding to its queries and going to bed. Probably more like four
or five hours if I sat through the whole thing.

### Some Simple Queries

    $ beet stats
    Tracks: 19526
    Total time: 7.7 weeks
    Approximate total size: 96.0 GiB
    Artists: 2352
    Albums: 1684
    Album artists: 821

    $ beet list year:2009
    ...
    The xx - xx - Basic Space
    The xx - xx - Infinity
    The xx - xx - Night Time
    The xx - xx - Stars
    Young MC - Old School Hip Hop Greats - I Come Off / Bust A Move (Live) - Young MC
    zefrank -  - whole

    $ beet list -a year:2009
    ...
    tUnE-yArDs - BiRd-BrAiNs
    tUnE-yArDs - BiRd-DrOpPiNgS
    Various Artists - Legends of Benin
    Various Artists - Nigeria 70 Vol. 1
    Various Artists - Old School Hip Hop Greats
    M. Ward - Hold Time
    The xx - xx

I can get stats for a specific match.

    $ beet stats year:2009
    Tracks: 724
    Total time: 2.0 days
    Approximate total size: 4.3 GiB
    Artists: 113
    Albums: 62
    Album artists: 57

I can query across a range.

    $ beet stats year:2000..2009
    Tracks: 8264
    Total time: 3.2 weeks
    Approximate total size: 37.6 GiB
    Artists: 1267
    Albums: 742
    Album artists: 415

Searches are case insensitive by default

    $ beet list -a strokes
    The Strokes - Angles
    The Strokes - Comedown Machine
    The Strokes - First Impressions of Earth
    The Strokes - Is This It
    The Strokes - Room on Fire

I can sort by a field.

    $ beet list -a strokes year+
    The Strokes - Is This It
    The Strokes - Room on Fire
    The Strokes - First Impressions of Earth
    The Strokes - Angles
    The Strokes - Comedown Machine

Output can be defined by a format string.

    $ beet list -af '($year) $albumartist - $album' strokes year+
    (2001) The Strokes - Is This It
    (2003) The Strokes - Room on Fire
    (2006) The Strokes - First Impressions of Earth
    (2011) The Strokes - Angles
    (2013) The Strokes - Comedown Machine

But then I found out `$year` is not the year of the original release

    $ beet list -af '($year) $albumartist - $album' waits year+
    (1978) Tom Waits - Blue Valentine
    (1983) Tom Waits - Swordfishtrombones
    (1985) Tom Waits - Rain Dogs
    (1992) Tom Waits - Bone Machine
    (1993) Tom Waits - Nighthawks at the Diner
    (1993) Tom Waits - The Black Rider
    (1999) Tom Waits - Mule Variations
    (2002) Tom Waits - Alice
    (2002) Tom Waits - Blood Money
    (2004) Tom Waits - Real Gone
    (2006) Tom Waits - Orphans: Brawlers, Bawlers & Bastards
    (2006) Tom Waits - Orphans: Brawlers, Bawlers & Bastards
    (2008) Tom Waits - Closing Time
    (2010) Tom Waits - Heartattack and Vine
    (2011) Tom Waits - Bad as Me
    (2011) Tom Waits - Franks Wild Years
    (2012) Tom Waits - Small Change
    (2012) Tom Waits - The Heart of Saturday Night

What? This makes no sense.

    $ beet fields

It’s a long list, but I noticed `year` and `original_year` for both
tracks and albums.

    $ beet list -af '$original_year $album' waits original_year+
    1973 Closing Time
    1974 The Heart of Saturday Night
    1975 Nighthawks at the Diner
    1976 Small Change
    1978 Blue Valentine
    1980 Heartattack and Vine
    1983 Swordfishtrombones
    1985 Rain Dogs
    1987 Franks Wild Years
    1992 Bone Machine
    1993 The Black Rider
    1999 Mule Variations
    2002 Alice
    2002 Blood Money
    2004 Real Gone
    2006 Orphans: Brawlers, Bawlers & Bastards
    2006 Orphans: Brawlers, Bawlers & Bastards
    2011 Bad as Me

What about that year query earlier

    $ beet stats original_year:2000..2009
    Tracks: 6835
    Total time: 2.6 weeks
    Approximate total size: 30.9 GiB
    Artists: 1025
    Albums: 577
    Album artists: 316

    $ beet stats mb_albumid::^$
    Tracks: 1601
    Total time: 4.6 days
    Approximate total size: 9.5 GiB
    Artists: 550
    Albums: 233
    Album artists: 190

See if I can merge the two entries for "Orphans: Brawlers, Bawlers &
Bastards".

    $ beet stats Orphans artist:'Tom Waits'
    Tracks: 56
    Total time: 3.2 hours
    Approximate total size: 173.6 MiB
    Artists: 1
    Albums: 2
    Album artists: 1

    $ beet list -af '$mb_albumid - $id - $album' Orphans
    5f5ba554-5653-3196-bd1d-9e4f8f857ce6 - 376 - Orphans: Brawlers, Bawlers & Bastards
    5f5ba554-5653-3196-bd1d-9e4f8f857ce6 - 1581 - Orphans: Brawlers, Bawlers & Bastards

These are the same album as far as MusicBrainz is concerned. I tried
removing and reimporting a couple times, but all that resulted in was
new album IDs. Oops.

Oh I know. Reassign all those tracks to the same `album_id`, then delete
the extras.

    $ beet list -af '$id' orphans
    1685
    1686
    1687
    $ beet modify album:orphans album_id=1685
    Modifying 56 items.
    Tom Waits - Orphans: Brawlers, Bawlers & Bastards - Bend Down the Branches      album_id: 1686 -> 1685
    ...
    $ beet remove -a id:1686
    $ beet remove -a id:1687
    $ beet list -af '$id' orphans
    1685

Okay *that* took care of it.

### Writing Back

Now that I imported the information and am more or less satisfied with
what beets found, I ask beets to write any new metadata back to the
files.

Rhythmbox will update its information when tracks are updated. Changes
the sort order in "Artists" which confused me.

Hey, does Rhythmbox support showing original\_year?

No it does not.

Hold on what’s this? A Rhythmbox plugin to use Beets? Oh never mind
that’s just for using beets as a source. Maybe later.

### MOAR METADATA

Right. I established that import works, even though many tracks had no
easy MusicBrainz match. I established that writing back to the files
work, even though Rhythmbox doesn’t show *all* the nifty new fields by
default.

But I want more! Give me chord keys\! Give me rhythm information\! What
is `mood_aggressive`? I don’t know. I don’t care. Gimme\!

The [AcousticBrainz
plugin](http://beets.readthedocs.io/en/v1.4.3/plugins/acousticbrainz.html)
for beets sends MusicBrainz identifiers to
[AcousticBrainz](http://acousticbrainz.org/), getting detailed track
information. Some of that is low-level audio data provided by
[Essentia](http://essentia.upf.edu/documentation/), while many other
fields are derived from that low-level information.

I looked around for explanations of the new fields. The AcousticBrainz
[accuracy page](http://acousticbrainz.org/datasets/accuracy) lists the
derived fields, along with information about their accuracy. Combine
that with the [Essentia music
descriptors](http://essentia.upf.edu/documentation/streaming_extractor_music.html#music-descriptors)
and honestly I still have no idea what’s going on. It seems fascinating,
though. I plan to look at the code for these projects when I get some
spare time.

**`config.yml`**

```yaml
directory: ~/Music
import:
  copy: no
  write: no
plugins: acousticbrainz
```

    $ pip install requests

    $ beet acousticbrainz

That took a while (about 12 hours).

Okay I don’t understand all of these values, but I like it well enough
to write them back. I think I like this approach of treating the beets
database as a staging area before committing to the original files.

Honestly why does Tori Amos have the highest danceability score for
every query? That confuses me.

### Querying the fancy fields

#### Use Types

#### Null Fields

AcousticBrainz couldn’t find a match for every track.

    $ beet ls -f \
        '$chords_key $chords_scale - $rhythm - $bpm $average_loudness $danceable - $artist - $title' \
        ^danceable::^$ \
        danceable+ average_loudness+ bpm+

### BETTER GENRES

I usually ignore genre classification in my library. Using the lastgenre
plugin

    $ pip install pylast

### Acoustic Fingerprinting

    $ beet stats mb_trackid::^$
    Tracks: 1601
    Total time: 4.6 days
    Approximate total size: 9.5 GiB
    Artists: 550
    Albums: 233
    Album artists: 190

I wonder if acoustic fingerprinting could help me here. The [Chromaprint
plugin](http://beets.readthedocs.io/en/v1.4.3/plugins/chroma.html)
relies on [pyacoustid](https://github.com/beetbox/pyacoustid), which
relies on the [Chromaprint](https://acoustid.org/chromaprint) library.

    $ sudo zypper in libchromaprint-devel
    ...
    $ pip install pyacoustid

Now I can enable the Chromaprint plugin.

```yaml
plugins: acousticbrainz types lastgenre chroma
```

Beets gets acoustic fingerprints for any new music, and I can use the
`fingerprint` command to get them for music already in my library.

    $ beet fingerprint

That helped Beets identify a few hundred more tracks.

    beet stats mb_albumid::^$
    Tracks: 1085
    Total time: 3.1 days
    Approximate total size: 6.3 GiB
    Artists: 316
    Albums: 155
    Album artists: 126

Good enough for me!

## Playing

It’s great fun to get all this information about my music, but can I use
it to help pick what music to play? Turns out I can, even without
switching from Rhythmbox.

### Playlists

I can create one-off playlists by redirecting a query to a text file.

    $ beet ls -f '$path' genre:Metal ^danceable::^$ danceable:0.8.. bpm:90.. danceable- average_loudness- bpm- > dance-metal.m3u
    $ head dance-metal.m3u
    /home/random/Music/Marilyn Manson/Antichrist Superstar/14 - Minute of Decay.ogg
    /home/random/Music/Marilyn Manson/Smells Like Children [EP]/12 Dance Of The Dope Hats [Remix].m4a
    /home/random/Music/Compilations/The Matrix Reloaded/1-10 Dread Rock.m4a
    /home/random/Music/Compilations/The Matrix Reloaded/1-03 Reload.m4a
    /home/random/Music/Marilyn Manson/Antichrist Superstar/15 - The Reflecting God.ogg
    /home/random/Music/Marilyn Manson/Mechanical Animals/08 I Want To Disappear.m4a
    /home/random/Music/Compilations/The Matrix Reloaded/1-06 The Passportal.m4a
    /home/random/Music/Mount Eerie/Wind_s Poem/10 (something).mp3
    /home/random/Music/Marilyn Manson/Antichrist Superstar/12 - Antichrist Superstar.ogg

(process screenshot)

  - :plus:
  - From File
  - Browse to location
  - Select
  - Enter the name

I can also use the [Smart Playlist
plugin](http://beets.readthedocs.io/en/v1.4.3/plugins/smartplaylist.html)
if I want beets to automatically update the playlist whenever I add new
music.

I will be looking at alternate music players like MPD soon — just not
today.

## What Next?

  - Playing music with MPD
  - Getting music stats
