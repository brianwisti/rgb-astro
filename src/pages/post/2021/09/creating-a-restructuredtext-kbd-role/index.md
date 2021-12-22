---
category: programming
date: 2021-09-23
description: But first a couple others as I figure this out
draft: false
format: rst
layout: layout:PublishedArticle
tags:
- rst
- python
title: Creating a reStructuredText kbd Role
---

<div class="contents topic" id="contents">
<p class="topic-title">Contents</p>
<ul class="simple">
<li><a class="reference internal" href="#what-even-is-a-role" id="id1">What even is a role?</a></li>
<li><a class="reference internal" href="#inline-roles-in-your-document" id="id2">Inline roles in your document</a></li>
<li><a class="reference internal" href="#defining-roles-in-your-code" id="id3">Defining roles in your code</a><ul>
<li><a class="reference internal" href="#tag-references" id="id4"><tt class="docutils literal">:tag:</tt> references</a></li>
<li><a class="reference internal" href="#a-kbd-role" id="id5">A <tt class="docutils literal">:kbd:</tt> role</a></li>
<li><a class="reference internal" href="#there-s-a-perfectly-good-kbd-element" id="id6">There's a perfectly good <tt class="docutils literal">&lt;kbd&gt;</tt> element</a></li>
</ul>
</li>
<li><a class="reference internal" href="#wrap-it-up" id="id7">Wrap it up</a></li>
</ul>
</div>
<p>Today's the day I learn how to create custom roles in <a class="p-category reference external" href="/tags/rst">#rst</a>. There's
already <a class="reference external" href="https://docutils.sourceforge.io/docs/howto/rst-roles.html">documentation</a> on how to do this. I'm just applying it for my
specific case.</p>
<div class="topic">
<p class="topic-title">Setup</p>
<p>Install some stuff if you want to play along.</p>
<pre class="code console literal-block">
<span class="generic prompt">$ </span>pip install -U docutils invoke
</pre>
<p>Some of the requirements are specific to my writing flow.</p>
<pre class="code console literal-block">
<span class="generic prompt">$ </span>pip install python-frontmatter
</pre>
<p>For experimentation, I copied the build code from my <a class="reference external" href="/post/2021/08/trying-a-thing-with-neovim/">Neovim rst plugin</a> into
the site's <a class="reference external" href="https://www.pyinvoke.org/">Invoke</a> task file. Easier than updating remote plugins and
restarting the editor with every change.</p>
<div class="docutils container">
<tt class="caption docutils literal">tasks.py</tt><pre class="code python literal-block" id="tasks-py">
  <span class="literal string doc">&quot;&quot;&quot;Site generation tasks for randomgeekery.org&quot;&quot;&quot;</span>

  <span class="keyword namespace">import</span> <span class="name namespace">locale</span>

  <span class="keyword namespace">import</span> <span class="name namespace">frontmatter</span>
  <span class="keyword namespace">import</span> <span class="name namespace">rich</span>
  <span class="keyword namespace">from</span> <span class="name namespace">docutils.core</span> <span class="keyword namespace">import</span> <span class="name">publish_parts</span>
  <span class="keyword namespace">from</span> <span class="name namespace">invoke</span> <span class="keyword namespace">import</span> <span class="name">task</span>

  <span class="name">locale</span><span class="operator">.</span><span class="name">setlocale</span><span class="punctuation">(</span><span class="name">locale</span><span class="operator">.</span><span class="name">LC_ALL</span><span class="punctuation">,</span> <span class="literal string double">&quot;&quot;</span><span class="punctuation">)</span>

  <span class="keyword">def</span> <span class="name function">convert_rst_file_for_hugo</span><span class="punctuation">(</span><span class="name">source_filename</span><span class="punctuation">:</span> <span class="name builtin">str</span><span class="punctuation">)</span> <span class="operator">-&gt;</span> <span class="keyword constant">None</span><span class="punctuation">:</span>
      <span class="literal string doc">&quot;&quot;&quot;Transform a single reStructuredText file so Hugo can handle it.&quot;&quot;&quot;</span>

      <span class="name">target_filename</span> <span class="operator">=</span> <span class="name">determine_target</span><span class="punctuation">(</span><span class="name">source_filename</span><span class="punctuation">)</span>
      <span class="name">post</span> <span class="operator">=</span> <span class="name">frontmatter</span><span class="operator">.</span><span class="name">load</span><span class="punctuation">(</span><span class="name">source_filename</span><span class="punctuation">)</span>
      <span class="name">parts</span> <span class="operator">=</span> <span class="name">publish_parts</span><span class="punctuation">(</span><span class="name">source</span><span class="operator">=</span><span class="name">post</span><span class="operator">.</span><span class="name">content</span><span class="punctuation">,</span> <span class="name">writer_name</span><span class="operator">=</span><span class="literal string double">&quot;html&quot;</span><span class="punctuation">)</span>
      <span class="name">post</span><span class="operator">.</span><span class="name">content</span> <span class="operator">=</span> <span class="name">parts</span><span class="punctuation">[</span><span class="literal string double">&quot;body&quot;</span><span class="punctuation">]</span>
      <span class="name">post</span><span class="operator">.</span><span class="name">metadata</span><span class="punctuation">[</span><span class="literal string double">&quot;format&quot;</span><span class="punctuation">]</span> <span class="operator">=</span> <span class="literal string double">&quot;rst&quot;</span>

      <span class="keyword">with</span> <span class="name builtin">open</span><span class="punctuation">(</span><span class="name">target_filename</span><span class="punctuation">,</span> <span class="literal string double">&quot;w&quot;</span><span class="punctuation">)</span> <span class="keyword">as</span> <span class="name">out</span><span class="punctuation">:</span>
          <span class="name">out</span><span class="operator">.</span><span class="name">write</span><span class="punctuation">(</span><span class="name">frontmatter</span><span class="operator">.</span><span class="name">dumps</span><span class="punctuation">(</span><span class="name">post</span><span class="punctuation">))</span>
          <span class="name">rich</span><span class="operator">.</span><span class="name">print</span><span class="punctuation">(</span><span class="literal string affix">f</span><span class="literal string double">&quot;:crayon: </span><span class="literal string interpol">{</span><span class="name">target_filename</span><span class="literal string interpol">}</span><span class="literal string double">&quot;</span><span class="punctuation">)</span>


  <span class="keyword">def</span> <span class="name function">determine_target</span><span class="punctuation">(</span><span class="name">source</span><span class="punctuation">:</span> <span class="name builtin">str</span><span class="punctuation">)</span> <span class="operator">-&gt;</span> <span class="name builtin">str</span><span class="punctuation">:</span>
      <span class="literal string doc">&quot;&quot;&quot;Return the filename that rst transformations should write to.&quot;&quot;&quot;</span>

      <span class="comment single"># Using an odd suffix so Hugo doesn't try to build the rst itself</span>
      <span class="keyword">if</span> <span class="operator word">not</span> <span class="name">source</span><span class="operator">.</span><span class="name">endswith</span><span class="punctuation">(</span><span class="literal string double">&quot;.rst.txt&quot;</span><span class="punctuation">):</span>
          <span class="keyword">raise</span> <span class="name exception">ValueError</span><span class="punctuation">(</span><span class="literal string affix">f</span><span class="literal string double">&quot;Look at </span><span class="literal string interpol">{</span><span class="name">source</span><span class="literal string interpol">}</span><span class="literal string double"> more closely before transforming it.&quot;</span><span class="punctuation">)</span>

      <span class="keyword">return</span> <span class="name">source</span><span class="operator">.</span><span class="name">replace</span><span class="punctuation">(</span><span class="literal string double">&quot;.rst.txt&quot;</span><span class="punctuation">,</span> <span class="literal string double">&quot;.html&quot;</span><span class="punctuation">)</span>


  <span class="name decorator">&#64;task</span>
  <span class="keyword">def</span> <span class="name function">rst</span><span class="punctuation">(</span><span class="name">c</span><span class="punctuation">,</span> <span class="name">filename</span><span class="punctuation">):</span>
      <span class="literal string doc">&quot;&quot;&quot;Transform a single reStructuredText file.&quot;&quot;&quot;</span>

      <span class="name">convert_rst_file_for_hugo</span><span class="punctuation">(</span><span class="name">filename</span><span class="punctuation">)</span>
</pre>
</div>
<p>Then I use Invoke to do the transform:</p>
<pre class="code console literal-block">
<span class="generic prompt">$ </span>inv content/draft/creating-a-restructuredtext-kbd-role/index.rst.txt
<span class="generic output">🖍 content/draft/creating-a-restructuredtext-kbd-role/index.html</span>
</pre>
<p>Some variation of this is bound to work for you.</p>
</div>
<p>Let's get started!</p>
<div class="section" id="what-even-is-a-role">
<h1><a class="toc-backref" href="#id1">What even is a role?</a></h1>
<p>First, we need the background. There's this thing called <strong class="term">interpreted
text</strong>. It's a reserved bit of functionality for specially marked text.  Folks
coming to reStructuredText from Markdown mostly know it as the weird reason
they have to use double backticks for <tt class="docutils literal">code</tt>.</p>
<pre class="code rst literal-block">
<span class="name variable">`interpreted text`</span>
</pre>
<p>Intepreted text has all sorts of fancy potential. I mainly know it for the fact
that rst links use it. Unless told otherwise, <a class="reference external" href="https://docutils.sourceforge.io/">Docutils</a> treats interpreted text
as a citation.</p>
<pre class="code html literal-block">
<span class="punctuation">&lt;</span><span class="name tag">cite</span><span class="punctuation">&gt;</span>interpreted text<span class="punctuation">&lt;/</span><span class="name tag">cite</span><span class="punctuation">&gt;</span>
</pre>
<p>It assumes any interpreted text is <tt class="docutils literal"><span class="pre">:title-reference:</span></tt> — that is, it
references the title of a book, movie, song, or other publication.  The <a class="reference external" href="https://developer.mozilla.org/en-US/docs/Web/HTML/Element/cite">cite</a>
element is a perfectly reasonable choice for that.</p>
<p>But what if you aren't specifically talking about a title? <strong class="term">Roles</strong>
provide an explicit label for your interpreted text.</p>
<pre class="code rst literal-block">
<span class="name attribute">:term:</span><span class="name variable">`Roles`</span>
</pre>
<p>What's a <tt class="docutils literal">:term:</tt> in rst? Nothing. I made it up. Seems like a good role for
when I introduce a new name and I want it to stand out.</p>
<p>I need to define the role to use it. Otherwise?</p>
<div class="figure">
<img alt="screenshot of docutils error message" src="docutils-unknown-role.png" />
<p class="caption">Docutils embeds an error message below the offending block</p>
</div>
<p>So up at the top of my document use the <a class="reference external" href="https://docutils.sourceforge.io/docs/ref/rst/directives.html#custom-interpreted-text-roles">role directive</a> to create <tt class="docutils literal">:term:</tt>
and register it with the parser.</p>
<pre class="code rst literal-block">
<span class="punctuation">..</span> <span class="operator word">role</span><span class="punctuation">::</span> term
</pre>
<p>Now that Docutils knows about the role, it can turn it into HTML.</p>
<pre class="code html literal-block">
<span class="punctuation">&lt;</span><span class="name tag">span</span> <span class="name attribute">class</span><span class="operator">=</span><span class="literal string">&quot;term&quot;</span><span class="punctuation">&gt;</span>Roles<span class="punctuation">&lt;/</span><span class="name tag">span</span><span class="punctuation">&gt;</span>
</pre>
<p>It still doesn't have any inherent <em>meaning</em>, but I can put some style rules on
it so that anything I label with the <tt class="docutils literal">:term:</tt> role shows up a little
differently.</p>
</div>
<div class="section" id="inline-roles-in-your-document">
<h1><a class="toc-backref" href="#id2">Inline roles in your document</a></h1>
<p>If I want the term to stand out a little more, I can adjust my role definition.</p>
<pre class="code rst literal-block">
<span class="punctuation">..</span> <span class="operator word">role</span><span class="punctuation">::</span> term(strong)
</pre>
<p>Now it inherits from the <tt class="docutils literal">:strong:</tt> role, keeping the <tt class="docutils literal">&quot;term&quot;</tt> CSS class.</p>
<pre class="code html literal-block">
<span class="punctuation">&lt;</span><span class="name tag">strong</span> <span class="name attribute">class</span><span class="operator">=</span><span class="literal string">&quot;term&quot;</span><span class="punctuation">&gt;</span>Roles<span class="punctuation">&lt;/</span><span class="name tag">strong</span><span class="punctuation">&gt;</span>
</pre>
<p>You can inherit from any role. That makes it a nice way to create aliases
or slight variations to existing roles.</p>
<p>But I want to get fancy. Let's look at defining reStructuredText roles in
Python.</p>
</div>
<div class="section" id="defining-roles-in-your-code">
<h1><a class="toc-backref" href="#id3">Defining roles in your code</a></h1>
<p>Defining a role has two main steps. Okay, three. Because first we need to import
some libraries.</p>
<pre class="code python literal-block">
<span class="keyword namespace">from</span> <span class="name namespace">docutils</span> <span class="keyword namespace">import</span> <span class="name">nodes</span>
<span class="keyword namespace">from</span> <span class="name namespace">docutils.parsers.rst</span> <span class="keyword namespace">import</span> <span class="name">roles</span>
</pre>
<p><em>Now</em> we create a function that knows what to do when given
a role and some preprocessed parameters.</p>
<pre class="code python literal-block">
<span class="keyword">def</span> <span class="name function">role_term</span><span class="punctuation">(</span><span class="name">name</span><span class="punctuation">,</span> <span class="name">rawtext</span><span class="punctuation">,</span> <span class="name">text</span><span class="punctuation">,</span> <span class="name">lineno</span><span class="punctuation">,</span> <span class="name">inliner</span><span class="punctuation">,</span> <span class="name">options</span><span class="operator">=</span><span class="punctuation">{},</span> <span class="name">content</span><span class="operator">=</span><span class="punctuation">[]):</span>
    <span class="literal string doc">&quot;&quot;&quot;Return text marked as domain terminology.&quot;&quot;&quot;</span>
    <span class="operator">...</span>
</pre>
<p>That's quite a function signature to take in without context, so here's a
breakdown of what got sent when Docutils saw my first <tt class="docutils literal">:term:Roles</tt>:</p>
<table border="1" class="docutils">
<colgroup>
<col width="12%" />
<col width="38%" />
<col width="49%" />
</colgroup>
<thead valign="bottom">
<tr><th class="head">parameter</th>
<th class="head">value</th>
<th class="head">explanation</th>
</tr>
</thead>
<tbody valign="top">
<tr><td><tt class="docutils literal">name</tt></td>
<td><tt class="docutils literal">term</tt></td>
<td>the role name</td>
</tr>
<tr><td><tt class="docutils literal">rawtext</tt></td>
<td><tt class="docutils literal"><span class="pre">:term:`Roles`</span></tt></td>
<td>all text input including role and markup</td>
</tr>
<tr><td><tt class="docutils literal">text</tt></td>
<td><tt class="docutils literal">Roles</tt></td>
<td>the interpreted text content</td>
</tr>
<tr><td><tt class="docutils literal">lineno</tt></td>
<td><tt class="docutils literal">103</tt></td>
<td>the interpreted text starts on this line</td>
</tr>
<tr><td><tt class="docutils literal">inliner</tt></td>
<td><tt class="docutils literal">&lt;docutils…Inliner object at …&gt;</tt></td>
<td>the object that called this function</td>
</tr>
<tr><td><tt class="docutils literal">options</tt></td>
<td><tt class="docutils literal">{}</tt></td>
<td>a dictionary of customization options</td>
</tr>
<tr><td><tt class="docutils literal">content</tt></td>
<td><tt class="docutils literal">[]</tt></td>
<td>a list of strings containing text content</td>
</tr>
</tbody>
</table>
<p>I won't pretend I know how to use all these yet. That's okay. <tt class="docutils literal">role_term</tt>
only cares about three:</p>
<ul class="simple">
<li><tt class="docutils literal">rawtext</tt></li>
<li><tt class="docutils literal">text</tt></li>
<li><tt class="docutils literal">options</tt> — just in case</li>
</ul>
<p>I chose to mirror the inline directive I made earlier, creating a <cite>strong</cite> node
with a class of <tt class="docutils literal">&quot;term&quot;</tt>.</p>
<pre class="code python literal-block">
<span class="name">term_node</span> <span class="operator">=</span> <span class="name">nodes</span><span class="operator">.</span><span class="name">strong</span><span class="punctuation">(</span><span class="name">rawtext</span><span class="punctuation">,</span> <span class="name">text</span><span class="punctuation">,</span> <span class="operator">**</span><span class="name">options</span><span class="punctuation">)</span>
<span class="name">term_node</span><span class="operator">.</span><span class="name">set_class</span><span class="punctuation">(</span><span class="literal string double">&quot;term&quot;</span><span class="punctuation">)</span>
</pre>
<p>Anyone calling <tt class="docutils literal">role_term</tt> expects a tuple with two node lists: one for
content, and another holding any error nodes I may need to create. In this case
the content list has my term node and the error list is empty.</p>
<pre class="code python literal-block">
<span class="keyword">return</span> <span class="punctuation">[</span><span class="name">term_node</span><span class="punctuation">],</span> <span class="punctuation">[]</span>
</pre>
<p>With our role implementation defined, we register it and the name associated
with it.</p>
<pre class="code python literal-block">
<span class="keyword">def</span> <span class="name function">role_term</span><span class="punctuation">(</span><span class="name">name</span><span class="punctuation">,</span> <span class="name">rawtext</span><span class="punctuation">,</span> <span class="name">text</span><span class="punctuation">,</span> <span class="name">lineno</span><span class="punctuation">,</span> <span class="name">inliner</span><span class="punctuation">,</span> <span class="name">options</span><span class="operator">=</span><span class="punctuation">{},</span> <span class="name">content</span><span class="operator">=</span><span class="punctuation">[]):</span>
    <span class="literal string doc">&quot;&quot;&quot;Return text marked as domain terminology.&quot;&quot;&quot;</span>

    <span class="name">term_node</span> <span class="operator">=</span> <span class="name">nodes</span><span class="operator">.</span><span class="name">strong</span><span class="punctuation">(</span><span class="name">rawtext</span><span class="punctuation">,</span> <span class="name">text</span><span class="punctuation">,</span> <span class="operator">**</span><span class="name">options</span><span class="punctuation">)</span>
    <span class="name">term_node</span><span class="operator">.</span><span class="name">set_class</span><span class="punctuation">(</span><span class="literal string double">&quot;term&quot;</span><span class="punctuation">)</span>

    <span class="keyword">return</span> <span class="punctuation">[</span><span class="name">term_node</span><span class="punctuation">],</span> <span class="punctuation">[]</span>

<span class="name">roles</span><span class="operator">.</span><span class="name">register_canonical_role</span><span class="punctuation">(</span><span class="literal string single">'term'</span><span class="punctuation">,</span> <span class="name">role_term</span><span class="punctuation">)</span>
</pre>
<p>I don't need my inline <tt class="docutils literal">role</tt> directive anymore, so I remove it. Registering
<tt class="docutils literal">role_term</tt> makes it available to every document processed by this particular
Python script.</p>
<p>Okay, now I basically know how to implement a reStructuredText role. Let's keep
going.</p>
<div class="section" id="tag-references">
<h2><a class="toc-backref" href="#id4"><tt class="docutils literal">:tag:</tt> references</a></h2>
<p>I link to tags on this site frequently. Since I'm the main audience for this
site, it's mostly to give me a shortcut to related content. But hey it may help
<em>you</em> find related content to if you happen to click through.</p>
<p>Couple of problems with those tag links, though. First off, they look exactly
like every other link in my published HTML. It would be nice for them to stand
out a bit when I'm reading. Second, they look like every other link in my post
source. It would be nice for them to stand out a bit when I'm <em>writing</em>.</p>
<p>So let's make a <tt class="docutils literal">:tag:</tt> reference role.</p>
<pre class="code python literal-block">
<span class="keyword">def</span> <span class="name function">role_reference_tag</span><span class="punctuation">(</span>
    <span class="name">name</span><span class="punctuation">,</span> <span class="name">rawtext</span><span class="punctuation">,</span> <span class="name">text</span><span class="punctuation">,</span> <span class="name">lineno</span><span class="punctuation">,</span> <span class="name">inliner</span><span class="punctuation">,</span> <span class="name">options</span><span class="operator">=</span><span class="punctuation">{},</span> <span class="name">content</span><span class="operator">=</span><span class="punctuation">[]</span>
<span class="punctuation">):</span>
    <span class="literal string doc">&quot;&quot;&quot;Return a reference to a site tag.&quot;&quot;&quot;</span>

    <span class="name">tag_ref</span> <span class="operator">=</span> <span class="literal string affix">f</span><span class="literal string double">&quot;/tags/</span><span class="literal string interpol">{</span><span class="name">text</span><span class="literal string interpol">}</span><span class="literal string double">&quot;</span>
    <span class="name">tag_node</span> <span class="operator">=</span> <span class="name">nodes</span><span class="operator">.</span><span class="name">reference</span><span class="punctuation">(</span><span class="name">rawtext</span><span class="punctuation">,</span> <span class="name">text</span><span class="punctuation">,</span> <span class="name">refuri</span><span class="operator">=</span><span class="name">tag_ref</span><span class="punctuation">,</span> <span class="operator">**</span><span class="name">options</span><span class="punctuation">)</span>
    <span class="name">tag_node</span><span class="operator">.</span><span class="name">set_class</span><span class="punctuation">(</span><span class="literal string double">&quot;p-category&quot;</span><span class="punctuation">)</span>

    <span class="keyword">return</span> <span class="punctuation">[</span><span class="name">tag_node</span><span class="punctuation">],</span> <span class="punctuation">[]</span>

<span class="name">roles</span><span class="operator">.</span><span class="name">register_canonical_role</span><span class="punctuation">(</span><span class="literal string single">'tag'</span><span class="punctuation">,</span> <span class="name">role_reference_tag</span><span class="punctuation">)</span>
</pre>
<div class="sidebar">
I thought about putting the <tt class="docutils literal">#</tt> in CSS, but not every <tt class="docutils literal"><span class="pre">p-category</span></tt> is a
tag. I can always change my mind later, maybe make a distinct <tt class="docutils literal">tag</tt> CSS
class.</div>
<p>It looks similar to <tt class="docutils literal">:term:</tt>, except because I'm referencing something I use
a <tt class="docutils literal">reference</tt> node and give it a link to that tag's page as <tt class="docutils literal">refuri</tt>.  The
<tt class="docutils literal"><span class="pre">p-category</span></tt> class is a <a class="p-category reference external" href="/tags/microformats">#microformats</a> thing for <a class="p-category reference external" href="/tags/indieweb">#indieweb</a>. I also
decided to prefix my tag text with the traditional octothorpe used to mark tags
out in the wild.</p>
<pre class="code rst literal-block">
<span class="name attribute">:tag:</span><span class="name variable">`microformats`</span>
</pre>
<p>Oh yes that is <em>much</em> nicer to read than a standard reStructuredText link.</p>
<pre class="code html literal-block">
<span class="punctuation">&lt;</span><span class="name tag">a</span> <span class="name attribute">class</span><span class="operator">=</span><span class="literal string">&quot;p-category reference external&quot;</span> <span class="name attribute">href</span><span class="operator">=</span><span class="literal string">&quot;/tags/microformats&quot;</span><span class="punctuation">&gt;</span>#microformats<span class="punctuation">&lt;/</span><span class="name tag">a</span><span class="punctuation">&gt;</span>
</pre>
<p>There's my <tt class="docutils literal"><span class="pre">p-category</span></tt> class, along with an unsurprising <tt class="docutils literal">reference</tt> —
since it's a clear way to indicate the reference node I used — and a
slightly confusing <tt class="docutils literal">external</tt> class. Pretty sure that means &quot;external to the
document.&quot;</p>
</div>
<div class="section" id="a-kbd-role">
<h2><a class="toc-backref" href="#id5">A <tt class="docutils literal">:kbd:</tt> role</a></h2>
<p>Something I need rather often is a way to indicate keyboard input.
<tt class="keyboard docutils literal">Control c</tt>, stuff like that.</p>
<pre class="code python literal-block">
<span class="keyword">def</span> <span class="name function">role_kbd</span><span class="punctuation">(</span><span class="name">name</span><span class="punctuation">,</span> <span class="name">rawtext</span><span class="punctuation">,</span> <span class="name">text</span><span class="punctuation">,</span> <span class="name">lineno</span><span class="punctuation">,</span> <span class="name">inliner</span><span class="punctuation">,</span> <span class="name">options</span><span class="operator">=</span><span class="punctuation">{},</span> <span class="name">content</span><span class="operator">=</span><span class="punctuation">[]):</span>
    <span class="literal string doc">&quot;&quot;&quot;Return literal text marked as keyboard input.&quot;&quot;&quot;</span>

    <span class="name">kbd_node</span> <span class="operator">=</span> <span class="name">nodes</span><span class="operator">.</span><span class="name">literal</span><span class="punctuation">(</span><span class="name">rawtext</span><span class="punctuation">,</span> <span class="name">text</span><span class="punctuation">,</span> <span class="operator">**</span><span class="name">options</span><span class="punctuation">)</span>
    <span class="name">kbd_node</span><span class="operator">.</span><span class="name">set_class</span><span class="punctuation">(</span><span class="literal string double">&quot;keyboard&quot;</span><span class="punctuation">)</span>

    <span class="keyword">return</span> <span class="punctuation">[</span><span class="name">kbd_node</span><span class="punctuation">],</span> <span class="punctuation">[]</span>
</pre>
<pre class="code rst literal-block">
<span class="name attribute">:kbd:</span><span class="name variable">`Control c`</span>
</pre>
<pre class="code html literal-block">
<span class="punctuation">&lt;</span><span class="name tag">tt</span> <span class="name attribute">class</span><span class="operator">=</span><span class="literal string">&quot;keyboard docutils literal&quot;</span><span class="punctuation">&gt;</span>Control c<span class="punctuation">&lt;/</span><span class="name tag">tt</span><span class="punctuation">&gt;</span>
</pre>
<p>Well that was easy. A bit verbose, but okay. That's not the real problem
though.</p>
</div>
<div class="section" id="there-s-a-perfectly-good-kbd-element">
<h2><a class="toc-backref" href="#id6">There's a perfectly good <tt class="docutils literal">&lt;kbd&gt;</tt> element</a></h2>
<p>This blog is HTML, right? Can't I just use the <a class="reference external" href="https://developer.mozilla.org/en-US/docs/Web/HTML/Element/kbd">kbd</a> element in my role?</p>
<p>Yes, but kind of no. It's considered poor form to put raw HTML in your output
nodes. Docutils writes all sorts of content, and a <tt class="docutils literal">&lt;kbd&gt;</tt> would be pretty
ungainly sitting in a PDF. Ideally you'd take care of writing HTML in an HTML
Writer. Unfortunately, I have no idea how to work an HTML Writer yet.</p>
<p>But we <em>can</em> output raw HTML in a role implementation. It would be frowned on
slightly less if we flagged it as a raw role.</p>
<pre class="code python literal-block">
<span class="keyword namespace">import</span> <span class="name namespace">html</span>

<span class="keyword">def</span> <span class="name function">role_raw_kbd</span><span class="punctuation">(</span><span class="name">name</span><span class="punctuation">,</span> <span class="name">rawtext</span><span class="punctuation">,</span> <span class="name">text</span><span class="punctuation">,</span> <span class="name">lineno</span><span class="punctuation">,</span> <span class="name">inliner</span><span class="punctuation">,</span> <span class="name">options</span><span class="operator">=</span><span class="punctuation">{},</span> <span class="name">content</span><span class="operator">=</span><span class="punctuation">[]):</span>
    <span class="literal string doc">&quot;&quot;&quot;Return literal text marked as keyboard input.&quot;&quot;&quot;</span>

    <span class="name">escaped_text</span> <span class="operator">=</span> <span class="name">html</span><span class="operator">.</span><span class="name">escape</span><span class="punctuation">(</span><span class="name">text</span><span class="punctuation">)</span>
    <span class="name">kbd_html</span> <span class="operator">=</span> <span class="literal string affix">f</span><span class="literal string double">&quot;&lt;kbd&gt;</span><span class="literal string interpol">{</span><span class="name">escaped_text</span><span class="literal string interpol">}</span><span class="literal string double">&lt;/kbd&gt;&quot;</span>
    <span class="name">options</span><span class="punctuation">[</span><span class="literal string double">&quot;format&quot;</span><span class="punctuation">]</span> <span class="operator">=</span> <span class="literal string double">&quot;html&quot;</span>
    <span class="name">kbd_node</span> <span class="operator">=</span> <span class="name">nodes</span><span class="operator">.</span><span class="name">raw</span><span class="punctuation">(</span><span class="name">rawtext</span><span class="punctuation">,</span> <span class="name">kbd_html</span><span class="punctuation">,</span> <span class="operator">**</span><span class="name">options</span><span class="punctuation">)</span>

    <span class="keyword">return</span> <span class="punctuation">[</span><span class="name">kbd_node</span><span class="punctuation">],</span> <span class="punctuation">[]</span>


<span class="name">roles</span><span class="operator">.</span><span class="name">register_canonical_role</span><span class="punctuation">(</span><span class="literal string single">'raw-kbd'</span><span class="punctuation">,</span> <span class="name">role_raw_kbd</span><span class="punctuation">)</span>
</pre>
<p>Better pull in the <a class="reference external" href="https://docs.python.org/3/library/html.html">html</a> standard library and escape that text. Otherwise I'd
feel awful silly when talking about indenting with <kbd>&gt;&gt;</kbd> in <a class="p-category reference external" href="/tags/vim">#vim</a> or
something and it breaks the whole page.</p>
<pre class="code rst literal-block">
<span class="name attribute">:raw-kbd:</span><span class="name variable">`&gt;&gt;`</span>
</pre>
<p>Yeah, that works. It's not too bad to look at while writing.</p>
<pre class="code html literal-block">
<span class="punctuation">&lt;</span><span class="name tag">kbd</span><span class="punctuation">&gt;</span><span class="name entity">&amp;lt;&amp;lt;</span><span class="punctuation">&lt;/</span><span class="name tag">kbd</span><span class="punctuation">&gt;</span>
</pre>
<p>And there we go. An honest to goodness <tt class="docutils literal">&lt;kbd&gt;</tt> element. And <tt class="docutils literal"><span class="pre">:raw-kbd:</span></tt> will
be easier to search for if and when I get around to custom HTML Writers.</p>
<p>Figuring out a role for keyboard input was the reason I started writing this
post — though my favorite new role is <tt class="docutils literal">:tag:</tt>. Anyways, I think this is a
good spot to stop writing and start editing.</p>
</div>
</div>
<div class="section" id="wrap-it-up">
<h1><a class="toc-backref" href="#id7">Wrap it up</a></h1>
<p>…pardon me while I copy those role functions back into my Neovim plugin…</p>
<p>Well that was fun. I wanted a role for keyboard input, and I got it. Plus, my
tags are a little easier to find in the page. <em>And</em> I have a <tt class="docutils literal">:term:</tt> role
for when I'm feeling pedagogical.</p>
<p>Cool.</p>
<p>Roles are just a first step in customizing Docutils output. No idea when I'll
get to the rest. You can learn more for yourself with <a class="reference external" href="https://docutils.sourceforge.io/">Docutils</a> and
heavily customized publishing environments like <a class="reference external" href="https://www.sphinx-doc.org/en/master/">Sphinx</a>.</p>
<p>Me, I'm just having a grand time embedding this whole authoring flow in the
middle of my <a class="p-category reference external" href="/tags/hugo">#hugo</a> site. May want to think about a new theme though if
I'm going to continue with Hugo. Perhaps borrow from Alexander Carlton's <a class="reference external" href="https://www.fisodd.com/code/b-side/">Hugo
B-side</a>.</p>
</div>