---
aliases:
- /blogspot/2007/02/12_mp4info-issues.html
- /post/2007/mp4info-issues/
- /2007/02/12/mp4info-issues/
category: blogspot
date: 2007-02-12 00:00:00
layout: layout:PublishedArticle
slug: mp4info-issues
tags:
- ruby
title: Mp4Info issues
updated: 2015-03-28 00:00:00
uuid: 05791c44-5d02-431c-a05d-d16dc8676f4f
---

:::note Update 2015-03-28

No idea whether this is still true, or even if it was just something stupid I
was doing in 2007.

:::

[mp4info]: https://github.com/arbarlow/ruby-mp4info

[mp4info][] thinks that my 5 minute Bob Newhart track is 2 seconds long. Looks
like that is an issue on several tracks. I need to dig into that, see why Perl's
MP4::Info picks up the correct length but the Ruby counterpart does not.