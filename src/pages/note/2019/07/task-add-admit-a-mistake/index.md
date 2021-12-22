---
aliases:
- /note/2019/184/task-add-admit-a-mistake/
date: 2019-07-03 16:18:47
layout: layout:PublishedArticle
slug: task-add-admit-a-mistake
tags:
- taskwarrior
- oops
title: task add 'admit a mistake'
uuid: 7db7a148-0a29-418b-9b3a-6f1d05db7a95
---

My [glance][] at the Idea Bucket only worked by luck. The `+LATEST` virtual tag
is for the latest task in the system, not just the latest in the filter. I want
the `newest` report, which lists tasks by freshness, then `limit:` to control
the number of tasks reported.

[glance]: /note/2019/06/checking-in-on-my-idea-bucket/

```
$ task '(+idea or +learn)' newest limit:1

ID  Created    Age Mod Project Tags     Description
180 2019-07-02 19h 19h Site    idea ops automate permalink switches
                                          2019-07-02 for when I do a mass change, create aliases of old form

54 tasks, 1 shown
```

Okay right. I threw some new ideas in the last few days. Better set a higher
limit.

```
$ task '(+idea or +learn)' newest limit:3

ID  Created    Age Mod Project Tags             Description
180 2019-07-02 19h 19h Site    idea ops         automate permalink switches
                                                  2019-07-02 for when I do a mass change, create aliases of old form
176 2019-06-28 4d  4d          db learn         json1 extension for sqlite
175 2019-06-28 4d  4d          javascript learn set up entropic for Node
```