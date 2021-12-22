---
aliases:
- /programming/2014/06/25_perl-subref-signatures.html
- /post/2014/perl-subref-signatures/
- /post/2014/06/perl-520-signatures-in-subroutine-references/
- /2014/06/25/perl-5.20-signatures-in-subroutine-references/
category: programming
date: 2014-06-25 00:00:00
layout: layout:PublishedArticle
slug: perl-520-signatures-in-subroutine-references
tags:
- perl
title: Perl 5.20 Signatures in Subroutine References
uuid: df17eaeb-6dc8-435d-8d83-6c7492b3c09d
---

[Perl]: http://perl.org
[Perl][] 5.20 has experimental support for function signatures. That's good 
news. I just thought to check if signatures can be used in subroutine 
references. They can.
<!--more-->

```perl
# Set a base set of features.
use 5.20.0;

# Signatures are experimental, so are not enabled by default.
use feature 'signatures';

# Otherwise Perl will warn about using the experimental feature
no warnings 'experimental::signatures';

sub hello($person) {
  say "Hello, $person";
}

my $goodbye = sub($person) {
  say "Goodbye, $person";
};

my $me = "Brian";

hello( $me );
$goodbye->( $me );
```

It's a simple test. Just checking to see if I can maybe use this feature in 
my own projects.

    $ perl sig-test.pl
    Hello, Brian
    Goodbye, Brian

[Pygments]: http://pygments.org/

This pleases me. It's not going to make life easier for [Pygments][], though.
