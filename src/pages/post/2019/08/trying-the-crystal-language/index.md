---
aliases:
- /2019/08/25/trying-the-crystal-language/
category: Programming
cover_image: cover.png
date: 2019-08-25
description: In which I use Crystal for a simple shell task
layout: layout:PublishedArticle
slug: trying-the-crystal-language
tags:
- crystal
- taskwarrior
title: Trying the Crystal Language
updated: 2020-01-20
uuid: 636d64cd-8ac2-421f-afe0-f3cd3f62079b
---

[Crystal](https://crystal-lang.org/) is a statically typed, compiled
programming language that looks a *lot* like [Ruby](/tags/ruby). Let’s
try it out! Maybe even work on a [Taskwarrior](/tags/taskwarrior) thing
I’ve been wanting to do.

## Motivation

I want to play with a compiled language, but I’m not in the mood for Go
or Rust.

Crystal looks friendly. Similar syntax to Ruby. Statically typed, ruling
out a category of silly mistakes I always make (passing the wrong kind
of value). Uses type inference, which means it can figure out what type
a variable is without us telling it. Compiled, so you can run things
quicker than in Ruby.

The philosophy summarized on the front page of the Crystal home page is
"Fast as C, slick as Ruby". That works for me.

I don’t care if it compiles super fast or the executable is super fast.
An executable that runs quicker than my utility scripts, written in a
language just as friendly, will be nice.

## Installation

The documentation provides instructions on [how to install
Crystal](https://crystal-lang.org/reference/installation/) across
several platforms. Today I’m on my Windows partition. Though they’re
working on a full Windows port, the best path for now is to use
[Homebrew](https://brew.sh/) on
[WSL](https://docs.microsoft.com/en-us/windows/wsl/wsl2-about).

:::warning

I’m using WSL 2, which is still in development. I haven’t tested any of
this under WSL 1.

:::

    $ brew install crystal
    ...
    $ crystal version
    Crystal 0.30.1 (2019-08-15)
    LLVM: 8.0.1
    Default target: x86_64-unknown-linux-gnu

`crystal` provides a collection of subcommands.

    $ crystal help

    Usage: crystal [command] [switches] [program file] [--] [arguments]

    Command:
        init                     generate a new project
        build                    build an executable
        docs                     generate documentation
        env                      print Crystal environment information
        eval                     eval code from args or standard input
        play                     starts Crystal playground server
        run (default)            build and run program
        spec                     build and run specs (in spec directory)
        tool                     run a tool
        help, --help, -h         show this help
        version, --version, -v   show version

Oh my there are some interesting commands in there\! I’ll just focus on
the ones that result in me running code.

## One-liners with `eval`

Crystal does not ship with an interactive shell. Makes sense,
considering that it’s supposed to be a compiled language. Still, it’s
more flexible than I expected. If all I want is a one-liner, Crystal can
do that!

    $ crystal eval 'puts "Hi!"'
    Hi!

Okay, that wasn’t super exciting. What about pretty-printing the current
environment variables?

    $ crystal eval 'pp ENV'
    {"BF" => "$albumartist | $album | $track/$tracktotal | $title",
    "BREW_PREFIX" => "/home/linuxbrew/.linuxbrew",
    "CLICOLOR" => "1",
    ...
    "_" => "/home/linuxbrew/.linuxbrew/bin/crystal",
    "wg_date" => "#[]%Y-%m-%d %H:%M%z#[default]"}

[ENV](https://crystal-lang.org/api/ENV.html) is a Hash-like accessor.
You can access and iterate through environment variables as if they were
keys in a Hash.

    $ crystal eval 'ENV.each { |k, v| puts "#{k}: #{v}" }'

Except that the `pp` output was sorted. That’s fine. We’ll sort the
keys.

    $ crystal eval 'ENV.keys.sorted.each { |k| puts "#{k}: #{ENV[k]}" }'

Printing data as JSON is a pretty common task. Common enough that it’s a
Hash method here. Except ENV isn’t a
[Hash](https://crystal-lang.org/api/Hash.html). It’s a "Hash-like
accessor."

No problem, we can make a Hash from `ENV`.

    $ crystal eval 'require "json"; env = Hash.zip(ENV.keys, ENV.values); puts env.to_json'
    {"NVM_DIR":"/home/random/.nvm","HOSTTYPE":"x86_64","PYENV_HOME":"/home/random/.pyenv", ...
    "WSLENV":"","_":"/home/linuxbrew/.linuxbrew/bin/crystal"}

Well. I lost my sorting and the JSON isn’t exactly pretty-printed. I
know I can fix this from inside Crystal, but my one-liner would get
clunky. Hey, this is a one-liner. Let’s pipe it to
[jq](https://stedolan.github.io/jq/)\!

    $ crystal eval \
      'require "json"; env = Hash.zip(ENV.keys, ENV.values); puts env.to_json' \
      | jq --sort-keys '.'

There, now it’s all pretty-printed.

![Colorized JSON via jq](crystal-env-jq.png)

One-liners are fun.

What was I doing next? Oh right. Crystal source files.

## Shell scripts with `run`

I have no idea how to do dependency management in Crystal yet. Something
about [shards](https://crystal-lang.org/reference/the_shards_command/).
But even stock Crystal looks like it would work as a glue language for
shell scripts. Plus, the `run` command lets you ignore the build process
and pretend your code is being run directly.

**`hello-user.cr`**

```crystal
#!/usr/bin/env crystal

print "Who are you? "
name = gets

if name == ENV["USER"]
  puts "Hey there #{name}!"
  tasks = `task +DUE count`.to_i
  puts "You have #{tasks} tasks due."
  puts "Better get on it!" if tasks > 0
else
  puts "I was not expecting you to say \"#{name}\"!"
end
```

- Since `run` is the default command, you could make a plain old Crystal script! What can I say, I like the old ways.
- Crystal ignores trailing whitespace in `to_i`. You’ll still want to `chomp` when examining the output of a command.

Remember, this is just me using `#!` to say `crystal run hello-user.cr`

    $ chmod 700 hello-user.cr
    $ ./hello-user.cr
    Who are you? random
    Hey there random!
    You have 3 tasks due.
    Better get on it!

It looks a *lot* like Ruby. You could take out that `#!` and it would
*almost* work as-is.

    $ ruby hello-user.cr
    Who are you? random
    I was not expecting you to say "random
    "!

Almost.

## `build`

Okay, directly running scripts is great for testing or quick tasks, but
Crystal *is* a compiled language. Let’s compile something.

[Paul Fenwick](https://twitter.com/pjf/status/852466839145795584) and
[Dave Jacoby](https://jacoby.github.io/2017/10/25/making-taskwarrior-work-for-me.html)
have — or had, no idea if they still do — a neat trick to show quick
task status in their shell prompt. I’ll do the same thing, but in
Crystal.

**`task-indicator.cr`**

```crystal
URGENT       = '\u{2757}'  # exclamation
DUE_TOMORROW = '\u{1f4c5}' # calendar
DUE_TODAY    = '\u{1f631}' # screaming
OVERDUE      = '\u{2620}'  # ded
OK           = "$"         # normal

def has_ready_tasks(extra_filter)
  `task +READY #{extra_filter} count`.to_i > 0
end

def task_indicator
  case
  when has_ready_tasks("+OVERDUE")
    OVERDUE
  when has_ready_tasks("+TODAY")
    DUE_TODAY
  when has_ready_tasks("+TOMORROW")
    DUE_TOMORROW
  when has_ready_tasks("urgency \\> 10")
    URGENT
  else
    "$"
  end
end

print task_indicator
```

Does it work?

    $ crystal run task-indicator.cr
    {{}}

Yeah, I know. I’m working on it. *Anyways* let’s build this thing.

    $ crystal build task-indicator.cr
    $ ls -lhF
    total 1.3M
    -rwxrwxr-x 1 random random 1.3M Aug 25 14:17 task-indicator*
    -rw-rw-r-- 1 random random  546 Aug 25 14:05 task-indicator.cr

There’s a new executable called `task-indicator`. It’s not exactly
small, but it produces the same output. Yes, the screaming face.

## `build --release`

The default build includes a lot of debugging information that I won’t
need in my daily usage. I’ll make a release version.

    $ crystal build --release task-indicator.cr -o task-indicator-release
    $ ls -lhF
    total 2.0M
    -rwxrwxr-x 1 random random 1.3M Aug 25 14:17 task-indicator*
    -rwxrwxr-x 1 random random 665K Aug 25 14:23 task-indicator-release*
    -rw-rw-r-- 1 random random  546 Aug 25 14:05 task-indicator.cr

I didn’t *have* to give it a different name. I wanted to see the size
difference between debug and release builds.

    $ cp task-indicator-release ~/bin/task-indicator

Then over in my `.bashrc`:

**`~/.bashrc`**

```bash
# Terminal colours (after installing GNU coreutils)
NM="\[\033[0;38m\]"  # means no background and white lines
HI="\[\033[0;34m\]"  # change this for username letter colors
HII="\[\033[0;31m\]" # change this for hostname letter colors
SI="\[\033[0;33m\]"  # this is for the current directory
IN="\[\033[0;0m\]"

PS1="$NM[ $HI\u $SI\w$NM ] \$(__git_ps1) $IN\n\$(task-indicator) "
```

![Output of task-indicator.cr showing something due today](run-task-indicator.png)

Nice.

At first I put the output of `task-indicator` in a variable, and put the
variable in `$PS1`. Except that variable was only evaluated on shell
start. Instead put the invocation directly in `$PS1` with a leading
backslash. Now the indicator is live, as I expected it to be.

## Done!

I wanted to learn some basic Crystal usage and find ways to work the
language into my daily shell routine. With `eval`, `run`, and `build`
all at my disposal, it sure looks like a success! I even used Crystal
to make a Taskwarrior indicator, which has been on my task list since
last year.

I don’t know yet if Crystal is *better* than Ruby. Even at this early
point it’s just as useful and just as much fun. Since "be useful and
have fun" is a major thing for me, I’ll be exploring Crystal more\!
