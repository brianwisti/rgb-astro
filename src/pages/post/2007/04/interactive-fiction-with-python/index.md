---
aliases:
- /coolnamehere/2007/04/19_interactive-fiction-with-python.html
- /post/2007/interactive-fiction-with-python/
- /2007/04/18/interactive-fiction-with-python/
category: coolnamehere
date: 2007-04-18 00:00:00
layout: layout:PublishedArticle
series:
- Python Interactive Fiction
slug: interactive-fiction-with-python
tags:
- python
- ifiction
- learn
title: Interactive Fiction with Python
updated: 2009-07-11 00:00:00
uuid: 80581bcf-0ba0-43f5-90e1-36e0eae3a170
---

The idea for this article came from a coolnamehere reader 
named Laura. Thanks, Laura! I was looking for good Python ideas.
<!--more-->

## Pages

* Introduction
* [01 Building a Single Round](/post/2007/04/python-interactive-fiction-01-handling-a-single-round/)
* [02 Tying The Scenes Together](/post/2007/04/python-interactive-fiction-02-tying-the-scenes-together/)
* [03 Handling Multiple Turns](/post/2007/06-python-interactive-fiction-03-handling-multiple-turns/)

## Introduction

I loved [Choose Your Own Adventure](http://www.cyoa.com/ "Choose Your Own Adventure Home") 
books when as a kid. I consumed them pretty much non-stop until my hobbies expanded into
gaming and programming. 

One of my readers recently asked how hard it would be to write simple text 
adventure games. It occurred to me that she was essentially describing a digital
version of "Choose Your Own Adventure." Then I started figuring out how I would write this
kind of game in order to answer her question.

I ended up sending her an email that said "You can do it" followed by several hundred words
that really belonged in a tutorial. It would be better to put the information here than to
clutter her inbox too much, I think.

By the way - if what you *really* want to do is create interactive fiction and you're not
interested in creating the game engine itself, I suggest you take a close look at
[Inform](http://inform-fiction.org/). It is a remarkable system with its own custom language
for creating your tales.

## Describing the Game

Interactive fiction can be more straightforward than a lot of games, because the game 
author decides everything that can happen. The game we're making here is even more 
straightforward than most interactive fiction, because we are only providing the 
user with narrow lists of choices.

Our version of interactive fiction is going to consist of a bunch of scenes along with paths 
that can be taken in each scene. A path can lead to one of two things:

1. Another scene, with its own list of paths
2. The end of the story, whether it is a success or a failure.

Let's take a moment to describe game play. A game like this can be described in a single paragraph.

> The user is shown a scene description and a menu of actions that can be done in that scene. 
> When she selects an action, she is presented with the description and menu for that scene. 
> This is repeated for each action she chooses, until she reaches a scene with no actions. The 
> game is over when she reaches a scene with no actions.

This is a fair description of what we are trying to do, but it is missing at least one 
element: quitting. Let's make "quit" an option available on every menu, even if there 
are no actions available.

> There is a *quit* command available on every menu, whether there are actions available for 
> that scene or not. Selecting *quit* will end the program.

## The Story Map

Okay - you've got the rough idea of what you want. You probably want to map the 
story out on paper before turning it into code, because that will make the task 
of programming it a lot easier. Let's start with a really small story, say five 
scenes. Each scene has a description and a menu of paths to other scenes.

### Scene 1: The Field

> You are standing in a field. To the north of you are some mountains, to the 
> east of you is a forest, to the west of you is a cave, and to the south of 
> you is a valley.

Paths

+ Go to the mountains
+ Go into the forest
+ Go into the cave
+ Go to the valley

### Scene 2: The Mountains

> You are standing at the foot of a mountain range. Huge impassable peaks 
> loom over you. There is a cave to the east, and a field south of you 
> leading into a valley.

Paths

+ Go into the cave
+ Go south into the field

### Scene 3: The Forest

> A giant confused bear mistakes you for one of her cubs and takes you away 
> with her. Although you eventually learn to love your new bear family, your 
> adventuring days are over.

Paths

+ None *(This is a story ending)*

### Scene 4: The Cave

> You are in a long dark cave. You see points of daylight at either end of the 
> cave, one to the northeast and one to the southwest.

Paths

+ Go northeast *(leads to the mountains)*
+ Go southwest *(leads to the field)*

### Scene 5: The Valley

> You are standing in the middle of a huge, beautiful valley. Standing right 
> before you is ... whatever it you were looking for. Success!

Paths

+ None *(This is a story ending)*

We have scenes and we have a complete description of how the game works. This is 
more or less what they call a "specification," because it specifies what the program 
will need to do. Specifications can become incredibly huge as your goals become 
more complex. Writing them is an art - you have to get all the requirements down 
on paper, but you also try to keep things short and sweet so that your development 
team will actually *read* them. It is even harder than that, because the requirements 
change as development continues. Yep - writing specs is hard, and I haven't gotten 
the art down myself.