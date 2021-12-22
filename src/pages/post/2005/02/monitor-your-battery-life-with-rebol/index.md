---
aliases:
- /coolnamehere/2005/02/28_monitor-your-battery-life.html
- /post/2005/monitor-your-battery-life/
- /2005/02/28/monitor-your-battery-life-with-rebol/
category: coolnamehere
date: 2005-02-28
layout: layout:PublishedArticle
slug: monitor-your-battery-life-with-rebol
tags:
- rebol
- learn
title: Monitor Your Battery Life With REBOL
updated: 2009-07-11 00:00:00
uuid: cce1fc1b-ec92-4ab4-8165-5773cb400f74
---

[KDE]: https://kde.org
[Ubuntu]: https://ubuntu.com

One thing you like to keep track of on your laptop is how much juice is left in your battery.
There’s nothing quite like being in the middle of some insane hacking session and watching as the computer suddenly gets tired and blacks out on you.
Of course, I’ve already got a handy battery monitor in my [KDE][] panel, but what if I’m not in KDE?
Okay, okay, there are handy battery monitors for nearly every desktop environment out there.
That’s not my point, though.
My point is that I’d like to explore some basic system stuff using REBOL on an [Ubuntu][] 8.10 system.
Got it?
Okay, good.
Now that we’ve settled this little detail, let’s move on.

<aside class="admonition note">
<p class="admonition-title">Note</p>

I should mention that if all you want is a command-line printout of your battery information on Linux,
you can get that with the command `acpi -b`.
Still, reinventing wheels can be fun.
Why not give this a shot?

</aside>

## The Raw Materials

Text is like water in UNIX-type systems.
It is everywhere, and nearly everything can be accessed as a text file.
Linux follows this ideal by keeping system information in a number of files in the `/proc/` directory.
I could probably find everything I might want to know about the system in that directory,
but let’s just focus on the directories which contain battery information.


<aside class="admonition note">
<p class="admonition-title">Note</p>

Ubuntu keeps the files in `/proc/`, but other distros may keep the files in other locations, such as `/var/proc/`.
Poke around on your own system to find out the specifics for your distribution.

</aside>

    >> read %/proc/acpi/battery/
    == [%BAT0/]
    >> read %/proc/acpi/battery/BAT0/
    == [%alarm %state %info]

I only have one battery, and this time I only see one folder under `/proc/acpi/battery`.
There were two folders when I ran this on another machine a while back.

    >> print read %/proc/acpi/battery/BAT0/state
    present:                 yes
    capacity state:          ok
    charging state:          charged
    present rate:            0 mA
    remaining capacity:      4263 mAh
    present voltage:         12495 mV

That one battery happens to be fully charged.
Good thing, because it’s been sitting plugged in all day.
I’m curious.
Let’s see what the `state` file looks like when I unplug the computer.

    >> print read %/proc/acpi/battery/BAT0/state
    present:                 yes
    capacity state:          ok
    charging state:          discharging
    present rate:            0 mA
    remaining capacity:      4341 mAh
    present voltage:         12107 mV

Okay, so it is pretty easy to tell when your computer is plugged in and when it isn’t.
The `info` file contains some more useful information about the battery which will come in handy later on.

    >> print read %/proc/acpi/battery/BAT0/info
    present:                 yes
    design capacity:         4400 mAh
    last full capacity:      4263 mAh
    battery technology:      rechargeable
    design voltage:          10800 mV
    design capacity warning: 210 mAh
    design capacity low:     147 mAh
    capacity granularity 1:  63 mAh
    capacity granularity 2:  4053 mAh
    model number:            Primary
    serial number:
    battery type:            LION
    OEM info:                Hewlett-Packard

What about the `alarm` file?

    >> print read %/proc/acpi/battery/BAT0/alarm
    alarm:                   unsupported

Oh well, I wasn’t really sure what I’d do with that information anyhow.

Now that we’ve seen what the raw information looks like, let’s work on making a useful utility which processes that information.

## Beginning the Script

```
#!/usr/local/bin/rebol -qs

REBOL [
    Title: "Battery Monitor"
    File: %battery.r
    Date: 24-Feb-2009
    Author: "Brian Wisti"
]

battery-dir: %/proc/acpi/battery/

batteries: read %/proc/acpi/battery/

foreach battery batteries [
    print battery
    battery-state: rejoin [ battery-dir battery "state" ]
    print read battery-state
]
```

We need that `-s` command line parameter in there if we want to run this script peacefully.
What happens if we don’t?
Every time we run the script, REBOL throws a little dialog asking us if we’re sure we want this script touching our precious files.
All in all, a good thing to do, but we _know_ we are okay with this script reading our files, precious or otherwise.

Right.
We are looking for every battery directory, and printing out its `state`.
What does that look like?
Not much, right now.

    BAT0/
    present:                 yes
    capacity state:          ok
    charging state:          charged
    present rate:            0 mA
    remaining capacity:      4360 mAh
    present voltage:         12465 mV

It’s time to start looking at REBOL’s `parse` rules.

Tell me not to be scared.

### Playing at Parse

Each item is on one line.
The key is on the left side, then there’s a colon and some whitespace before reaching the actual value.
I’d like to get at the information in this file as a hash:
a dictionary datatype where values on the right are tied to keys on the left.
Let’s use Parse and split along the colon character, like so.

```
#!/usr/local/bin/rebol -qs

REBOL [
    Title: "Battery Monitor"
    File: %battery.r
    Date: 24-Feb-2009
    Author: "Brian Wisti"
]

battery-dir: %/proc/acpi/battery/

batteries: read %/proc/acpi/battery/

foreach battery batteries [
    print battery
    battery-state: read rejoin [ battery-dir battery "state" ]
    print battery-state
    state: make hash! parse/all battery-state ":"

    ; Print out what we have so far for debugging purposes.
    foreach [ key value ] state [
        print [ key "--" value ]
    ]
]
```

That doesn’t *quite* do the job we wanted, unfortunately.
All of the whitespace is stuck with `value`, obscuring the actual value.

    BAT0/
    present:                 yes
    capacity state:          ok
    charging state:          discharging
    present rate:            0 mA
    remaining capacity:      4310 mAh
    present voltage:         12081 mV

    present --                  yes
    capacity state
              ok
    charging state --           discharging
    present rate
                0 mA
    remaining capacity --       4310 mAh
    present voltage
             12081 mV
    -- none

We want to get rid of the leading whitespace for each value.

I need to think for a minute…

[Perl]: /tags/perl

Okay, I know how I would do this with a regular expression in [Perl]:

```perl
#!/usr/bin/perl

use Modern::Perl;
use Fatal qw(open close);

my %state = ();
open(my $state, "/proc/acpi/battery/BAT0/state");
while (my $line = <$state>) {
  chomp($line);
  my ($key, $value) = split(/:/, $line);
  $value =~ s{^\s*}{};
  $state{$key} = $value;
}

close $state;

# Print out what we have so far for debugging purposes.
foreach my $key (keys %state) {
  say $key, " -- ", $state{$key};
}
```

This obviously isn’t the only Perl solution I could have chosen, but it was the first one that came to mind.
The point is that it gets the job done.
It’s kind of ugly, but Perl is kind enough to let you be ugly if you’re in a hurry.

    $ perl battery.pl
    present voltage -- 12021 mV
    capacity state -- ok
    present rate -- 0 mA
    remaining capacity -- 4088 mAh
    charging state -- discharging
    present -- yes

How do I strip the leading whitespace in Rebol?
I know there’s a "right" way, but for now I just want to get those spaces out of there.

```
#!/usr/local/bin/rebol -qs

REBOL [
    Title: "Battery Monitor"
    File: %battery.r
    Date: 24-Feb-2009
    Author: "Brian Wisti"
]

battery-dir: %/proc/acpi/battery/

batteries: read %/proc/acpi/battery/

foreach battery batteries [
    battery-file: rejoin [ battery-dir battery "state" ]
    state: make hash! []
    print battery

    foreach line read/lines battery-file [
        parse line [
            copy key thru ":"
            copy value to end
        ]
        value: trim value
        append state key
        append state value
    ]

    ; Print out what we have so far for debugging purposes.
    foreach [ key value ] state [
        print [ key "--" value ]
    ]
]
```

This is a lot longer than the Perl version, but you could argue that it’s easier to read.
And I just _know_ that there’s a better way to do it.
Sadly, we won’t know what the better way is until we learn a little more about how Parse works.

    $ ./battery.r
    BAT0/
    present: -- yes
    capacity state: -- ok
    charging state: -- discharging
    present rate: -- 0 mA
    remaining capacity: -- 4242 mAh
    present voltage: -- 12375 mV

Well, that colon is still in there, but at least I got rid of the leading spaces in the values.

I’ll come back to that issue after I’ve learned a little bit more about Parse.
For now, let’s focus on the fact that we are finally getting to the data.
That means we have reached a milestone, and it also means we can stretch our legs for a minute.
Good circulation is important, after all.

Let’s refactor before we move on.
I like to have my code as clean as I know how to make it each step of the way.

```
#!/usr/local/bin/rebol -qs

REBOL [
    Title: "Battery Monitor"
    File: %battery.r
    Date: 24-Feb-2009
    Author: "Brian Wisti"
]

battery-dir: %/proc/acpi/battery/
batteries: make hash! [ ]

; Load battery information
foreach battery read battery-dir [
    battery-file: rejoin [ battery-dir battery "state" ]
    state: make hash! []

    foreach line read/lines battery-file [
        parse line [
            copy key to ":"
            skip
            copy value to end (trim value)
        ]
        repend state [ key value ]
    ]
    repend batteries [ battery state ]
]

; Print out what we have so far for debugging purposes.
foreach [ name info ] batteries [
    print name
    foreach [ key value ] info [
        print [ key "--" value ]
    ]
]
```

You aren’t supposed to change the actual functionality during refactoring, because the whole idea is to make it do exactly the same thing it did before, but in a more sane style. I was hit by a lightbulb moment while refactoring the `parse` rule, though, and decided to see what would happen if `skip` would get me past that colon. Sure enough, that did the trick!

    $ ./battery.r
    BAT0/
    present -- yes
    capacity state -- ok
    charging state -- charged
    present rate -- 0 mA
    remaining capacity -- 4299 mAh
    present voltage -- 12540 mV

### Useful Output

Now let’s take this raw data and turn it into output that I can actually do something with.
To do that, we need to decide what information we care about and what we don’t.

* I don’t care about batteries I don’t have.
  Don’t show them to me.
* I care about whether the computer is plugged in or not.
* I can’t convert remaining capacity of total capacity in my head.
  Just show me a percentage remaining.
* I *certainly* can’t convert present rate and remaining capacity.
  Show me a time value instead.

#### Don’t Show Batteries I Don’t Have

This should be the easiest step.
All we need to do is check the value of the "present" key.
Should be no problem at all.

```
; Print out what we have so far for debugging purposes.
foreach [ name info ] batteries [
    if "yes" = select info "present" [
        print name
        foreach [key value] info [
            print [ key "--" value ]
        ]
    ]
]
```

#### Show Me If The Computer Is Plugged In

We are now officially out of the "print out what we have for debugging purposes" stage.
From here on, we will be creating the output we expect to see.

```
foreach [ name info ] batteries [
    if "yes" = select info "present" [
        charging-state: select info "charging state"
        print [ name charging-state ]
    ]
]
```

Rather than step through and display every single item of data, we are printing one line with minimal information:
the name of the battery and whether it is charging or not.

    $ ./battery.r
    BAT0/ discharging

I like this.
It is easy for me to understand this output compared to the raw files.

#### Show Me Percentage Of Remaining Battery Capacity

I will want to know how much power is remaining if the battery is either "charging" or "discharging".
I don’t know what `mAh` is – *milliAmp-hours?*.
I prefer to see this in terms of what percentage is remaining.
A full battery has 100%, and an empty battery has 0%.
Seems easy enough, but we don’t have the total capacity listed in the state file.
To get this information, we will need to look at the `info` file.

```
foreach [ name info ] batteries [
    if "yes" = select info "present" [
        charging-state: select info "charging state"
        prin [ name charging-state ]
        info-file: rejoin [ battery-dir name "info" ]
        foreach line read/lines info-file [
            if parse line [
                "design capacity:"
                copy capacity to end (trim capacity)
            ] [
                items: parse capacity none
                cap: to-integer items/1
                items: parse select state "remaining capacity" none
                rem: to-integer items/1
                per: to-integer (rem / cap * 100)
                prin join " " [ per "%" ]
                break
            ]
        ]
        print []
    ]
]
```

Now I can see the percentage remaining:

    $ ./battery.r
    $ BAT0/ discharging 91%

Yes, that’s the output that I want, but the code is turning into something … *evil*.
Or at least something *ugly*.
I should consider refactoring again before I move on to the next step.
I will just show you the end result of the refactoring, but these are the ideas that guided me as I looked at my code:

* Go ahead and read all the data files. It’s not like memory is an issue for an app like this.
  * Don’t forget to look for duplicate keys when assembling the hash.
* Remove duplication where possible.
* Only use `print` once for each battery.
  Narrowing down the sources of output can make debugging and reading easier.

And here’s the refactoring.

```
#!/usr/local/bin/rebol -s

REBOL [ ]

;;
;; Function Definitions
;;

get-value: func [
    "Get numeric part of a value in the battery info hash"
    information [hash!]   "A Hash containing battery data"
    key         [string!] "A key to look up in the hash"
    /local value tokens numeric-value
] [
    value: select information key
    tokens: parse value none
    numeric-value: to-integer tokens/1
    return numeric-value
]

;;
;; Main logic starts here.
;;

battery-dir: %/proc/acpi/battery/
batteries: make hash! [ ]

; Load battery information.
foreach battery read battery-dir [
    state: make hash! []
    battery-files: read rejoin [ battery-dir  battery ]

    foreach file battery-files [
        full-path: rejoin [ battery-dir battery file ]

        foreach line read/lines full-path [
            parse line [
                copy key to ":"
                skip
                copy value to end (trim value)
            ]
            unless select state key [
                repend state [ key value ]
            ]
        ]
    ]
    repend batteries [ battery state ]
]

; Display information for each battery
foreach [ name info ] batteries [

    ; ... but only if the battery is present.
    if "yes" = select info "present" [
        charging-state: select info "charging state"

        capacity: get-value info "design capacity"
        remaining: get-value info "remaining capacity"
        percent: to-integer (remaining / capacity * 100)

        battery-text: reform [
            name
            charging-state
            join percent [ "%" ]
        ]
        print battery-text
    ]
]
```

The end result is the same as before, but I’ve made the code easy to read again.
This process of writing and refactoring is pretty much standard to my development style.
Well, I’m not the *only* one who writes code like this.
Anyhow.
Let’s move on, shall we?

#### Show Me Estimated Time Remaining

In order to calculate the time remaining before the battery runs out, we need to get the remaining charge and the rate that we’re using it up.

```
        ...
        print battery-text
        print select info "remaining capacity"
        print select info "present rate"
    ]
]
```

Wow, I really don’t know what those numbers mean.
We could fake it until we get a result that looks like what I see when I scrub the mouse over my KDE battery applet.
I think I will do a little bit of searching on the Web, though.
There is probably some sort of reference to the ACPI state files.

I have a rule not to spend more than fifteen minutes looking something up online, unless the end result of such a search would be money or finding something that pleases my wife.
This is neither, and I’ve just spent fifteen minutes making a few clumsy stabs at finding a reference for the ACPI state file.
No luck, so let’s go with the faking it.

The KDE panel says I have a little over two hours left on my laptop.
With a couple of quick hacks, my script more or less agrees with KDE.
There’s an occasional difference of a minute or two, but that is not an urgent issue for something like this.
I would be much more concerned if this script was going to be used in a production environment, or in an environment where being off by a couple of seconds could cost somebody their life.
On the other hand, what are they doing using some script they cobbled off the Web to keep their loved ones alive?
And then they’ll probably get mad at *me* when it goes wrong.
I swear, some people are just too strange for words.

What?
Oh, right.
Here’s the finished version of the utility.
Took me a couple of hours, but a lot of that was me learning the basics of `parse`.

```
#!/usr/local/bin/rebol -s

REBOL [
    Title: "Battery Monitor"
    File: %battery.r
    Date: 14-mar-2005
    Author: "Brian Wisti"
]

;;
;; Function Definitions
;;

get-value: func [
    "Get numeric part of a value in the battery info hash"
    information [hash!]   "A Hash containing battery data"
    key         [string!] "A key to look up in the hash"
    /local value tokens numeric-value
] [
    value: select information key
    tokens: parse value none
    numeric-value: to-integer tokens/1
    return numeric-value
]

;;
;; Main logic starts here.
;;

battery-dir: %/proc/acpi/battery/
batteries: make hash! [ ]

; Load battery information.
foreach battery read battery-dir [
    state: make hash! []
    battery-files: read rejoin [ battery-dir battery ]

    foreach file battery-files [
        full-path: rejoin [ battery-dir battery file ]

        foreach line read/lines full-path [
            parse line [
                copy key to ":"
                skip
                copy value to end (trim value)
            ]
            unless select state key [
                repend state [ key value ]
            ]
        ]
    ]
    repend batteries [ battery state ]
]

; Display information for each battery
foreach [ name info ] batteries [

    ; ... but only if the battery is present.
    if "yes" = select info "present" [
        charging-state: select info "charging state"

        capacity: get-value info "design capacity"
        remaining: get-value info "remaining capacity"
        percent: to-integer (remaining / capacity * 100)

        rate: get-value info "present rate"
        either rate > 0 [
            seconds: remaining / rate * 60 * 60
            time-remaining: to-time to-integer seconds
        ] [
            time-remaining: "--"
        ]

        battery-text: reform [
            name
            charging-state
            join percent [ "%" ]
            time-remaining
        ]
        print battery-text
    ]
]
```

Running it shows a problem on Ubuntu.
The discharge rate in the state file is listed as zero, which means the script has no way to determine estimated time remaining.

    wisti grabbag $ ./battery.r
    BAT0/ discharging 82% --

This is a known issue, but I do not yet know a way around it.
I left the original code intact just in case *your* laptop does not have this problem.

Now, if I wanted to make this readily accessible from the command line, which I do, then I would just copy `laptop.r` to someplace on my path.
I might even rename to something like `check-battery` without the ".r" suffix, to make it look more like any old command.
This is a common manuever on the command line.
Many of the commands you use every day in the shell are just thinly disguised scripts, written in one language or another.

    wisti grabbag $ cp battery.r ~/bin/check-battery

And now I have one written in REBOL.

## Conclusion

This project was an exercise to see how difficult it would be to create a relatively simple utility.
It was a challenge until I started getting the hang of Parse.
I think Parse is easier to understand than regular expressions, but regular expressions have the advantage that they are familiar to more Linux developers.
Still - get Parse out of the way, and creating useful applications in REBOL suddenly becomes very easy.

### Additional Ideas

There are a number of different things you could do to enhance or refine this script.
Here are a couple of ideas.

* This script is *not* portable.
  It assumes that you have the same file setup as my HP notebook running Ubuntu 8.10.
  Any differences brought on by different distributions or operating systems are unaccounted for.
  You might want to alter the script to look in the right places for your machine.
* The script is *not* robust.
  What happens if there’s a zero in the wrong place, or ACPI can’t figure out how what the rate of discharge is?
  I don’t know, but it’s probably not something good.
  You might want to make it more robust by checking for possible errors.
* Hey, what about writing this as a View application?
  Yeah, you could make a cute little picture of a battery that empties out as the remaining power drops.
  Why stop there? You could implement a whole system monitor, like [gkrellm](http://gkrellm.net/).
  That might be fun.
