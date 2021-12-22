---
aliases:
- /2019/11/17/summarizing-a-file-with-crystal/
category: Programming
cover_image: cover.png
date: 2019-11-17
description: Been busy, but let's take a minute to summarize a file's details with
  [Crystal](https://crystal-lang.org/)
draft: false
layout: layout:PublishedArticle
slug: summarizing-a-file-with-crystal
tags:
- crystal
- files
title: Summarizing A File With Crystal
updated: 2019-11-24 16:31:33
uuid: 5d3045fe-1d5d-46b8-b333-b7ec8c74e828
---

Okay, I don’t have a lot of time here. We’re on a tight schedule. But
hey tests are running so I’ll write a tiny bit of
[Crystal](/tags/crystal).

How would I print a quick summary of a file? Besides
[`ls`](http://www.man7.org/linux/man-pages/man1/ls.1.html), of course. I
mean how would I print a quick summary of a file using Crystal?

``` crystal
filename = "#{ENV["HOME"]}/Dropbox/Camera Uploads/2019-11-13 08.11.12.png"
puts `ls -l #{filename}`
```

    -rw-r--r-- 1 randomgeek randomgeek 3346960 Nov 13 08:11 /home/randomgeek/Dropbox/Camera Uploads/2019-11-13 08.11.12.png

We already looked at [Crystal as a glue
language](/post/2019/08/trying-the-crystal-language/). No, I’m wondering
more about how I would get this information using Crystal’s [standard
library](https://crystal-lang.org/api/).

Turns out I can get the same information with
[`File::Info`](https://crystal-lang.org/api/File/Info.html).

``` crystal
puts File.info "#{ENV["HOME"]}/Dropbox/Camera Uploads/2019-11-13 08.11.12.png"
```

    Crystal::System::FileInfo(@stat=LibC::Stat(@st_dev=2051, @st_ino=6983901, \
      @st_nlink=1, @st_mode=33188, @st_uid=1000, @st_gid=1000, @__pad0=0,     \
      @st_rdev=0, @st_size=3346960, @st_blksize=4096, @st_blocks=6552,        \
      @st_atim=LibC::Timespec(@tv_sec=1573661608, @tv_nsec=641856438),        \
      @st_mtim=LibC::Timespec(@tv_sec=1573661472, @tv_nsec=0),                \
      @st_ctim=LibC::Timespec(@tv_sec=1573661609, @tv_nsec=941857986),        \
      @__glibc_reserved=StaticArray[0, 0, 0]))

This is both more and less information than I was hoping for. Clearly
whoever wrote `to_s` for `File::Info` figured the main time you would
need to directly print the object is when you were debugging.

That makes sense, and they provide methods to get at the information I
care about most.

``` crystal
# Returns a multiline string summary of a single file
def describe_file(filename)
    info = File.info(filename)

    size = ->(bytes : UInt64) {
      scales = { {1024**3, "GB"}, {1024**2, "MB"}, {1024, "KB"} }
      scale = scales.find { |i| bytes > i[0] }

      scale.nil? ? "#{bytes} bytes" : "%.2f %s" % [bytes / scale[0], scale[1]]
    }.call(info.size)

    String.build do |str|
      str << "Filename: #{filename}\n"
      str << "Size:     #{size}\n"
      str << "Modified: #{info.modification_time}\n"
    end
end

filename = "#{ENV["HOME"]}/Dropbox/Camera Uploads/2019-11-13 08.11.12.png"
puts describe_file filename
```

    Filename: /home/randomgeek/Dropbox/Camera Uploads/2019-11-13 08.11.12.png
    Size:     3.19 MB
    Modified: 2019-11-13 16:11:12 UTC

I grabbed the logic from [Weighing Files With
Python](/post/2019/06/weighing-files-with-python/) to get a description
of the size in kilobytes, megabytes, or gigabytes. That is easier for my
brain to understand than the
[`UInt64`](https://crystal-lang.org/api/UInt64.html) integer byte count
provided by
[`File::Info.size`](https://crystal-lang.org/api/File/Info.html#size:UInt64-instance-method).

Yes, the whole thing is more clever than the situation requires, but I
*am* trying to learn the language here. Using a
[`Proc`](https://crystal-lang.org/api/Proc.html) was one way to
basically copy and paste the logic from my earlier post and reformat for
Crystal. Sure, I could have — and probably should have — defined a new,
separate method. At the same time, Procs are great to show that there’s
this bit of behavior you want to encapsulate, but you don’t plan to use
anywhere else.

But really it was just a bit of late night silliness so I could see
Crystal Procs in action. Silliness for the sake of learning is okay.

And what did I learn?

- [`File::Info`](https://crystal-lang.org/api/File/Info.html) gives me
  what I want for file summaries.
- Crystal supports [Tuples](https://crystal-lang.org/api/Tuple.html):
  special immutable lists that can be more efficient than a full
  [`Array`](https://crystal-lang.org/api/Array.html)
- [`String.build`](https://crystal-lang.org/api/String.html#build\(capacity=64,&block\):self-class-method)
  is a nice-looking way to make multiline strings without heredocs or
  `+=`. Apparently there are [performance
  reasons](https://crystal-lang.org/reference/guides/performance.html)
  to use it too, but I’ll never see them in this short program. Same
  with Tuples really, but the type you specify can tell people what
  your intentions are.
- [`Proc`](https://crystal-lang.org/api/Proc.html) argument types must
  be specified. That must mean the compiler treats them differently
  than normal methods.

Hang on. I’m curious to explore that last one. Procs are treated
differently. Are they faster?

``` crystal
require "benchmark"

filename = "#{ENV["HOME"]}/Dropbox/Camera Uploads/2019-11-13 08.11.12.png"
bytes = File.info(filename).size

def describe_size(bytes)
  scales = { {1024**3, "GB"}, {1024**2, "MB"}, {1024, "KB"} }
  scale = scales.find { |i| bytes > i[0] }

  scale.nil? ? "#{bytes} bytes" : "%.2f %s" % [bytes / scale[0], scale[1]]
end

size_proc = ->(bytes : UInt64) {
  scales = { {1024**3, "GB"}, {1024**2, "MB"}, {1024, "KB"} }
  scale = scales.find { |i| bytes > i[0] }

  scale.nil? ? "#{bytes} bytes" : "%.2f %s" % [bytes / scale[0], scale[1]]
}


Benchmark.ips do |benchmark|
  benchmark.report("using method") do
    size = describe_size(bytes)
  end

  benchmark.report("using proc") do
    size = size_proc.call(bytes)
  end
end
```

    $ crystal run --release proc_vs_def.cr
    using method   2.20M (455.45ns) (± 6.08%)  352B/op        fastest
      using proc   2.18M (458.85ns) (± 5.46%)  352B/op   1.01× slower

The method is almost three whole nanoseconds faster than the Proc. I
wonder…

    $ crystal run --release proc_vs_def.cr
    using method   2.15M (465.37ns) (± 5.93%)  352B/op   1.01× slower
    using proc   2.16M (462.10ns) (± 6.04%)  352B/op        fastest

Yeah, that’s what I thought. For this case at least, local environment
variations — did Spotify just hit a new track? — will have a bigger
impact than whether I choose a Proc or a method.

Okay, tests are done. Everything passed, yay\! Back to it. Maybe back to
the drawing, actually.
