---
aliases:
- /blogspot/2007/11/26_xcbxlibunlock-issues-java-on-fedora.html
- /post/2007/xcbxlibunlock-issues-java-on-fedora/
- /2007/11/26/xcb_xlib_unlock-issues-java-on-fedora/
category: blogspot
date: 2007-11-26 00:00:00
layout: layout:PublishedArticle
slug: xcb-xlib-unlock-issues-java-on-fedora
tags:
- linux
- java
- I fixed it!
title: xcb_xlib_unlock issues - Java on Fedora
uuid: 413dc0a9-1617-429b-a119-d4ed01e87f64
---

I decided to install the Sun JDK on my new Fedora install today. Tried downloading the JDK/NetBeans self-installing bundle. It didn't work. I got an error in xcb_xlib:xcb_xlib_unlock - something about a failed assertion. While running the installer. Drat.
<!--more-->

Installation required skipping the Netbeans IDE and just using the self-extracting JDK archive. Then, in order to get Swing to work, I had to remove Xinerama references from any copy of libmawt.so that was in my Java install. There's a sed script floating out there, but that wasn't working for me. Before I spent effort figuring out sed, I edited the files from vim.


<pre>[brian@localhost ~]$ sudo vim /opt/jdk1.6.0_03/jre/lib/i386/xawt/libmawt.so
[brian@localhost ~]$ sudo vim /opt/jdk1.6.0_03/jre/lib/i386/motif21/libmawt.so
[brian@localhost ~]$ sudo vim /opt/jdk1.6.0_03/jre/lib/i386/headless/libmawt.so
[brian@localhost ~]$</pre>

In each case I executed a simple regex

<pre>:%s/XINERAMA/FAKEEXT/g</pre>

It's the same as the sed script. I was too lazy to fix a short script that I will probably only use once.

Java's happy now, so I'm going to go do a little coding.