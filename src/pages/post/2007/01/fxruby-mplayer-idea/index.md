---
aliases:
- /blogspot/2007/01/30_fxruby-mplayer-idea.html
- /post/2007/fxruby-mplayer-idea/
- /2007/01/30/fxruby-mplayer-idea/
category: blogspot
cover_image: cover.png
date: 2007-01-30 00:00:00
layout: layout:PublishedArticle
slug: fxruby-mplayer-idea
tags:
- project
- ruby
title: FXRuby MPlayer Idea
uuid: a9d294e0-12b4-4176-8af5-01f0a28284d1
---

A few weeks back I wrote up a GUI front-end for <a href="http://www.mplayerhq.hu/">mplayer</a>. It works nice enough, but it suffers from a few aesthetic issues:
<!--more-->

<ul><li>    It's written with <a href="http://poe.perl.org/">POE</a> and <a href="https://metacpan.org/pod/distribution/Tk/Tk.pod">Perl/Tk</a>. I managed to write the code in such a way that it's readable, but ... well, Perl/Tk looks like ass. It's okay for smaller projects, but it becomes more and more obvious as your project grows that it's just not pretty enough. Tcl/Tk has <a href="http://tktable.sourceforge.net/tile/">Tile</a>, which would make things all pretty, but I'm not comfortable writing apps with Tcl. POE is also okay, but I have no POE-fu to speak of. So the application code is also starting to look like ass. </li><li>    MPlayer slave mode is not working completely as advertised, or it's not interacting well with my POE-ass code. Whatever. Pause does not actually pause. It just hiccups for a second and goes back to playing. I will work around that, but I'll also be keeping my eyes open for something else.</li></ul>I have chosen to rewrite the front end with Ruby - specifically <a href="http://fxruby.org/">FXRuby</a>. I might have used <a href="http://ruby-gnome2.sourceforge.jp/">Ruby/Gtk2</a>, but for some reason I can't convince this stupid computer that I have the Gtk2 development libs. Score one more point of hate for Redhat-based distros.

Yes, the basic interface is familiar. No, it's not a clone. All this baby is planned to do is import, organize, and play your music files. Even then, you are probably better off with the original if it's available for your platform.