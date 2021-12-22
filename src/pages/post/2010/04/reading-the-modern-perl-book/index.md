---
aliases:
- /blogspot/2010/04/06_reading-modern-perl-book.html
- /post/2010/reading-modern-perl-book/
- /2010/04/06/reading-the-modern-perl-book/
category: blogspot
date: 2010-04-06 00:00:00
layout: layout:PublishedArticle
slug: reading-the-modern-perl-book
tags:
- perl
title: Reading the Modern Perl Book
uuid: a7d3cf66-46b8-470e-944e-958191200704
---

<p>I'm in the Perl phase of my language obsession rotation. I've created a handy language obsession table you can use to simulate the behavior for your favorite <a href="http://sjgames.com/gurps/">GURPS</a> Geek campaign.</p>
<!--more-->

<p>Roll 3d6 for the subject.</p>

<table>
<thead>
  <tr>
    <th>Roll</th>
    <th>Result</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>3-6</td>
    <td><a href="http://perl.org">Perl</a></td>
  </tr>
  <tr>
    <td>7-9</td>
    <td><a href="http://python.org">Python</a></td>
  </tr>
  <tr>
    <td>10-11</td>
    <td><a href="http://www.ruby-lang.org/en/">Ruby</a></td>
  </tr>
  <tr>
    <td>12-13</td>
    <td><a href="http://www.parrot.org/">Parrot</a></td>
  </tr>
  <tr>
    <td>14</td>
    <td><a href="http://php.net">PHP</a></td>
  </tr>
  <tr>
    <td>15-18</td>
    <td>Something shiny I found on the Web. You can get plausible results by selecting a random entry from the <a href="http://en.wikipedia.org/wiki/List_of_programming_languages">Wikipedia list of programming languages</a>.
    </td>
  </tr>
</tbody>
</table>

<p>Every week after the first, roll 1d6.</p>

<table>
<thead>
  <tr>
    <th>Roll</th>
    <th>Result</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>1-3</td><td>Continue last week's  language</td>
  </tr>
  <tr>
    <td>4-6</td><td>Roll on Table 1 for a new language</td>
  </tr>
</tbody>
</table>

<p>Alternately, you can set a duration of 1d6 weeks. That's handy for an ADHD NPC geek, where you don't want to check every week. Note that this is free time obsession. The language at <code>$work</code> is whatever <code>$work</code> requires.</p>

<p>I don't know why I felt the need to share this. I've already spent more time on that silly table than the actual subject I wanted to write about.</p>

<p>So anyways - I'm messing about with Perl. I have been reading chromatic's <a href="http://modernperlbooks.com/mt/index.html">Modern Perl blog</a> for a while - even when I'm not in a Perl cycle. It's good, you should try it out. He presents a needed perspective on Perl as something more than a musty system administration language.</p>

<p>chromatic is also writing a book and <a href="http://github.com/chromatic/modern_perl_book">maintaining the draft on github</a>. I finally decided I wanted to read that draft. The README and a tiny bit of Git knowledge provide all I need.</p>

<pre>
$ git clone git://github.com/chromatic/modern_perl_book.git
$ cd modern_perl_book
$ perl build/tools/build_chapters.pl
</pre>

<p>Now there is a handful of POD files in build/chapters which I could read with perldoc.</p>

<pre>
$ ls build/chapters
chapter_01.pod  chapter_03.pod  chapter_05.pod  chapter_07.pod  chapter_09.pod  chapter_11.pod  chapter_13.pod  chapter_15.pod
chapter_02.pod  chapter_04.pod  chapter_06.pod  chapter_08.pod  chapter_10.pod  chapter_12.pod  chapter_14.pod  chapter_16.pod
$ perldoc build/chapters/chapter_01.pod
</pre>

<p>
I can also generate HTML for those days when perldoc just isn't making me happy.</p>

<pre>
$ perl build/tools/build_html.pl
Can't locate Pod/PseudoPod/HTML.pm in @INC (@INC contains: /usr/local/lib/perl5/5.10.1/darwin-2level /usr/local/lib/perl5/5.10.1 /usr/local/lib/perl5/site_perl/5.10.1/darwin-2level /usr/local/lib/perl5/site_perl/5.10.1 /usr/local/lib/perl5/site_perl .) at build/tools/build_html.pl line 6.
BEGIN failed--compilation aborted at build/tools/build_html.pl line 6.
</pre>

<p>
Oops. It looks like there's a dependency. No problem.
</p>

<pre>
$ sudo cpan Pod::PseudoPod::HTML
$ perl build/tools/build_html.pl
$ ls build/html
chapter_01.html chapter_04.html chapter_07.html chapter_10.html chapter_13.html chapter_16.html
chapter_02.html chapter_05.html chapter_08.html chapter_11.html chapter_14.html style.css
chapter_03.html chapter_06.html chapter_09.html chapter_12.html chapter_15.html
</pre>

<p>
Now I can open the chapters in my favorite Web browser.
</p>

<pre>
$ elinks build/html/chapter_01.html
</pre>

<p>
From here, I can pay attention to chromatic's <a href="http://twitter.com/chromatic_x">tweets</a> - or his <a href="http://identi.ca/chromatic">dents</a>, since he seems more active on Identi.ca - or watch the <a href="http://github.com/chromatic/modern_perl_book">modern_perl_book repository on github</a>. Whenever he mentions new content, I will refresh and rebuild.
</p>

<pre>
$ git pull
$ perl build/tools/build_chapters.pl
$ perl build/tools/build_html.pl
</pre>

<p>I don't want to remember three whole commands. Am I taking <a href="http://c2.com/cgi/wiki?LazinessImpatienceHubris">Laziness</a> too far? Perhaps. Nevertheless, here's a Perl script to handle the task. It should only rebuild the chapters and HTML if there was an update in the repository.</p>

    #!/usr/bin/env perl
    # refresh.pl

    use Modern::Perl;

    my $git_pull = `git pull`;

    if ( $git_pull =~ m{\AAlready up-to-date.} ) {
        say "No changes to book.";
    }
    else {
        print $git_pull; # Show what updates were made.

        say "Building chapters.";
        system qw(perl build/tools/build_chapters.pl);

        say "Building HTML.";
        system qw(perl build/tools/build_html.pl);

        say "All done. Enjoy the update!";
    }