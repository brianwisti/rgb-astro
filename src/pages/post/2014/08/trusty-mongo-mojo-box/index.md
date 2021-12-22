---
aliases:
- /tools/2014/08/05_trusty-mongo-mojo.html
- /post/2014/trusty-mongo-mojo/
- /2014/08/05/trusty-mongo-mojo-box/
category: tools
date: 2014-08-05 00:00:00
layout: layout:PublishedArticle
slug: trusty-mongo-mojo-box
tags:
- virtualization
- vagrant
- perl
- mongodb
- mojolicious
title: Trusty Mongo Mojo Box
uuid: 57b9809c-ddef-41d2-978f-c88eca0e9e3a
---

<aside class="admonition tldr">
<p class="admonition-title">tl;dr</p>

Install Vagrant & VirtualBox. `mkdir my-box && cd my-box && vagrant init
brianwisti/trusty-mongo-mojo`. Be aware that this is my first packaged
Vagrant box, and it is probably not great.

</aside>

## Motivation

I want to explore [Mojolicious](http://mojolicio.us/) and
[MongoDB](https://www.mongodb.org/). Both of these are available for
each operating system I use. Unfortunately, each operating system is a
unique environment, with its own quirks. I usually work my way around
these quirks, but I also want to explore a number of
[virtualization](http://en.wikipedia.org/wiki/Virtualization) tools that
have become popular. This is an opportunity to learn how to set up a
[Vagrant](http://vagrantup.com) box for my Mojolicious / MongoDB
explorations.

## Creating The Box

A [virtual machine](http://en.wikipedia.org/wiki/Virtual_machine) is
basically a simulated operating system running on whatever your host
machine is: Windows, Linux, OS X - whatever. That virtual machine lives
its life as if it has its own environment. It is useful for application
development, testing, application hosting, and security research. You
can have a library of guest virtual machines, each dedicated to a
particular task.

I have now exhausted my knowledge of virtualization, so let us move on.

Vagrant provides a single configuration and command set for managing
aspects of multiple virtual machine managers. You can use Vagrant to
create identical virtual machine "boxes" on host operating systems.
These definitions — and the boxes themselves — can be shared with
others.

Although multiple virtual machine managers are supported by Vagrant,
[VirtualBox](https://www.virtualbox.org/) is widely used and has the
best support.

My Vagrant box needs an operating system. This is my first time through,
so I will keep it simple: [Ubuntu](http://ubuntu.com) 14.04. I figure
that I can find plenty of resources online if I get stuck.

Go to [Vagrant Cloud](https://vagrantcloud.com/) for packaged Vagrant
boxes with your favorite distribution and virtual machine provider.
Vagrant Cloud provides a social network approach to shared boxes,
allowing you to find and favorite useful options or even sharing your
own. There is an Ubuntu account on Vagrant Cloud with a
[trusty64](https://vagrantcloud.com/ubuntu/trusty64) box, presenting a
14.04 64 bit release that can be used in VirtualBox.

The `vagrant init` command initializes a new Vagrant box. I will
reference trusty64 to give this box a starting point.

    $ mkdir mongo-mojo
    $ cd mongo-mojo
    $ vagrant init ubuntu/trusty64
    A `Vagrantfile` has been placed in this directory. You are now
    ready to `vagrant up` your first virtual environment! Please read
    the comments in the Vagrantfile as well as documentation on
    `vagrantup.com` for more information on using Vagrant.

I could start the box up now and have a more or less blank starting
point. Instead I will provision it so that it has the packages and tools
needed for me to start development quickly. My goal is to get the latest
releases of MongoDB, Perl 5, Mojolicious, and
[Mango](https://metacpan.org/pod/Mango) — a pure Perl MongoDB driver
written by the same developer who created Mojolicious.

Vagrant
[provisioning](http://docs.vagrantup.com/v2/provisioning/index.html) can
be done via several approaches, but I go for the short and sweet method
of writing a [shell
script](http://docs.vagrantup.com/v2/provisioning/shell.html).

I am going to install MongoDB via the [provided Ubuntu
packages](http://docs.mongodb.org/manual/tutorial/install-mongodb-on-ubuntu/),
so that I do not have to worry about startup scripts and all that. I
will also install `build-essential` so that I can build
[Perlbrew](http://perlbrew.pl/).

**`bootstrap/system.sh`**

```bash
#!/bin/bash

# Install MongoDB
apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
echo 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen' \
  | tee /etc/apt/sources.list.d/mongodb.list
apt-get -q update
apt-get -q -y install mongodb-org
service mongod start

# Install development dependencies
apt-get -q -y install build-essential

# Set up vagrant user environment
su -c "source /vagrant/bootstrap/user.sh" vagrant
```

`system.sh` invokes `user.sh` as the default vagrant user. `user.sh`
contains the instructions to install Perlbrew and the latest
[Perl](http://perl.org). Once that is out of the way,
[cpanm](https://metacpan.org/pod/cpanm) will install Mojolicious and
Mango.

**`bootstrap/user.sh`**

```bash
#!/bin/bash

# Install perlbrew
curl -L http://install.perlbrew.pl | bash
echo 'source ~/perl5/perlbrew/etc/bashrc' >> $HOME/.profile
source ~/perl5/perlbrew/etc/bashrc

# Install local Perl and app libs
perlbrew install perl-5.20.0
perlbrew switch perl-5.20.0
perlbrew install-cpanm
cpanm Mojolicious
cpanm Mango
```

My Vagrantfile varies only a little from the default. One thing to
notice is that I have set up port forwarding so I can view running
Mojolicious applications from a browser in the host system.

**`Vagrantfile`**

```ruby
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  # Use Ubuntu 14.04 64 bit
  config.vm.box = "ubuntu/trusty64"

  # Install system requirements
  config.vm.provision "shell", path: "bootstrap/system.sh"

  # Configure guest services to be accessible on host
  config.vm.network "forwarded_port", guest: 3000, host: 3000
end
```

Now just run `vagrant up` and wait.

    $ vagrant up

I end up waiting quite a while.

Okay, okay. I admit that it took me a couple of tries to get those shell
scripts working right. After each correction, `vagrant provision` reran
the provisioning stage of `vagrant up`.

Eventually it finishes.

## Testing the Box

I will not even pretend I know what I am doing here. The whole point of
this exercise is to learn Mojolicious, MongoDB, and Mango. Oh yeah, and
Vagrant. I just copy the sample application from the [Mango Github
README](https://github.com/kraih/mango).

**`app.pl`**

```perl
use Mojolicious::Lite;
use Mango;
use Mango::BSON ':bson';

my $uri = 'mongodb://localhost:27017/test';
helper mango => sub { state $mango = Mango->new($uri) };

# Store and retrieve information non-blocking
get '/' => sub {
  my $c = shift;

  my $collection = $c->mango->db->collection('visitors');
  my $ip         = $c->tx->remote_address;

  # Store information about current visitor
  $collection->insert({when => bson_time, from => $ip} => sub {
    my ($collection, $err, $oid) = @_;

    return $c->render_exception($err) if $err;

    # Retrieve information about previous visitors
    $collection->find->sort({when => -1})->fields({_id => 0})->all(sub {
      my ($collection, $err, $docs) = @_;

      return $c->render_exception($err) if $err;

      # And show it to current visitor
      $c->render(json => $docs);
    });
  });
};

app->start;
```

I would like to configure my editor to invoke needed commands through
Vagrant. Perhaps later. For now, SSH will do.

    $ vagrant ssh
    $ cd /vagrant
    $ morbo app.pl

Back in my browser, I hit `http://localhost:3000` a couple times and
get:

``` json
[
  {
    "from": "10.0.2.2",
    "when": 1407276553541
  },
  {
    "from": "10.0.2.2",
    "when": 1407276551337
  }
]
```

Well how about that? Everything works\!

## Packaging

Installing everything took a *long* time. I do not want to wait for the
full provisioning process every time I create a new box. Can I take a
snapshot of this box and use it for other projects?

Of course I can. The Vagrant docs provide some
[guidelines](http://docs.vagrantup.com/v2/boxes/base.html) for creating
a new box for packaging.

<aside class="admonition warning">
<p class="admonition-title">Warning</p>

There is a warning in the packaging documentation that looks serious.

> **Advanced topic\!** Creating a base box can be a time consuming and
> tedious process, and is not recommended for new Vagrant users. If
> you’re just getting started with Vagrant, we recommend trying to
> find existing base boxes to use first.

Blah, blah, blah. If I listened to every warning, I wouldn’t know what
my hair smells like when it’s on fire. *You* may want to be more
careful, though.

</aside>

The Vagrant [package
command](http://docs.vagrantup.com/v2/cli/package.html) takes your
virtual machine and wraps it up into a single box file that you can
reuse or share with others. Maybe I can just package my trusty64-derived
box.

    $ vagrant package

Apparently yes. The resulting box is about 750MB, which seems large.

[William Walker](http://williamwalker.me/) wrote a post about [Creating
a Custom Vagrant
Box](http://williamwalker.me/blog/creating-a-custom-vagrant-box.html),
with many useful instructions. I am ignoring most of those useful
instructions right now, though I will come back to them later. What
caught my eye was his suggestion for reducing the size of the box. You
can use `dd` to clear out some space from inside the box.

    $ vagrant ssh
    $ sudo dd if=/dev/zero of=/EMPTY bs=1M
    $ sudo rm -f /EMPTY
    $ sudo shutdown -h now

I rebuild my package. That brings it down to 649MB - still large, but
better than 750. I will come back later when I have the time and see if
I can cut it down a little more.

    $ vagrant add test-trusty-mongo-mojo package.box
    $ cd ..
    $ mkdir test-tmm
    $ cd test-tmm
    $ vagrant init test-trust-mongo-mojo
    A `Vagrantfile` has been placed in this directory. You are now
    ready to `vagrant up` your first virtual environment! Please read
    the comments in the Vagrantfile as well as documentation on
    `vagrantup.com` for more information on using Vagrant.

I test it with the same Mojolicious application I used above and — hot
dog — it works.

## Sharing

Now is the part where I jump straight off the cliff of rational thinking
and share every horrible mistake I made with you and anyone else who
wants it.

Should you use MongoDB in production? I have no idea, but I bet that
it’s a really bad idea to use my [trusty-mongo-mojo
box](https://vagrantcloud.com/brianwisti/trusty-mongo-mojo) in
production. Still — could be interesting to play with.

    $ vagrant init brianwisti/trusty-mongo-mojo

Have fun.

## Was It Worth It?

That’s a good question. It was great as a learning experience. I enjoyed
learning more about [Vagrant](http://vagrantup.com). I don’t know yet
whether it was worth my time to create this bundle. Mojolicious and
MongoDB are already fairly easy to install on whatever platform. We’ll
see. I do know that I’d like to revisit this package, clean it up, and
maybe follow up with a similar package for
[Dancer](http://perldancer.org/). It’s just plain *fun* to make these
packages.

## What Now?

All that’s left now is to learn all the things. The online [Perl
documentation](http://perldoc.perl.org/) is current with Perl 5.20.
[Mojolicious::Lite](http://mojolicio.us/perldoc/Mojolicious/Lite) is as
good a place as any to start with learning Mojolicious. There’s a
[MongoDB manual](http://docs.mongodb.org/manual/) to peruse. Mango does
not yet have the polished guides that Mojolicious does, but browsing the
[Mango MetaCPAN page](https://metacpan.org/release/Mango) will get me a
ways.

Oh yeah. When I’m done for the day, I’ll exit my vagrant session and
suspend the virtual machine.

    $ vagrant exit
    $ vagrant suspend