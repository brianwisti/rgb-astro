---
draft: true
layout: layout:Article
tags:
- files
- python
title: Indexing my files with Python
uuid: 4cd4b2ba-d6eb-479b-9fe2-e12b2f7ff647
---

I have an awful lot of files in cloud storage (Dropbox, OneDrive, and more). I probably have a lot of duplicated files in that cloud storage. Well. I know I have a lot of duplicated files. I'm looking right at them.

But I can't organize my files by looking at them one at a time. Besides, duplication is only part of the problem. There are also many near-duplicates. Draft, second, and 5th editions of books. Burst shots of single subjects, from those times that needed exactly the right picture of a flower. At some point I need to decide which of those similar files I want to keep.

And there's the ones that look like duplicates but aren't really, like the song that shows up in its album, a best of compilation, a label compilation, and oh yeah three or four soundtracks.

And I keep adding more files. But if I do this work on my Windows partition, I've got a little time before my local hard drive fills up and I have to start getting my answers through API calls to cloud storage providers.

Before I get into the weeds of every specific file and what to do with it, I want a high level idea of the landscape.


## What do I want to know?

-   How many files do I have in cloud storage?
-   How much space do they all take up on my hard drive?
-   How many types of files do I have in cloud storage?
    -   How many files of each type?
    -   How much space does each type take up?
-   How many unique files do I have in cloud storage?
    -   How many unique files of each type?


## The easy answers: file count and space occupied

```python
    """Gather and display a summary of files found in my main storage folders."""

    import os
    from typing import List

    HOME = os.environ["HOME"]
    ROOT_DIRS = (
        os.path.join(HOME, "Dropbox"),
        os.path.join(HOME, "OneDrive"),
    )


    def summarize_files(root_dirs: List[str]) -> None:
        file_count = 0
        file_size = 0

        for directory in root_dirs:

            print(f"Indexing {directory}...")
            for root, _, files in os.walk(directory):
                for filename in files:
                    file_count += 1
                    full_path = os.path.join(root, filename)

                    try:
                        file_size += os.path.getsize(full_path)
                    except FileNotFoundError:
                        long_windows_path = "\\\\?\\" + full_path
                        file_size += os.path.getsize(long_windows_path)

        print("Done!")
        print(f"{file_count=:,}")
        print(f"{file_size=:,}")


    if __name__ == "__main__":
        summarize_files(ROOT_DIRS)
```

Around 253GB spread across close to 63,000 files. Yeah I don't want to organize that by hand.

<aside class="admonition note">
<p class="admonition-title">Note</p>

Windows / Linux hybrid folks, don't do this in WSL.

```
$ time python index_files.py
...
real    3m50.577s
user    0m6.733s
sys     0m37.685s
```

```
PS C:\Users\brian\Projects> Measure-Command { python .\index_files.py | Out-Default  }
...
Days              : 0
Hours             : 0
Minutes           : 0
Seconds           : 7
Milliseconds      : 396
Ticks             : 73964807
TotalDays         : 8.56074155092593E-05
TotalHours        : 0.00205457797222222
TotalMinutes      : 0.123274678333333
TotalSeconds      : 7.3964807
TotalMilliseconds : 7396.4807
```

</aside>

## What kinds of files?

It might be a little easier for me to sort things out if I know the landscape. I can learn this landscape by answering the questions about file types.

-   How many types of files do I have?
-   How many files of each type do I have?
-   How much space does each type of file take up?

Mind you, I only care about files in a couple specific locations: my Dropbox and OneDrive folders.

```python
    HOME = os.environ["HOME"]
    ROOT_DIRS = (
        os.path.join(HOME, "Dropbox"),
        os.path.join(HOME, "OneDrive"),
    )
```

It's worth putting the details I want in a distinct type.

```python
    FileSummary = namedtuple("FileSummary", ["full_path", "size", "file_type"])
```

That way I can wrap my head around summarizing it beter.

```python
    def get_file_summary(full_path: str) -> FileSummary:
        """Return a file's interesting details."""

        # Python gets confused about long filenames on Windows sometimes.
        if sys.platform == "win32" and not os.path.exists(full_path):
            full_path = f"\\\\?\\{full_path}"

        file_size = os.path.getsize(full_path)
        file_type, _ = mimetypes.guess_type(full_path)

        return FileSummary(full_path, file_size, file_type)
```

I'm okay with getting an exception if the system _still_ can't find the file. The traceback can help me figure out the problem.

```python

    Tally = Dict[str, int]
    TypeTally = Dict[str, Tally]

    @dataclass
    class SummaryTracker:
        total_count: int = 0
        total_size: int = 0
        file_types: TypeTally = field(default_factory=dict)

        def track_summary(self, file_summary: FileSummary) -> None:
            self.total_count += 1
            self.total_size += file_summary.size
            file_type = file_summary.file_type

            if file_type not in self.file_types:
                self.file_types[file_type] = {
                    "count": 0,
                    "size": 0,
                }

            self.file_types[file_type]["count"] += 1
            self.file_types[file_type]["size"] += file_summary.size

        def numeric(self, n: int) -> str:
            return f"{n:,}"

        def show(self) -> None:
            table = Table(title="File Summary")
            table.add_column("Description")
            table.add_column("Count", justify="right")
            table.add_column("Size", justify="right")

            table.add_row("Total", self.numeric(self.total_count), self.numeric(self.total_size))

            for file_type, tally in self.file_types.items():
                table.add_row(file_type, self.numeric(tally["count"]), self.numeric(tally["size"]))

            console = Console()
            console.print(table)
```

```python
    """Display a summary of files found in my main storage folders."""

    from collections import namedtuple
    from dataclasses import dataclass, field
    import mimetypes
    import os
    import sys
    from typing import Dict, List

    from rich.console import Console
    from rich.table import Table

        HOME = os.environ["HOME"]
        ROOT_DIRS = (
            os.path.join(HOME, "Dropbox"),
            os.path.join(HOME, "OneDrive"),
        )

        FileSummary = namedtuple("FileSummary", ["full_path", "size", "file_type"])

        def get_file_summary(full_path: str) -> FileSummary:
            """Return a file's interesting details."""

            # Python gets confused about long filenames on Windows sometimes.
            if sys.platform == "win32" and not os.path.exists(full_path):
                full_path = f"\\\\?\\{full_path}"

            file_size = os.path.getsize(full_path)
            file_type, _ = mimetypes.guess_type(full_path)

            return FileSummary(full_path, file_size, file_type)


        Tally = Dict[str, int]
        TypeTally = Dict[str, Tally]

        @dataclass
        class SummaryTracker:
            total_count: int = 0
            total_size: int = 0
            file_types: TypeTally = field(default_factory=dict)

            def track_summary(self, file_summary: FileSummary) -> None:
                self.total_count += 1
                self.total_size += file_summary.size
                file_type = file_summary.file_type

                if file_type not in self.file_types:
                    self.file_types[file_type] = {
                        "count": 0,
                        "size": 0,
                    }

                self.file_types[file_type]["count"] += 1
                self.file_types[file_type]["size"] += file_summary.size

            def numeric(self, n: int) -> str:
                return f"{n:,}"

            def show(self) -> None:
                table = Table(title="File Summary")
                table.add_column("Description")
                table.add_column("Count", justify="right")
                table.add_column("Size", justify="right")

                table.add_row("Total", self.numeric(self.total_count), self.numeric(self.total_size))

                for file_type, tally in self.file_types.items():
                    table.add_row(file_type, self.numeric(tally["count"]), self.numeric(tally["size"]))

                console = Console()
                console.print(table)

    def summarize_files(root_dirs: List[str]) -> None:
        tracker = SummaryTracker()

        for directory in root_dirs:

            print(f"Indexing {directory}...")
            for root, _, files in os.walk(directory):
                for filename in files:
                    full_path = os.path.join(root, filename)
                    file_summary = get_file_summary(full_path)
                    tracker.track_summary(file_summary)

        print("Done!")
        tracker.show()

    if __name__ == "__main__":
        summarize_files(ROOT_DIRS)
```


## How many unique files?

This is

```python
    """Gather and display a summary of files found in my main storage folders."""

    import hashlib
    import os
    from typing import List

    HOME = os.environ["HOME"]
    ROOT_DIRS = (
        os.path.join(HOME, "Dropbox"),
        os.path.join(HOME, "OneDrive"),
    )


    def calculate_checksum(filepath: str) -> str:
        """Return the md5 hexdigest for the named file."""
        md5 = hashlib.md5()

        with open(filepath, "rb") as f:
            md5.update(f.read())

        return md5.hexdigest()

    def summarize_files(root_dirs: List[str]) -> None:
        file_count = 0
        file_size = 0
        checksums = set()

        for directory in root_dirs:

            print(f"Indexing {directory}...")
            for root, _, files in os.walk(directory):
                for filename in files:
                    file_count += 1
                    full_path = os.path.join(root, filename)

                    if not os.path.exists(full_path):
                        # Windows does long filenames, but not without a little work in Python.
                        full_path = "\\\\?\\" + full_path

                    file_size += os.path.getsize(full_path)

                    try:
                        checksums.add(calculate_checksum(full_path))
                    except PermissionError:
                        print(f"Cannot read {full_path} for unique signature; moving on")

        print("Done!")
        unique_files = len(checksums)
        print(f"{file_count=:,}")
        print(f"{file_size=:,}")
        print(f"{unique_files=:.}")


    if __name__ == "__main__":
        summarize_files(ROOT_DIRS)
```


## Building on what we've got

-   total file count <= 0
-   total file size <= 0
-   file types <= empty dictionary
-   For each storage root in (Dropbox, OneDrive, Sync?)
    -   Walk that directory
    -   For each file found:
        -   file size <= get from file stats
        -   file type <= mimetype of file
        -   total file count <= total file count + 1
        -   total file space <= total file size + file size
        -   if file type not in file types
            -   file type sumary <= dictionary:
                -   file count <= 0
                -   file size <= 0


## Okay, _now_ the bit about unique files

-   How many unique files do I have?
-   How many unique files do I have for each type?


## Make it pretty

```python
    from rich.console import Console
    from rich.table import Table

    # pip install rich
    # pip install pygments commonmark rich
    def display_summaries(summaries: List[DirSummary]) -> None:
        table = Table(title="File Indexing Summary")
        table.add_column("Description")
        table.add_column("Count")
        table.add_column("Size")

        for summary in summaries:
            table.add_row(
                summary.description,
                f"{summary.file_count:,}",
                f"{summary.file_size:,}",
            )

        console = Console()
        console.print(table)
```


## Can I make that faster?

... show time of process

-   I was using normal sane linear Python. What if I used `asyncio`?
-   I was using Python. What if I used Nim, a compiled and statically typed language that looks a bit like Python?
