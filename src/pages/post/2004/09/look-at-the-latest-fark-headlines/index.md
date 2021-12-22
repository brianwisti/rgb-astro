---
aliases:
- /coolnamehere/2004/09/17_look-at-the-latest-fark-headlines.html
- /post/2004/look-at-the-latest-fark-headlines/
- /2004/09/17/look-at-the-latest-fark-headlines/
category: coolnamehere
date: 2004-09-17 00:00:00
layout: layout:PublishedArticle
slug: look-at-the-latest-fark-headlines
tags:
- ruby
- learn
title: Look at the Latest Fark Headlines
updated: 2009-07-11 00:00:00
uuid: ad8004ae-d561-4d79-8cb1-295b6f03daff
---

The Problem
-----------

I want to look at the [Fark](http://fark.com/) headlines without opening
a browser. Why? I dunno, maybe I just want to see what’s new since the
last time I looked, without being distracted by the site clutter.

Now, I could just turn off images and go to the site, and that would
work fine. Actually, it would work quite well. No need for this article,
then. I’m off for some coffee …

What? I *have* to write something in here about Ruby? … okay.

ahem.

I want to look at the [Fark](http://fark.com/) headlines without opening
a browser. Why? Well, as it so happens, I am logged into a machine via
`ssh`, and using elinks to load the page will result in a lot of extra
clutter from text versions of ads which obscure the headlines. I’m just
interested in seeing what interesting, scary, or amusing things have
been posted on Fark since the last time I checked.

Finding a Solution
------------------

Well, we could always just dump the Fark page to the console:

``` ruby
require 'open-uri'

headlines = open('http://www.fark.com/').read()
puts headlines
```

Three lines of code and we have output.

    $ ruby19 fark.rb
    ⋮
    <!-- START copyright_html() -->
    <div id="footer">
    <span class="boldy"><a target="_top" href="http://www.fark.com/nomirror/"></a>\
    Copyright &copy; 1999-2009 Fark, Inc</span><br>
    <strong>Last updated: Mon Mar  9 16:28:19 2009</strong><br>
    <a target="_top" href="http://www.fark.com/cgi/feedback.pl">Contact us</a> | <\
    a target="_top" href="http://www.fark.com/cgi/feedback.pl?type=error">Report a\
    bug/error msg</a><br>
    <a target="_top" href="http://www.fark.com/farq/legal.shtml">Terms of service/\
    legal/privacy policy</a>
    <br>
    <div class="finalfootnote"><script type="text/javascript">
    //<![CDATA[
    document.write('<'+'img src="http://www.fark.com/cgi/ll.pl?l=H384ABPoSz-uDukni\
    hQDAVhlkEgde6Pxu7ZO_uxPBp5SfD&amp;v='); var fw=(window.innerWidth) ? window.in\
    nerWidth : document.body.offsetWidth; var fh=(window.innerHeight) ? window.inn\
    erHeight : document.body.offsetHeight; var fc=window.screen.colorDepth; docume\
    nt.writeln(((fh*8192)+fw)+'&amp;c='+fc+'" width="4" height="1" alt=""'+'>');
    //]]></script><noscript><img src="http://www.fark.com/cgi/ll.pl?l=H384ABPoSz-u\
    DuknihQDAVhlkEgde6Pxu7ZO_uxPBp5SfD&amp;v=0" width="4" height="1" alt=""></nosc\
    ript>
    </div>
    </div>
    <!-- END copyright_html() -->
    </div> <!-- siteContainer -->
    </body>
    </html>

But running this doesn’t quite get the result I was looking for. I just
want the headlines, and I want them without the HTML, thank you very
much.

Fark and a lot of other news sites make [RSS](https://blogging.im/RSS)
feeds available. These are special XML files containing mainly - you
guessed it, the headlines, without the HTML, you’re very welcome.

``` ruby
require 'open-uri'

url = 'http://www.fark.com/fark.rss'
headlines = open(url).read()
puts headlines
```

This is a little closer to what we want.

    $ ruby fark.rb
    ⋮
    <item>
     <title>&#34;Hindsight isn&#39;t only 20/20, it&#39;s usually also sober&#34; [Dumbass]</title>
     <description><![CDATA[Atlanta Journal Constitution]]></description>
     <link>http://www.fark.com/cgi/comments.pl?IDLink=4255950</link>
     <pubDate>Mon, 09 Mar 2009 02:05:43 EDT</pubDate>
     <guid isPermaLink="false">http://www.fark.com/cgi/go.pl?i=4255950</guid>
    </item>
    </channel>
    </rss>

Now I get the RSS file dumped to the console. At least the story
headlines are little easier to find. To get the behavior I want, though,
we’re going to need to chop out the bits we don’t care about and get
straight to the headlines. This task is straightforward in Ruby, thanks
to the [RSS](http://ruby-doc.org/stdlib/libdoc/rss/rdoc/index.html)
library. The RSS library has recently been made an official part of the
standard libs, which makes a lot of this exercise much easier.

``` ruby
require 'open-uri'
require 'rss'

rss_url = 'http://www.fark.com/fark.rss'
document = open(rss_url).read()
rss = RSS::Parser.parse(document)
rss.items.each do |item|
  puts item.title
end
```

Okay, now what does this look like?

    $ ruby19 fark.rb
    Worried about being the washed-up former high school football star while \
    those nerds you picked on become millionaires later in life? Well, good n\
    ews [Interesting]
    State mental hospital drops off severely ill woman at bus station to make\
    it home by herself. Since this is Fark, you can assume she didn't make it\
    [Sad]
    Professional coffee taster's tongue insured for $14 million. The man's to\
    ngue works magic on the bean [Amusing]
    In celebration of his 69th birthday tomorrow, Chuck Norris will randomly \
    select one lucky child to be thrown into the sun [Hero]
    Moving pot plants to an undisclosed location to deter would-be burglars i\
    s a GREAT idea. Just don't do it using an open-bed pickup truck. Police m\
    ight see you [Florida]
    Nothing solves an $8 billion dollar deficit like a good old fashioned bak\
    e sale [Stupid]
    Yet another indicator of America's continuing decline: pediatricians now \
    recommend that children between the ages of 2 and 10 be routinely screene\
    d for heart disease [Sad]
    Computer glitch caused Austrailian airliner to plunge 1,000 feet and the \
    toilets to flush counterclockwise [Scary]
    This year's Maxwell Smart Special Achievement Award goes to the US Triden\
    t missile program, for keeping the composition of a key material so secre\
    t that no one knows how to make it anymore [Fail]
    Unique portrait of William Shakespeare reveals much about the notorious b\
    ard, such as the stunning realization that he looks like Russell Brand [I\
    nteresting]
    Just what the filthy rich need -- a place to super-poke their filthy rich\
    friends [Dumbass]
    Man/Boy love group NAMBLA puts $10,000 hit on New York's Attorney General\
    ; because decades in jail is so worth $10G [Asinine]
    Christian salt, contraceptive robberies, and a wallet full of teeth: Fark\
    's Headlines of the Week 3/1 to 3/7 [FarkBlog]
    ⋮

This is even better still, but that’s an awful lot of headlines. How
about just the most recent ones? How about the last 10?

``` ruby
require 'open-uri'
require 'rss'

rss_url = 'http://www.fark.com/fark.rss'
limit = 10

document = open(rss_url).read()
rss = RSS::Parser.parse(document)
rss.items.each_with_index do |item, index|
  break if index >= limit
  puts item.title
end
```

What does it look like now?

    $ ruby19 fark.rb
    Today's moral outrage comes from Geneva, Switzerland, where a known prostitut\
    e activist was buried in the same cemetery as John Calvin [Strange]
    Meghan McCain calls Ann Coulter "offensive" and "insulting," adding "are you \
    going to finish those fries?" [Interesting]
    Worried about being the washed-up former high school football star while thos\
    e nerds you picked on become millionaires later in life? Well, good news [Int\
    eresting]
    State mental hospital drops off severely ill woman at bus station to make it \
    home by herself. Since this is Fark, you can assume she didn't make it [Sad]
    Professional coffee taster's tongue insured for $14 million. The man's tongue\
    works magic on the bean [Amusing]
    In celebration of his 69th birthday tomorrow, Chuck Norris will randomly sele\
    ct one lucky child to be thrown into the sun [Hero]
    Moving pot plants to an undisclosed location to deter would-be burglars is a \
    GREAT idea. Just don't do it using an open-bed pickup truck. Police might see\
    you [Florida]
    Nothing solves an $8 billion dollar deficit like a good old fashioned bake sa\
    le [Stupid]
    Yet another indicator of America's continuing decline: pediatricians now reco\
    mmend that children between the ages of 2 and 10 be routinely screened for he\
    art disease [Sad]
    Computer glitch caused Austrailian airliner to plunge 1,000 feet and the toil\
    ets to flush counterclockwise [Scary]

Now we’ve got it down to the freshest 10, but each item is still filling
up a lot of space. One way to cut down the length of each line is to
split each headline into multiple lines. Let’s start by cutting the
category and title into two separate lines:

``` ruby
require 'open-uri'
require 'rss'

rss_url       = 'http://www.fark.com/fark.rss'
limit         = 10
title_pattern = Regexp.new %r{\[(.+?)\]\s(.+)$}

document = open(rss_url).read()
rss = RSS::Parser.parse(document)
rss.items.each_with_index do |item, index|
  break if index >= limit
  title_match = title_pattern.match(item.title)
  if title_match then
    puts title_match[1].upcase, title_match[2]
  end
end
```

It’s a lot easier for me to read the output now.

    $ ruby19 fark.rb
    INTERESTING
    Research shows that older fathers tends to has more kids who is dumb
    FLORIDA
    If you want to avoid suspicion of driving under the influence, the first \
    step would be to make sure you're driving on a full set of tires
    INTERESTING
    Vatican claims washing machine is most liberating 20th century invention \
    for women. Sybian didn't even make the list
    STRANGE
    Today's moral outrage comes from Geneva, Switzerland, where a known prost\
    itute activist was buried in the same cemetery as John Calvin
    INTERESTING
    Meghan McCain calls Ann Coulter "offensive" and "insulting," adding "are \
    you going to finish those fries?"
    INTERESTING
    Worried about being the washed-up former high school football star while \
    those nerds you picked on become millionaires later in life? Well, good n\
    ews
    SAD
    State mental hospital drops off severely ill woman at bus station to make\
    it home by herself. Since this is Fark, you can assume she didn't make it
    AMUSING
    Professional coffee taster's tongue insured for $14 million. The man's to\
    ngue works magic on the bean
    HERO
    In celebration of his 69th birthday tomorrow, Chuck Norris will randomly \
    select one lucky child to be thrown into the sun
    FLORIDA
    Moving pot plants to an undisclosed location to deter would-be burglars i\
    s a GREAT idea. Just don't do it using an open-bed pickup truck. Police m\
    ight see you

Occasionally I saw HTML entities in the output. `&quot;`, stuff like
that. Let’s fix that problem before we move on to anything else.

``` ruby
require 'open-uri'
require 'rss'
require 'cgi'

rss_url       = 'http://www.fark.com/fark.rss'
limit         = 10
title_pattern = Regexp.new %r{\[(.+?)\]\s(.+)$}

document = open(rss_url).read()
rss = RSS::Parser.parse(document)
rss.items.each_with_index do |item, index|
  break if index >= limit
  title_match = title_pattern.match(item.title)
  if title_match then
    category = CGI::unescapeHTML(title_match[2]).upcase
    title    = CGI::unescapeHTML(title_match[1])
    puts category, title
  end
end
```

It isn’t an issue this time, but I feel better.

    $ ruby19 fark.rb
    INTERESTING
    Research shows that older fathers tends to has more kids who is dumb
    FLORIDA
    If you want to avoid suspicion of driving under the influence, the first \
    step would be to make sure you're driving on a full set of tires
    INTERESTING
    Vatican claims washing machine is most liberating 20th century invention \
    for women. Sybian didn't even make the list
    STRANGE
    Today's moral outrage comes from Geneva, Switzerland, where a known prost\
    itute activist was buried in the same cemetery as John Calvin
    INTERESTING
    Meghan McCain calls Ann Coulter "offensive" and "insulting," adding "are \
    you going to finish those fries?"
    INTERESTING
    Worried about being the washed-up former high school football star while \
    those nerds you picked on become millionaires later in life? Well, good n\
    ews
    SAD
    State mental hospital drops off severely ill woman at bus station to make\
    it home by herself. Since this is Fark, you can assume she didn't make it
    AMUSING
    Professional coffee taster's tongue insured for $14 million. The man's to\
    ngue works magic on the bean
    HERO
    In celebration of his 69th birthday tomorrow, Chuck Norris will randomly \
    select one lucky child to be thrown into the sun
    FLORIDA
    Moving pot plants to an undisclosed location to deter would-be burglars i\
    s a GREAT idea. Just don't do it using an open-bed pickup truck. Police m\
    ight see you

Wherever possible, I’m using standard library tools to get my work done.
I’m too lazy to remember escaping every possible HTML entity, and I
would rather spend a few minutes searching through the [Standard Library
documentation](http://www.ruby-doc.org/stdlib/) to find what I need.
It’s a good habit, and you might want to try it yourself.

Maybe I only care about particular types of headline. Say, I want to be
interested, but not amused.

``` ruby
require 'open-uri'
require 'rss'
require 'cgi'

rss_url            = 'http://www.fark.com/fark.rss'
limit              = 10
title_pattern      = Regexp.new %r{\[(.+?)\]\s(.+)$}
preferred_category = 'INTERESTING'

document = open(rss_url).read()
rss = RSS::Parser.parse(document)
rss.items.each_with_index do |item, index|
  break if index >= limit
  title_match = title_pattern.match(item.title)
  if title_match then
    category = CGI::unescapeHTML(title_match[2]).upcase
    if category == preferred_category then
      title = CGI::unescapeHTML(title_match[1])
      puts title
    end
  end
end
```

And it does indeed show me only "interesting" headlines.

    $ ruby19 fark.rb
    New study concludes that viewing television before age 2 has no negative \
    effect on development. Great - NOW who are we supposed to blame for rampa\
    nt toddler sex and violence??
    Research shows that older fathers tends to has more kids who is dumb
    Vatican claims washing machine is most liberating 20th century invention \
    for women. Sybian didn't even make the list
    Meghan McCain calls Ann Coulter "offensive" and "insulting," adding "are \
    you going to finish those fries?"
    Worried about being the washed-up former high school football star while \
    those nerds you picked on become millionaires later in life? Well, good n\
    ews

That’s pretty nifty, except that it only looks for Interesting items out
of the last 10 headlines, rather than looking for the last 10
Interesting headlines.

``` ruby
require 'open-uri'
require 'rss'
require 'cgi'

rss_url            = 'http://www.fark.com/fark.rss'
limit              = 10
title_pattern      = Regexp.new %r{\[(.+?)\]\s(.+)$}
preferred_category = 'Interesting'

document = open(rss_url).read()
rss = RSS::Parser.parse(document)

index = 0
rss.items.each do |item|
  title_match = title_pattern.match(item.title)
  if title_match then
    category = CGI::unescapeHTML(title_match[2])
    if category.upcase == preferred_category.upcase then
      title = CGI::unescapeHTML(title_match[1])
      puts title
      index += 1
      break if index >= limit
    end
  end
end
```

Is this any better?

    $ ruby19 fark.rb
    New study concludes that viewing television before age 2 has no negative \
    effect on development. Great - NOW who are we supposed to blame for rampa\
    nt toddler sex and violence??
    Research shows that older fathers tends to has more kids who is dumb
    Vatican claims washing machine is most liberating 20th century invention \
    for women. Sybian didn't even make the list
    Meghan McCain calls Ann Coulter "offensive" and "insulting," adding "are \
    you going to finish those fries?"
    Worried about being the washed-up former high school football star while \
    those nerds you picked on become millionaires later in life? Well, good n\
    ews

Well, we can only look at today’s headlines. I guess we can’t be sure of
ten interesting things happening every day. Still, at least I know I’m
getting all of the interesting headlines that are available, up to my
limit.

Next problem: the only way I can fetch different headline types is to
manually dig in to the source code and change the category.

``` ruby
require 'open-uri'
require 'rss'
require 'cgi'
require 'optparse'

rss_url            = 'http://www.fark.com/fark.rss'
limit              = 10
title_pattern      = Regexp.new %r{(.+)\s\[(.+)\]$}
preferred_category = nil

# Get the preferred category, if any, from the command line.
opts = OptionParser.new do |opts|
  opts.banner = "#{$0} [options]"
  opts.separator("")
  opts.separator("Specific Options")

  opts.on("-c", "--category CATEGORY",
          "Only grab headlines in specific category") do |cat|
    preferred_category = cat
  end

  opts.on_tail("-h", "--help", "Show this usage display") do
    puts opts
  end
end

opts.parse!(ARGV)
document = open(rss_url).read()
rss = RSS::Parser.parse(document)

index = 0
rss.items.each_with_index do |item, index|
  break if index >= limit
  title_match = title_pattern.match(item.title)
  if title_match then
    category = CGI::unescapeHTML(title_match[2])

    if preferred_category.nil?
      puts title, category
    elsif category.upcase == preferred_category.upcase then
      puts title
      index += 1
      break if index >= limit
    end
  end
end
```

Let’s test it by requesting "PSA" headlines.

    $ ruby19 fark.rb -c psa

    Attention zoo visitors - please do not taunt the concrete chimpanzee

That works. Pretty nicely, I might add.
[OptParse](http://www.ruby-doc.org/stdlib/libdoc/optparse/rdoc/) is a
great library for handling command-line arguments.

This program now does everything that I set out to do, and then some. I
might choose to do a some refactoring to "bulletproof" the code, or wrap
it up in some OO niceness to make it pretty. The truth is that this
application is exactly what it needs to be for now, and I think that I
shouldn’t overwork something that I may never come back to. Maybe later
I’ll come back to it when I think of new features or find new bugs, and
*then* I can overwork it to my heart’s content.

I hope you enjoyed working along with me as much as I enjoyed sitting
here and typing random nonsense to myself.

What Else?
----------

I may be done with this exercise for now, but here are a few ideas about
features that can be added to make it a little cooler. Go ahead and try
them out!

- Add word wrap to make the output a little more readable.
- Add a parameter to change the number of headlines grabbed.
- Modify so that this script will work with other newsfeeds.
- Modify so that the functionality of this script can be embedded in
  other Ruby programs.

Revision History
----------------

- 12 March 2009: Ran under Ruby 1.9, changed parsing to reflect Fark RSS changes
- 3 January 2007: Major rewrite to incorporate RSS library and changes at Fark
- 19 September 2004: Changed the network library used from `net/http`
  to `open-uri` in the refactoring stage. This is from a suggestion
  that was made by Gavin Sinclair, Frederick Ros, and others. It’s a
  good suggestion, and I’m *not* going to ignore a good suggestion!
- 17 September 2004: Initial version released.