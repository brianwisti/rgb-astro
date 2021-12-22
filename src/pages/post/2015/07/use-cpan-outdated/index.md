---
aliases:
- /tools/2015/07/09_use-cpan-outdated.html
- /post/2015/use-cpan-outdated/
- /2015/07/09/use-cpan-outdated/
category: tools
date: 2015-07-09 00:00:00
layout: layout:PublishedArticle
slug: use-cpan-outdated
tags:
- perl
title: Use cpan-outdated
uuid: 950e9629-e941-4bca-b6e3-eeacffec3b7c
---

[cpan-outdated]: https://metacpan.org/pod/distribution/cpan-outdated/script/cpan-outdated
[TOKUHIROM]: https://metacpan.org/author/TOKUHIROM
[cpanminus]: https://metacpan.org/pod/App::cpanminus

Thought I'd share [TOKUHIROM][]'s [cpan-outdated][] tool, which simplifies the task of keeping your installed Perl 5 modules up to date. It simply lists available updates to Perl modules you have installed. That functionality is available in the CPAN shell with the `r` command, but it is hard to beat the convenience of the [cpan-outdated][] command line tool.
<!--more-->

## Installing cpan-outdated

cpan-outdated is available on CPAN as "App::cpanoutdated". Install it with your preferred tool - in my case, [cpanminus][].

```
$ cpanm App::cpanoutdated
```

Installation will put  `cpan-outdated` on your path.

## Using cpan-outdated

Like any good executable, [cpan-outdated][] has a `--help` option.

```
$ cpan-outdated --help
Usage:
        # print the list of distribution that contains outdated modules
        % cpan-outdated

        # print the list of outdated modules in packages
        % cpan-outdated -p

        # verbose
        % cpan-outdated --verbose

        # alternate mirrors
        % cpan-outdated --mirror file:///home/user/minicpan/

        # additional module path(same as cpanminus)
        % cpan-outdated -l extlib/
        % cpan-outdated -L extlib/

        # install with cpan
        % cpan-outdated | xargs cpan -i

        # install with cpanm
        % cpan-outdated    | cpanm
        % cpan-outdated -p | cpanm
```

Let's see what that looks like on my machine.

```
$ cpan-outdated
B/BI/BINGOS/Archive-Extract-0.76.tar.gz
P/PJ/PJF/autodie-2.29.tar.gz
X/XS/XSAWYERX/Dancer2-0.161000.tar.gz
B/BO/BOOK/DateTime-Format-Mail-0.402.tar.gz
E/ET/ETHER/HTTP-Message-6.07.tar.gz
N/NE/NEILB/Lingua-EN-FindNumber-1.31.tar.gz
S/SR/SRI/Mojolicious-6.13.tar.gz
B/BD/BDFOY/Test-File-1.44.tar.gz
E/ET/ETHER/Test-Pod-1.51.tar.gz
```

Use `-p` to just list packages without path information.

```
$ cpan-outdated -p
Archive::Extract
autodie
Dancer2
DateTime::Format::Mail
HTTP::Headers
Lingua::EN::FindNumber
Mojolicious
Test::File
Test::Pod
```

I find the `-p` output easier to read at a glance.

Pipe the output of [cpan-outdated][] to [cpanminus][] to immediately update the outdated modules.

```
$ cpan-outdated -p | cpanm
--> Working on Archive::Extract
Fetching http://www.cpan.org/authors/id/B/BI/BINGOS/Archive-Extract-0.76.tar.gz ... OK
Configuring Archive-Extract-0.76 ... OK
Building and testing Archive-Extract-0.76 ... OK
Successfully installed Archive-Extract-0.76 (upgraded from 0.74)
--> Working on autodie
Fetching http://www.cpan.org/authors/id/P/PJ/PJF/autodie-2.29.tar.gz ... OK
Configuring autodie-2.29 ... OK
Building and testing autodie-2.29 ... OK
Successfully installed autodie-2.29 (upgraded from 2.28)
--> Working on Dancer2
Fetching http://www.cpan.org/authors/id/X/XS/XSAWYERX/Dancer2-0.161000.tar.gz ... OK
Configuring Dancer2-0.161000 ... OK
Building and testing Dancer2-0.161000 ... OK
Successfully installed Dancer2-0.161000 (upgraded from 0.160003)
--> Working on DateTime::Format::Mail
Fetching http://www.cpan.org/authors/id/B/BO/BOOK/DateTime-Format-Mail-0.402.tar.gz ... OK
Configuring DateTime-Format-Mail-0.402 ... OK
Building and testing DateTime-Format-Mail-0.402 ... OK
Successfully installed DateTime-Format-Mail-0.402 (upgraded from 0.401)
--> Working on HTTP::Headers
Fetching http://www.cpan.org/authors/id/E/ET/ETHER/HTTP-Message-6.07.tar.gz ... OK
Configuring HTTP-Message-6.07 ... OK
Building and testing HTTP-Message-6.07 ... OK
Successfully installed HTTP-Message-6.07 (upgraded from 6.05)
--> Working on Lingua::EN::FindNumber
Fetching http://www.cpan.org/authors/id/N/NE/NEILB/Lingua-EN-FindNumber-1.31.tar.gz ... OK
Configuring Lingua-EN-FindNumber-1.31 ... OK
Building and testing Lingua-EN-FindNumber-1.31 ... OK
Successfully installed Lingua-EN-FindNumber-1.31 (upgraded from 1.30)
--> Working on Mojolicious
Fetching http://www.cpan.org/authors/id/S/SR/SRI/Mojolicious-6.13.tar.gz ... OK
Configuring Mojolicious-6.13 ... OK
Building and testing Mojolicious-6.13 ... OK
Successfully installed Mojolicious-6.13 (upgraded from 6.12)
--> Working on Test::File
Fetching http://www.cpan.org/authors/id/B/BD/BDFOY/Test-File-1.44.tar.gz ... OK
Configuring Test-File-1.44 ... OK
Building and testing Test-File-1.44 ... OK
Successfully installed Test-File-1.44 (upgraded from 1.43)
--> Working on Test::Pod
Fetching http://www.cpan.org/authors/id/E/ET/ETHER/Test-Pod-1.51.tar.gz ... OK
Configuring Test-Pod-1.51 ... OK
Building and testing Test-Pod-1.51 ... OK
Successfully installed Test-Pod-1.51 (upgraded from 1.50)
9 distributions installed
```

That's pretty much all there is to it! [cpan-outdated][] is a simple tool, but it fills its role perfectly.