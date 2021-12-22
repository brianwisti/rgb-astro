---
aliases:
- /programming/2014/12/13_duplicate-files.html
- /post/2014/duplicate-files/
- /2014/12/13/finding-and-removing-duplicate-files/
category: programming
date: 2014-12-13 00:00:00
description: Perl CPAN modules to simplify file cleanup
layout: layout:PublishedArticle
slug: finding-and-removing-duplicate-files
tags:
- perl
- files
title: Finding and Removing Duplicate Files
uuid: df061bdd-5c6e-42be-a1e6-3b24d171fe77
---

I had a clever idea a couple months ago: to write a blog post detailing
how to find recursively find duplicate files in a folder. My technique
was good enough: track file sizes, find files that had the same file
size and [MD5 hash](http://en.wikipedia.org/wiki/MD5#MD5_hashes), and
display the resulting list. It wasn’t foolproof, but it showed some
thought. After spending a little too much time on the post, I realized I
had never checked [CPAN](http://www.cpan.org/). Of course there is
already a module to handle that exact task.

## The Problem

So here is my problem. I have — let’s see —

    $ find ~/Sync -type f | wc -l
        44388

I have 44,388 files in my Sync folder.

I organized my home machines recently. When I say "organized" I mean
that everything got swept into my `~/Sync` folder to deal with later.
The refuse of several years squirreling files into random locations is
now sitting in that single folder.

Well, now it is time to clean that single folder up. I want to find and
delete duplicate files. I planned to focus on image files, but
File::Find::Duplicates makes it easier to find *all* duplicates.

## The Solution

[File::Find::Duplicates](https://metacpan.org/pod/File::Find::Duplicates)
exports a `find_duplicate_files` subroutine, which finds the duplicate
files in a list of folders.

First tell me how many sets of duplicates I have.

**`count-dupes.pl`**

```perl
use 5.20.0;
use warnings;

use File::Find::Duplicates;

my $root       = "$ENV{HOME}/Sync";
my @dupes      = find_duplicate_files( $root );
my $dupe_count = @dupes;

say "Found $dupe_count sets of duplicates in $root";
```

This will tell me how much work is ahead of me.

    $ perl count-dupes.pl
    Found 3465 sets of duplicates in /Users/brian/Sync

Removing the files was easy, but it rattled my nerves.

**`remove-dupes.pl`**

```perl
use 5.20.0;
use warnings;

use Carp qw(croak);
use File::Basename;
use File::Find::Duplicates;

my $root  = "$ENV{HOME}/Sync";
my @dupes = find_duplicate_files( $root );

my $deleted;

for my $dupeset ( @dupes ) {
  # Pick a file to serve as primary.
  # Using string-based sorting as arbitrary rule to establish what's first.
  my ( $prime, @secondary ) = sort @{ $dupeset->files };

  # Delete the duplicates
  for my $file ( @secondary ) {
    unlink $file
      or croak "Unable to unlink $file: $!";
    $deleted++;
  }

}

say "Deleted $deleted files.";
```

I fought the temptation to add progress bars or anything like that.
Focus on getting the job done. I can add work if I end up revisiting
this task later.

    $ perl remove-dupes.pl
    Deleted 3509 files.

I removed a lot of files. Are there still any duplicates?

    $ perl count-dupes.pl
    Found 0 sets of duplicates in /Users/brian/Sync

Thing is, I suspect that my `Sync` directory contains many empty
subdirectories.

## About Those Directories

[File::Find::Rule::DirectoryEmpty](https://metacpan.org/pod/File::Find::Rule::DirectoryEmpty)
helps with exactly that problem. It extends the useful
[File::Find::Rule](https://metacpan.org/pod/File::Find::Rule) module to
simplify finding files with characteristics you define.

**`find-leaves.pl`**

```perl
use 5.20.0;
use warnings;

use File::Find::Rule::DirectoryEmpty;

my $root = "$ENV{HOME}/Sync";
my @empties = File::Find::Rule
  ->directoryempty()
  ->in( $root );
my $empty_count = @empties;
say "$empty_count empty directories";
```

    $ perl find-leaves.pl
    2904 empty directories

Yow. I can delete those directories, but then there could be parent
directories that are now empty, and then grandparent directories, and
then —

You know what? Just keep looking and deleting until there no more empty
directories.

**`remove-leaves.pl`**

```perl
use 5.20.0;
use warnings;

use Carp qw(croak);
use File::Find::Rule::DirectoryEmpty;

my $deleted = 0;
my $root    = "$ENV{HOME}/Sync";
my $found   = File::Find::Rule->new()->directoryempty();

while ( my @empties = $found->in( $root ) ) {
  my $empty_count = @empties;
  say "Found $empty_count empty directories";

  for my $empty ( @empties ) {
    rmdir $empty
      or croak "Unable to rmdir $empty: $!";
    $deleted++;
  }
}

say "$deleted empty folders deleted";
```

I like a little logging on each pass so that I know what my program is
seeing.

    $ perl remove-leaves.pl
    Found 2904 empty directories
    Found 529 empty directories
    Found 29 empty directories
    Found 5 empty directories
    3467 empty folders deleted

I might dig in later to *actually* organize the remaining files. I may
even automate it with some Perl. This is good enough for today, though.

## Done

    $ find ~/Sync/ -type f | wc -l
       40880

Now I have 40,880 files in my `~/Sync` folder. Maybe I should have
counted directories too.