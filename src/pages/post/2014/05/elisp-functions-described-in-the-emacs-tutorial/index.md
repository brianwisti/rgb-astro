---
aliases:
- /emacs/2014/05/27_elisp-functions-described-in-the-emacs-tutorial.html
- /post/2014/elisp-functions-described-in-the-emacs-tutorial/
- /2014/05/27/elisp-functions-described-in-the-emacs-tutorial/
category: tools
date: 2014-05-27 00:00:00
layout: layout:PublishedArticle
slug: elisp-functions-described-in-the-emacs-tutorial
tags:
- emacs
- elisp
- tutorial
title: Elisp Functions Described in the Emacs Tutorial
uuid: 772fe617-fda6-4b86-bc92-509632ce2953
---

[other day]: /post/2014/05/the-emacs-tutorial-as-elisp-tour

The [other day][] I talked some sort of nonsense about organizing my
notes into some sort of coherent blog post. Heck with that. Life is
too short. Instead I will just dump them here and hope somebody
finds them useful. Maybe later I can do something with it. For now
it's just supplemental material for the official Emacs tutorial
<!--more-->

## Functions in the Emacs Tutorial

Function                     | Keybinding           | Description                                                      
-----------------------------|----------------------|------------------------------------------------------------------
`save-buffers-kill-terminal` | `C-x C-c`            | Save and quit Emacs                                              
`keyboard-quit`              | `C-g`                | Cancels entry of a command                                       
`scroll-up-command`          | `C-v`                | Scroll content up                                                
`scroll-down-command`        | `M-v`                | Scroll cowntent down                                             
`recenter-top-bottom`        | `C-l`                | Redraw window cycling point through center/top/bottom of window  
`previous-line`              | `C-p`                | Put point on previous line                                       
`next-line`                  | `C-n`                | Put point on next line                                           
`backward-char`              | `C-b`                | Put point on previous character                                  
`forward-char`               | `C-f`                | Put point on next character                                      
`forward-word`               | `M-f`                | Put point on next word                                           
`backward-word`              | `M-b`                | Put point on previous word                                       
`move-beginning-of-line`     | `C-a`                | Put point on line start                                          
`move-end-of-line`           | `C-e`                | Put point on line end                                            
`backward-sentence`          | `M-a`                | Put point on previous sentence start                             
`forward-sentence`           | `M-e`                | Put point on next sentence start                                 
`beginning-of-buffer`        | `M-<`                | Put point on buffer start                                        
`end-of-buffer`              | `M->`                | Put point on buffer end                                          
`universal-argument`         | `C-u`                | Begin a numeric argument for the following command               
`delete-other-windows`       | `C-x 1`              | Make window fill its frame                                       
`self-insert-command`        | `<character>`        | Inserts the character you type                                   
`newline`                    | `RETURN`             | Insert a newline & move point to next line                       
`delete-backward-char`       | `DEL`                | Delete characters before point                                   
`delete-char`                | `C-d`                | Delete characters after point                                    
`backward-kill-word`         | `M-DEL`              | Delete word before point                                         
`kill-word`                  | `M-d`                | Delete word after point                                          
`kill-line`                  | `C-k`                | Kill from point to end of line                                   
`kill-sentence`              | `M-k`                | Kill from point to end of sentence                               
`set-mark-command`           | `C-SPACE`            | Start marking a region for later action                          
`kill-region`                | `C-w`                | Cut text in marked region                                        
`yank`                       | `C-y`                | Yank (paste) text at point                                       
`yank-pop`                   | `M-y`                | cycle through kill ring w/last yank                              
`undo`                       | `C-/`                | Undo last command                                                
`find-file`                  | `C-x C-f`            | Prompt in minibuffer to open a file in buffer                    
`save-buffer`                | `C-x C-s`            | Save buffer contents to file                                     
`list-buffers`               | `C-x C-b`            | Display a list of existing buffers                               
`switch-to-buffer`           | `C-x b`              | Minibuffer prompt switch window view to different buffer         
`save-some-buffers`          | `C-x s`              | Prompt to save each changed buffer                               
`suspend-frame`              | `C-z` or `C-x C-z`   | exit Emacs temporarily                                           
`replace-string`             | `M-x replace-string` | minibuffer - replace instances of a string in buffer after point 
`recover-file`               | `M-x recover-file`   | Revisit buffer using last auto-saved contents                    
`text-mode`                  | `M-x text-mode`      | Major mode for editing text for humans to read                   
`describe-mode`              | `C-h m`              | Show documentation for current major and minor modes             
`auto-fill-mode`             | `M-x auto-fill-mode` | Toggle automatic line breaking                                   
`fill-paragraph`             | `M-q`                | Fill paragraph at / after point.                                 
`isearch-forward`            | `C-s`                | minibuffer - Do incremental search forward                       
`isearch-backward`           | `C-r`                | minibuffer - Do incremental search backward                      
`split-window-below`         | `C-x 2`              | Split selected window horizontally. Selected window becomes top  
`scroll-other-window`        | `C-M-v`              | Scroll next window                                               
`other-window`               | `C-x o`              | Select next window in cyclic window order                        
`delete-other-windows`       | `C-x 1`              | Make selected window fill its frame                              
`find-file-other-window`     | `C-x 4 C-f`          | Edit file in other window                                        
`make-frame`                 | `C-x 5 2`            | Return newly created frame displaying current buffer             
`delete-frame`               | `C-x 5 0`            | Delete selected frame                                            
`help-for-help`              | `C-h ?`              | Launches interactive help mode                                   
`describe-key-briefly`       | `C-h c <key>`        | Prints name of function invoked by `<key>`                       
`describe-key`               | `C-h k <key>`        | Display documentation of function invoked by `<key>`             
`describe-function`          | `C-h f <function>`   | Display documentation of `<function>`                            
`describe-variable`          | `C-h v <variable>`   | Display documentation of `<variable>`                            
`apropos-command`            | `C-h a <pattern>`    | Show all commands with names containing `<pattern>`              
`info`                       | `C-h i`              | Enter the Info documentation browser                             
`info-emacs-manual`          | `C-h r`              | Display the Emacs manual in Info mode                            

## Notes

 I found some things noteworthy while building this list. 

### Numeric Arguments

- Digits or minus sign after `C-u` form the numeric argument. 
- Default is `4`
- Usually treated as numeric argument
- Sometimes it's just a flag. The following command changes
  behavior based on the presence of `universal-argument` rather
  than the details of its value

| `C-u 8 C-f` | Move forward 8 characters |
| `C-u C-f`   | Move forward 4 characters |
| `C-u 2 C-v` | Scroll screen 2 lines     |

### Disabled Commands

Some commands such as `downcase-region` `C-x C-l` are disabled by
default in Emacs. They confuse beginners. You get an interactive
prompt to try it, enable it, and whatever.

[DisabledCommands]: http://www.emacswiki.org/emacs/DisabledCommands

There's no big list of disabled commands. Instead each command
has a hook telling whether it's disabled or not. The EmacsWiki
[DisabledCommands][] page presents functions to list and enable
disabled functions.

### Inserting and Deleting

*Everything* you type invokes a function. Most of the
alphanumeric keys simply insert the character and move
point. Some, like =newline= and =delete-backward-character=,
trigger functions that relate to behavior users expect when
entering those keys.

They take numeric arguments too. `C-u 4 *` will insert `****`
into the buffer.

### Undo

Undo ignores movement commands, and `self-insert-command` are
lumped into groups of up to 20.

### Extending the Command Set

There are only so many keys on the average keyboard. Less common
commands get invoked either through an extended keybinding like
`C-x <character>` or direct invocation via `M-x <name>`.

+ `C-x <character>` Character eXtend
+ `M-x <name>` Named command eXtend
  + Offers tab completion

### Searching

Incremental search is like a minibuffer mode. There are special
bindings for the keys and everything.

### Multiple Frames

*Frames* are what what most windowing systems refer to as
*windows*, but Emacs was already using that term.

Frames only work in GUI, because the terminal can only display a
single frame at a time. See /elscreen/ for an alternative that
works in both terminal and GUI.