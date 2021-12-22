---
aliases:
- /blogspot/2007/12/05_perl-510-beta-everywhere.html
- /post/2007/perl-510-beta-everywhere/
- /2007/12/05/perl-5.10-beta-everywhere/
- /post/2007/12/perl-5.10-beta-everywhere/
category: blogspot
date: 2007-12-05 00:00:00
layout: layout:PublishedArticle
slug: perl-510-beta-everywhere
tags:
- perl
title: Perl 5.10 beta Everywhere
uuid: ee25036c-51f2-4f71-81e4-405318c6157c
---

I decided to install Perl 5.10 on all my machines after the thrill of installing ActivePerl 5.10 beta on my Windows VM last night. Yes yes, it is true that strange things will thrill me.
<!--more-->

I downloaded and compiled devel.tar.gz from perl.org for my Linux install. I just need to remember that the binary is called perl5.9.5 and 'use 5.010;' will fail. I need to do 'use feature qw(:5.10);' on that machine. Good to know, that was mostly an experiment.

The Mac gets the beta. I was so lazy tonight. How lazy was I? Rather than get up and walk eight feet to the Mac I did the install via ssh.

    $ ssh 192.168.1.100
    $ elinks activestate.com
    (find and download the dmg of the beta)
    $ hdiutil attach ActivePerl-5.10.0.1000-Beta-darwin-8.10.0-gcc-283192.dmg
    $  sudo installer -pkg /Volumes/ActivePerl-5.10/ActivePerl-5.10.pkg/ -target / -verbose -dumplog > ~/install.log 2>&1
    $  /usr/local/ActivePerl-5.10/bin/perl -E 'say "Hello";'
    Hello

Then I fired up vim and added some lines to my ~/.bash_profile

``` bash
export ACTIVEPERL=/usr/local/ActivePerl-5.10
export PATH=$ACTIVEPERL/site/bin:$ACTIVEPERL/bin:$PATH
export PERLMANPATH=$ACTIVEPERL/site/man:$ACTIVEPERL/man:$PERLMANPATH
```

    $ . ~/.bash_profile
    $ which perl
    /usr/local/ActivePerl-5.10/bin/perl

Then I adjusted the settings in my vimrc so that Perl files are associated with the beta. That's a bit of specialized yet trivial monkey business though, so I won't bother to show it.

Oh yeah, I nearly forgot to unmount the dmg.

    $ hdiutil detach /Volumes/ActivePerl-5.10

Then I was so ridiculously lazy that I just spent 20 minutes describing a 3 minute process, just in case I need to install with a dmg via ssh again in the future.