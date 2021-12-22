---
aliases:
- /post/2017/logging-money-in-org-mode/
- /2017/07/31/logging-money-in-org-mode/
category: tools
cover_image: cover.png
date: 2017-07-31
draft: false
layout: layout:PublishedArticle
slug: logging-money-in-org-mode
tags:
- emacs
- OrgMode
- budgeting
title: Logging Money In Org Mode
updated: 2020-03-01
uuid: cf7820f5-ed9b-4840-8599-9e79c1625574
---

[Org mode]: https://orgmode.org

I am setting up Emacs [Org mode][] to track how I use my money. This is a
healthy habit, which I applied in the past with a little paper notebook. This
needs to be as easy as that little notebook, or I will never use it.

<aside class="admonition">
<p class="admonition-title">Updates</p>

2020-03-01
: It wasn’t. I didn’t. But I’ve built on this for a new approach. If it sticks
  for a whole week I’ll post about it.

</aside>

I only want to see how I use my money. This can eventually become part of a
budget, but all I want today is the ability to make quick money notes.

* My friend paid me back some money they borrowed
* One of the housemates chipped in for groceries
* I treated myself to coffee.

Stuff like that. Let’s see what I come up with.

What about my phone?

I know there are budgeting phone apps. Those apps just haven’t served my needs.
I spend more time in front of a computer than using my phone. I type at a
keyboard quicker than on a phone.

## The Setup

[journaling features]: http://www.howardism.org/Technical/Emacs/journaling-org.html
[capture template]: http://orgmode.org/manual/Capture-templates.html#Capture-templates

I already use [journaling features][] of Emacs org mode to record tasks that I
accomplish through the day. That journal could also record income and expenses.
I need a new org [capture template][] and menu item for money, though.

## Adding a menu entry and template

`org-capture-templates` holds templates for creating new org entries. I manually
edit mine, although the recommended approach to managing those is through the
Emacs Customize interface. Old habits die hard.

```elisp
;; Probably easier for most folks to manage this with Customize (C-c c C),
;; but setting this stuff directly helps me understand the structure better.

(setq org-capture-templates
      (quote
       (("p" "Personal")
        ; ... other entries removed for clarity
        ("pm" "Money entry" entry
         (file+datetree "~/Sync/org/agendas/journal.org")
         "** %U - %^{Amount} %^{Summary} :money:%^g"))))
```

I start with fields needed for the template selection menu in `org-capture`. I
also tell org mode to save money entries will in the `journal.org` file under a
*date tree*, which presents a year / month / date heirarchy for entries.
Finally, I describe the capture template.

[template expansion]: http://orgmode.org/manual/Template-expansion.html#Template-expansion

A capture template can be a string or file containing text and template
directives. A short string describes money entries. The table below explains the
[template expansion][] rules I used.

| Code          | What it does
| ------------- | ------------
| `%U`          | Creates an _inactive_ timestamp, which will not appear in my regular agenda
| `%^{Amount}`  | Prompts me for the dollar amount of this transaction
| `%^{Summary}` | Prompts me for a summary of this transaction
| `%^g`         | Prompts me for additional tags for this transaction

This template does not validate input. I don’t know how to do that yet. I must
remember to use money values for "Amount" and to tag every transaction as
`:income` or `:expense:`. Later I can learn how to enforce these rules with
code.

## Triggering a Capture

<kbd>C-c c</kbd> is a global binding which starts `org-capture` from whatever I’m doing.

![menu 1 for money capture](org-capture-menu-1.png "<kbd>C-c c</kbd> to enter org capture menu")

![menu 2 for money capture](org-capture-menu-2.png "<kbd></kbd> then <kbd>m</kbd> for a Personal Money entry")

I get prompted for Amount, Summary, and tags. Once I answer those prompts, I am
shown the Capture buffer. I don’t need to change anything, so I finalize the
entry with `C-c C-c`.

![Finalize capture buffer](org-money-capture-buffer.png "<kbd>C-c C-c</kbd> to finalize")

After I finalize the entry, Emacs closes the Capture buffer and returns me to
whatever I was doing before. I can complete the whole process in about five
seconds, which makes it even more convenient for me than the old paper notebook.

## Filtering my agenda

Even though Org knows `journal.org` is an agenda file, inactive timestamps
aren’t shown in the default agenda view. I’m okay with this for now. Things can
get a little cluttered if I start showing every logged item.

### Show me all the `:money:` entries

`C-c a` opens the menu of Agenda commands. m lets me search for tag matches.
Let’s start with all `:money:` entries.

![Filtered on money](agenda-filter-money.png "<kbd>C-c a m money</kbd> to filter on the :money: tag")

### Show me income

I already have the agenda match view open, so I use C-u r` to refresh with a
new search string, "income".

![Filtered on income](agenda-filter-income.png "<kbd>C-u r income</kbd> to filter on the :income: tag")

### Show me expenses

Again, I use `C-u r` to refresh, this time looking for entries that match
"expense".

![Filtered on expense](agenda-filter-expense.png "<kbd>C-u r expense</kbd> to filter on the :expense: tag")

## STOP HERE

Oh I want to get fancy so bad. Honestly though, I need to set the basic habit of
logging all the little things I do with my money. Besides, this gives me
something to learn and write future blog posts about!