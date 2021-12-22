---
aliases:
- /blogspot/2007/06/29_im-too-cheap-to-buy-radio-alarm.html
- /post/2007/im-too-cheap-to-buy-radio-alarm/
- /2007/06/29/im-too-cheap-to-buy-a-radio-alarm/
category: blogspot
date: 2007-06-29 00:00:00
layout: layout:PublishedArticle
slug: im-too-cheap-to-buy-a-radio-alarm
tags:
- applescript
- os x
- unix
title: I'm too cheap to buy a radio alarm
uuid: 3b0214af-d9fb-40b2-9cac-db15ed78ab52
---

I have trouble waking up on time. That's probably because I have trouble getting to bed on time. You can tell I have trouble getting to bed on time, because it's 1:40 in the morning right now and I'm writing a little blog post instead of going to bed.
<!--more-->

I'm working on getting to sleep earlier. Hey, I might even be to bed by 2, instead of 3 or 3:30. Waking up takes a few tricks. Say, for example: an alarm clock that's too big for me to pick it up and stuff under my pillow like a gift for the tooth fairy. A loud annoying beeping gift. How about getting a bigger alarm and putting across the room? Well you would expect that to work, but apparently I can get up, walk over to the alarm, hit the snooze, pick up the alarm, bring it back to bed, and stuff the alarm under the bed for the tooth fairy again, all without actually waking up.

Yes, one issue is that the alarm clocks are battery powered. We live in a small, old apartment, and there just aren't enough outlets to go around. I had to unplug the lamp so that I could plug the computer in and type this.

But I have found a solution, or at least something which is not so easily circumvented. I've turned our beautiful iMac G4 into a glorified radio alarm. Turns out that it was actually quite simple. First I needed an application that plays music. Right, that would be iTunes. Next, I need a radio station that both of us like. Why not just use a playlist? I don't know, I guess I actually wanted this to be a <span style="font-style: italic;">radio</span> alarm. I'm odd. I do crazy things. I stash timepieces under my pillow, and blog in the middle of the night. Really, a radio station feed is not the strangest idea I've had.

Should I use our local [NPR](http://npr.org/)affiliate? No, I
don't think so. Light jazz mixed with news and traffic reports are *not* going
to make us jump out of bed all energized. I decided to use my favorite college
station, [KEXP](http://www.kexp.org/). The morning DJ is good, and
the morning selection is fantastic unless it's Winter and his
[SAD](http://www.sada.org.uk/)has kicked in.

I've got my app, I've got my radio station feed. Now a little AppleScript to automate the process of firing up and playing the station. I haven't experimented much with AppleScript, but there's no time like the present for putting a simple script together:

~~~applescript
-- PlayKEXP.applescript
--  Play the KEXP live stream

tell application "iTunes"
  set sound volume to 60
  play user playlist "KEXP Live"
end tell
~~~

I test it with `osascript PlayKEXP.applescript`. It works like a charm.

Now to set this alarm so it goes off at a set time every day. This is the part where I really love the UNIXy goodness of OS X. I can just use crontab. So here's my new crontab file:

    # minute/hour/mday/month/wday/command
    30  6   *   *   *   osascript /Users/brian/iTunesScripts/PlayKEXP.applescript

Then I make sure that crontab knows about the task:

    $ crontab mycrontab

This was my first time using crontab for a personal task as well. It's awesome. Every morning at 6:30 iTunes will set the volume and start playing the KEXP broadcast.

So there you have it. It's simple and it works. I'm going to bed now.