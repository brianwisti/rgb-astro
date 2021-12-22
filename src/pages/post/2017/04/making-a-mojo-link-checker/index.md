---
aliases:
- /post/2017/making-a-mojo-link-checker/
- /2017/04/11/making-a-mojo-link-checker/
category: Programming
date: 2017-04-11
draft: false
layout: layout:PublishedArticle
slug: making-a-mojo-link-checker
tags:
- perl
- site
- mojolicious
title: Making A Mojo Link Checker
uuid: 0a59ade7-b170-49e9-8732-e8b8c03e484d
---

I wrote a Perl script using utility features in Mojolicious to check all of the links in my Hugo site.

[link rot]: https://en.wikipedia.org/wiki/Link_rot

Nothing lasts forever. Sites get reorganized, move, or disappear.
As my own site has gotten older — some of these pages are over fifteen years old — links from old posts stop working.
[link rot][] is a fact of life on the Internet.
I want to minimize it here.

Instead of manually checking each of the 245 posts on this site, I chose to write some code that identifies the dead end links.
Then I could manually adjust the bad links.
Yay!
That’s hand-crafted automation there.

## use Mojo!

[Mojolicious]: http://mojolicious.org/
[Perl]: https://perl.org/
[excellent support]: http://mojolicious.org/perldoc#REFERENCE

[Mojolicious][] is a [Perl][] framework for making Web applications.
It also happens to provide [excellent support][] for a wide range of Web-related programming.

[before]: /tags/mojolicious/

I mentioned Mojolicious here [before][].
I use it as a part of my daily dev toolkit, even though I *still* haven’t made a real Web app with it.

## The code

I could just dump the script here and go on with my day, but I feel like typing a lot for some reason.
Let’s go through the major chunks of the code.

### The setup

```perl
use 5.24.0;
use warnings;
use experimental 'signatures';
```

Whenever possible, I specify the latest version of Perl (currently [5.24](http://perldoc.perl.org/perl5240delta.html).
It enables some features and deprecates others.
If nothing else, it reminds me when I last worked on the code.
Recent Perl versions automatically enable [`strict`](http://perldoc.perl.org/strict.html),
but it’s useful for me to also turn on [`warnings`](http://perldoc.perl.org/warnings.html).

The [`experimental`](https://metacpan.org/pod/experimental) CPAN module saves
some boiler plate when using Perl features that have not fully stabilized ---
such as function [signatures](http://perldoc.perl.org/feature.html#The-'signatures'-feature).

```perl
use Mojo::DOM;
use Mojo::File;
use Mojo::JSON qw(decode_json);
use Mojo::URL;
use Mojo::UserAgent;
```

Mojolicious provides a remarkable amount of functionality for such a small installation. This is just what I’m explicitly using.

[LWP::UserAgent]: https://metacpan.org/pod/LWP::UserAgent[L
[Requests]: http://docs.python-requests.org/en/master/

[Mojo::DOM](http://mojolicious.org/perldoc/Mojo/DOM)
: HTML/XML DOM parser that supports [CSS Selectors](https://www.w3.org/TR/CSS2/selector.html)

[Mojo::File](http://mojolicious.org/perldoc/Mojo/File)
: for handling filepaths and easy reading / writing files.

[Mojo::JSON](http://mojolicious.org/perldoc/Mojo/JSON)
: `decode_json` lets me turn the [Hugo](http://gohugo.io/) `config.json` file into a Perl structure.

[Mojo::URL](http://mojolicious.org/perldoc/Mojo/URL)
: understands the components of Uniform Resource Locators

[Mojo::UserAgent](http://mojolicious.org/perldoc/Mojo/UserAgent)
: makes HTTP and WebSocket requests (similar to [LWP::UserAgent][], or [Requests][] for Python people)

### From the top

```perl
my $config_file   = "config.json";
my $config        = decode_json(Mojo::File->new($config_file)->slurp);
my $site          = Mojo::URL->new($config->{BaseURL});
my $root          = $config->{publishDir} || 'public';
my $checked_links = {};
my $ua            = Mojo::UserAgent->new;
$ua->max_redirects( 5 ); # some sites love lots of redirects

my $test_file = shift @ARGV // '';

if ( $test_file ) {
  check_links_in( $test_file, $ua );
}
else {
  my $path = Mojo::File->new( $root );
  my $files = $path->list_tree->grep( qr{ \. (?:html|xml )$ }x );

  $files->each( sub { check_links_in($_); } );
}
```

This is the important bit:
load the config, create a user agent, and check links in one or all of the generated HTML files.
I checked the generated HTML files in `public` because I didn’t feel like messing with `hugo server` or a Mojolicious mini-app.
Scraping a local server could be an option later.

[configuration formats]: http://gohugo.io/overview/configuration/
[`slurp`]: http://mojolicious.org/perldoc/Mojo/File#slurp
[`decode_json`]: http://mojolicious.org/perldoc/Mojo/JSON#decode_json

Using Mojolicious for everything was so much fun that I rewrote `config.yaml` as `config.json` to allow using `Mojo::JSON` here.
Hugo’s built-in support for different [configuration formats][] made that a painless shift.
Then Mojo lets me [`slurp`][] the contents of the config file into a single string,
which [`decode_json`][] turns into a hash reference.

[`list_tree`]: http://mojolicious.org/perldoc/Mojo/File#list_tree
[Mojo::Collection]: http://mojolicious.org/perldoc/Mojo/Collection

[`list_tree`][] gives a recursive directory listing of everything under `$root` as a [Mojo::Collection][].
Collections provide a tidy toolkit of list handling functionality without requiring me to go back and forth between arrays and array references.
I could find and iterate over all the HTML and XML files in vanilla Perl 5, but I like this better.

[`@ARGV`]: http://perldoc.perl.org/perlvar.html#%40ARGV

After a few runs, I added the ability to specify a single file in [`@ARGV`][].
That way I can figure things out when that one link in that one file causes trouble.

### Checking links in a file

```perl
sub check_links_in($filename) {
  my $html = Mojo::File->new( $filename )->slurp;
  my $dom = Mojo::DOM->new( $html );
  my $links = $dom->find( '[href], [src]' );

  $links->each( sub($link, $n) {
    my $target = $link->attr( "href" ) || $link->attr( "src" );

    # Assume status will not change during the same run.
    return if exists $checked_links->{ $target };

    $checked_links->{ $target } = 1;
    my $url = Mojo::URL->new( $target );

    # Ignore email links
    return if $url->scheme && $url->scheme eq 'mailto';

    $checked_links->{ $target } = file_exists_for( $url )
      // external_link_works_for( $url )
      // 0;

    # In this version we only care about invalid links.
    unless ( $checked_links->{ $target } ) { say summary_for( $target, $filename ); }
  });
}
```

[`find`]: http://mojolicious.org/perldoc/Mojo/DOM#find
[`attr`]: http://mojolicious.org/perldoc/Mojo/DOM#attr
[`scheme`]: http://mojolicious.org/perldoc/Mojo/URL#scheme

Once again I `slurp` a file into a string.
This time it gets handed off to `Mojo::DOM` so it can [`find`][] any elements with `src` or `href` attributes,
and then create a `Mojo::URL` from the appropriate [`attr`][].
`Mojo::URL` does the tedious work of parsing URLs and making components like [`scheme`][] available.

Leaning on the `//` defined-or logical shortcut lets me take advantage of the
three boolean states of Perl: truthy, falsey, and "I dunno." Each URL-testing
subroutine can return `undef` to indicate that it doesn’t know what to do with
the URL, and let the next subroutine in line handle it. If nobody knows what to
do with it, then that’s a bad link and gets remembered as a falsey value.

[`each`]: http://mojolicious.org/perldoc/Mojo/Collection#each

<aside class="admonition note">
<p class="admonition-title">Note</p>

[`each`][] hands two items to the subroutine it invokes: an item in the
collection and what number in the collection that item is (starting from 1). No,
I don’t use `$n`, but I wanted you to see that it’s available. You can also
access the item as `$_` as I did earlier. You can even do your subroutine
arguments the old fashioned way with `@_`.

</aside>

### Is it an internal link?

```perl
sub file_exists_for($url) {
  # Ignore full urls that aren't pointed at my site.
  if ( $url->host && $url->host ne $site->host ) {
    return;
  }

  if ( $url->fragment && $url->path eq '') {
    # Points to a URL fragment within itself
    # Today I don't care about those.
    # If I did, I'd remember what file $url came from, load it, and check the DOM.
    return 1;
  }

  my $path = $url->path
    or return;

  if ( $path eq '/' || $path->trailing_slash ) {
    $path = $path->merge("index.html")
  }

  my $file = $root . $path;
  return -f $file;
}
```

I would check for `../` abuse if this was a general purpose script, but it’s
mostly links I added by hand and checked manually at some point in the last
fifteen years. So - assuming past me was not acting maliciously or foolishly, we
rule out more likely situations:

[`path`]: http://mojolicious.org/perldoc/Mojo/URL#path
[one page]: link:/post/2014/10/blog-writing-in-org-mode/

* The URL [`host`](http://mojolicious.org/perldoc/Mojo/URL#host) points to something besides my site, which means it can’t be a local file.
* The link has a [`fragment`](http://mojolicious.org/perldoc/Mojo/URL#fragment) pointing to a named anchor and nothing else.
  I only have that on [one page][] right now, and I don’t feel like complicating this script for a single page.
* The [`path`][] isn’t set, which at this point means an empty link. That can’t be good.
* If the link *is* to a local file, we check whether it exists.

[Mojo::Path]: http://mojolicious.org/perldoc/Mojo/Path
[trailing slash]: http://mojolicious.org/perldoc/Mojo/Path#trailing_slash
[`merge`]: http://mojolicious.org/perldoc/Mojo/Path#merge

[Mojo::Path][] manipulation delights me.
Sure, this could be a regular expression substition with fewer characters of
code, but someone else seeing [`merge`][] after a check for a [trailing slash][]
would probably understand that I’m adjusting for the common practice of
`/thing/` being a link to `/thing/index.html`. They might understand even if
they weren’t Perl developers!

### Is it a working external link?

```perl
sub external_link_works_for($url, $ua) {
  my $response;

  # Ignore tutorial demo links
  return 1
    if $url->host && $url->host eq 'localhost';

  # Ex: //www.youtube.com/embed/bWqSuBg8AMo
  # Produced by some Hugo shortcodes.
  my $is_protocol_relative = !$url->scheme && $url->host && $url->host ne $site->host;

  if ( $is_protocol_relative ) {
    # Use my site's choice of HTTP / HTTPS
    $url->scheme( $site->scheme );
  }

  eval {
    $response = $ua->head( $url )->result;
  };

  if ( $@ ) {
    warn "When checking $url: $@";
    return;
  }

  return $response->is_success;
}
```

[protocol-relative URLs]: https://www.paulirish.com/2010/the-protocol-relative-url/
[`head`]: http://mojolicious.org/perldoc/Mojo/UserAgent#head

After some quick checks to ensure I’m not looking at a blog demo link and that I
handle [protocol-relative URLs][] correctly, I wrap a simple [`head`][] request
in an `eval` block.

[`HTTP HEAD`]: https://ochronus.com/http-head-request-good-uses/
[`result`]: http://mojolicious.org/perldoc/Mojo/Transaction#result
[HTTP transaction]: http://mojolicious.org/perldoc/Mojo/Transaction/HTTP
[`is_success`]: http://mojolicious.org/perldoc/Mojo/Message/Response#is_success

I use [`HTTP HEAD`][] because I only care about whether the link is valid. I
don’t want the full content at the link. `eval` lets me catch timeouts and
requests being sent to Web sites which no longer exist. Assuming no errors, this
eventually returns whether the [`result`][] of the [HTTP transaction][]
succeeded with [`is_success`][].


### Summarize it

```perl
sub summary_for($target, $filename) {
  die "Didn't check [$target]?"
    unless exists $checked_links->{ $target };

  my $status = $checked_links->{ $target }
    ? "+"  # It worked!
    : "-"  # Something went wrong.
    ;
  return "$status $filename $target";
}
```

Today I only looked for bad links, but it can be useful to know the status of
*all* links in my site. I used it a few times during development. May as well
leave that bit of logic in.

## What’s That Do?

    $ ./scripts/link-checker > links.txt

A couple hundred lines like this, basically.

    When checking http://coolnamehere.com: Premature connection close at scripts/check-links.pl line 53.
    - public/categories/blogspot/index.html http://coolnamehere.com
    - public/categories/blogspot/index.html http://blogspot.com
    When checking http://vim.org/: Can't connect: Name or service not known at scripts/check-links.pl line 53.
    - public/categories/blogspot/index.html http://vim.org/
    When checking http://jruby.codehaus.org: Connect timeout at scripts/check-links.pl line 53.
    - public/categories/blogspot/index.html http://jruby.codehaus.org
    - public/categories/blogspot/index.html http://devzone.zend.com/article/2262-Zend-Framework-1.0.0-production-release
    When checking http://jruby.codehaus.org/: Connect timeout at scripts/check-links.pl line 53.
    - public/categories/coolnamehere/index.html http://jruby.codehaus.org/

Goodness those are embarrassing.

Okay I’m gonna go fix this.

Some links just won’t work with this code.
I may revisit this later, but I got what I need.
All links should at least work in a browser for now.

An added bonus that I didn’t expect: this code also ran on Windows 10 with no changes needed.

## More Ideas

Improvements that I thought of while putting this together, which I may eventually try out.

[`robots.txt`]: http://www.robotstxt.org/robotstxt.html
[Mojo::Base]: http://mojolicious.org/perldoc/Mojo/Base
[Mojo::UserAgent]: http://mojolicious.org/perldoc/Mojo/UserAgent

* Be a good bot citizen by paying attention to [`robots.txt`][]
  I tried that in an early version of the script, but hardly any of the sites provided one.
  I’ll ponder and try not to run the script too often for now.
* Wrap things up in a [Mojo::Base][] class for organization.
* Run an instance and scrape that live - see if it makes a difference!
* Use non-blocking requests, since [Mojo::UserAgent][] supports them.
* Cache results to disk, since working links tend to stay that way for *at least* a few days.
* Find out why some URLs didn’t work.
  Was it a `robots.txt` thing? A weird redirect? They worked in the browser, after all.

Honestly the script does what I need it to, and I might never implement these other ideas.