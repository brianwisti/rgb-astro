---
aliases:
- /coolnamehere/2010/10/11_0e-parrot-namespaces.html
- /post/2010/0e-parrot-namespaces/
- /2010/10/11/parrot-babysteps-0e-parrot-namespaces/
category: coolnamehere
date: 2010-10-11 00:00:00
layout: layout:PublishedArticle
series:
- Parrot Babysteps
slug: parrot-babysteps-0e-parrot-namespaces
tags:
- parrot
- learn
title: Parrot Babysteps 0e - Parrot Namespaces
uuid: bcd11d37-0f8e-440c-ad05-673cbaf32115
---

[previous Babystep]: /post/2010/08/parrot-babysteps-0d-the-spacetrade-project
[Star Trader]: https://en.wikipedia.org/wiki/Star_Trader

Where was I? In the [previous Babystep][], I started working out some rough ideas for a version of the old
school [Star Trader][] game written in Parrot PIR. I made a quick description and sketched up a list of
the features that would need to be created. One of those features was an interactive shell to be used in
developing and hacking on that Space Trade game. I wrote a simple shell that could be extended, making it
easier to expand the capabilities of the shell in the future - or even use the shell in some completely
unforeseen future application. 

[namespace]: http://en.wikipedia.org/wiki/Namespace_(computer_science)

I like that shell, but it is not perfect. Programming languages like Parrot support [namespaces][], which you
can think of as dictionaries that the language uses to look up variables and subroutines. My problem with the
shell today revolves around the fact that every subroutine used in defining or
extending the shell exists in the global namespace. They are available everywhere - in every line of code for
the SpaceTrade game and anything that uses it. This may not be a huge problem by itself, because right
now there are only a few subroutines. The number of subroutines will grow as the project evolves, however.
This will have a couple of different effects.

* Subroutine names will be harder to remember, because the global namespace is one big bucket. I like to put
  related subroutines into little boxes so that I can focus on shell behavior when I'm looking at shell code,
  and game behavior when I'm looking at game code.
* Subroutine names could get rather contorted. What happens if I make Space Trade available, and against all
  odds it becomes a runaway success? Five, maybe even ten people download it and play it. It is likely
  that at least one of those people will want to write their own shell for the game. They will have to come up
  with some odd names for their shell code, such as `register_awesome_commands`, because I have selfishly 
  used all the good names for my own shell.

## Namespaces

[Namespaces]: http://en.wikipedia.org/wiki/Namespace_(computer_science)
[Parrot Namespaces]: http://docs.parrot.org/parrot/latest/html/docs/book/pir/ch04_variables.pod.html#Namespaces
[Test::More]: https://github.com/parrot/parrot/blob/master/runtime/parrot/include/test_more.pir

[Namespaces][] provide a way to insulate the parts of a computer program from each other. The subroutines and
variables defined in one namespace will not interfere with the subroutines and variables in another. This
means that I can have my `register_default_commands` subroutine for my own shell, and you can have a
`register_default_commands` subroutine in your own shell, and they never need to know about each other.
It does mean you must take extra steps if you want to use the subroutine from my package in your own code, or
I must somehow provide a means to push the subroutines that I consider appropriate into your namespace. That
is what [Test::More][] does. Defining something like that is an exercise in careful judgment and reasonable
coding. In other words, we will not be doing that with SpaceTrade any time soon.

I will try to focus on the most important elements of [Parrot Namespaces][] rather than get carried away with
all of the little details.

### Organizing the Namespaces

Even though the SpaceTrade game has very little code right now, I want to put a little thought into organizing
my namespaces before I create them. The first layer is easy: all of the code supporting the SpaceTrade game
will go in the "SpaceTrade" namespace.

* SpaceTrade: Code for the SpaceTrade Game

Parrot supports nested namespaces, so "SpaceTrade" can contain any number of namespaces. I'm sure there will
be many contained namespaces for game setup and play, but I will only specify the one I am working on today:
"SpaceTrade::Shell."

* SpaceTrade: Code for the SpaceTrade Game
** SpaceTrade::Shell: A simple interactive shell for SpaceTrade

The names do not mean anything to Parrot. It does not force a particular way of organizing your namespaces.
Nested namespaces are a convenience so that *we* know two chunks of code are somewhat related.

#### The `.namespace` Directive

The `.namespace` directive is used to tell Parrot that the following code belongs in a particular namespace.
Its argument is a hash index specifying the name.

    .namespace ['SpaceTrade']

Use a complex key to indicate a nested namespace.

    .namespace ['SpaceTrade';'Shell']

All of the code after the `.namespace` directive gets filed in the namespace associated with the key you
handed to it. This lasts until you declare a new namespace.

It's time to try it out in `spacetrade.pir`. All of the code written so far is for the shell, so I can
probably get away with putting my `.namespace` directive at the top of the file.

    # example-0e-01/lib/spacetrade.pir
    .namespace ['SpaceTrade';'Shell']

    .sub 'main' :main
        run_shell()
    .end

    .sub run_shell
        # ...

[Perl]: /tags/perl/

Why do I say "SpaceTrade::Shell" rather than `['SpaceTrade';'Shell']` when talking about my namespace in this
article? That is mainly because I am lazy. My fingers do not enjoy typing out all the characters to say
`['SpaceTrace';'Shell']`, so I want to use a shorthand. "SpaceTrade::Shell" mimics a convention used by some
Parrot programmers when talking about namespaces. It is a convention derived from the way that namespaces - or
"packages" - are declared in [Perl][], which is another language of choice for many Parrot developers. I will
switch to another convention if I see one that is both widely used and easy to type.

Back to SpaceTrade. I run `setup.pir test` out of curiosity.

    $ parrot setup.pir test
    t/01-shell-metacommands.t .. ok
    All tests successful.
    Files=1, Tests=6,  0.015 wallclock secs
    Result: PASS

The tests pass, which is kind of cool. But *why* do they pass, if I have defined a namespace in `spacetrade.pir`?
The tests should complain about missing subroutines if they are in a different namespace, right?

Yes, that is right. However, the `.include` directive effectively dumps the code from your included file
right where you put the directive. The tests exist in the `['SpaceTrade';'Shell']` namespace because we never
indicated that we were moving onto a new one.

That might even be okay for these tests. After all, they are just telling me that the shell subroutines work,
not that namespace handling works. The SpaceTrade namespaces are going to get more cluttered as time goes on,
though. I am going to be more explicit in the namespace handling for my tests in order to prepare for that
clutter.

### The Default Namespace

To specify that you are going back to the default namespace, hand an empty key to the `.namespace`
directive.

    .namespace [ ]

I understand the idea here. The default namespace is no namespace at all, so it gets an empty key. Let's put
that line in `01-shell-metacommands.pir`.

    # example-0e-02/t/01-shell-metacommands.pir

    .include 'lib/spacetrade.pir'

    .namespace [ ]

    .sub 'main' :main
        .include 'test_more.pir'
        # ...

What happens if I run the tests now?

    $ parrot setup.pir test
    t/01-shell-metacommands.t .. Dubious, test returned 1
    Failed 6/6 subtests

    Test Summary Report
    -------------------
    t/01-shell-metacommands.t (Tests: 0 Failed: 0)
      Non-zero exit status: 1
      Parse errors: Unknown TAP token: "Could not find sub register_default_commands"
                    Unknown TAP token: "current instr.: 'main' pc 275 (t/01-shell-metacommands.t:14)"
    Bad plan.  You planned 6 tests but ran 0.
    Files=1, Tests=0,  0.014 wallclock secs
    Result: FAIL
    test fails
    current instr.: 'setup' pc 829 (runtime/parrot/library/distutils.pir:379)

This is the error I was expecting to see initially, so I am happy. I suppose I could have put that 
`.namespace [ ]` directive at the end of `spacetrade.pir` - Parrot does not have any rules about where to end one
namespace and start another - but I feel like that would have broken the way `.include` behaves. I will
probably learn a better way to handle these little namespace issues eventually.

[Step 07]: /post/2009/10/parrot-babysteps-07-writing-subroutines

Now I have library code tucked into a namespace and test code that doesn't know about the shell subroutines.
A quick look at [Step 07][] shows how to get those shell subroutines into our current namespace. The
`get_global` opcode allows us to grab a variable from another namespace. We used it in [Step 07][] to grab the
`chomp` subroutine from the String::Utils namespace. Let's use `get_global` to make the tested subroutines
available.

    # example-0e-03/t/01-shell-metacommands.t
    .include 'lib/spacetrade.pir'

    .namespace [ ]

    .sub 'main' :main
        .include 'test_more.pir'

        plan(6)

        .local pmc    register_default_commands
        .local pmc    evaluate_command
        .local pmc    register_command
        .local pmc    commands
        .local string expected
        .local string output

        register_default_commands = get_global ['SpaceTrade';'Shell'], 'register_default_commands'
        evaluate_command = get_global ['SpaceTrade';'Shell'], 'evaluate_command'
        register_command = get_global ['SpaceTrade';'Shell'], 'register_command'

        commands = register_default_commands()

        # ...

As we can see, that's *almost* good enough.

    1..6
    ok 1 - :help should be a registered default command
    ok 2 - :quit should be a registered default command that returns an empty string
    ok 3 - :help should reflect registered commands
    not ok 4 - User command ":dude" should result in string "Dude!"
    # Have: Invalid command: :dude points to nonexistent sub say_dude
    # Want: Dude!
    ok 5 - Shell should warn about unknown commands
    ok 6 - Shell should warn about invalid commands

Up until now we have been using subroutine names when registering commands, but that is not going to work
anymore. SpaceTrade no longer knows exactly where it should look for the subroutines with those names.
Instead of names, let's try using the subroutines themselves.

    # example-0e-04/lib/spacetrade.pir
    .sub register_command
        .param pmc    commands
        .param string name
        .param pmc    code
        .param string explanation

        .local pmc    command
        .local pmc    callback

        command = new 'Hash'
        command['code'] = code
        command['explanation'] = explanation

        commands[name] = command
        goto RETURN_COMMANDS

      RETURN_COMMANDS:
        .return(commands)
    .end

`register_command` doesn't look a lot different. The names have changed to show what is going on, but we are
still just building a Hash of commands and relying on `evaluate_command` to sort out any problems.

Naturally, that means `evaluate_command` is where the changes become obvious.

    # example-0e-04/lib/spacetrade.pir
    .sub evaluate_command
        .param pmc    commands
        .param string name

        .local int    has_command
        .local pmc    command_info
        .local pmc    code
        .local int    is_invokable
        .local pmc    command_sub
        .local string output

        has_command = exists commands[name]
        unless has_command goto UNKNOWN_COMMAND

        command_sub = commands[name;'code']
        if_null command_sub, INVALID_COMMAND

        is_invokable = does command_sub, 'invokable'
        unless is_invokable goto INVALID_COMMAND

        output = command_sub(commands)
        goto RETURN_OUTPUT

      UNKNOWN_COMMAND:
        output = "Unknown command: " . name
        goto RETURN_OUTPUT

      INVALID_COMMAND:
        output = "Invalid command: " . name
        output .= " does not point to a valid subroutine"

      RETURN_OUTPUT:
        .return(output)
    .end

We do a few simple checks when somebody tries to evaluate a command.

* Do we have an entry for the command?
* Is there something actually *at* the entry?
* Is the thing stored for the command look like something we can treat as a subroutine?

[#parrot]: http://irclog.perlgeek.de/parrot

That's what the `does` check handles, incidentally. Right now we only know about subroutines, but later on we
may get into strange creations that aren't subroutines but can be invoked as if they were. From what the folks
on [#parrot][] tell me, you would ask `command_sub` if it is invokable. All I know is that it worked and that I
like the folks on [#parrot][] very much.

We should make one more change before heading over to the tests. `register_default_commands` needs to adjust
to the new way of registering commands.

    # example-0e-04/lib/spacetrade.pir
    .sub register_default_commands
        .local pmc commands
        .local pmc help_command
        .local pmc quit_command

        commands = new 'Hash'
        help_command = get_global 'default_help'
        quit_command = get_global 'default_quit'
        commands = register_command(commands, ':help', help_command, 'This view')
        commands = register_command(commands, ':quit', quit_command, 'Exit the shell')

        .return(commands)
    .end

If you don't explicitly hand a namespace to `get_global`, it will use whatever namespace it's called from. In
this case, that is the SpaceTrade::Shell namespace.

We have to change the tests themselves now. There is actually only one test that needs to be changed. Look in
`01-shell-metacommands.t` for the line that registers the `:dude` command.

    # example-0e-03/t/01-shell-metacommands.t
    # ...
    commands = register_command(commands, ':dude', 'say_dude', 'Say "Dude!"')

Instead of handing a string, create a PMC to hold the `say_dude` subroutine and had *that* to
`register_command`.

    # example-0e-04/t/01-shell-metacommands.t
    .local pmc my_sub
    my_sub = get_global 'say_dude'
    commands = register_command(commands, ':dude', my_sub, 'Say "Dude!"')

Once again, we're using `get_global` to grab from the current namespace, which is the default namespace now.

All right, the tests should run okay.

It is possible to set and get truly global variables with `get_root_global` and `set_root_global`, but I do
not recommend it. What happens if you decide that the global `my_config` should be an Array instead of a Hash? 
Every piece of code that uses a global variable must be updated.

The same problem exists with package globals, even though it may be on a smaller scale. There's a solution -
or at least a way to make the problem even smaller. Whenever I see data and several subroutines that need to
work on that data, I start to see objects.