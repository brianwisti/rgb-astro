---
aliases:
- /blogspot/2009/07/02_in-which-brian-whinges-about-perl-5.html
- /post/2009/in-which-brian-whinges-about-perl-5/
- /2009/07/02/in-which-brian-whinges-about-the-perl-5-release-schedule/
category: coolnamehere
date: 2009-07-02 00:00:00
layout: layout:PublishedArticle
slug: in-which-brian-whinges-about-the-perl-5-release-schedule
tags:
- perl
title: In Which Brian Whinges About The Perl 5 Release Schedule
updated: 2015-03-27 00:00:00
uuid: 5cab78f4-c480-474c-8194-7ed1f27f7cec
---

<aside>
<h3>Update: 2015-03-27</h3>

<p>
The current version of Perl 5 is 5.20.2. My complaints from this post have
been addressed and then some since 2009.
</p>

<h3>Update: 2010-02-23</h3>

<p>
I just have to say that none of this is personal against the pumpkings. It's a tough job, and not many people have the right combination of skills and time to pull it off. I just had thoughts I wanted to get off my chest.
</p>
</aside>

<h2>First, The Whinging</h2>

<p>Perl 5.10.0 was released on 18 December, 2007. <a href="http://modernperlbooks.com">chromatic</a>, a fairly prominent Perl hacker, has been pushing hard for some kind of update to Perl 5 since - well, probably about 19 December 2007. For their own reasons, the pumpkings have not been willing to produce such an update. That is annoying.</p>

<p>Now, don't get me wrong. I know Perl 5 is widely installed. I know Perl 5 can be a bit of a monster to patch and maintain. I know that large shops dread the release of a new Perl 5 because it will be a matter of minutes before their developers starting pleading for the update to be available to them so they can fix old annoyances in millions of lines of production code - okay, maybe only hundreds of thousands in that <em>particular</em> shop - that barely works. CPAN authors will release new versions of their libraries which don't work on the old Perl. Old code will break if it uses the new Perl.  There will be chaos. Panic. Forty years of darkness. The dead rising from the grave.  Human sacrifice, dogs and cats living together - mass hysteria.</p>

<p>That doesn't mean we should stop improving Perl 5, though. You don't have to update your code if doing so will cause your organization to spontaneously combust. The old versions of Perl 5 are <a href="http://www.cpan.org/src/">still available to download</a>. Older versions of CPAN modules are also readily available. Maintenance programmers can keep on being maintenance programmers and the rest of us can start working on new stuff. We won't combust. Please, for the sake of the language, put something out there that we can point and say that shows Perl 5 is still active!</p>

<p>I know, Perl's not dead. But to paraphrase Jello Biafra: <em>Perl's not dead, it just deserves to die when it becomes another stale maintenance language</em>.</p>

<p>I'm not even asking for Perl 5.12.0. I wouldn't mind. I'm asking for less than that, though. I'm asking for signs of life, a regular <em>blip</em> next to the "Latest Version" text at <a href="http://perl.org">http://perl.org</a>.  A bug fix release would be nice. </p>

<p>What prompted this bit of extended whining? Well, on the ride to work this morning I was thinking about chromatic's <a href="http://www.modernperlbooks.com/mt/2009/07/fearpm.html">latest post</a>, which got me thinking about his other posts, which got me thinking about how long it's been since Perl 5.10.0 was released. What has happened in the languages I pay attention to in the year and a half since 18 December 2007?</p>

<p>So I looked up the language releases as well as I could. Not the alphas, betas, or even the release candidates. Not the supplemental projects like <a href="https://metacpan.org/pod/Moose">Moose</a>, <a href="http://rubyonrails.com">Rails</a>, or <a href="http://pygame.org">Pygame</a> which add tons of fun to their respective languages and application domains. Just language releases, including bug fixes.</p>

<h2>Releases Between 18 December 2007 and 2 July 2009 of Languages I Care About</h2>

<h3>Python</h3>

<table>
<thead>
<tr><th>Version</th><th>Released On</th></tr>
</thead>
<tbody>
<tr><td>3.1.0</td><td>27 June 2009</td></tr>
<tr><td>2.6.2</td><td>14 April 2009</td></tr>
<tr><td>3.0.1</td><td>13 February 2009</td></tr>
<tr><td>3.0.0</td><td>3 December 2008</td></tr>
<tr><td>2.5.4</td><td>23 December 2008</td></tr>
<tr><td>2.5.3</td><td>19 December 2008</td></tr>
<tr><td>2.4.6</td><td>19 December 2008</td></tr>
<tr><td>2.6.1</td><td>4 December 2008</td></tr>
<tr><td>2.6.0</td><td>1 October 2008</td></tr>
<tr><td>2.4.5</td><td>11 March 2008</td></tr>
<tr><td>2.3.7</td><td>11 March 2008</td></tr>
<tr><td>2.5.2</td><td>21 February 2008</td></tr>
</tbody>
</table>
<p>Total releases since 18 December 2007: <em>12</em></p>

<h3>Ruby</h3>
<table>
<thead>
<tr>
<th>Version</th>
<th>Released On</th>
</tr>
</thead>
<tbody>
<tr>
<td>1.9.1-p129</td>
<td>12 May 2009</td>
</tr>
<tr>
<td>1.8.7-p160</td>
<td>18 April 2009</td>
</tr>
<tr>
<td>1.8.6-p368</td>
<td>18 April 2009</td>
</tr>
<tr>
<td>1.9.1</td>
<td>30 January 2009</td>
</tr>
<tr>
<td>1.8.7-p72</td>
<td>11 August 2008</td>
</tr>
<tr>
<td>1.8.6-p287</td>
<td>11 August 2008</td>
</tr>
<tr>
<td>1.8.7</td>
<td>31 April 2008</td>
</tr>
<tr>
<td>1.9.0</td>
<td>25 December 2007</td>
</tr>
</tbody>
</table>
<p>Total releases since 18 December 2007: <em>8</em></p>
<h3>PHP</h3>
<table>
<thead>
<tr>
<th>Version</th>
<th>Released On</th>
</tr>
</thead>
<tbody>
<tr>
<td>5.3.0</td>
<td>30 June 2009</td>
</tr>
<tr>
<td>5.2.10</td>
<td>18 June 2009</td>
</tr>
<tr>
<td>5.2.9</td>
<td>26 February 2009</td>
</tr>
<tr>
<td>5.2.8</td>
<td>8 December 2008</td>
</tr>
<tr>
<td>5.2.7</td>
<td>4 December 2008</td>
</tr>
<tr>
<td>4.4.9</td>
<td>7 August 2008</td>
</tr>
<tr>
<td>5.2.6</td>
<td>1 May 2008</td>
</tr>
<tr>
<td>4.4.8</td>
<td>3 January 2008</td>
</tr>
</tbody>
</table>
<p>Total releases since 18 December 2007: <em>8</em></p>

<h3>Parrot</h3>

<p>Parrot releases are harder to count because of their prolific release cycle. 1.0.0 is considered the "stable" release, although the 3 monthly releases since then are quite stable for me and the project had many public monthly releases prior to 1.0.</p>
<table>
<thead>
<tr>
<th>Version</th>
<th>Released On</th>
</tr>
</thead>
<tbody>
<tr>
<td>1.3.0</td>
<td>16 June 2009</td>
</tr>
<tr>
<td>1.2.0</td>
<td>20 May 2009</td>
</tr>
<tr>
<td>1.1.0</td>
<td>21 April 2009</td>
</tr>
<tr>
<td>1.0.0</td>
<td>17 March 2009</td>
</tr>
<tr>
<td>0.9.1</td>
<td>17 February 2009</td>
</tr>
<tr>
<td>0.9.0</td>
<td>21 January 2009</td>
</tr>
<tr>
<td>0.8.2</td>
<td>17 December 2008</td>
</tr>
<tr>
<td>0.8.1</td>
<td>19 November 2008</td>
</tr>
<tr>
<td>0.8.0</td>
<td>21 October 2008</td>
</tr>
<tr>
<td>0.7.1</td>
<td>17 September 2008</td>
</tr>
<tr>
<td>0.7.0</td>
<td>19 August 2008</td>
</tr>
<tr>
<td>0.6.4</td>
<td>15 July 2008</td>
</tr>
<tr>
<td>0.6.3</td>
<td>17 June 2008</td>
</tr>
<tr>
<td>0.6.2</td>
<td>20 May 2008</td>
</tr>
<tr>
<td>0.6.1</td>
<td>15 April 2008</td>
</tr>
<tr>
<td>0.6.0</td>
<td>18 March 2008</td>
</tr>
<tr>
<td>0.5.3</td>
<td>21 February 2008</td>
</tr>
<tr>
<td>0.5.2</td>
<td>15 January 2008</td>
</tr>
<tr>
<td>0.5.1</td>
<td>18 December 2007</td>
</tr>
</tbody>
</table>
<p>Total releases since 18 December 2007: <em>19</em>, <em>4</em>, or <em>1</em> depending on whether you count <em>all</em> public releases, all 1.x releases, or only the stable 1.0.0 release.</p>
<h3>Rakudo</h3>
<p>It's not completely fair to include Rakudo in this list, since it's still shy of a 1.0 release. However, it is worth pointing out that Rakudo has had 5 monthly development releases since outgrowing Parrot and adopting its own cycle in early 2009.</p>
<h3>Perl 5</h3>
<table>
<thead>
<tr>
<th>Version</th>
<th>Released On</th>
</tr>
</thead>
<tbody>
<tr>
<td>5.8.9</td>
<td>16 December 2008</td>
</tr>
<tr>
<td>5.10.0</td>
<td>18 December 2007</td>
</tr>
</tbody>
</table>
<p>Total releases since 18 December 2007: <em>2</em></p>
<h2>What Do These Numbers Say To Me?</h2>
<p>Not much, really. They're numbers. This is not detailed analysis. This is just looking, whining, and pondering. But the overall feel I get when I look at this list is that Perl 5 is not active compared to other languages.  Its maintainers have things to do besides fix or apply patches for <a href="http://rt.perl.org/rt3/Public/Search/Simple.html?Query=Queue%20=%20%27perl5%27%20AND%20%28Status%20=%20%27open%27%20OR%20Status%20=%20%27new%27%20OR%20Status%20=%20%27stalled%27%29">existing bugs</a> or new features. If I were a developer or startup CTO looking for a language to work and play with - and that's the perspective I'm taking, rather than the grizzled veterans maintaining 12 year old apps running on
a custom patched Perl - I would have a hard time believing that Perl is worth my time. </p>
<p>Those releases are more than just a bundle of features and fixes. They are how we take the pulse of a language. They are how we measure its health.  Perl 5's pulse is a little slow, a little unsteady. You might think that this is a sign of stability. I don't agree. It's a sign of stagnancy to me. It has the stink of sickness.</p>
<p>I'm not going to be alarmist and say that Perl is dead or dying. Programming languages rarely if ever die. But wouldn't it be great if Perl 5 was healthy and strong? Please, ignore the people that insist on stagnancy and release Perl more often!</p>
<p>P.S. If you didn't like my Jello Biafra paraphrasing, you should be grateful I didn't go with my other idea of "Perl 5's not dead, it's being kept in a hole in the basement and told to put the lotion on its skin." Because sharing that would have been pretty tasteless.</p>