---
aliases:
- /post/2016/disqus-in-hugo/
- /2016/06/23/using-disqus-in-hugo/
category: tools
date: 2016-06-23 00:00:00
layout: layout:PublishedArticle
slug: using-disqus-in-hugo
tags:
- hugo
- site
- disqus
title: Using Disqus in Hugo
uuid: d4d8caee-5d75-4b88-8e60-396a8cd2dc14
---

All right fine. Some visitor may want to leave a comment about one or another
of my posts. I can do that with Hugo.
<!--more-->

[documented steps]: http://gohugo.io/extras/comments/
[Hugo]: http://gohugo.io
[Disqus]: https://disqus.com/

I used the [documented steps][] for adding [Disqus][] comments to [Hugo][].
Though Hugo provides a usable internal template for Disqus, using it as-is
will result in a record-keeping headache if you test your site locally.

* You look at the page locally
* The Disqus code is loaded
* Disqus creates a new comment thread for your local page
* Before you know it you have dozens of `localhost:1313` comment threads
obscuring the live threads.

To avoid that, use the following `partials/disqus.html` fragment described
in the Hugo documentation. It will skip loading comments when viewing your
content from localhost.

``` html
<div id="disqus_thread"></div>
<script type="text/javascript">

(function() {
      // Don't ever inject Disqus on localhost--it creates unwanted
      // discussions from 'localhost:1313' on your Disqus account...
      if (window.location.hostname == "localhost")
                return;

      var dsq = document.createElement('script'); dsq.type = 'text/javascript'; dsq.async = true;
      var disqus_shortname = '{{ .Site.DisqusShortname }}';
      dsq.src = '//' + disqus_shortname + '.disqus.com/embed.js';
      (document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0]).appendChild(dsq);
})();
</script>
<noscript>Please enable JavaScript to view the <a href="http://disqus.com/?ref_noscript">comments powered by Disqus.</a></noscript>
<a href="http://disqus.com/" class="dsq-brlink">comments powered by <span class="logo-disqus">Disqus</span></a>
```

That template needs `.Site.DisqusShortname`, which you set in your site config.

```yaml
disqusShortName: yourshortname # whatever you set up on Disqus
```

Now you can use the partial in the appropriate template. I put the call for mine in `_default/single.ace`.

``` handlebars
    footer
      = include partials/timeline.html .
      {{ partial "disqus.html" . }}
```

There. Now if you really want to say anything, are viewing the live site,
and have JavaScript enabled, you can in the section below.

[David Wheeler]: http://theory.pm/

I will probably adjust the template over time, since I don't want to burden non-commenting
visitors with the extra load from calling out to Disqus. I like the approach [David Wheeler][]
took with his site: do nothing until visitor directly uses the "Load Comments" button.