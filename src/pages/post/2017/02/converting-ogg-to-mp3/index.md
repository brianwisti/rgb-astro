---
aliases:
- /post/2017/converting-ogg-to-mp3/
- /2017/02/25/converting-ogg-to-mp3/
category: Programming
date: 2017-02-25
draft: false
layout: layout:PublishedArticle
slug: converting-ogg-to-mp3
tags:
- perl
- raku lang
- perl 6
- music
title: Converting OGG To MP3
uuid: e554fc83-917a-4521-8dbc-bc3e658c6f74
---

[Ogg Vorbis]: http://vorbis.com/
[FFmpeg]: http://ffmpeg.org/
[Perl 6]: https://raku.org/

I have ignored my MacBook Pro for a few months. Now my iTunes and Rhythmbox
music libraries are out of sync. The Rhythmbox library includes a handful of
[Ogg Vorbis][] files. Because iTunes does not support Ogg by default, I will use
[FFmpeg][] to convert those files to MP3. For the sake of novelty, [Perl 6][] is
the glue language for the task.

I know. I could go digging in the box at the bottom of the back of the closet
and rerip those CDs. But the closet is all the way over there. I’m right here. I
don’t feel like getting up, and I do feel like using Perl 6 for something.

Don’t you judge me.

<aside class="admonition">

This is a quick journey into Perl 6 for my own amusement, and not a tutorial.
I linger on the stuff that caught my attention rather than explain all the details.
Still -- hopefully it’s useful to you!

</aside>

## Perl 6 Star Notes

[Rakudo Star]: http://rakudo.org/downloads/star/
[Rakudo]: http://rakudo.org/

I installed [Rakudo Star][] 2017.01 from source. Some of this information may be
useful to others poking at a new [Rakudo][] installation.

### Did I Set Up My Path Correctly?

I misread the path setup instructions after `make` finished,
and ended up flailing in confusion for several minutes before I double-checked the Makefile.
You can skip the flailing by reading correctly or by rerunning the "welcome message."

    $ make welcome-message

    Rakudo Star has been built and installed successfully.
    Please make sure that the following directories are in PATH:
      /home/random/src/rakudo-star-2017.01/install/bin
      /home/random/src/rakudo-star-2017.01/install/share/perl6/site/bin

### What Version Of Perl 6 Do I Have?

Just throwing it in so you can see what I’m working with.

    $ perl6 --version
    This is Rakudo version 2017.01 built on MoarVM version 2017.01
    implementing Perl 6.c.

### What Modules Do I Have?

[zef]: https://github.com/ugexe/zef
[usage summary]: https://github.com/ugexe/zef#usage

As of version 2017.01, Rakudo includes [zef][] as its default package manager.
See its [usage summary][] for details of finding and installing modules.
For the moment I want to know what came with my Rakudo Star installation.

    $ zef list --installed
    ===> Found via /home/random/src/rakudo-star-2017.01/install/share/perl6
    CORE:ver('6.c'):auth('perl')
    ===> Found via /home/random/src/rakudo-star-2017.01/install/share/perl6/site
    Test::Mock:ver('1.3')
    LWP::Simple:ver('0.090'):auth('Cosimo Streppone')
    Pod::To::HTML:ver('0.3.7')
    panda:ver('2016.02')
    NativeHelpers::Blob:ver('0.1.10'):auth('github:salortiz')
    SVG
    JSON::Tiny
    Grammar::Debugger
    zef:auth('github:ugexe')
    HTTP::Easy:ver('1.1.0')
    XML::Writer
    Template::Mojo:ver('0.1')
    File::Which
    File::Temp
    File::Directory::Tree:auth('labster')
    TAP::Harness::Prove6:ver('0.0.1'):auth('Leon Timmermans')
    Terminal::ANSIColor:ver('0.2')
    DBIish:ver('0.5.9')
    SVG::Plot
    Template::Mustache:auth('github:softmoth')
    File::Find:ver('0.1')
    Debugger::UI::CommandLine
    Grammar::Profiler::Simple:ver('0.01'):auth('Jonathan Scott Duff')
    Pod::To::BigPage:ver('0.2.1'):auth('Wenzel P. P. Peppmeyer')
    PSGI:ver('1.2.0')
    p6doc
    HTTP::Status
    Linenoise:ver('0.1.1'):auth('Rob Hoelz')
    JSON::Fast:ver('0.7')
    Native::Resources:ver('0.1.0'):auth('Rob Hoelz')
    Shell::Command
    LibraryMake:ver('1.0.0'):auth('github:retupmoca')
    MIME::Base64:ver('1.2'):auth('github:retupmoca')
    Digest::MD5:ver('0.05'):auth('Cosimo Streppone')
    URI:ver('0.1.2')
    JSON::RPC:ver('0.17.1'):auth('Pawel Pabian')

It would be nice if the output had a sort option.
I can sort myself, though I’d lose information about where the modules were found.

    $ zef list --installed | sort

I’m sure pull requests are welcome.

### How Do I Get At The Documentation?

Once you stop flailing with your setup and know what modules are installed,
use https://github.com/perl6/doc[p6doc] to read module documentation.

    $ p6doc File::Find

Okay I have my Rakudo Star installation sorted out.
Time for the task at hand.

## Quick question: How many?

How many Ogg files do I have, anyways?

    $ find ~/Music/ -name '*.ogg' | wc -l
    212

More than a handful, but still - that’s not too bad.
Let’s take a minute to look at the Perl 6 I used.

### Count The Files From Perl 6

[File::Find]: https://github.com/tadzik/File-Find
[File::Find::Rule]: https://metacpan.org/pod/File::Find::Rule
[lazy list]: https://docs.perl6.org/language/list.html#Lazy_Lists

In order to get a feel for what I’m doing in Perl 6, I’m going to use Perl 6 to count the Ogg files.
This task relies on [File::Find][], which comes with Rakudo Star.
Perl 6 File::Find works like Perl 5’s [File::Find::Rule][].
You describe characteristics of the files you’re looking for,
and it hands you back a [lazy list][] of files that match.

```
use v6;

use File::Find;

my $music_dir = %*ENV<HOME> ~ "/Music";
my @ogg_files = find(
    dir  => $music_dir,
    name => /\.ogg$/,
);
my $count = @ogg_files.elems;
say "I see $count Ogg files";
```

This does the same as the one-liner: look in `$HOME/Music` for and files suffixed with `.ogg`, and tell me how many matches it found.

    $ perl6 ogg-to-mp3.p6
    I see 212 Ogg files

Yay I get exactly the same number of files that `find` found!
Okay now I’m going to convert them to MP3.
I’ll put them in a working directory so that I don’t confuse Rhythmbox.

FFmpeg can handle conversion, but my string starts looking a bit funky thanks to funky Perl quoting rules.
Anyways.

```
use v6;

use File::Find;
use Audio::Taglib::Simple;

my $music_dir = %*ENV<HOME> ~ "/Music";
my @ogg_files = find(
  dir  => $music_dir,
  name => /\.ogg$/,
);

for @ogg_files -> $ogg_file {
  my $path = IO::Path.new($ogg_file);

  # Where will the converted file go?
  my $working_dir = "converted";
  my $new_dir = $path.dirname.subst($music_dir, $working_dir);
  my $new_file = $path.basename.subst($path.extension, "mp3");
  my $mp3_file = "$new_dir/$new_file";

  # Create the directory path if needed
  # (still returns True if $new_dir already exists)
  mkdir $new_dir;

  # Ask ffmpeg to convert.
  #   -y                    <- overwrite if $mp3_file exists
  #   -v warning            <- report warnings & errors but not general info
  #   -i "$ogg_file"        <- Read from here (quoted for spaces)
  #   -map_metadata "0:s:0" <- include title, artist, etc (quoted for P6 interpolation oddness)
  #   "$mp3_file"           <- write to here (quoted for spaces)
  my $captured = qqx{ffmpeg -y -v warning -i "$ogg_file" -map_metadata "0:s:0" "$mp3_file"};
  print $captured;
  print ".";
}
say "DONE";
```

[IO::Path]: https://docs.perl6.org/type/IO$COLON$COLONPath
[`qqx`]: https://docs.perl6.org/language/quoting#Shell_quoting_with_interpolation:_qqx

[IO::Path][] objects understand how file and directory paths work.
Constructing the `$mp3_file` filename was easy enough thanks to a little string substitution on the Path components.

[`qqx`][] shell quoting allows variable interpolation,
though Perl 6 saw `0:s:0` as a thing it needed to interpolate until I wrapped it in quotes.
It took me a while to figure out the correct FFmpeg invocation, so breaking it down in the comments made sense.
Oh and if there’s any output from the conversion I print it.

[types]: https://docs.perl6.org/type.html
[routines]: https://docs.perl6.org/routine.html
[modules]: https://modules.perl6.org/

<aside class="admonition">

I need to remind myself that I’m putting down notes here and not writing a tutorial,
but I suggest newcomers to Perl 6 explore the [types][] and [routines][].

Yes, Perl 6 syntax can be strange and intimidating.
You don’t need to learn all the syntax to get stuff done.
The types and routines hold most of what you need for daily work.
Can’t find it there?
Look at the [modules][].
Easy stuff should still be easy.
This is Perl, after all.

</aside>

### Quality Control

[Audio::Taglib::Simple]: https://github.com/zoffixznet/perl6-audio-taglib-simple

I used [Audio::Taglib::Simple][] to double-check my work while figuring out the correct `ffmpeg` incantaion.

    $ sudo apt-get install libtagc0
    $ zef install Audio::Taglib::Simple

```
use v6;
use Audio::Taglib::Simple;

for @*ARGS -> $mp3_file {
  my $mp3_tags = Audio::Taglib::Simple.new("$mp3_file");
  say "$mp3_file: {$mp3_tags.title} - {$mp3_tags.album} - {$mp3_tags.artist}";
  $mp3_tags.free;
}
```

This takes any command line arguments and presents a summary of track information for each argument.
It will choke if I hand it anything that’s not an MP3 file, but for an idle weekend thing on my own machine it’s fine.

    $ perl6 check-mp3.p6 converted/Melvins/Houdini/*
    converted/Melvins/Houdini/01 - Hooch.mp3
    Hooch - Houdini - Melvins
    converted/Melvins/Houdini/02 - Night Goat.mp3
    Night Goat - Houdini - Melvins
    converted/Melvins/Houdini/03 - Lizzy.mp3
    Lizzy - Houdini - Melvins
    converted/Melvins/Houdini/04 - Going Blind.mp3
    Going Blind - Houdini - Melvins
    converted/Melvins/Houdini/05 - Honey Bucket.mp3
    Honey Bucket - Houdini - Melvins
    converted/Melvins/Houdini/06 - Hag Me.mp3
    Hag Me - Houdini - Melvins
    converted/Melvins/Houdini/07 - Set Me Straight.mp3
    Set Me Straight - Houdini - Melvins
    converted/Melvins/Houdini/08 - Sky Pup.mp3
    Sky Pup - Houdini - Melvins
    converted/Melvins/Houdini/09 - Joan of Arc.mp3
    Joan of Arc - Houdini - Melvins
    converted/Melvins/Houdini/10 - Teet.mp3
    Teet - Houdini - Melvins
    converted/Melvins/Houdini/11 - Copache.mp3
    Copache - Houdini - Melvins
    converted/Melvins/Houdini/12 - Pearl Bomb.mp3
    Pearl Bomb - Houdini - Melvins
    converted/Melvins/Houdini/13 - Spread Eagle Beagle.mp3
    Spread Eagle Beagle - Houdini - Melvins

Cool. It worked.

### What Now?

[Syncthing]: https://syncthing.net/

I move the converted files to my `~/Sync` folder and let [Syncthing][] handle copying them to the Mac.
They import into iTunes and I’m all done!

Wait. I still have to sync the files that were imported to Rhythmbox as MP3 but aren’t on iTunes yet.

Not today, though.
