---
category: Tools
date: 2020-06-14 22:30:00
description: Trying out another windows package manager
draft: false
format: micro
layout: layout:PublishedArticle
slug: winget
tags:
- windows
- package manager
title: winget
uuid: 8962db7d-b4d0-4720-9a3a-4fbfb5633391
---

[winget][winget] is a command line package manager for Windows 10, open-sourced
under the [MIT License][mit].  Roughly equivalent to `apt` or `brew`.  If you
already know and love [Chocolatey][chocolatey], you’re fine.  Stick with that
for now. `winget` shows promise though.

The other night I installed [Strawberry Perl][strawberry-perl] and played with
[Image::ExifTool][image-exiftool] a tiny bit.

Yesterday I successfully installed Emacs and started doing real work writing
Perl code with it.

Exciting!

:::note

Well, not *work* work.  The new job doesn’t start until tomorrow, and is mostly
[Python][python].

:::

## How do I get Winget?

`winget` is still in preview.  You can get it as part of the [Windows
Insider][windows-insider] program, like me.  Slow Ring should be fine.  If you
don’t feel like taking the risk on a preview release of Windows, you can grab
it from the [winget-cli repository][winget-cli-repo].

## Finding and installing stuff with ``winget``

One goal when in Windows is to *use* Windows, and not just spend all day hiding
in WSL.  If I want to use Windows, I need [Perl][perl].

Hey, I’ll allow myself a few crutches here and there.

``` text
PS > winget search perl
Name            Id                            Version  Matched
----------------------------------------------------------------
Strawberry Perl StrawberryPerl.StrawberryPerl 5.30.2.1
Xampp           ApacheFriends.Xampp           7.4.6    Tag: Perl
```

Ooh, [XAMPP][xampp].  I haven't messed with that in years.

But no I'm just here for Perl today.  Strawberry Perl is an excellent Perl
setup for Windows.  Provides all the core stuff, a bunch of [useful
extras][useful-extras], and the tools you need to install additional libraries.

`winget show` displays additional details about a package.

``` text
PS > winget show StrawberryPerl
Found Strawberry Perl [StrawberryPerl.StrawberryPerl]
Version: 5.30.2.1
Publisher: strawberryperl.com project
Description: Strawberry Perl is a perl environment for MS Windows containing all you need to run and develop perl
applications. It is designed to be as close as possible to perl environment on UNIX systems.
Homepage: http://strawberryperl.com/
License: Perl.org
Installer:
  SHA256: 2365e89623b496ca530443a362e765f3e8de9daa744b07924b17ae7aa0b06002
  Download Url: http://strawberryperl.com/download/5.30.2.1/strawberry-perl-5.30.2.1-32bit.msi
  Type: Msi
```

Yep, that's what I want.

``` text
PS > winget install StrawberryPerl
```

Things do get automatically added to your path, but not right away.  Somebody
more familiar with Windows probably knows what to do.  Me?  When it doesn't
catch right away I log out and back in.  That always does the trick.

``` text
PS > perl --version
This is perl 5, version 30, subversion 2 (v5.30.2) built for MSWin32-x86-multi-thread-64int

Copyright 1987-2020, Larry Wall

Perl may be copied only under the terms of either the Artistic License or the
GNU General Public License, which may be found in the Perl 5 source kit.

Complete documentation for Perl, including FAQ lists, should be found on
this system using "man perl" or "perldoc perl".  If you have access to the
Internet, point your browser at http://www.perl.org/, the Perl Home Page.
```

Now what about all the other package manger functionality?

## What about updating, listing, uninstalling, etc?

Um.  Well.  I mentioned `winget` is in preview, right?  Check the development
[roadmap][].

[winget]: https://docs.microsoft.com/en-us/windows/package-manager/winget/
[mit]: https://github.com/microsoft/winget-cli/blob/master/LICENSE
[chocolatey]: https://chocolatey.org/
[image-exiftool]: https://metacpan.org/release/Image-ExifTool
[strawberry-perl]: https://strawberryperl.com
[python]: /tags/python
[windows-insider]: https://insider.windows.com/en-us/
[winget-cli-repo]: https://github.com/microsoft/winget-cli
[perl]: /tags/perl
[xampp]: https://www.apachefriends.org/index.html
[useful-extras]: http://strawberryperl.com/release-notes/5.30.2.1-64bit.html
[roadmap]: https://github.com/microsoft/winget-cli/blob/master/doc/windows-package-manager-v1-roadmap.md