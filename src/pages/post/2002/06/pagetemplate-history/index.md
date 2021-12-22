---
aliases:
- /coolnamehere/2002/06/02_pagetemplate-history.html
- /post/2002/pagetemplate-history/
- /2002/06/02/pagetemplate-history/
category: coolnamehere
date: 2002-06-02 00:00:00
layout: layout:PublishedArticle
slug: pagetemplate-history
tags:
- pagetemplate
title: PageTemplate History
updated: 2009-07-11 00:00:00
uuid: 45d95874-afcd-47c6-be0a-3f73df9e14e7
---

I’ll admit it. This list is very bad. Nevertheless, I keep telling
myself it’s better than nothing.

  - Version 1.0
      - Basic logic structure (var, if, and in)
      - Support for multiple Namespaces
  - Version 1.1
      - include content from external files
  - Version 1.2
      - New Command: unless
      - Added support for CommentCommands
      - Loop Metavariables: `FIRST`, `LAST`, `ODD`
      - include\_path can be a list of paths
      - Loosened rules for VariableCommands (check respond\_to? rather
        than has\_method?)
      - Lessened penalty for missing files in IncludeCommands (returns
        an error string rather than raising an exception)
      - Strengthened the system for running in tainted environments.
  - Version 2.0
      - Added Preprocessors
          - `[%var sampleCode :escapeHTML %]`
      - Added a CaseCommand
      - Better access of object fields and subfields
  - Version 2.1
      - LoopCommands can accept multiple iterators now
      - Added else if functionality
      - New Glossary allows HTML::Template-style syntax.
  - Version 2.1.1
      - In-memory caching
  - Version 2.1.5
      - Improvements on working with mod\_ruby
  - Version 2.1.7
      - Added Namespace\#delete method
  - Version 2.2.0
      - DefineCommand
      - FilterCommand
      - Fixed bug in FileSource\#get\_filename