---
aliases:
- /2019/11/29/directory-listings-with-crystal/
category: programming
date: 2019-11-29
description: I swear I'm not reinventing `ls`.
draft: false
layout: layout:PublishedArticle
slug: directory-listings-with-crystal
tags:
- crystal
- files
title: Directory Listings With Crystal
uuid: 63d91af4-5f4b-44bf-b3ce-16a9f1b1dc2b
---

[summarize one file with Crystal]: /post/2019/11/summarizing-a-file-with-crystal/

Okay, I know how to [summarize one file with Crystal][]. What about directories?

## List files in a directory

Let’s start with a list of the directory’s contents. We can worry about
summarizing them later.

[Dir](https://crystal-lang.org/api/Dir.html) knows all about directories
and their contents. Open a directory with a string containing a path,
and ask for its children.

``` crystal
dirname = "#{ENV["HOME"]}/Sync/Books/computer"
puts Dir.open(dirname).children
```

    ["programmingvoiceinterfaces.pdf", "Databases", "task-2.5.1.ref.pdf", "Perl", "Tools",
    "devopsish", "diy", "Hacking_ The Art of Exploitation, 2nd Edition.pdf",
    "The Linux Programming Interface.pdf", "Web Layout", "Java", "JavaScript", "Generative_Art.pdf",
    "Mac OS X Lion_ The Missing Manual.PDF", "highperformanceimages.pdf", "jsonatwork.pdf",
    "Microsoftish", "Python", "Ruby", "PHP", "Misc-lang", "tools", "Data Science", "Principles", "cs",
    "vistaguidesv2"]

[Dir\#children](https://crystal-lang.org/api/Dir.html#children:Array\(String\)-instance-method)
gets you all the files in a directory except the special `.` and `..`
items. If you need those, use
[Dir\#entries](https://crystal-lang.org/api/Dir.html#entries:Array\(String\)-instance-method).

I need to look at each child if I want a readable summary of the
directory. I could mess with the
[Array](https://crystal-lang.org/api/Array.html) returned by
`Dir#children`. There’s a better way, though. Crystal provides a handy
[iterator](https://en.wikipedia.org/wiki/Iterator) with
[Dir\#each\_child](https://crystal-lang.org/api/Dir.html#each_child\(dirname,&block\)-class-method).

``` crystal
Dir.open(dirname).each_child { |child| puts child }
```

    programmingvoiceinterfaces.pdf
    Databases
    task-2.5.1.ref.pdf
    Perl
    Tools
    devopsish
    diy
    Hacking_ The Art of Exploitation, 2nd Edition.pdf
    The Linux Programming Interface.pdf
    Web Layout
    Java
    JavaScript
    Generative_Art.pdf
    Mac OS X Lion_ The Missing Manual.PDF
    highperformanceimages.pdf
    jsonatwork.pdf
    Microsoftish
    Python
    Ruby
    PHP
    Misc-lang
    tools
    Data Science
    Principles
    cs
    vistaguidesv2

That’s *much* easier to read. Yes. I can work with `Dir#each_child` to
create a summary.

## Summarize the directory contents

I want file names, sizes, and modification times. I already have the
names. [File.info](https://crystal-lang.org/api/File/Info.html) provides
size and time details. Formatting can be handled with a mix of
[sprintf](https://crystal-lang.org/api/toplevel.html#sprintf\(format_string,args:Array%7CTuple\):String-class-method)
and
[Number\#format](https://crystal-lang.org/api/Number.html#format\(separator='.',delimiter=',',decimal_places:Int?=nil,*,group:Int=3,only_significant:Bool=false\):String-instance-method).

``` crystal
Dir.open(dirname).each_child do |child|
  info = File.info "#{dirname}/#{child}"
  puts "%-50s %10d %24s" % { child, info.size.format, info.modification_time }
end
```

I worked these column widths out manually. There are more robust
approaches. In fact, I’ll get to one of them in a few paragraphs.

    programmingvoiceinterfaces.pdf                     18,597,798  2019-02-17 15:32:27 UTC
    Databases                                               4,096  2019-10-26 04:31:25 UTC
    task-2.5.1.ref.pdf                                    130,899  2019-02-17 15:32:27 UTC
    Perl                                                    4,096  2019-10-26 04:31:25 UTC
    Tools                                                   4,096  2019-10-25 14:44:36 UTC
    devopsish                                               4,096  2019-10-26 04:31:25 UTC
    diy                                                     4,096  2019-10-19 07:27:54 UTC
    Hacking_ The Art of Exploitation, 2nd Edition.pdf   4,218,534  2019-02-17 15:32:26 UTC
    The Linux Programming Interface.pdf                19,628,791  2019-02-17 15:32:26 UTC
    Web Layout                                              4,096  2019-10-19 07:27:57 UTC
    Java                                                    4,096  2019-10-26 04:31:25 UTC
    JavaScript                                              4,096  2019-10-26 04:31:25 UTC
    Generative_Art.pdf                                 22,777,770  2019-02-17 15:32:26 UTC
    Mac OS X Lion_ The Missing Manual.PDF              43,051,912  2019-02-17 15:32:26 UTC
    highperformanceimages.pdf                          51,412,248  2019-02-17 15:32:26 UTC
    jsonatwork.pdf                                     10,193,473  2019-02-17 15:32:26 UTC
    Microsoftish                                            4,096  2019-10-19 07:28:00 UTC
    Python                                                  4,096  2019-10-26 04:31:25 UTC
    Ruby                                                    4,096  2019-10-26 04:31:25 UTC
    PHP                                                     4,096  2019-10-26 04:31:25 UTC
    Misc-lang                                               4,096  2019-10-26 04:31:25 UTC
    tools                                                   4,096  2019-10-25 14:41:26 UTC
    Data Science                                            4,096  2019-10-26 04:31:25 UTC
    Principles                                              4,096  2019-10-20 01:23:43 UTC
    cs                                                      4,096  2019-10-19 01:37:08 UTC
    vistaguidesv2                                           4,096  2019-10-19 06:56:45 UTC

This is nice and tidy! Of course, now I have more thoughts. The items
need to be sorted — by name is good enough. I also want a more obvious
indicator which ones are directories

``` crystal
Dir.open(dirname) do |dir|
  dir.children.sort.each do |child|
    info = File.info "#{dirname}/#{child}"
    child += "/" if info.directory?
    puts "%-50s %10s %24s" % { child, info.size.format, info.modification_time }
  end
end
```

If a trailing `/` for directories is good enough for `ls -F`, it’s good
enough for me.

    Data Science/                                           4,096  2019-10-26 04:31:25 UTC
    Databases/                                              4,096  2019-10-26 04:31:25 UTC
    Generative_Art.pdf                                 22,777,770  2019-02-17 15:32:26 UTC
    Hacking_ The Art of Exploitation, 2nd Edition.pdf   4,218,534  2019-02-17 15:32:26 UTC
    Java/                                                   4,096  2019-10-26 04:31:25 UTC
    JavaScript/                                             4,096  2019-10-26 04:31:25 UTC
    Mac OS X Lion_ The Missing Manual.PDF              43,051,912  2019-02-17 15:32:26 UTC
    Microsoftish/                                           4,096  2019-10-19 07:28:00 UTC
    Misc-lang/                                              4,096  2019-10-26 04:31:25 UTC
    PHP/                                                    4,096  2019-10-26 04:31:25 UTC
    Perl/                                                   4,096  2019-10-26 04:31:25 UTC
    Principles/                                             4,096  2019-10-20 01:23:43 UTC
    Python/                                                 4,096  2019-10-26 04:31:25 UTC
    Ruby/                                                   4,096  2019-10-26 04:31:25 UTC
    The Linux Programming Interface.pdf                19,628,791  2019-02-17 15:32:26 UTC
    Tools/                                                  4,096  2019-10-25 14:44:36 UTC
    Web Layout/                                             4,096  2019-10-19 07:27:57 UTC
    cs/                                                     4,096  2019-10-19 01:37:08 UTC
    devopsish/                                              4,096  2019-10-26 04:31:25 UTC
    diy/                                                    4,096  2019-10-19 07:27:54 UTC
    highperformanceimages.pdf                          51,412,248  2019-02-17 15:32:26 UTC
    jsonatwork.pdf                                     10,193,473  2019-02-17 15:32:26 UTC
    programmingvoiceinterfaces.pdf                     18,597,798  2019-02-17 15:32:27 UTC
    task-2.5.1.ref.pdf                                    130,899  2019-02-17 15:32:27 UTC
    tools/                                                  4,096  2019-10-25 14:41:26 UTC
    vistaguidesv2/                                          4,096  2019-10-19 06:56:45 UTC

This is better\! I can use this information. Time to look at arbitrary
directories.

## Specifying a directory via `ARGV`

[ARGV](https://crystal-lang.org/api/toplevel.html#ARGV) is a top level
array holding arguments intended for your program. If we called a
compiled Crystal program like this:

    $ ./list ~/Sync/Books/computer

`~/Sync/Books/computer` would be the first and only item in `ARGV`.

<aside class="admonition note">
  <p class="admonition-title">Note</p>

Some languages include the program name in their list of arguments.
Crystal keeps the program name in `PROGRAM_NAME`, and the arguments in
`ARGV`.

</aside>

If I needed anything more than "grab the first item in `ARGV`," I’d
probably use
[OptionParser](https://crystal-lang.org/api/OptionParser.html). But all
I need is "grab the first item in `ARGV`."

**`list.cr`**

```crystal
# list information about a directory's contents
dirname = ARGV[0]

Dir.open(dirname) do |dir|
  dir.children.sort.each do |child|
    info = File.info "#{dirname}/#{child}"
    child += "/" if info.directory?
    puts "%-50s %10s %24s" % { child, info.size.format, info.modification_time }
  end
end
```

    $ crystal run list.cr -- ~/Sync/pictures/
    1/                                                      4,096  2019-10-18 15:28:30 UTC
    1999/                                                   4,096  2019-10-18 15:28:30 UTC
    2001/                                                   4,096  2019-10-18 15:28:30 UTC
    2007/                                                   4,096  2019-10-18 15:28:30 UTC
    2009/                                                   4,096  2019-10-18 15:28:30 UTC
    2010/                                                   4,096  2019-10-18 15:28:30 UTC
    2011/                                                   4,096  2019-10-18 15:28:30 UTC
    2012/                                                   4,096  2019-10-18 15:28:30 UTC
    2013/                                                   4,096  2019-10-18 15:28:30 UTC
    2014/                                                   4,096  2019-10-18 15:28:30 UTC
    2015/                                                   4,096  2019-10-18 15:28:30 UTC
    2016/                                                   4,096  2019-10-18 15:28:30 UTC
    2017/                                                   4,096  2019-10-18 15:28:30 UTC
    2018/                                                   4,096  2019-10-18 15:28:30 UTC
    digikam4.db                                         4,386,816  2019-02-17 15:58:19 UTC
    recognition.db                                      4,755,456  2019-02-17 15:58:19 UTC
    thumbnails-digikam.db                              197,328,896  2019-02-17 15:58:21 UTC

<aside class="admonition note">
  <p class="admonition-title">Note</p>

When using `crystal run` to execute a script, use `--` to split
arguments for `crystal` and those for your script. `list.cr` is for
Crystal. `~/Sync/pictures/` is for the script.

</aside>

This works, if you use it exactly right. Right now is where I’m tempted
to say "Error handling is left as an exercise for the reader." But no.
Not this time.

Let’s build this up so it handles common errors and concerns.

## Writing `list.cr`

There are a few things I want this program to do.

- Tell me if I forgot the argument.
- Tell me if the argument isn’t a real path.
- If the argument is a directory, summarize the contents of that
  directory.
- If the argument is a file, not a directory? Um — make a listing with
  one entry for the file.
- I really want to be a little more precise with the column sizes.

That covers the likeliest possibilities running this program on my own
computer. Besides, Crystal will let me know I forgot something.

I assembled this
[top-down](https://en.wikipedia.org/wiki/Top-down_and_bottom-up_design),
describing what I want to do and then describing how to do it. And even
though Crystal doesn’t require a main method, that seems like a good
place to start. If nothing else, it keeps the core logic in one place.

What does `main` do? It displays a `summary_table` of whatever I hand to
it. If anything goes wrong, it quits with a `fatal_error`.

``` crystal
main

# Print a brief file or directory summary specified via command line argument
def main()
  fatal_error("Missing FILENAME") if ARGV.size != 1

  begin
    puts summary_table ARGV[0]
  rescue ex
    fatal_error ex.message
  end
end
```

I don’t need to consider every possible error. But I should make sure
we’re polite about the errors we do encounter. Rescue any
[exceptions](https://crystal-lang.org/reference/syntax_and_semantics/exception_handling.html)
that occur and hand them to `fatal_error`.

`fatal_error` prints its `error` message and usage info to
[STDERR](https://crystal-lang.org/api/toplevel.html#STDERR).

``` crystal
# Quit with an error and usage info
def fatal_error(error)
  STDERR.puts error
  STDERR.puts "USAGE: #{PROGRAM_NAME} FILENAME"
  exit 1
end
```

That non-zero
[exit](https://crystal-lang.org/api/toplevel.html#exit\(status=0\):NoReturn-class-method)
tells the shell something went wrong. Handy for piped commands and
customized shell prompts that incorporate execution status.

The summary table glues together a collection of summary rows — even if
it’s just a collection of one — composed from file summaries and
formatted according to some basic guidelines about column size.

``` crystal
# Return a string description of a file or directory
def summary_table(filepath)
  summaries = dir_summaries(filepath) || { file_summary(filepath) }
  columns = column_sizes(summaries)

  summaries.map { |s| summary_row(s, columns) }.join("\n")
end
```

[Short-circuit
assignment](https://dev.to/walpolesj/short-circuit-assignment-25ik) uses
the
[or](https://crystal-lang.org/reference/syntax_and_semantics/or.html)
operator `||` to succintly set our summaries. We got a directory
summary? Use it. No? Okay, try treating it as a single file. Whichever
one returns a useful value first gets assigned to `summaries`.

Since we’re going top-down, we can say that a directory summary is a
sorted collection of files summaries and move on.

``` crystal
# Return a multiline description of a directory
def dir_summaries(dirname)
  return unless File.directory? dirname

  Dir.open(dirname) do |dir|
    dir.children.sort.map { |child| file_summary File.join(dirname, child) }
  end
end
```

Returning early for non-directories simplifies short-circuit assignment.
This method knows it may be handed a regular file. Stopping right away
prevents that from being treated the same as an error.

Oh *here’s* the work of summarizing. Build a name. Describe the size.
Turn the file’s modification time into something we can read.

Okay that’s not much work after all. Especially considering that I
already figured out how to describe size.

``` crystal
# Return a one-line description of a file
def file_summary(filename)
basename = File.basename filename
size = describe_size File.size filename
mod_time = File.info(filename).modification_time.to_local.to_s "%F %T"

basename += "/" if File.directory? filename

{ basename, size, mod_time }
end
```

That’s a lot of [method
chaining](https://en.wikipedia.org/wiki/Method_chaining). Method chains
are useful, but brittle. Temped to at least hide it in a new
describe\_time method. Oh well. Next time.

[the other day]: /post/2019/11/summarizing-a-file-with-crystal/

Yep. Turned that Proc from [the other day][] into a method.

``` crystal
# Return string description of byte size as bytes/KB/MB/GB
def describe_size(bytes)
  scales = { {1024**3, "GB"}, {1024**2, "MB"}, {1024, "KB"} }
  scale = scales.find { |i| bytes > i[0] }

  scale, term = if scale
                  { bytes / scale[0], scale[1] }
                else
                  { bytes, "bytes" }
                end

  return "#{scale.humanize} #{term}"
end
```

[Number\#humanize](https://crystal-lang.org/api/Number.html#humanize\(io:IO,precision=3,separator='.',delimiter=',',*,base=10**3,significant=true,prefixes:Indexable=SI_PREFIXES\):Nil-instance-method)

is a delightful convenience method for readable numbers. It adds commas
where expected. It trims floating point numbers to more digestible
precision. No word yet on whether it slices or dices.

`column_sizes` is dangerously close to clever — the bad kind of smart
where I’m likely to miss a mistake. The intent is reasonable enough.
Find how long each field is in each summary. Figure out which is the
longest value for each column. But there’s probably a more legible way
to do it.

``` crystal
# Return a list containing the size needed to fit each field.
def column_sizes(summaries)
  sizes = summaries.map { |field| field.map { |field| field.size } }
  (0..2).map { |i| sizes.max_of { |column| column[i] } }
end
```

Oh thank goodness. Back to fairly legible code with `summary_row`.
Although. Honestly? I’m being so specific with how each item in the
summary is treated. That calls out for a class, or at least a
[struct](https://crystal-lang.org/reference/syntax_and_semantics/structs.html).

Not enough time to rewrite the whole program, though. Sometimes it’s
more important to get to the next task than to get this one perfect.

``` crystal
# Return a one-line description of a file
def summary_row(summary, columns)
  path_column, size_column, mod_column = columns

  String.build do |str|
    str << summary[0].ljust(path_column) << " "
    str << summary[1].rjust(size_column) << " "
    str << summary[2].ljust(mod_column)
  end
end
```

Like most languages, Crystal’s
[String](https://crystal-lang.org/api/String.html) class has *many*
methods to make life easier.
[String\#ljust](https://crystal-lang.org/api/String.html#ljust\(len,char:Char=''\)-instance-method)
pads the end of a string.
[String\#rjust](https://crystal-lang.org/api/String.html#rjust\(len,char:Char=''\)-instance-method)
pads at the start, which is nice for number columns. Though my humanized
numbers do reduce the effectiveness of a numeric column.

That’s it? I’m done? Excellent!

Let’s build it and look at a random folder in my Sync archive.

    $ crystal build list.cr
    $ ./list ~/Sync/music-stuff/
    examine-iTunes.py 564 bytes 2019-02-17 07:58:19
    itunes.xml          29.8 MB 2019-02-17 07:58:19
    ratings.rb          1.02 KB 2019-02-17 07:58:19
    rhythmdb.xml        14.8 MB 2019-02-17 07:58:19

Oh hey. Stuff from a couple old [music management](/tags/music) posts.
Getting back to those is on the task list. I’ll get there.

Anyways. My `list` program works!

I learned a fair bit about managing collections in Crystal. Also, the
"small methods" approach that served me well in Ruby seems just as handy
here.

## Yeah, I know

If file information was all I needed, I could get the same details and
more with
[ls](https://www.gnu.org/software/coreutils/manual/html_node/ls-invocation.html#ls-invocation).

    $ ls -gGhp ~/Sync/pictures/
    total 197M
    drwxr-xr-x  3 4.0K Oct 18 08:28 1/
    drwxr-xr-x  7 4.0K Oct 18 08:28 1999/
    drwxr-xr-x  3 4.0K Oct 18 08:28 2001/
    drwxr-xr-x  8 4.0K Oct 18 08:28 2007/
    drwxr-xr-x  8 4.0K Oct 18 08:28 2009/
    drwxr-xr-x  5 4.0K Oct 18 08:28 2010/
    drwxr-xr-x  5 4.0K Oct 18 08:28 2011/
    drwxr-xr-x  8 4.0K Oct 18 08:28 2012/
    drwxr-xr-x 14 4.0K Oct 18 08:28 2013/
    drwxr-xr-x 14 4.0K Oct 18 08:28 2014/
    drwxr-xr-x 14 4.0K Oct 18 08:28 2015/
    drwxr-xr-x 13 4.0K Oct 18 08:28 2016/
    drwxr-xr-x 12 4.0K Oct 18 08:28 2017/
    drwxr-xr-x 11 4.0K Oct 18 08:28 2018/
    -rw-r--r--  1 4.2M Feb 17  2019 digikam4.db
    -rw-r--r--  1 4.6M Feb 17  2019 recognition.db
    -rw-r--r--  1 189M Feb 17  2019 thumbnails-digikam.db

But I wouldn’t have learned anything about Crystal. I wouldn’t have had
nearly as much fun, either. And — not counting other concerns like
"paying rent" or "eating" — fun is the most important part!