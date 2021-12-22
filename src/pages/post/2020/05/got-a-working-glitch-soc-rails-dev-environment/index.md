---
category: tools
cover_image: cover.png
date: 2020-05-05 06:26:21
description: I remain ambivalent about Rails development
draft: false
format: md
layout: layout:PublishedArticle
slug: got-a-working-glitch-soc-rails-dev-environment
tags:
- rails
- mastodon
- ruby
- sort of
- mostly rails
title: Got a Working glitch-soc Rails Dev Environment
uuid: 65191876-a1da-4356-b8b7-37ac0b0eca4a
---

I wanted to build and test a development instance of
[`glitch-soc`][glitch-soc], a friendly fork of [Mastodon][mastodon].  I
succeeded.  But I am very tired now.  Here are my notes, along with some
after-the-fact editorializing.

It’s less tutorial and more confessional.  I haven’t used Rails much since 4.0
was shiny.  So there’s likely some common practice workflow that I don’t know
yet.  But I got it to work.

## Install glitch-soc locally

`glitch-soc` documentation refers you to [Mastodon docs][mastodon-docs] ,
Mastodon’s [installation instructions][installation-instructions] seem focused
on production installations.  I bounce back and forth between Mastodon’s
[README][readme] and its [developer documentation][developer-documentation].

The README says I need:

- [PostgreSQL][postgresql] 9.5+
- [Redis][redis] 4+
- [Ruby][ruby] 2.5+
- [Node.js][nodejs] 10.13+

[rbenv][] and [nvm][] help with the language requirements, but this fresh
[Manjaro][manjaro] partition lacks the other requirements.

### Install Redis

Used the [Arch wiki][arch-wiki] as a guide.  Didn’t need to edit config,
though.  Instance installed via [Pamac][pamac] is already configured to only
listen to `127.0.0.1`.

    $ pamac install redis
    $ sudo systemctl start redis
    $ sudo systemctl enable redis

Version installed
: 6.0

### Install Postgresql

Once again, going off the [Arch wiki entry][arch-wiki-psql].

    $ pamac install postgresql
    $ sudo -iu postgres
    > initdb -D /var/lib/postgres/data
    > exit
    $ sudo systemctl start postgresql.service
    $ sudo systemctl enable postgresql.service
    $ sudo -iu postgres
    > createuser --interactive
    Enter name of role to add: random
    Shall the new role be a superuser? (y/n) y
    > exit
    $ createdb random

That reminds me.  I want to finish reading [The Art of PostgreSQL][postgres-book].

Version installed
: 12.2

### Clone project and install dev dependencies

Not the required services.  I just installed those.  Languages and libraries.

#### fork & clone repo

Since I hope to contribute bug fixes someday, I’ll fork the [repo][] rather than
just clone it.  I clone my fork instead.

Dev language is weird.

    $ git clone git@github.com:brianwisti/mastodon.git
    $ cd mastodon

The project’s `.ruby-version` file specifies Ruby 2.6.6.  Rbenv immediately
warns me that I lack the correct installed version.  It also doesn’t recognize
the version when I try installing it, so I must refresh [ruby-build][]

    $ git -c ~/.rbenv/plugins/ruby-build pull
    $ rbenv install

2.6.6 is a bit more specific than "2.5+" but no big deal. Got the right Ruby
version. Time to install the gems.

    $ bundle install

Oh hey what’s this? It seems relevant to my [interests][].

    ⋮
    Post-install message from microformats:
    Prior to version 4.0.0, the microformats gem was named "microformats2."

Adding a task to look more closely at [mircroformats-ruby][].  It’s more active
than [mf2py][].

[Yarn][yarn] manages the node-specific project dependencies.  Better install
that.

    $ npm install -g yarn

Okay now I can install the Node stuff.

    $ yarn install
    yarn install v1.22.4
    [1/6] Validating package.json...
    error @tootsuite/mastodon@: The engine "node" is incompatible with this module. Expected version ">=10.13 <13". Got "13.11.0"
    error Found incompatible module.
    info Visit https://yarnpkg.com/en/docs/cli/install for documentation about this command.

At some point I should [enable][] automatic `nvm use`.  Meanwhile I’ll just
install.

:::note

Or maybe I could play with [Volta][volta].  Not today. Maybe later.

:::

    $ nvm install
    Found '/home/random/Projects/mastodon/.nvmrc' with version <12>
    Downloading and installing node v12.16.3...
    ⋮
    Now using node v12.16.3 (npm v6.14.4)
    $ npm install -g yarn
    $ yarn install

No complaints about Node.js versions now.  Good.  Time to actually set up the
application?

Dev docs say `rails db:setup`, so that’s what I type.

    $ rails db:setup
    zsh: command not found: rails

Oh right.  Because I’m not using a fresh Rails app, but an existing project.  I
could use `bundle exec` but for some reason I feel stubborn.  I must make at
least one step of my installation process match the documentation.

I use [direnv][], so I can add the path locally.

**`.envrc`**

```bash
PATH_add "bin"
```

Then I need to let direnv know this change is acceptable.

    $ direnv allow

There’s probably a better Rails-specific or Zsh-specific approach, but I’m in a
hurry.

    $ rails db:setup

Loads of text follows. That’s good, right?

Instructions go straight to running the application, but that’s not my style.

## Getting tests to pass

I want to run tests first. Blame [Perl][perl]. I have certain expectations
after years of watching `cpan` run tests before declaring something installed.

    $ rspec
    ⋮
    332) Auth::ChallengesController POST #create with incorrect password renders challenge
        Failure/Error: = javascript_pack_tag "locales", integrity: true, crossorigin: 'anonymous'

        ActionView::Template::Error:
            Webpacker can't find locales in /home/random/Projects/mastodon/public/packs-test/manifest.json. Possible causes:
            1. You want to set webpacker.yml value of compile to true for your environment
                unless you are using the `webpack -w` or the webpack-dev-server.
            2. webpack has not yet re-run to reflect updates.
            3. You have misconfigured Webpacker's config/webpacker.yml file.
            4. Your webpack configuration is not creating a manifest.
            Your manifest contains:
            {
            }
        # ./app/views/layouts/application.html.haml:23:in `_app_views_layouts_application_html_haml___4376952060303332774_47460103924140'
        # ./app/views/layouts/auth.html.haml:13:in `_app_views_layouts_auth_html_haml___1721087443773625754_47460102744080'
        # ./app/controllers/concerns/challengable_concern.rb:47:in `render_challenge'
        # ./app/controllers/auth/challenges_controller.rb:20:in `create'
        # ./app/controllers/concerns/localized.rb:18:in `block in set_locale'
        # ./app/controllers/concerns/localized.rb:17:in `set_locale'
        # ./spec/controllers/auth/challenges_controller_spec.rb:31:in `block (4 levels) in <top (required)>'
        # ------------------
        # --- Caused by: ---
        # Webpacker::Manifest::MissingEntryError:
        #   Webpacker can't find locales in /home/random/Projects/mastodon/public/packs-test/manifest.json. Possible causes:
        #   1. You want to set webpacker.yml value of compile to true for your environment
        #      unless you are using the `webpack -w` or the webpack-dev-server.
        #   2. webpack has not yet re-run to reflect updates.
        #   3. You have misconfigured Webpacker's config/webpacker.yml file.
        #   4. Your webpack configuration is not creating a manifest.
        #   Your manifest contains:
        #   {
        #   }
        #   ./app/views/layouts/application.html.haml:23:in `_app_views_layouts_application_html_haml___4376952060303332774_47460103924140'
    ⋮

    Finished in 4 minutes 4.3 seconds (files took 6.07 seconds to load)
    2680 examples, 332 failures, 23 pending

Mhm.  That’s what I thought.  I’m going to need to write a post about getting
this to work, aren’t I?

Let’s skip the hour or two of flailing and digging into past `glitch-soc` and
Mastodon tickets.

The problem?  [Webpacker][webpacker] doesn’t compile assets for the test
environment, because [CircleCI][circleci] already does that.

**`.config/webpacker.yml`**

```yaml
test:
  <<: *default

  # CircleCI precompiles packs prior to running the tests.
  # Also avoids race conditions in parallel_tests.
  compile: false

  # Compile test packs to a separate directory
  public_output_path: packs-test
```

Set `compile` to `true` and everything passes.  Except they need that as
`false` for CircleCI.  That — does this mean they never run any tests locally
in development?  That tests only run after a commit is pushed?

Inconceivable.  The very thought is like fingernails on a chalkboard.  Surely I
missed something in the documentation.

Well I’m going to run tests locally one way or another.

Gimme a second.

Okay how about this?

First, clean up the compiled assets from my config experiment.

    $ RAILS_ENV=test rake assets:clobber

Next, precompile the assets and run tests again.

    $ RAILS_ENV=test rake assets:precompile
    $ rspec
    ⋮
    Finished in 4 minutes 10.6 seconds (files took 6.04 seconds to load)
    2680 examples, 0 failures, 23 pending

Huzzah! Aside from that ghastly test time.  I’ve seen worse.  I’ve *written*
worse.

Clearly I need to automate this.  Maybe something to do with Foreman.  Maybe
just a shell script that clobbers, precompiles, and runs tests.

A real fix — if one is needed, and I didn’t just miss a vital paragraph of
documentation — would be to give CircleCI its own environment distinct from the
default test environment.

## Good enough

Will I actually do anything with my `glitch-soc` fork?  No idea.  But I want to
share this for other dusty Ruby folks whose Rails applications predate
[Webpack][webpack].

I should at least fiddle with instance settings enough to get a cute
screenshot.

[glitch-soc]: https://glitch-soc.github.io/docs/
[mastodon]: https://joinmastodon.org/
[mastodon-docs]: https://docs.joinmastodon.org
[installation-instructions]: https://docs.joinmastodon.org/admin/install/
[readme]: https://github.com/tootsuite/mastodon
[developer-documentation]: https://docs.joinmastodon.org/dev/setup/
[postgresql]: https://www.postgresql.org/
[redis]: https://redis.io/
[ruby]: https://www.ruby-lang.org
[nodejs]: https://nodejs.org
[rbenv]: https://github.com/rbenv/rbenv
[nvm]: https://github.com/nvm-sh/nvm
[manjaro]: https://manjaro.org/
[arch-wiki]: https://wiki.archlinux.org/index.php/Redis
[pamac]: https://wiki.manjaro.org/index.php?title=Pamac
[postgres-book]: https://theartofpostgresql.com/
[repo]: https://github.com/glitch-soc/mastodon
[ruby-build]: https://github.com/rbenv/ruby-build
[interests]: /tags/indieweb
[microformats-ruby]: https://github.com/microformats/microformats-ruby
[mf2py]: https://github.com/microformats/mf2py
[yarn]: https://yarnpkg.com/
[enable]: https://github.com/nvm-sh/nvm#calling-nvm-use-automatically-in-a-directory-with-a-nvmrc-file
[volta]: https://volta.sh/
[direnv]: https://direnv.net
[perl]: /tags/perl
[webpacker]: https://github.com/rails/webpacker
[circleci]: https://circleci.com/
[webpack]: https://webpack.js.org/
[arch-wiki-psql]: https://wiki.archlinux.org/index.php/PostgreSQL
