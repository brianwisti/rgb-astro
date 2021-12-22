---
category: programming
date: 2021-08-15
description: Spent the day goofing off with Mastodon.py
draft: false
format: md
layout: layout:PublishedArticle
tags:
- python
- mastodon
title: Tooting with Python
uuid: 53713d6b-a624-44ab-9f23-535794bd2b6d
---

## What?

Let's set up a [Mastodon][mastodon] application with Python to read and post toots.

### How?

[Python][python] is the [second best][second-best] tool for any job in 2021,
which makes it an excellent glue language.  I've been centering my site
workflow around it. That means the [Mastodon.py][mastodon-py] library, which I
have dabbled with once or twice before.

### Why?

Because I've let the [#IndieWeb][indieweb-tag] social aspects of this site go
stale and one step to fixing that is restoring POSSE automation. The first part
of *that* is making sure I remember how to automate posting to Mastodon.

## Ok fine; get on with it

Course, you're going to need an account at a Mastodon instance.  I have
[mine][hackers-town].  You can find one suitable for your tastes at [Mastodon
instances][instances].

:::note

If you don't already know Mastodon, think of it as island versions of
[Twitter][twitter].  Each instance has its own practices and policies depending on who
runs it, so it's very much a "hanging out at a friend's house" experience.
Lots more details, but much more than I feel like covering.

It's fun. You should try it out maybe. You can even host your own instance
if you're hard-core into DIY.

:::

### Registering your application

I have 2FA enabled, so it turned out to be easier for me to set up the
application in account preferences (under the "Development" section).

I entered an application name, added my Website for "Application website," and
selected the scopes that are important to me for today's explorations.

`read`
: read all your account's data

`write:statuses`
: publish statuses

That's enough to cover today's play.  I'm not creating my own full-fledged
Mastodon client so I don't need every permission.

### Connecting your application

``` python
import json
import os
import sys
from dataclasses import dataclass
from typing import Any, Callable, Dict

from mastodon import Mastodon
from rich.pretty import pprint
```

:::note

Spoiler alert: yes I'll be using [Rich][rich] and [dataclasses][] along with
Mastodon.py.  Nothing fancy planned with Rich today. It's just part of my
regular toolkit.

The dataclasses library comes standard with Python these days, but you may
need to install the others:

``` bash
pip install --upgrade rich mastodon
```

:::

The Mastodon instance developer panel gives me the details I need to connect.
I set them as workspace environment variables with [direnv][] out of habit, but
you could just as easily hard-code them in Python or define in a config file of
your own.

``` python
API_BASE = os.environ.get("API_BASE")
CLIENT_KEY = os.environ.get("CLIENT_KEY")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
```

From my first few attempts writing this post, I know I'll want a class to
organize views for the connection.

```python
@dataclass
class App:
    """Provides convenience methods for querying an instance and posting toots."""

    mastodon: Mastodon
```

Once I have a connection, I don't care about those application config details.
Rather than storing them in the instance, I'll use a class method to handle the
work and return my new App with only the details I *do* care about.

``` python
 class App:

    @classmethod
    def connect(
        cls,
        client_key: str = CLIENT_KEY,
        api_base_url: str = API_BASE,
        client_secret: str = CLIENT_SECRET,
        access_token: str = ACCESS_TOKEN,
    ) -> "App":
        """Return an App connected to a specific Mastodon instance."""

        mastodon = Mastodon(
            client_id=client_key,
            api_base_url=api_base_url,
            client_secret=client_secret,
            access_token=access_token,
        )
        return cls(mastodon=mastodon)
```

Basic setup's done. Let's create an App and see if it worked.

``` python
if __name__ == "__main__":
    app = App.connect()
    pprint(app)
```
<pre style="font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">App</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">mastodon</span>=<span style="font-weight: bold">&lt;</span><span style="color: #ff00ff; text-decoration-color: #ff00ff; font-weight: bold">mastodon.Mastodon.Mastodon</span><span style="color: #000000; text-decoration-color: #000000"> object at </span><span style="color: #008080; text-decoration-color: #008080; font-weight: bold">0x7ff14f1e8850</span><span style="font-weight: bold">&gt;)</span>
  </pre>

:::note{title="Exporting Rich output"}

My code doesn't look *exactly* like what I've shared here. I take advantage
of Rich's export features to simplify sharing program output.

``` python
import rich

# ...

if __name__ == "__main__":
    rich.reconfigure(record=True, width=80)
    # ...
    rich.get_console().save_html("output.html", inline_styles=True)
```

The extra bits change two aspects of Rich's default [Console][console] behavior:

- record output so it can be exported by `save_text` or `save_html` and I can add it here in my post
- set console width to 80, simplifying display of exported output within the confines of a Web page

After `app` does its thing, I export any output as formatted HTML,
where I can edit as needed and insert here.

:::

So anyways, we verified that our connection works. Let's take a look at what
that connection provides.

### The instance

Mastodon.py provides methods specifically for [reading instance
details][reading-data-instances].  For example,
[`instance_health`][instance-health] tells of if a quick health check
succeeded.

``` python
app = App.connect()

if app.mastodon.instance_health():
    rich.print("Connection instance is [green]healthy[/green]")
else:
    rich.print("Connection instance is [red][b]not[/b] healthy![/red]")
    sys.exit(1)
```

 <pre style="font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">Connection instance is <span style="color: #008000; text-decoration-color: #008000">healthy</span>
   </pre>

#### Instance details

Most of the querying methods return a dictionary or a list of dictionaries.
[`Mastodon.instance`][mastodon-instance] returns an [instance
dict][instance-dict].

I don't feel like showing every item in that dictionary, though. Let's pick a
few to make a decent summary. Oh hey, and let's cache that dictionary to disk
so I'm not making a fresh API query every time I check this post while I'm
writing it.

:::note

Be considerate about server resources for Mastodon. Most instances are run as
personal projects. There's no need for us to run up their AWS bill.

:::

``` python
def stored(func: Callable) -> Dict[str, Any]:
    def inner(*args, **kwargs):
        filename = f"{func.__name__}.json"
        rich.print(f"stored.inner for {func.__name__}")

        if os.path.exists(filename):
            with open(filename, "r") as f:
                rich.print(f"Loading data from {filename}")
                data = json.load(f)
            return data

        rich.print(f"Calling {func.__name__}")
        data = func(*args, **kwargs)

        with open(filename, "w") as f:
            rich.print(f"Writing data to {filename}")
            json.dump(data, f, indent=4, default=str)

        return data

    return inner
```

I can do proper memoization later. "Look for a file before you hit the server"
is good enough for writing a blog post.

``` python
class App:

    @stored
    def instance(self) -> Dict[str, Any]:
        """Return a dictionary of information about the connected instance."""

        return self.mastodon.instance()

    def instance_summary(self) -> Dict[str, Any]:
        """Return a small dictionary of instance information."""

        instance = self.instance()
        fields = ["uri", "title", "short_description"]
        data = {field: instance[field] for field in fields}
        data["contact_account"] = instance["contact_account"]["display_name"]

        return data
```

Time to look at that instance summary.

``` python
if __name__ == "__main__":
    app = App.connect()

    if app.mastodon.instance_health():
        rich.print("Connection instance is [green]healthy[/green]")
    else:
        rich.print("Connection instance is [red][b]not[/b] healthy![/red]")
        sys.exit(1)

    pprint(app.instance_summary())
```

<pre style="font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">Connection instance is <span style="color: #008000; text-decoration-color: #008000">healthy</span>
  stored.inner for instance
  Calling instance
  Writing data to instance.json
  <span style="font-weight: bold">{</span>
  <span style="color: #7fbf7f; text-decoration-color: #7fbf7f">│   </span><span style="color: #008000; text-decoration-color: #008000">'uri'</span>: <span style="color: #008000; text-decoration-color: #008000">'hackers.town'</span>,
  <span style="color: #7fbf7f; text-decoration-color: #7fbf7f">│   </span><span style="color: #008000; text-decoration-color: #008000">'title'</span>: <span style="color: #008000; text-decoration-color: #008000">'hackers.town'</span>,
  <span style="color: #7fbf7f; text-decoration-color: #7fbf7f">│   </span><span style="color: #008000; text-decoration-color: #008000">'short_description'</span>: <span style="color: #008000; text-decoration-color: #008000">"A bunch of technomancers in the fediverse. Keep it fairly clean please. This arcology is for all who wash up upon it's digital shore."</span>,
  <span style="color: #7fbf7f; text-decoration-color: #7fbf7f">│   </span><span style="color: #008000; text-decoration-color: #008000">'contact_account'</span>: <span style="color: #008000; text-decoration-color: #008000">'The_Gibson'</span>
  <span style="font-weight: bold">}</span>
  </pre>

### Reading the timelines

Mastodon's [timeline methods][timeline-methods] provide different views of
recent post activity, both public and private.  To simplify demonstration on
this public blog post, I'll stick to [`timeline_public`][timeline-public].

``` python
class App:
  @stored
  def timeline_public(self) -> List[Dict[str, Any]]:
      return self.mastodon.timeline_public()
```

The [toot-dict][toot-dict] also contains far more information than I need, so
let's summarize those like with instances.

``` python
class App:

  def timeline_summary(self) -> Dict[str, Any]:
      timeline = self.timeline_public()
      return [
          {
              "date": toot["created_at"],
              "author": toot["account"]["display_name"],
              "content": toot["content"],
          }
          for toot in timeline
      ]
```

Adding `app.timeline_summary()` to the main block:

``` python
if __name__ == "__main__":
    app = App.connect()

    if app.mastodon.instance_health():
        rich.print("Connection instance is [green]healthy[/green]")
    else:
        rich.print("Connection instance is [red][b]not[/b] healthy![/red]")
        sys.exit(1)

    pprint(app.instance_summary())
    pprint(app.timeline_summary(), max_string=80)
```

<pre style="font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">Connection instance is <span style="color: #008000; text-decoration-color: #008000">healthy</span>
  stored.inner for instance
  Loading data from instance.json
  <span style="font-weight: bold">{</span>
  <span style="color: #7fbf7f; text-decoration-color: #7fbf7f">│   </span><span style="color: #008000; text-decoration-color: #008000">'uri'</span>: <span style="color: #008000; text-decoration-color: #008000">'hackers.town'</span>,
  <span style="color: #7fbf7f; text-decoration-color: #7fbf7f">│   </span><span style="color: #008000; text-decoration-color: #008000">'title'</span>: <span style="color: #008000; text-decoration-color: #008000">'hackers.town'</span>,
  <span style="color: #7fbf7f; text-decoration-color: #7fbf7f">│   </span><span style="color: #008000; text-decoration-color: #008000">'short_description'</span>: <span style="color: #008000; text-decoration-color: #008000">"A bunch of technomancers in the fediverse. Keep it fairly clean please. This arcology is for all who wash up upon it's digital shore."</span>,
  <span style="color: #7fbf7f; text-decoration-color: #7fbf7f">│   </span><span style="color: #008000; text-decoration-color: #008000">'contact_account'</span>: <span style="color: #008000; text-decoration-color: #008000">'The_Gibson'</span>
  <span style="font-weight: bold">}</span>
  stored.inner for timeline_public
  Calling timeline_public
  Writing data to timeline_public.json
  <span style="font-weight: bold">[</span>
  <span style="font-style: italic">    .. skipping a few ...</span>
  <span style="color: #7fbf7f; text-decoration-color: #7fbf7f">│   </span><span style="font-weight: bold">{</span>
  <span style="color: #7fbf7f; text-decoration-color: #7fbf7f">│   │   </span><span style="color: #008000; text-decoration-color: #008000">'date'</span>: <span style="color: #008000; text-decoration-color: #008000">'2021-08-15 22:24:35+00:00'</span>,
  <span style="color: #7fbf7f; text-decoration-color: #7fbf7f">│   │   </span><span style="color: #008000; text-decoration-color: #008000">'author'</span>: <span style="color: #008000; text-decoration-color: #008000">'Endless Screaming'</span>,
  <span style="color: #7fbf7f; text-decoration-color: #7fbf7f">│   │   </span><span style="color: #008000; text-decoration-color: #008000">'content'</span>: <span style="color: #008000; text-decoration-color: #008000">'&lt;p&gt;AAAAAAAAAAAAAAAAAAAAH&lt;/p&gt;'</span>
  <span style="color: #7fbf7f; text-decoration-color: #7fbf7f">│   </span><span style="font-weight: bold">}</span>,
  <span style="color: #7fbf7f; text-decoration-color: #7fbf7f">│   </span><span style="font-weight: bold">{</span>
  <span style="color: #7fbf7f; text-decoration-color: #7fbf7f">│   │   </span><span style="color: #008000; text-decoration-color: #008000">'date'</span>: <span style="color: #008000; text-decoration-color: #008000">'2021-08-15 22:24:43.531000+00:00'</span>,
  <span style="color: #7fbf7f; text-decoration-color: #7fbf7f">│   │   </span><span style="color: #008000; text-decoration-color: #008000">'author'</span>: <span style="color: #008000; text-decoration-color: #008000">'Lynne'</span>,
  <span style="color: #7fbf7f; text-decoration-color: #7fbf7f">│   │   </span><span style="color: #008000; text-decoration-color: #008000">'content'</span>: <span style="color: #008000; text-decoration-color: #008000">'&lt;p&gt;This just touched a single topic that I’ve never heard being brought up anywh'</span>+<span style="color: #008080; text-decoration-color: #008080; font-weight: bold">97</span>
  <span style="color: #7fbf7f; text-decoration-color: #7fbf7f">│   </span><span style="font-weight: bold">}</span>
  <span style="font-weight: bold">]</span>
  </pre>

Nice. Looks like `content` is in HTML format. Need to remember that if I ever
make a more interesting Mastodon client.

But I'm ready to start tooting.

### Writing

Mastodon [write methods][write-methods] let us add toots, polls, replies, reblogs, faves. All
that good stuff.

Let's stick with your basic toot for now.

``` python
class App:
  def status_post(self, status: str, visibility: str = "direct") -> Dict[str, Any]:
      """Post a toot to our connection, private unless we say otherwise."""

      return self.mastodon.status_post(status, visibility=visibility)
```

``` python
if __name__ == "__main__":
    app = App.connect()

    if app.mastodon.instance_health():
        rich.print("Connection instance is [green]healthy[/green]")
    else:
        rich.print("Connection instance is [red][b]not[/b] healthy![/red]")
        sys.exit(1)

    status_text = "Ignore me, just messing with Mastodon.py"
    app.status_post(status_text)
```

#[It worked!](./toot.jpg [screenshot of posted toot])

Okay my brain is fading. Should probably put away the keyboard soon.

## Wrap it up

Am I done?

Well, no. I still need to turn this into a proper command line application that
looks for the newest published blog post and posts a toot about it. But that's
not going to happen in today's post.

I had fun, and that's the important part.

[mastodon]: https://joinmastodon.org
[python]: https://python.org
[second-best]: https://twitter.com/glyph/status/1426414435275448324
[mastodon-py]: https://mastodonpy.readthedocs.io/en/stable/
[indieweb-tag]: /tags/indieweb
[hackers-town]: https://hackers.town/@randomgeek
[instances]: https://instances.social
[twitter]: https://twitter.com
[dataclasses]: https://docs.python.org/3/library/dataclasses.html
[rich]: https://rich.readthedocs.io/en/stable/index.html
[direnv]: https://direnv.net
[console]: https://rich.readthedocs.io/en/stable/reference/console.html#rich.console.Console
[reading-data-instances]: https://mastodonpy.readthedocs.io/en/stable/#reading-data-instances
[instance-health]: https://mastodonpy.readthedocs.io/en/stable/#mastodon.Mastodon.instance_health
[mastodon-instance]: https://mastodonpy.readthedocs.io/en/stable/#mastodon.Mastodon.instance
[instance-dict]: https://mastodonpy.readthedocs.io/en/stable/#instance-dicts
[timeline-methods]: https://mastodonpy.readthedocs.io/en/stable/#reading-data-timelines
[timeline-public]: https://mastodonpy.readthedocs.io/en/stable/#mastodon.Mastodon.timeline_public
[toot0dict]: https://mastodonpy.readthedocs.io/en/stable/#toot-dicts
[write-methods]: https://mastodonpy.readthedocs.io/en/stable/#writing-data-statuses