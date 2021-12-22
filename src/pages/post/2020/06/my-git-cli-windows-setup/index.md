---
category: tools
date: 2020-06-19 05:55:00
description: This was mostly an excuse to get better with PowerShell
draft: false
format: md
layout: layout:PublishedArticle
slug: my-git-cli-windows-setup
tags:
- windows
- git
- PowerShell
title: My Git CLI Windows setup
uuid: 06ae2b51-6005-444e-a17d-7d21e7ae1f8a
---

For the sake of continuous learning — and so I could use a couple work-related
applications that don’t work even with [WINE][wine] — I decided to spend more
time in Windows.  Let’s see if I can comfortably use [Git][git] from
[PowerShell][powershell].  I’ll use the [OpenSSH for Windows][openssh-windows]
server for key management, since it’s already available on my system.

## Setting up Git

[winget][] knows about several Git-related packages, so my installation command
needs to be specific.

``` powershell
winget install –exact Git.Git
```

The installation puts Git’s `cmd` folder onto `$env:Path`, but PowerShell
won’t see that until I refresh the variable.

``` powershell
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
```

And there it is!

``` text
PS > $env:path -split ";"
C:\Windows\system32
⋮
C:\Program Files\Git\cmd
```

I need to start a new session eventually, though.  Can’t go around refreshing
my path like that every time I open a new terminal.  Though I suppose I could
put this in PowerShell initialization.

:::note

I know Git Bash is a thing, but I’m trying to learn Windows — not just paste a
comforting layer of UNIX duct tape over everything.  *Said while writing a blog
post from Vim on WSL 2.*

:::

*Anyways*, it looks like ``ssh-keygen`` is accessible via PowerShell.

``` text
PS > ssh-keygen -t rsa -b 4096 -C "brianwisti@pobox.com"
Generating public/private rsa key pair.
Enter file in which to save the key (C:\Users\brian/.ssh/id_rsa):
```

I add an SSH key with the details from `C:/Users/brian/.ssh/id_rsa.pub`, and
check out a repo.

``` text
PS > git clone ssh://git@git.hackers.town:2222/randomgeek/random-geekery-blog.git
Cloning into 'random-geekery-blog'...
```

That was easy enough.  There are a couple bits missing from my regular Git day,
though.

## Conveniences with posh-git

For starters, I enjoy a pretty shell prompt with version control details.
Let’s install the [beta release][beta-release] of [posh-git][].

``` powershell
Install-Module posh-git -Scope CurrentUser -AllowPrerelease -Force
```

``` text
PS C:\Users\brian\Projects\random-geekery-blog> Import-Module posh-git

~\Projects\random-geekery-blog [trunk ≡]>
```

Lovely! I can customize it later.

## Getting an SSH agent with posh-sshell

I dislike entering my ssh passphrase every time I interact with a version
control server.  Need to get some sort of `ssh-agent` working.

Looks like [posh-sshell][] can help with that?

``` powershell
Install-Module posh-sshell -Scope CurrentUser
Get-Service -Name ssh-agent | Set-Service -StartupType Manual
```

Of course, I should probably enable the ``ssh-agent`` service from an Admin
PowerShell session:

I don’t know why "Manual." That’s what this [Stackoverflow
answer][stackoverflow-answer] said, and it seems to be working.

Over in my PowerShell init, I make sure the new modules are loaded, set some
handy aliases for using my SSH keys, and start the SSH Agent.

**`Documents\PowerShell\profile.ps1`**

```powershell
Import-Module posh-git Import-Module posh-sshell

Set-Alias ssh-agent "$env:WinDir\System32\OpenSSH\ssh-agent.exe"
Set-Alias ssh-add "$env:WinDir\System32\OpenSSH\ssh-add.exe"

Start-SshAgent -Quiet
```

Knowing me I’ll eventually generate this from my [orgconfig][].

After starting a new session, everything seems successful.

``` text
~\Projects> ssh-add
~\Projects> git clone git@github.com:brianwisti/dotfiles.git
Cloning into 'dotfiles'...
The authenticity of host 'github.com (140.82.112.4)' can't be established.
RSA key fingerprint is SHA256:nThbg6kXUpJWGl7E1IGOCspRomTxdCARLviKw6E5SY8.
Are you sure you want to continue connecting (yes/no)?
Warning: Permanently added 'github.com,140.82.112.4' (RSA) to the list of known hosts.
warning: agent returned different signature type ssh-rsa (expected rsa-sha2-512)
remote: Enumerating objects: 405, done.
remote: Counting objects: 100% (405/405), done.
remote: Compressing objects: 100% (228/228), done.
remote: Total 1083 (delta 272), reused 299 (delta 172), pack-reused 678 receiving objects:  92% (997/1083)
Receiving objects: 100% (1083/1083), 743.31 KiB | 1.83 MiB/s, done.
Resolving deltas: 100% (571/571), done.
```

Did you see this bit?

``` text
Warning: Permanently added 'github.com,140.82.112.4' (RSA) to the list of known hosts.
warning: agent returned different signature type ssh-rsa (expected rsa-sha2-512)
```

That warning is a [known issue][known-issue] with OpenSSH on Windows, and
should go away in the next month or two. The bad news: until it’s fixed,
different repository servers handle the mismatch differently. What I noticed
while working through the process that became this post:

- Github issued the warning but let me continue
- A server running Gitea issued the warning and would *not* let me continue

This is significant enough to highlight:

:::warning

If you’re using the Windows OpenSSH server before the 2020 Fall Update, you
may want to skip the `ssh-agent` bits.

:::

But other than that, things are working pretty good. Learning is fun!

[wine]: https://winehq.org
[git]: https://git-scm.com/
[powershell]: https://docs.microsoft.com/en-us/powershell/
[openssh-windows]: https://docs.microsoft.com/en-us/windows-server/administration/openssh/openssh_install_firstuse
[winget]: https://docs.microsoft.com/en-us/windows/package-manager/winget/
[beta-release]: https://github.com/dahlbyk/posh-git
[posh-git]: https://www.powershellgallery.com/packages/posh-git/
[posh-sshell]: https://www.powershellgallery.com/packages/posh-sshell/0.3.1
[stackoverflow-answer]: https://stackoverflow.com/a/53606760
[orgconfig]: /config
[known-issue]: https://github.com/PowerShell/Win32-OpenSSH/issues/1551