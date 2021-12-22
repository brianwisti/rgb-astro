---
aliases:
- /2019/11/03/building-rakudo-and-moarvm-on-linux/
category: Tools
date: 2019-11-03
description: In which I rediscover `make && make test && make install`
layout: layout:PublishedArticle
slug: building-rakudo-and-moarvim-on-linux
tags:
- raku lang
- perl6
- linux
title: Building Rakudo and Moarvm on Linux
updated: 2021-08-21
uuid: 0e6b0789-3ea0-4461-be50-9c4f89190c71
---

[Rakubrew]: /post/2020/05/setting-up-raku-with-rakubrew

<aside class="admonition tldr">
  <p class="admonition-title">tl;dr</p>

2021-08-21
: skip all this and use [Rakubrew][]

</aside>

Not instructions, but a brain dump of compiling and checking a
[Rakudo](https://rakudo.org) installation.

Windows? No problem.

    > choco install rakudo

macOS? No problem.

    $ brew install rakudo

Linux?

    $ brew install rakudo

Well…

    ==> Installing dependencies for rakudo: moarvm and nqp
    ==> Installing rakudo dependency: moarvm
    ==> Downloading https://github.com/MoarVM/MoarVM/releases/download/2019.07.1/MoarVM-2019.07.1.tar.gz
    Already downloaded: /home/randomgeek/.cache/Homebrew/downloads/2c331d2b583c39890ed5fd765cea551c9e171136038a6a400217c7725ae60a9d--MoarVM-2019.07.1.tar.gz
    ==> perl Configure.pl --has-libatomic_ops --has-libffi --has-libtommath --has-libuv --optimize --prefix=/home/linuxbrew/.linuxbrew/Cellar/moarvm/2019.07.1
    ==> make realclean
    ==> make
    Last 15 lines from /home/randomgeek/.cache/Homebrew/Logs/moarvm/03.make:
    compiling src/jit/x64/emit.o
    linking libmoar.so
    /usr/bin/ld: /home/linuxbrew/.linuxbrew/lib/libtommath.a(bn_mp_exptmod_fast.o): relocation R_X86_64_32S against symbol `mp_reduce_2k' can not be used when making a shared object; recompile with -fPIC
    /usr/bin/ld: /home/linuxbrew/.linuxbrew/lib/libtommath.a(bn_mp_prime_is_prime.o): relocation R_X86_64_32 against symbol `ltm_prime_tab' can not be used when making a shared object; recompile with -fPIC
    /usr/bin/ld: /home/linuxbrew/.linuxbrew/lib/libtommath.a(bn_mp_rand.o): relocation R_X86_64_32 against `.rodata.str1.1' can not be used when making a shared object; recompile with -fPIC
    /usr/bin/ld: /home/linuxbrew/.linuxbrew/lib/libtommath.a(bn_mp_read_radix.o): relocation R_X86_64_32S against symbol `mp_s_rmap_reverse' can not be used when making a shared object; recompile with -fPIC
    /usr/bin/ld: /home/linuxbrew/.linuxbrew/lib/libtommath.a(bn_s_mp_exptmod.o): relocation R_X86_64_32 against symbol `mp_reduce' can not be used when making a shared object; recompile with -fPIC
    /usr/bin/ld: /home/linuxbrew/.linuxbrew/lib/libtommath.a(bn_mp_cnt_lsb.o): relocation R_X86_64_32S against `.rodata' can not be used when making a shared object; recompile with -fPIC
    /usr/bin/ld: /home/linuxbrew/.linuxbrew/lib/libtommath.a(bn_mp_is_square.o): relocation R_X86_64_32S against `.rodata' can not be used when making a shared object; recompile with -fPIC
    /usr/bin/ld: /home/linuxbrew/.linuxbrew/lib/libtommath.a(bn_mp_kronecker.o): relocation R_X86_64_32S against `.rodata' can not be used when making a shared object; recompile with -fPIC
    /usr/bin/ld: /home/linuxbrew/.linuxbrew/lib/libtommath.a(bn_mp_prime_is_divisible.o): relocation R_X86_64_32 against symbol `ltm_prime_tab' can not be used when making a shared object; recompile with -fPIC
    /usr/bin/ld: /home/linuxbrew/.linuxbrew/lib/libtommath.a(bn_mp_abs.o): relocation R_X86_64_PC32 against symbol `mp_copy' can not be used when making a shared object; recompile with -fPIC
    /usr/bin/ld: final link failed: bad value
    collect2: error: ld returned 1 exit status

Awkward.

I don’t want the `apt` version, because it’s from last year. Maybe I
want [rakudobrew](https://github.com/tadzik/rakudobrew)?

Well — maybe later. At the moment I just want to see if Rakudo builds at
all.

Let’s break down the big shell alias from Zoffix’s [Instructions to
build rakudo from source](https://github.com/zoffixznet/r) into discrete
steps.

    $ git clone https://github.com/rakudo/rakudo/ ~/rakudo
    $ echo 'export PATH="$HOME/rakudo/install/bin:$HOME/rakudo/install/share/perl6/site/bin:$PATH"' >> ~/.bashrc
    $ cd ~/rakudo
    $ git checkout master
    $ git pull
    $ git checkout $(git describe --abbrev=0 --tags)
    $ perl Configure.pl --gen-moar --gen-nqp --backends=moar
    $ make

And just to be on the safe side:

    $ make test
    Test Summary Report
    -------------------
    t/09-moar/Line_Break__LineBreak.t                             (Wstat: 0 Tests: 2 Failed: 0)
      TODO passed:   1
    t/09-moar/General_Category__extracted-DerivedGeneralCategory.t (Wstat: 0 Tests: 1 Failed: 0)
      TODO passed:   1
    Files=98, Tests=1760, 36 wallclock secs ( 0.34 usr  0.08 sys + 130.23 cusr  9.24 csys = 139.89 CPU)
    Result: PASS

Great!

    $ make install
    $ source ~/.bashrc

Now, a little Raku one-liner test.

    $ perl6 -e 'say "Yo, World! This is $*PERL - specifically: { ($*PERL, $*VM, $*DISTRO).map({ $_.gist })}"'
    Yo, World! This is Perl 6 - specifically: Perl 6 (6.d) moar (2019.07.1) ubuntu (19.10)

Using `gist` instead of normal stringification because I wanted all the
details. You can see with `$*PERL` inside the string that `Str` is not
for the gory details.

It’s a bit like `str` versus `repr` in the [Python](/tags/python) world.

Anyways yay, it worked\! If I ever get enough free time, I might
investigate the `brew` bug. But it took me three days to finish *this*
post.

[Andrew Shitov](https://raku.online/) already prepared for the “Perl 6”
→ “Raku” name transition with a shell alias:

    $ alias raku='perl6'

Not the worst way to keep the new name in mind.