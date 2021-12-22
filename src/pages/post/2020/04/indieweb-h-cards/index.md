---
aliases:
- /2020/04/11/indieweb-h-cards/
caption: My h-card as of a few minutes ago
category: tools
cover_image: cover.png
date: 2020-04-11 07:16:34
description: Using microformats to build a profile page
draft: false
layout: layout:PublishedArticle
slug: indieweb-h-cards
tags:
- indieweb
- microformats
- site
title: Indieweb h-cards
uuid: d932fcf6-f277-41d3-a3dd-e63e0ef30769
---

## You did what now?

I updated my home page h-card for IndieWeb.

### What?

[h-card]: http://microformats.org/wiki/h-card
[microformats2]: http://microformats.org/wiki/microformats2

[h-carg][] is a [microformats2][] vocabulary to describe people and
organizations. I added terms from that vocabulary as HTML classes to
elements of a profile section on the front page.

### Why?

[IndieWeb]: https://indieweb.org

It helps identify me for other folks on the [IndieWeb][]. Some have 
written tools and services that speak h-card. Mostly, the h-card vocabulary
gives me a convenient way to organize my biographical details for visitors to
this site.

## What are you talking about?

Describing yourself in a useful way presents a challenge, especially
online. Prose has the greatest clarity for human readers — assuming they
know the language you write in. Social networks give you a profile page
with slots for important details — assuming they include fields for the
details *you* consider important.

We can use h-card to identify ourselves and others in the IndieWeb.
Officially, it’s a collection of properties for detailing individuals
and groups of people. Informally, it’s also the descriptions we create
with those properties. I used the h-card vocabulary to create a profile.
That profile included details that I consider important.

### A minimal h-card

I have a name that I commonly use both online and off.

``` text
Brian Wisti
```

<aside class="admonition note">
  <p class="admonition-title">Note</p>

Really that’s my "good enough" name. It’s not the full legal name on my
social security card. Most of my friends don’t use it for me unless
they’re trying to tell me apart from all the other people named Brian.
Now is not the time for [Falsehoods Programmers Believe About
Names](https://www.kalzumeus.com/2010/06/17/falsehoods-programmers-believe-about-names/),
but know that h-card handles this dilemma better than many solutions.

</aside>

In a stroke of good fortune, this name conforms to local convention. A
surname disambiguates my family from others. A given name disambiguates
me from other members of my family.

Some clarity might help people unfamiliar with my local naming
convention, though.

Wrap the name in any element, give that element an `h-card` class, and
it’s an h-card!

``` html
<span class="h-card">Brian Wisti</span>
```

Now we’re definitely talking about a person. Or maybe an organization.
We’re talking about a named entity. We know that much.

But where can we get useful information about this entity? Over in
Twitter we say `@brianwisti` and it points to [my Twitter
profile](https://twitter.com/brianwisti). What’s an IndieWeb equivalent?

Since any element can hold an h-card, replace the `<span>` with a link
to my site.

``` html
<a class="h-card" href="https://randomgeekery.org">Brian Wisti</a>
```

This tells anyone that Brian Wisti — that’s me — considers
`https://randomgeekery.org` — that’s here, or rather [here](/) — the
center of his online identity.

This is sufficient to uniquely identify me online. It’s the form I’d use
when referencing someone else online. I could even get away with using
that form for my own card.

### A profile card

Where do I put my card?

I use my site’s root URL, but not everyone identifies so closely with
their Web site. Put your h-card on what you consider your profile page.
If your profile page is `yoursite.info/yourname`, then that’s where you
put the h-card.

Just make sure the location matches the URL specified in the card
itself!

This abbreviated form contains more assumptions than I like. We can
assume that "Brian Wisti" is a name. The format calls that an *implied
property*. There’s honestly nothing wrong with that. I spend enough time
in [Python](/tags/python) that I prefer explicit to implicit when
practical.

``` html
<a class="h-card p-name u-url"
  href="https://randomgeekery.org">Brian Wisti</a>
```

microformats2
[prefixes](http://microformats.org/wiki/microformats2-prefixes) confuse
me, but they have a consistent pattern and rules for
[parsing](http://microformats.org/wiki/microformats2-parsing).

**Rules for microformats2 properties**

| Prefix | What it's called         | What we expect them to describe                       | Examples                                     |
| ------ | ------------------------ | ----------------------------------------------------- | -------------------------------------------- |
| `h-*`  | root class name          | Details about a person, post, event, etc.             | `h-card`, `h-entry`, `h-event`               |
| `p-*`  | plain text property      | Names, bios, descriptive text                         | `p-name`, `p-note`, `p-x-pronoun-nominative` |
| `u-*`  | URL property             | where to find sites, images, or other resources       | `u-url`, `u-uid`, `u-photo`                  |
| `dt-*` | datetime value           | Calendar entries for events, birthdays, anniversaries | `dt-bday`, `dt-start`, `dt-end`              |
| `e-*`  | embedded markup property | entire document subtrees                              | `e-content`                                  |

Now we can see that the link is an h-card, the link is a home page, and
the contents are a name. This says exactly the same thing as the
previous version. Do the extra classes add any real value here?

For a parser, maybe. For a human reader, no. I can clarify things for
this human writer, though.

``` html
<section class="h-card">
  <a class="u-url" href="https://randomgeekery.org">
    <span class="p-name">Brian Wisti</span>
  </a>
</section>
```

I still haven’t added much in the way of useful information. This
structure shows me where I can add other elements, and that’s progress.
Remember that microformats focuses on making life easier for the people
using them. It’s just that some of us are a little odd.

Let’s add some stuff. Profile cards usually have an image and a bio,
right?

``` html
<section class="h-card">
  <img class="u-photo" src="/img/avatar-thumbnail.jpg" alt="Brian Wisti">
  <p>
    <a class="u-url" href="https://randomgeekery.org">
      <span class="p-name">Brian Wisti</span>
    </a>:
    <span class="p-note">
      caffeinated, occasionally crafty geek in Seattle
    </span>
  </p>
</section>
```

microformats clarify intent — once you know them. I might have a dozen
photos in an h-card. Assigning `u-photo` lets me say "This one matters
when talking about me." Regardless of how many paragraphs of text I put
in my card, we know that the `p-note` text is describing me.

Okay, that’s actually worth looking at. There’s some CSS styling, but I
won’t get into that. Just spend a few days on
[CSS-Tricks](https://css-tricks.com/) and have fun.

![simple h-card screenshot](hcard-photo.png "h-card with bio and photo")

### Linking your card to other services

<https://randomgeekery.org> may be my home page, but it’s not the only
place folks find me. I routinely post on Mastodon and Twitter. I
sometimes peek my head in to see what’s new on Github and LinkedIn.
h-card can help integrate with those as well.

Add them as [rel-me](https://indieweb.org/rel-me) links\!

``` html
<a class="u-url" rel="me" href="https://hackers.town/@randomgeek">Mastodon</a>
```

The [a
element](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/a)'s
`rel` attribute describes a relationship between your page and the link.
Use [me](http://microformats.org/wiki/rel-me) to tell people that this
link is also about you. It’s a way to
[consolidate](http://microformats.org/wiki/identity-consolidation) the
online identities you want connected.

``` html
<ul>
  <li>
    <a class="u-url" rel="me" href="https://hackers.town/@randomgeek">Mastodon</a>
  </li>
  <li>
    <a class="u-url" rel="me" href="https://twitter.com/brianwisti">Twitter</a>
  </li>
  <li>
    <a class="u-url" rel="me" href="https://github.com/brianwisti">Github</a>
  </li>
</ul>
```

My [hackers.town](https://hackers.town/@randomgeek) Mastodon profile has
a link to this site. The site includes a rel-me link to my hackers.town
profile. Mastodon users looking at my profile see a verified connection
between each.

![screenshot of Mastodon profile page](hackers-town-profile.png
  "That's how you get a verified check on Mastodon sites")

### RelMeAuth

[RelMeAuth](https://indieweb.org/RelMeAuth) takes advantage of the
relation between your site and [OAuth](https://oauth.net/) providers. If
IndieWeb authenticators like [IndieLogin](https://indielogin.com/) and
[IndieAuth](https://indieauth.net/) see rel-me links to known providers,
they let you verify your site and yourself through those providers.

![screenshot of indielogin.com authentication](indielogin-auth.png
  "I can use my Twitter or Github accounts to authenticate")

#### Specifying my main page

New problem. My h-card now includes several `u-url` links that are all
me. Which one is the real me? I make that link the `u-uid`.

``` html
<a class="u-url u-uid" href="https://randomgeekery.org">
  <span class="p-name">Brian Wisti</span>
</a>:
```

![screenshot of updated h-card](hcard-relme.png "Now my name links to my u-uid")

### Add some details

This is a reasonable stopping point for a profile h-card. It names,
shows, and describes me, including links to find me on assorted social
networks. But I’d like to add some more information. Using microformats,
of course.

#### Where do I live?

I live in the city of Seattle. My `p-note` already says so. But again:
it might be useful to highlight it as a location. Several h-card options
describe locations in all the detail you could want — right down to
latitude and longtitude. But no. I’ll use `p-locality` and *maybe*
revisit later if I want more specificity.

``` html
<span class="p-note">
    Caffeinated, occasionally crafty geek in <span class="p-locality">Seattle</span>.
</span>
```

#### What interests me?

We all have hobbies, right? With `p-category` I list things we could
discuss. Let’s make links out of some that I’ve posted about.

``` html
<span class="p-note">
  Caffeinated, occasionally crafty geek in <span class="p-locality">Seattle</span>.
  I like <span class="p-category">FOSS</span>,
  <a class="p-category" href="/tags/drawing">drawing</a>,
  and <a class="p-category" href="/tags/knitting">yarn</a>.
</span>
```

#### What should you call me?

What about pronouns? That’s one way to specify I’m a person instead of
an organization.

Maybe I could skip it. My picture is beardy and my name is masculine.
Obviously I’m male. Then again, what’s obvious to me may be less so to
someone else. Explicit versus implicit.

Do I just tag myself "male" and move on? I could use `p-sex` or
`p-gender-identity`. That sounds unusably clunky to me. I’m unconcerned
what folks think about my chromosones. I just want them to know it’s
okay to call me ["he"](https://pronoun.is/he).

That’s one of my favorite things about h-cards and microformats. You can
opt-in to the pieces you care about, and leave the rest alone.

I thought about Jamie Tanna's
[example](https://www.jvt.me/posts/2019/04/10/pronouns-microformats/):

``` html
<span class="p-x-pronoun-nominative">he</span>/
<span class="p-x-pronoun-oblique">him</span>/
<span class="p-x-pronoun-possessive">his</span>
```

I like it, but that’s more markup than I want. What about using the link
to [Pronoun Island](https://pronoun.is) I used a moment ago? Let me look
over the microformats [pronouns
brainstorming](http://microformats.org/wiki/h-card-brainstorming#Pronouns)
and come up with something I like.

``` html
<a class="u-pronoun" href="https://pronoun.is/he">he / him / his</a>
```

`u-pronoun` isn’t an official property. Even so, it follows the
microformats2 style by using the `u-` prefix to indicate a link.

Okay so what do I have now?

``` html
<section class="h-card">
  <img class="u-photo" src="/img/avatar-thumbnail.jpg" alt="Brian Wisti">
  <p>
    <a class="u-url u-uid" href="https://randomgeekery.org">
      <span class="p-name">Brian Wisti</span>
    </a>:
    (
      <a class="u-pronoun" href="https://pronoun.is/he">he / him / his</a>
    )
    <span class="p-note">
      Caffeinated, occasionally crafty geek in <span class="p-locality">Seattle</span>.
      I like <span class="p-category">FOSS</span>,
      <a class="p-category" href="/tags/drawing">drawing</a>,
      and <a class="p-category" href="/tags/knitting">yarn</a>.
    </span>
  </p>
  <ul>
    <li>
      <a class="u-url" rel="me" href="https://hackers.town/@randomgeek">Mastodon</a>
    </li>
    <li>
      <a class="u-url" rel="me" href="https://twitter.com/brianwisti">Twitter</a>
    </li>
    <li>
      <a class="u-url" rel="me" href="https://github.com/brianwisti">Github</a>
    </li>
  </ul>
</section>
```

![image](hcard-details.png "Some styling distinguishes identity links from details")

### Validate me

Now my h-card includes all the information I care about. Time to make
sure I put it together correctly\! h-cards exist in the context of other
documents, like my Web page. Validation is less formal: mainly, check
that microformats2-aware parsers find your information.

The [mf2 validator](https://pin13.net/mf2/) shows you the results of
parsing either a URL or text provided by you, which makes it useful for
double-checking your h-card while building it.

![mf2 validator JSON output screenshot](mf2-validator.png
  "The mf2 validator produces JSON from your h-card")

The [IndieWebify.me validator](https://indiewebify.me/validate-h-card/)
styles its report for readability. It even offers suggestions for common
details you could add.

![IndieWebify.me h-card suggestion screenshot](validated-hcard.png "IndieWebify.me h-card summary")

It doesn’t accept raw HTML, though. You need to provide a URL, which is
less handy for an in-development h-card.

## What about some other h-cards?

I’m pretty much done, other than a plan to incorporate [Fork
Awesome](https://forkaweso.me/Fork-Awesome/) for me rel-me links. But
that’s a topic for another day, if ever.

Do you want to see more h-cards out in the world? The IndieWeb wiki
maintains a list of [example
h-cards](https://indieweb.org/h-card#IndieWeb_Examples), including links
to other collections.

Most h-cards I see are small, but they don’t have to be. Martijn van der Ven's h-card
fills an entire page. Have fun coming up with something that works for
you!