---
aliases:
- /coolnamehere/2010/08/02_0d-the-spacetrade-project.html
- /post/2010/0d-the-spacetrade-project/
- /2010/08/02/parrot-babysteps-0d-the-spacetrade-project/
category: coolnamehere
date: 2010-08-02 00:00:00
layout: layout:PublishedArticle
series:
- Parrot Babysteps
slug: parrot-babysteps-0d-the-space-trade-project
tags:
- parrot
- learn
title: Parrot Babysteps 0d - The SpaceTrade Project
description: Trying to come up with an actual Parrot project
updated: 2010-08-30 00:00:00
uuid: 9445ddb9-240f-46a9-b838-19ccd5c129e4
---

[Stellar]: /post/2010/07/parrot-babysteps-0c-the-stellar-app
[Star Trader]: https://en.wikipedia.org/wiki/Star_Trader
[Trade Wars Rising]: http://tradewarsrising.com
[Oolite]: http://www.oolite.org/
[Eve Online]: http://eveonline.com

I might be done with the [Stellar][] application for the moment, but I don't think I'm done with the space
theme yet. 

Back in the ancient days, there was a nifty game called [Star Trader][]. You and your friends were
interstellar merchants trying to earn a few credits (or whatever) in a cold and uncaring universe. Star Trader
has had *many* popular descendants, which have evolved over the generations into games like [Trade Wars Rising][], 
[Oolite][] and [Eve Online][]. Those games are interactive and fun and great ways to kill many hours, but I've
got an itch for something old school. I want to revisit the joy of a text interface that demands your
imagination work overtime while you figure out what is going on.

[Dwarf Fortress]: http://www.bay12games.com/dwarves/

It is possible that I have been playing [Dwarf Fortress][] a little bit too much for my own good.

[original code]: https://web.archive.org/web/20131222221016/http://www.dunnington.u-net.com/public/basicgames/TRADES

This one is going to take some work. It is a fairly elaborate game. The map is random, markets change, and
merchants can be haggled with. I can use the [original code][] as a resource, but not very well. The listing I
could find was written in a HP-BASIC dialect that I am unfamiliar with. So I have to do more than just copy
the game. I'll have to make a game inspired by Star Trader instead. That seems to be what all the cool kids
are doing - assuming you use a rather flexible definition of "cool."

I talked about using a text interface, but I know that eventually I will want to choose my own interface for
the game. Players can choose their own approach, and bored coders will be able to create new ones. I will
start by keeping the game logic as abstract as I can, and worry about the details of play later.

## SpaceTrade Summary

Space Trade is a turn-based game in which one or more players assumes the role of an interstellar merchant in
the future. The game has a fixed number of turns, determined during game setup. Players are competing to have 
a pilot with the highest worth at the end of the game. The single player goal is to beat her own previous 
high scores.

Game play occurs on a map of star systems. Each star system has a trade classification, which makes the price
of goods vary from one system to the next. There is a port in every system for traders to buy and sell goods,
or to upgrade their ship's capabilities. Traders may attempt to haggle for a more favorable price, but this
might not work. As the game progresses, markets may change based on trade activity. A glut of a particular
good could temporarily reduce its value, or a run on that good could temporarily increase its value.

Traders may encounter hazards such as planetoids or pirates while travelling between systems. The results of
these encounters could be cargo loss or damage to the trader's ship. If a ship accumulates enough damage
without repair, it could be destroyed. Destruction of a ship ends the game for that trader.

### Development Tasks

My summary is a little vague compared to your average game, but there are a lot of juicy programming tasks in
there.

* Creating a star
* Building a star map
* Creating a new trader
* Buying cargo
* Selecting and travelling to a new system
* Selling cargo
* Dealing with changing markets
* Haggling with merchants
* Coping with environmental hazards (pirates, planetoids, etcetera)
* Enabling multiple players
* Upgrading a ship
* Scoring the endgame
* Tracking high scores
* Saving a game in play
* Loading a saved game

At each stage, we will work on the simple text interface and add randomization to make gameplay interesting.

I have never written a game in Parrot before. I have not written many games in *any* language. I understand if
one of your questions is "why not use language X?" - where *X* is Python, Perl, Ruby, Rakudo, D, or something
else. I might use language X another time, but then it would be part of the X Babysteps rather than the Parrot
Babysteps. 

Another question might be "Are we *ever* going to use Parrot to write a language?" Actually, yes. I'm going to
put together a simple script language that handles game behavior. Not a powerful megasmart language for high
end projects, but something for building the star map and playing the game itself. It will be used for saving
and sharing games, and inevitably for hacking game details. Hey, what fun is a game if you can't hack it?

That's three more on-going development tasks, then:

* Developing an interactive user shell
* Randomizing game play elements
* Creating a game scripting language

This is more complex than [Stellar][], and it will take more than a few steps to finish it. I am certain there
will be a lot of new Parrot territory to explore.

This should be fun. Let's get started!

## Setting up the project

[Step 09]: /post/2010/04/parrot-babysteps-09-simple-projects

Thanks to [Stellar][], I already know how I like to prepare my workspace for a new project.  The setup 
from [Step 09][] will provide the starting point for SpaceTrade.

    $ mkdir spacetrade
    $ mkdir spacetrade/t
    $ mkdir spacetrade/lib
    $ cd spacetrade

The `setup.pir` script will start out the same as the one used for [Stellar][].

    # example-0d-01/setup.pir
    .sub 'main' :main
        .param pmc args
        $S0 = shift args # Ignore my own filename
        load_bytecode 'distutils.pbc'

        # find out what command the user has issued.
        .local string directive
        directive = shift args

        # Used by test mode
        .local string prove_exec
        prove_exec = get_parrot()

        setup(directive, 'prove_exec' => prove_exec)
    .end

[Curses]: https://github.com/parrot/parrot/blob/master/runtime/parrot/library/Curses.pir
[SDL]: https://github.com/parrot/parrot/tree/master/runtime/parrot/library/SDL
[shell]: http://en.wikipedia.org/wiki/Shell_(computing)

There is one basic feature I want to get out of the way before I start handling game logic. User interaction
is important. Oh sure, there may eventually be interfaces in [Curses][] or [SDL][], but all that's needed for
now is a simple command line [shell][]. This shell will be used to examine the nuts and bolts of SpaceTrade
and to play a simple text-based version of the game.

### The SpaceTrade Interactive Shell

I believe that every interactive shell needs a few minimal components to be useful.

* A command to quit
* A command to get help
* A reasonable way to handle invalid input

A sample session with such a minimal shell might look like this:

    $ parrot lib/spacetrade.pir
    Welcome to SpaceTrade!
    Type ':help' for help, and ':quit' to quit.
    > waffles!
    Unknown command: waffles!
    Type ':help' for help, and ':quit' to quit.
    > :help
    COMMANDS
    :help    This view
    :quit    Exit the shell
    > :quit
    Goodbye!
    $

Why do I imagine this shell having commands prefixed by a `:` character? Well, "normal" commands would look
normal, but behavior like getting help or quitting the game are only important for dealing with the shell.
I want those special shell commands to look different from the normal game commands.

Of course, I may change my mind later. I am fickle.

What is the smallest amount of code I can use to get this end result and still feel comfortable?

    # example-0d-01/lib/spacetrade.pir
    .sub 'main' :main
        run_shell()
    .end

    .sub run_shell
        .local string input
        .local pmc    stdin
        .const string PROMPT     = '> '
        .const string QUICK_HELP = "Type ':help' for help, and ':quit' to quit."

        stdin = getstdin

        say "Welcome to SpaceTrade!"
        say QUICK_HELP

      READLINE:
        input = stdin.'readline_interactive'(PROMPT)
        if input == ':quit' goto EXIT
        if input == ':help' goto SHOW_USAGE
        goto SHOW_ERROR

      SHOW_USAGE:
        say "COMMANDS"
        say ":help    This view"
        say ":quit    Exit the shell"
        goto READLINE

      SHOW_ERROR:
        .local string error_message
        error_message = "Unknown command: "
        error_message .= input
        say error_message
        say QUICK_HELP
        goto READLINE

      EXIT:
        say "Goodbye!"
    .end

This works, but it doesn't look right. 

For a start, the commands are kind of a mess. When I add commands, I will have to add both an `if` check in the
`READLINE` section and a line of output in the `SHOW_USAGE` section. Then there are the blocks I would have to
add to provide that actual functionality. No, I do not like this at all. The shell commands should be better
organized so that adding and managing features is as easy as possible.

One approach would be to add a registry which stores the commands recognized by the shell.

### Creating a Command Registry

The idea is that I could have a simple structure that stores information about available commands, and the
application could add commands as needed. Let's start with a simple Hash and two subroutines for adding and
evaluating shell commands.

    # example-0d-02/t/01-shell-metacommands.t
    .include 'lib/spacetrade.pir'

    .sub 'main' :main
        .include 'test_more.pir'

        plan(1)

        .local pmc    commands
        .local string expected
        .local string output

        commands = new 'Hash'
        commands = register_command(commands, ':dude', 'say_dude', 'Say "Dude!"')
        expected = "Dude!"
        output = evaluate_command(commands, ':dude')
        is(output, expected, 'User command ":dude" should result in string "Dude!"')
    .end

    .sub say_dude
        .return("Dude!")
    .end

The first sub that's needed is `register_command`, which will add a `:dude` entry in the `commands` Hash with
appropriate information. 

    # example-0d-02/lib/spacetrade.pir

    .sub register_command
        .param pmc    commands
        .param string name
        .param string sub_name
        .param string explanation

        .local pmc    command
        .local pmc    callback

        command = new 'Hash'
        command['sub_name'] = sub_name
        command['explanation'] = explanation
        commands[name] = command

      RETURN_COMMANDS:
        .return(commands)
    .end

There is no special magic going on here. `command[':dude']` points to a Hash containing a subroutine name and
an explanation of the command. `commands` is returned to the caller once the new command has been added.

[step 06]: /post/2009/10/parrot-babysteps-06-files-and-hashes
[variable opcode]: http://docs.parrot.org/parrot/latest/html/src/ops/var.ops.html

You can probably figure out what I expect to happen from the test code. I have a `say_dude` sub, and somehow
I expect the shell to figure out how to call that sub when I ask for it by sending the `:dude` command.
We've actually already done this, back when we were grabbing the `chomp` sub in [step 06][]. The `get_global`
[variable opcode][] will look for a variable with a specified name and return it to us if it exists.

    # example-0d-02/lib/spacetrade.pir
    .sub evaluate_command
        .param pmc    commands
        .param string name

        .local string sub_name
        .local pmc    command_sub
        .local string output

        sub_name = commands[name;'sub_name']
        command_sub = get_global sub_name
        output = command_sub()

        .return(output)
    .end

There is one new bit of strangeness here, though:

    sub_name = commands[name;'sub_name']

This is called a "complex key," and lets us directly access the values in the Hash held at `commands[name]`.
Each index in a complex key is separated by a semicolon (`;`) character.  Without a 
complex key, we might have to do something like this:

    $P1 = commands[name]
    sub_name = $P1['sub_name']

[variables chapter]: http://docs.parrot.org/parrot/latest/html/docs/book/pir/ch04_variables.pod.html

I did not realize I could use a complex key until I scanned the [variables chapter][] of the Parrot PIR Book.
It is important to keep reviewing documentation, even if you think you already know a solution. Remember: 
regardless of what you know, there is probably a better way.

It is time to add basic error handling to the shell. `evaluate_command` needs to handle two major error cases.

1. User tries a command that doesn't exist
2. User tries a command that points to a nonexistent subroutine.

Okay, let's add the tests.

    # example-0d-03/t/01-shell-metacommands.t
    .sub 'main' :main
        .include 'test_more.pir'

        plan(3)

        .local pmc    commands
        .local string expected
        .local string output

        commands = new 'Hash'
        commands = register_command(commands, ':dude', 'say_dude', 'Say "Dude!"')
        expected = "Dude!"
        output = evaluate_command(commands, ':dude')
        is(output, expected, 'User command ":dude" should result in string "Dude!"')

        expected = "Unknown command: :sweet"
        output = evaluate_command(commands, ':sweet')
        is(output, expected, 'Shell should warn about unknown commands')

        commands = register_command(commands, ':whats-mine-say', 'whats_mine_say', "What's mine say?")
        expected = "Invalid command: :whats-mine-say points to nonexistent sub whats_mine_say"
        output = evaluate_command(commands, ':whats-mine-say')
        is(output, expected, 'Shell should warn about invalid commands')
    .end

    # ...

`evaluate_command` is a little more complicated now, but it is still manageable.

    # example-0d-03/lib/spacetrade.pir

    # ...

    .sub evaluate_command
        .param pmc    commands
        .param string name

        .local string sub_name
        .local pmc    command_sub
        .local string output

        sub_name = commands[name;'sub_name']
        unless sub_name goto UNKNOWN_COMMAND
        command_sub = get_global sub_name
        if_null command_sub, INVALID_COMMAND
        output = command_sub()
        goto RETURN_OUTPUT

      UNKNOWN_COMMAND:
        output = "Unknown command: " . name
        goto RETURN_OUTPUT

      INVALID_COMMAND:
        output = "Invalid command: " . name
        output .= " points to nonexistent sub "
        output .= sub_name

      RETURN_OUTPUT:
        .return(output)
    .end

    # ...

One thing that might catch your attention is the `if_null` opcode.

    if_null command_sub, INVALID_COMMAND

This will check if `command_sub` is null, and branch to `INVALID_COMMAND` if the subroutine we just tried to
grab is indeed null. To be perfectly honest with you, I'm not sure if a branch is the same as a `goto`. It
behaves the same in this code, so for now I will pretend that it is the same.

### Setting Up Those Default Shell Commands

This ends up working pretty much the same as the earlier code did, and it's a bit more flexible. Is this how
we make programming languages in Parrot? Well, no. This is not how we make programming languages in Parrot.
This is a very simple shell which will have a few simple commands, but try to pass everything else off to the
game itself. Proper language development is still a few Babysteps away.

    # example-0d-04/t/01-shell-metacommands.t
    .include 'lib/spacetrade.pir'

    .sub 'main' :main
        .include 'test_more.pir'

        plan(5)

        .local pmc    commands
        .local string expected
        .local string output

        commands = new 'Hash'
        commands = register_command(commands, ':dude', 'say_dude', 'Say "Dude!"')
        expected = "Dude!"
        output = evaluate_command(commands, ':dude')
        is(output, expected, 'User command ":dude" should result in string "Dude!"')

        expected = "Unknown command: :sweet"
        output = evaluate_command(commands, ':sweet')
        is(output, expected, 'Shell should warn about unknown commands')

        commands = register_command(commands, ':whats-mine-say', 'whats_mine_say', "What's mine say?")
        expected = "Invalid command: :whats-mine-say points to nonexistent sub whats_mine_say"
        output = evaluate_command(commands, ':whats-mine-say')
        is(output, expected, 'Shell should warn about invalid commands')

        commands = register_default_commands()

        expected =<<'EXPECTED'
    COMMANDS
    :help    This view
    :quit    Exit the shell
    EXPECTED
        output = evaluate_command(commands, ':help')
        is(output, expected, ':help should be a registered default command')

        expected = ''
        output = evaluate_command(commands, ':quit')
        is(output, expected, ':quit should be a registered default command that returns an empty string')
    .end

    .sub say_dude
        .return("Dude!")
    .end

The test code that has already been written shows a clear path for registering default commands. All that's
needed is the subroutines that will be invoked when the command is called.

    example-0d-04/lib/spacetrade.pir
    .sub register_default_commands
        .local pmc commands

        commands = new 'Hash'
        commands = register_command(commands, ':help', 'default_help', 'This view')
        commands = register_command(commands, ':quit', 'default_quit', 'Exit the shell')

        .return(commands)
    .end

    .sub default_help
        .local string output

        output =<<'OUTPUT'
    COMMANDS
    :help    This view
    :quit    Exit the shell
    OUTPUT

        .return(output)
    .end

    .sub default_quit
        .local string output
        output = ''
        .return(output)
    .end

There's a problem.

The problem is that I had to cheat on `default_help`. See, the way that I set up `evaluate_commands` is to
directly invoke the registered subroutine without any arguments. I would prefer that `default_help` examined
the currently registered commands and provided a real summary. It should even include my magnificent `:dude`
command in the summary.

    # example-0d-05/t/01-shell-metacommands.t
    .include 'lib/spacetrade.pir'

    .sub 'main' :main
        .include 'test_more.pir'

        plan(6)

        .local pmc    commands
        .local string expected
        .local string output

        commands = register_default_commands()

        expected =<<'EXPECTED'
    COMMANDS
    :help    This view
    :quit    Exit the shell
    EXPECTED
        output = evaluate_command(commands, ':help')
        is(output, expected, ':help should be a registered default command')

        expected = ''
        output = evaluate_command(commands, ':quit')
        is(output, expected, ':quit should be a registered default command that returns an empty string')

        commands = register_command(commands, ':dude', 'say_dude', 'Say "Dude!"')

        expected =<<'EXPECTED'
    COMMANDS
    :dude    Say "Dude!"
    :help    This view
    :quit    Exit the shell
    EXPECTED
        output = evaluate_command(commands, ':help')
        is(output, expected, ':help should reflect registered commands')

        expected = "Dude!"
        output = evaluate_command(commands, ':dude')
        is(output, expected, 'User command ":dude" should result in string "Dude!"')

        expected = "Unknown command: :sweet"
        output = evaluate_command(commands, ':sweet')
        is(output, expected, 'Shell should warn about unknown commands')

        commands = register_command(commands, ':whats-mine-say', 'whats_mine_say', "What's mine say?")
        expected = "Invalid command: :whats-mine-say points to nonexistent sub whats_mine_say"
        output = evaluate_command(commands, ':whats-mine-say')
        is(output, expected, 'Shell should warn about invalid commands')

    .end

    .sub say_dude
        .return("Dude!")
    .end

How am I supposed to do this? Let's start by rewriting `default_help` the way it should work: by preparing a
sorted list of registered commands and their summaries.

    # example-0d-05/lib/spacetrade.pir
    .sub default_help
        .param pmc    commands
        .local string output
        .local pmc    command_iter
        .local pmc    command_keys
        .local string key

        command_keys = new 'ResizablePMCArray'
        command_iter = iter commands

      NEXT_COMMAND:
        unless command_iter goto PREPARE_OUTPUT
        key = shift command_iter
        push command_keys, key
        goto NEXT_COMMAND

      PREPARE_OUTPUT:
        output = "COMMANDS\n"
        command_keys.'sort'()

        .local string command_name
        .local string command_explanation
        .local string command_summary
        command_iter = iter command_keys

      NEXT_SUMMARY:
        unless command_iter goto RETURN_OUTPUT
        command_name = shift command_iter
        command_explanation = commands[command_name;'explanation']
        command_summary = command_name . '    '
        command_summary .= command_explanation
        command_summary .= "\n"
        output .= command_summary
        goto NEXT_SUMMARY

      RETURN_OUTPUT:
        .return(output)
    .end

A little explanation about `default_help` couldn't hurt. Hashes use their own special tricks to make storing
their elements more effective, which means you have no guarantee of getting them in any particular order. I
want to see the commands in alphabetical order, so I will have to handle the ordering myself. I did that by
first building a list of keys.

        command_keys = new 'ResizablePMCArray'
        command_iter = iter commands

      NEXT_COMMAND:
        unless command_iter goto PREPARE_OUTPUT
        key = shift command_iter
        push command_keys, key
        goto NEXT_COMMAND


Once that list was constructed, it needed to be put in some sort of order. Luckily, the Array PMCs come
with a prepackaged `sort()` method - a special subroutine that works directly with the elements of the array.

        command_keys.'sort'()

The default sort behavior works for me. In this case they will be sorted more or less alphabetically.

Now, I could add a
lot of code to `evaluate_command` that will magically determine what sort of arguments are required by the
command, and to behave appropriately. But before I go doing a significant rewrite - how about an experiment? 
Maybe I can just call every command with `commands` as a parameter, and see what happens in the tests.

    # example-0d-05/lib/spacetrade.pir

    # ...

    .sub evaluate_command
        .param pmc    commands
        .param string name

        .local string sub_name
        .local pmc    command_sub
        .local string output

        sub_name = commands[name;'sub_name']
        unless sub_name goto UNKNOWN_COMMAND
        command_sub = get_global sub_name
        if_null command_sub, INVALID_COMMAND
        output = command_sub(commands)
        goto RETURN_OUTPUT

      UNKNOWN_COMMAND:
        output = "Unknown command: " . name
        goto RETURN_OUTPUT

      INVALID_COMMAND:
        output = "Invalid command: " . name
        output .= " points to nonexistent sub "
        output .= sub_name

      RETURN_OUTPUT:
        .return(output)
    .end

You have to be willing to experiment, because the results may occasionally surprise you.

    $ parrot t/01-shell-metacommands.t
    1..6
    ok 1 - :help should be a registered default command
    ok 2 - :quit should be a registered default command that returns an empty string
    ok 3 - :help should reflect registered commands
    ok 4 - User command ":dude" should result in string "Dude!"
    ok 5 - Shell should warn about unknown commands
    ok 6 - Shell should warn about invalid commands

How about that - it worked. PIR subroutines will apparently ignore positional parameters that they didn't ask
for, which means that `evaluate_command` can call `say_dude` and `default_help` with the same parameter list
and nothing bad will happen.

### The New and Slightly Improved Shell

A lot of work has gone into making the shell easier to use for me and people who want to hack on the game in
the future. Let's apply that work to the `run_shell` subroutine itself.

    # example-0d-05/lib/spacetrade.pir

    .sub run_shell
        .local pmc    commands
        .local string input
        .local string output
        .local pmc    stdin
        .const string PROMPT     = '> '
        .const string QUICK_HELP = "Type ':help' for help, and ':quit' to quit."

        commands = register_default_commands()
        stdin = getstdin

        say "Welcome to SpaceTrade!"
        say QUICK_HELP

      READLINE:
        input = stdin.'readline_interactive'(PROMPT)
        output = evaluate_command(commands, input)
        unless output goto EXIT
        say output
        goto READLINE

      EXIT:
        say "Goodbye!"
    .end

It's certainly shorter than what I started with. How well does it work?

    $ parrot lib/spacetrade.pir
    Welcome to SpaceTrade!
    Type ':help' for help, and ':quit' to quit.
    > :dude
    Unknown command: :dude
    > :help
    COMMANDS
    :help    This view
    :quit    Exit the shell

    > :quit
    Goodbye!

It isn't perfect, but it will work for the moment. This new shell has most of the 
core behavior from the original, and we have shown that it will not be hard to add 
new commands. There is still a large part of me that thinks the code for the shell 
should be tucked into its own corner, where it cannot get mixed up with the code for 
the actual game. That will have to wait for the next step, though.