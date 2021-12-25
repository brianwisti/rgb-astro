---
aliases:
- /note/2019/223/proudly-doing-it-wrong/
caption: Yeah that's Visual Studio Code. I'm trying new things.
cover_image: cover.png
date: 2019-08-12 03:04:00
layout: layout:PublishedArticle
slug: proudly-doing-it-wrong
tags:
- screenshot
- javascript
- no-i-know
- i-will-fix-it
title: Proudly doing it wrong
uuid: f880fe51-3798-441f-b231-0cc64aa751f1
---

1. write a [site weight][] script that prints a report to the console
2. make the script write the report to a file, and include the file in [/now][]. Now site building looks like:
    1. build the site
    2. weigh the site
    3. build the site and include the new report
    4. upload!
3. (today) make the script write the info as JSON instead
4. throw in some [vue.js][] to fetch the JSON and reproduce the original report format almost exactly.
5. profit?

But hey at least I don't need to rebuild the site after weighing it. And when free time next allows I'll learn
a little more Vue.js and make the report prettier.

[site weight]: /post/2019/06/weighing-files-with-python/
[/now]: /now
[vue.js]: https://vuejs.org/
