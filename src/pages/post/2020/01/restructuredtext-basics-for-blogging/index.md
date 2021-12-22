---
aliases:
- /2020/01/19/restructuredtext-basics-for-blogging/
category: Tools
date: 2020-01-19
description: I got carried away taking notes about basic RST usage
format: rst
layout: layout:PublishedArticle
slug: restructuredtext-basics-for-blogging
tags:
- python
- rst
- text
title: reStructuredText Basics For Blogging
uuid: 9463aeb7-8d86-4dc0-acec-8d45f93391fc
---

<p>Between reading <a class="reference external" href="/tags/python">Python</a> documentation and exploring <a class="reference external" href="/tags/nikola">Nikola</a>, I've been looking at <a class="reference external" href="https://docutils.sourceforge.io/rst.html">RST</a> a lot.
Let's figure out the basics.</p>

<div class="contents topic" id="contents">
  <p class="topic-title first">Contents</p>
  <ul class="simple">
  <li><a class="reference internal" href="#what-is-it" id="id5">What is it?</a></li>
  <li><a class="reference internal" href="#how-do-i-use-rst-in-my-blog" id="id6">How do I use RST in my blog?</a><ul>
  <li><a class="reference internal" href="#editor-support" id="id7">Editor support</a></li>
  <li><a class="reference internal" href="#extracting-styles" id="id8">Extracting styles</a></li>
  </ul>
  </li>
  <li><a class="reference internal" href="#what-does-it-look-like" id="id9">What does it look like?</a><ul>
  <li><a class="reference internal" href="#the-basics" id="id10">The basics</a><ul>
  <li><a class="reference internal" href="#paragraphs-and-inline-formatting" id="id11">Paragraphs and inline formatting</a></li>
  <li><a class="reference internal" href="#bullet-lists" id="id12">Bullet lists</a></li>
  <li><a class="reference internal" href="#links" id="id13">Links</a></li>
  </ul>
  </li>
  <li><a class="reference internal" href="#a-little-more" id="id14">A little more</a><ul>
  <li><a class="reference internal" href="#headers-and-sections" id="id15">Headers and sections</a></li>
  <li><a class="reference internal" href="#images-and-figures" id="id16">Images and figures</a></li>
  <li><a class="reference internal" href="#simple-tables" id="id17">Simple Tables</a></li>
  </ul>
  </li>
  <li><a class="reference internal" href="#directives" id="id18">Directives</a><ul>
  <li><a class="reference internal" href="#admonitions" id="id19">Admonitions</a></li>
  <li><a class="reference internal" href="#code-blocks" id="id20">Code blocks</a></li>
  </ul>
  </li>
  <li><a class="reference internal" href="#bonus-csv-tables" id="id21">Bonus: CSV Tables</a></li>
  <li><a class="reference internal" href="#another-bonus-list-tables" id="id22">Another Bonus: List tables</a></li>
  </ul>
  </li>
  <li><a class="reference internal" href="#what-did-i-miss" id="id23">What did I miss?</a></li>
  <li><a class="reference internal" href="#resources" id="id24">Resources</a></li>
  </ul>
</div>

<div class="section" id="what-is-it">
<h2><a class="toc-backref" href="#id5">What is it?</a></h2>
<p><a class="reference external" href="https://docutils.sourceforge.io/rst.html">reStructuredText</a> is a lightweight formatting language with a cumbersome name.
You mostly see it in <a class="reference external" href="https://www.python.org/dev/peps/pep-0287/">Python docstrings</a>, because it's the standard format for Python documentation.
Through site generators and <a class="reference external" href="https://www.sphinx-doc.org/en/master/index.html">Sphinx</a>, RST also shows up <a class="reference external" href="https://www.sphinx-doc.org/en/master/examples.html">behind the scenes</a> in blogs, projects, and technical books.</p>
<p>Nothing about RST limits it to technical writing —
well, except that most nontechnical folks aren't installing special Python libraries to write Hugo posts.</p>
<p>Anyways.
The essentials of the RST format are easy enough that it's suited for general writing.</p>
</div>
<div class="section" id="how-do-i-use-rst-in-my-blog">
<h2><a class="toc-backref" href="#id6">How do I use RST in my blog?</a></h2>
<p>If you already blog with Nikola or <a class="reference external" href="https://getpelican.com">Pelican</a>, you are all set.
Those site generators natively support reStructuredText.</p>
<p><a class="reference external" href="/tags/hugo">Hugo</a> will build <tt class="docutils literal">.rst</tt> content if you have <tt class="docutils literal">rst2html.py</tt> installed.</p>
<pre class="code shell-session literal-block">
<span class="generic prompt">$</span> pip install docutils
</pre>
<div class="section" id="editor-support">
<h3><a class="toc-backref" href="#id7">Editor support</a></h3>
<p>Emacs and Vim both include RST support built-in.
Visual Studio Code users can find a <a class="reference external" href="https://marketplace.visualstudio.com/items?itemName=lextudio.restructuredtext">useful plugin</a>.
But all you <em>need</em> is a plain text editor, preferably with automatic indentation.</p>
</div>
<div class="section" id="extracting-styles">
<h3><a class="toc-backref" href="#id8">Extracting styles</a></h3>
<p>The HTML generated by <tt class="docutils literal">rst2html.py</tt> has its own special classes.
My home-grown Hugo theme supports none of those classes, of course.
I couldn't figure out how to export the Docutils default stylesheet this morning.</p>
<p>So I made a document and grabbed the CSS rules from there for my own nefarious purposes.</p>
<pre class="code shell-session literal-block">
<span class="generic prompt">$</span> <span class="name builtin">echo</span> <span class="literal string double">&quot;hey\n&quot;</span> <span class="punctuation">|</span> rst2html.py &gt;&gt; sample.html
</pre>
</div>
</div>
<div class="section" id="what-does-it-look-like">
<h2><a class="toc-backref" href="#id9">What does it look like?</a></h2>
<p>Although RST is readable, more blog-type folks are familiar with a <a class="reference external" href="https://daringfireball.net/projects/markdown/">Markdown</a> flavor.
I know I was more familiar with Markdown when I started this.
Once you get the hang of it, you may find that RST has its charms.</p>
<div class="section" id="the-basics">
<h3><a class="toc-backref" href="#id10">The basics</a></h3>
<p>More than enough to write one of my blog <a class="reference external" href="/note">notes</a>.</p>
<div class="section" id="paragraphs-and-inline-formatting">
  <h4><a class="toc-backref" href="#id11">Paragraphs and inline formatting</a></h4>
  <p>It all starts with paragraphs.
  Plain text, separated by empty lines.
  The text lines of a paragraph are wrapped together.</p>

  <blockquote>Indent your paragraph if you want a nice blockquote.</blockquote>

  <p>You can <em>emphasize</em> text in a paragraph using asterisks.
  Double asterisks give <strong>more</strong> emphasis.
  You can wrap multiple words to <em>emphasize all of them</em>.
  I think doing that dilutes the effect, though.
  You end up with something that looks more like a conspiracy-themed newsletter.
  But hey.
  If that's the look you're going for?
  Have fun!</p>

  <pre class="code literal-block">
  It all starts with paragraphs.
  Plain text, separated by empty lines.
  The text lines of a paragraph are wrapped together.

      Indent your paragraph if you want a nice blockquote.

  You can <span class="generic emph">*emphasize*</span> text in a paragraph using asterisks.
  Double asterisks give <span class="generic strong">**more**</span> emphasis.
  You can wrap multiple words to <span class="generic emph">*emphasize all of them*</span>.
  </pre>

  <p>Use <tt class="docutils literal">double backticks</tt> for inline literals —
  characters displayed in a monospace font and often used to indicate code.
  This is a little confusing after Markdown, which uses a single backtick for literals.
  But RST uses those for <cite>interpreted text</cite>.</p>

  <pre class="code rst literal-block">
  Use <span class="literal string">``double backticks``</span> for inline literals —
  characters displayed in a monospace font and often used to indicate code.
  This is a little confusing after Markdown, which uses a single backtick for literals.
  But RST uses those for <span class="name variable">`interpreted text`</span>.
  </pre>

  <p>What's interpreted text?
  Well, it can mean a few things depending on the context of what's in and around it.
  You could even define your own with Python.
  Not today, though.</p>

  <div class="admonition note">
    <p class="first admonition-title">Note</p>
    <p class="last"><cite>rst2html.py</cite> transforms a lone bit of <tt class="docutils literal">`interpreted text`</tt> to <tt class="docutils literal">&lt;cite&gt;interpreted <span class="pre">text&lt;/cite&gt;</span></tt>.
    The <a class="reference external" href="https://developer.mozilla.org/en-US/docs/Web/HTML/Element/cite">citation</a> tag is used in HTML for referencing creative work: books, songs, blog posts.</p>
  </div>
</div>

<div class="section" id="bullet-lists">
  <h4><a class="toc-backref" href="#id12">Bullet lists</a></h4>

  <p>We already know what a basic bullet list looks like.</p>

  <ul class="simple">
    <li>You have some lines</li>
    <li>Each line starts with a special character and a space</li>
    <li>I used <tt class="docutils literal">*</tt> but RST allows a few:
      <ul>
        <li><tt class="docutils literal">*</tt></li>
        <li><tt class="docutils literal">-</tt></li>
        <li><tt class="docutils literal">+</tt></li>
      </ul>
    </li>
    <li>The important thing is to be consistent for a list or sublist
      <ul>
        <li>oh, and you can do sub lists with indentation!</li>
        <li>but you <em>need</em> blank lines between list levels</li>
      </ul>
    </li>
  </ul>

  <pre class="code literal-block">
  <span class="literal number">*</span> You have some lines
  <span class="literal number">*</span> Each line starts with a special character and a space
  <span class="literal number">*</span> I used <span class="literal string">``*``</span> but RST allows a few:

      <span class="literal number">-</span> <span class="literal string">``*``</span>
      <span class="literal number">-</span> <span class="literal string">``-``</span>
      <span class="literal number">-</span> <span class="literal string">``+``</span>

  <span class="literal number">*</span> The important thing is to be consistent for a list or sublist

      <span class="literal number">-</span> oh, and you can do sub lists with indentation!
      <span class="literal number">-</span> but you <span class="generic emph">*need*</span> blank lines between list levels
  </pre>
</div>

<div class="section" id="links">
<h4><a class="toc-backref" href="#id13">Links</a></h4>
<p>Links can be simple URL drops, like <a class="reference external" href="https://beatrockmusic.bandcamp.com/">https://beatrockmusic.bandcamp.com/</a>.
Or use some interpreted text for a more readable <a class="reference external" href="https://bambubeatrock.bandcamp.com/">link</a>.
I prefer <a class="reference external" href="https://rockyriverabeatrock.bandcamp.com/">reference</a> links.
It even looks nice for <a class="reference external" href="https://prometheusbrown.bandcamp.com/album/tag-init">longer references</a>, once you get used to it.</p>
<pre class="code literal-block">
Links can be simple URL drops, like https://beatrockmusic.bandcamp.com/.
Or use some interpreted text for a more readable <span class="literal string">`link </span><span class="literal string interpol">&lt;https://bambubeatrock.bandcamp.com/&gt;</span><span class="literal string">`_</span>.
I prefer reference_ links.
It even looks nice for <span class="literal string">`longer references`_</span>, once you get used to it.

<span class="punctuation">..</span> <span class="name tag">_reference:</span> https://rockyriverabeatrock.bandcamp.com/
<span class="punctuation">..</span> <span class="name tag">_longer references:</span> https://prometheusbrown.bandcamp.com/album/tag-init
</pre>
<p>See those last couple lines?
Those define link targets.
The <tt class="docutils literal">..</tt> at the beginning of the line tells RST this is explicit markup.
Explicit markup takes us out of the core document flow, letting us use extensions or define values.</p>
<p>For today's goal of basic blogging, this explanation is sufficient.</p>
<ul class="simple">
<li><tt class="docutils literal">.. _word: URL</tt> or <tt class="docutils literal">.. _long word: URL</tt> defines a target</li>
<li><tt class="docutils literal">word_</tt> makes a link to it.</li>
<li>for multiword targets, use <tt class="docutils literal">`long name`_</tt> to reference them.</li>
</ul>
</div>
</div>
<div class="section" id="a-little-more">
<h3><a class="toc-backref" href="#id14">A little more</a></h3>
<p>We've got <a class="reference internal" href="#the-basics">the basics</a>.
After these next few items, I have about 80% of everything I ever wrote on this site covered.</p>
<div class="section" id="headers-and-sections">
<h4><a class="toc-backref" href="#id15">Headers and sections</a></h4>
<div class="admonition warning">
<p class="first admonition-title">Warning</p>
<p class="last">Most blog generators demote your headers by at least one level.
That way your post title goes at the top of the heirarchy.
It also means my level three section headers generate <tt class="docutils literal">&lt;h4&gt;</tt> tags!
So don't go overboard with subsections.</p>
</div>
<p>You've been looking at section headers already, so it seems silly to put examples here.
Plus it messes up the document structure.</p>
<p>You need two lines to make a section header.
The text of the header itself forms the first line.
Use the text of the header itself for the first line.
In the second line, put enough non-alphanumeric characters to match your header's length.
Pick any you like —
well, any from the set of <tt class="docutils literal">= - ` : ' &quot; ~ ^ _ * + # &lt; &gt;</tt> —
as long as you stay consistent.</p>
<pre class="code literal-block">
<span class="generic heading">What does it look like?</span>
<span class="generic heading">=======================</span>

section 3
</pre>
<p>First symbols picked, so it's a level one header.</p>
<pre class="code literal-block">
<span class="generic heading">A little more</span>
<span class="generic heading">-------------</span>

section 3.1
</pre>
<p>I picked a new symbol for the indicator, so this is a level two header.</p>
<pre class="code literal-block">
<span class="generic heading">Headers and sections</span>
<span class="generic heading">~~~~~~~~~~~~~~~~~~~~</span>

section 3.1.1
</pre>
<p>Another new symbol means another level, taking us to a level three header.</p>
<pre class="code literal-block">
<span class="generic heading">Images and figures</span>
<span class="generic heading">~~~~~~~~~~~~~~~~~~</span>

section 3.1.2
</pre>
<p>These use the same symbol I used for <cite>Headers and sections</cite>, so this is another level three header.</p>
<pre class="code literal-block">
<span class="generic heading">Directives</span>
<span class="generic heading">----------</span>

section 1.2
</pre>
<p>Oh hey, remember this symbol?
We're back up to level two!</p>
<p>This is the only area where RST feels significantly more cumbersome to me than Markdown or AsciiDoc.
At least it's pretty to look at.</p>
</div>
<div class="section" id="images-and-figures">
<h4><a class="toc-backref" href="#id16">Images and figures</a></h4>
<p>I already have my own shortcodes for images in Hugo.
Oh, and the special logic for cover pictures.
Jeez I have my work cut out for me if and when I migrate to another generator.</p>
<p>Still, <a class="reference external" href="https://twitter.com/brianwisti/status/1219097732440301573">image</a> are a pretty fundamental part of blogging.
It would feel strange to skip them.</p>
<pre class="code literal-block">
<span class="punctuation">..</span> <span class="operator word">image</span><span class="punctuation">::</span> worst-cat.png
    <span class="name class">:alt:</span> Text reads &quot;This is the worst cat.&quot; Photo is a baby hippo
    <span class="name class">:target:</span> https://worstcats.tumblr.com/post/97243616862/this-is-the-worst-cat
</pre>
<p>Look, more explicit markup!
This calls the <a class="reference external" href="https://twitter.com/brianwisti/status/1219097732440301573">image</a> directive with <tt class="docutils literal">worst.cat.png</tt> as an argument
and a few options specified with what RST calls a <cite>field list</cite>.</p>
<p>You can make the image a link with <tt class="docutils literal">:target:</tt>, which is nice.</p>
<a class="reference external image-reference" href="https://worstcats.tumblr.com/post/97243616862/this-is-the-worst-cat"><img alt="Text reads &quot;This is the worst cat.&quot; Photo is a baby hippo" src="worst-cat.png" /></a>
<p>I prefer the HTML <a class="reference external" href="https://developer.mozilla.org/en-US/docs/Web/HTML/Element/figure">figure</a> for my images.
It allows me to add a readable caption, which is a great spot for attribution.</p>
<pre class="code rst literal-block">
<span class="punctuation">..</span> <span class="operator word">figure</span><span class="punctuation">::</span> worst-cat.png
    <span class="name class">:alt:</span> Text reads &quot;This is the worst cat.&quot; Photo is a baby hippo

    via the <span class="literal string">`Worst Cats`_</span> Tumblr blog
</pre>
<p>This directive is conceptually much closer to what I'm thinking of.
You even get a whole paragraph to set the caption.
Text after the first paragraph becomes the legend.
Interested parties can read the <a class="reference external" href="https://docutils.sourceforge.io/docs/ref/rst/directives.html#figure">figure documentation</a> for more details about that.</p>
<div class="figure">
<img alt="Text reads &quot;This is the worst cat.&quot; Photo is a baby hippo" src="worst-cat.png" />
<p class="caption">via the <a class="reference external" href="https://worstcats.tumblr.com/post/97243616862/this-is-the-worst-cat">Worst Cats</a> Tumblr blog</p>
</div>
<p>Unfortunately it's not <em>really</em> a <tt class="docutils literal">&lt;figure&gt;</tt>.
This is a <tt class="docutils literal">div.figure</tt> holding an <tt class="docutils literal">img</tt> and a <tt class="docutils literal">p.caption</tt> instead of a <tt class="docutils literal">&lt;figcaption&gt;</tt>.
As a purist, I recognize that I must eventually fix this.</p>
</div>
<div class="section" id="simple-tables">
<h4><a class="toc-backref" href="#id17">Simple Tables</a></h4>
<p>Tables are very handy for summarizing information.
RST allows extremely complex table formatting.
Fortunately for me, I never use extremely complex table formatting.
<a class="reference external" href="https://docutils.sourceforge.io/docs/ref/rst/restructuredtext.html#simple-tables">simple-tables</a> work just fine.</p>
<pre class="code literal-block">
========= =================
Generator Supports RST
========= =================
Nikola    Yes
Pelican   Yes
Sphinx    Yes
Hugo      If you install <span class="name variable">`docutils`</span>
Gatsby    ??
Eleventy  ??
Jekyll    ??
Middleman ??
========= =================
</pre>
<p>Overflow is okay, as long as the table markers themselves line up.
Still.
It's untidy.
Excuse me a moment.</p>
<pre class="code literal-block">
========= =========================
Generator Supports RST
========= =========================
Nikola    Yes
Pelican   Yes
Sphinx    Yes
Hugo      If you install <span class="name variable">`docutils`</span>
Gatsby    ??
Eleventy  ??
Jekyll    ??
Middleman ??
========= =========================
</pre>
<p>That's better.</p>
<table border="1" class="docutils">
<colgroup>
<col width="26%" />
<col width="74%" />
</colgroup>
<thead valign="bottom">
<tr><th class="head">Generator</th>
<th class="head">Supports RST</th>
</tr>
</thead>
<tbody valign="top">
<tr><td>Nikola</td>
<td>Yes</td>
</tr>
<tr><td>Pelican</td>
<td>Yes</td>
</tr>
<tr><td>Sphinx</td>
<td>Yes</td>
</tr>
<tr><td>Hugo</td>
<td>If you install <cite>docutils</cite></td>
</tr>
<tr><td>Gatsby</td>
<td>??</td>
</tr>
<tr><td>Eleventy</td>
<td>??</td>
</tr>
<tr><td>Jekyll</td>
<td>??</td>
</tr>
<tr><td>Middleman</td>
<td>??</td>
</tr>
</tbody>
</table>
<p>Table construction can get more elaborate.
Check out <a class="reference external" href="https://docutils.sourceforge.io/docs/ref/rst/restructuredtext.html#grid-tables">grid-table</a> if that sort of thing interests you.
It can also get simpler, with <cite>csv-table</cite> and <cite>table-listing</cite> directives.</p>
</div>
</div>
<div class="section" id="directives">
<h3><a class="toc-backref" href="#id18">Directives</a></h3>
<p><a class="reference external" href="https://docutils.sourceforge.io/docs/ref/rst/restructuredtext.html#directives">Directives</a> are used to extend RST.
They're written in Python, but you don't need to understand Python to use them.</p>
<p>Directives share a basic structure:</p>
<pre class="code rst literal-block">
<span class="punctuation">..</span> <span class="operator word">directive-name</span><span class="punctuation">::</span> arguments
    <span class="name class">:option-name:</span> option-values

    body
</pre>
<p>The details vary with every directive.
Some require a body, some take no options.
<a class="reference external" href="https://docutils.sourceforge.io/docs/ref/rst/directives.html#table-of-contents">content</a> generates a full table of contents without requiring arguments, options, or a body!</p>
<pre class="code rst literal-block">
<span class="punctuation">..</span> <span class="operator word">content</span><span class="punctuation">::</span>
</pre>
<p>We've already looked at a couple directives.
Do I have a favorite?
Strangely enough, I do.</p>
<div class="section" id="admonitions">
<h4><a class="toc-backref" href="#id19">Admonitions</a></h4>
<p>Most of this site's history has been me talking to myself.
Sometimes I talk back.
So I'm always looking for a good way to add assorted interjections and comments.
Markdown doesn't officially support that sort of thing, so as a result my <tt class="docutils literal">.md</tt> files have nonstandard components.
Heck, for a while I had my own Hugo shortcode for this sort of thing.</p>
<p>Fortunately, these side notes are part of RST as <a class="reference external" href="https://docutils.sourceforge.io/docs/ref/rst/directives.html#admonitions">admonitions</a>.</p>
<pre class="code literal-block">
<span class="punctuation">..</span> <span class="operator word">note</span><span class="punctuation">::</span> Don't forget to mention admonitions!
</pre>
<div class="admonition note">
<p class="first admonition-title">Note</p>
<p class="last">Don't forget to mention admonitions!</p>
</div>
<p>There are several admonition types, from the casual note to the dire alert.</p>
<pre class="code literal-block">
<span class="punctuation">..</span> <span class="operator word">warning</span><span class="punctuation">::</span> Don't overuse admonitions!
</pre>
<div class="admonition warning">
<p class="first admonition-title">Warning</p>
<p class="last">Don't overuse admonitions!</p>
</div>
<p><tt class="docutils literal">note</tt> and <tt class="docutils literal">warning</tt> should suffice for most cases.</p>
</div>
<div class="section" id="code-blocks">
<h4><a class="toc-backref" href="#id20">Code blocks</a></h4>
<p>This is mostly a coding blog.
So of course I'm going to cover the <a class="reference external" href="https://docutils.sourceforge.io/docs/ref/rst/directives.html#code">code</a> directive.
You give it a language and some code.
<a class="reference external" href="https://pygments.org/">Pygments</a> handles the highlighting.
It handles <em>nearly</em> every language I have handed to it, so it should work nice.</p>

<p>How about a little snippet of Python from my <a class="reference external" href="/post/2019/01/circular-grids-with-python-and-pillow/">circular grids</a> post?</p>

<pre class="code literal-block">
<span class="punctuation">..</span> <span class="operator word">code</span><span class="punctuation">::</span> <span class="keyword">python</span>

<span class="keyword"></span>    <span class="keyword">def</span> <span class="name function">main</span><span class="punctuation">():</span>
        <span class="literal string doc">&quot;&quot;&quot;Create a circle template from command line options&quot;&quot;&quot;</span>
        <span class="comment single"># Get details from command line or use defaults</span>
        <span class="name">parser</span> <span class="operator">=</span> <span class="name">argparse</span><span class="operator">.</span><span class="name">ArgumentParser</span><span class="punctuation">()</span>
        <span class="name">parser</span><span class="operator">.</span><span class="name">add_argument</span><span class="punctuation">(</span><span class="literal string double">&quot;--size&quot;</span><span class="punctuation">,</span> <span class="name">help</span><span class="operator">=</span><span class="literal string double">&quot;length of image side in pixels&quot;</span><span class="punctuation">,</span>
                            <span class="name builtin">type</span><span class="operator">=</span><span class="name builtin">int</span><span class="punctuation">,</span> <span class="name">default</span><span class="operator">=</span><span class="name">DEFAULT_SIZE</span><span class="punctuation">)</span>
        <span class="name">parser</span><span class="operator">.</span><span class="name">add_argument</span><span class="punctuation">(</span><span class="literal string double">&quot;--circles&quot;</span><span class="punctuation">,</span> <span class="name">help</span><span class="operator">=</span><span class="literal string double">&quot;number of circles&quot;</span><span class="punctuation">,</span>
                            <span class="name builtin">type</span><span class="operator">=</span><span class="name builtin">int</span><span class="punctuation">,</span> <span class="name">default</span><span class="operator">=</span><span class="name">DEFAULT_CIRCLES</span><span class="punctuation">)</span>
        <span class="name">parser</span><span class="operator">.</span><span class="name">add_argument</span><span class="punctuation">(</span><span class="literal string double">&quot;--slices&quot;</span><span class="punctuation">,</span> <span class="name">help</span><span class="operator">=</span><span class="literal string double">&quot;number of slices&quot;</span><span class="punctuation">,</span>
                            <span class="name builtin">type</span><span class="operator">=</span><span class="name builtin">int</span><span class="punctuation">,</span> <span class="name">default</span><span class="operator">=</span><span class="name">DEFAULT_SLICES</span><span class="punctuation">)</span>
        <span class="name">args</span> <span class="operator">=</span> <span class="name">parser</span><span class="operator">.</span><span class="name">parse_args</span><span class="punctuation">()</span>
        <span class="name">size</span> <span class="operator">=</span> <span class="name">args</span><span class="operator">.</span><span class="name">size</span>
        <span class="name">circle_count</span> <span class="operator">=</span> <span class="name">args</span><span class="operator">.</span><span class="name">circles</span>
        <span class="name">slice_count</span> <span class="operator">=</span> <span class="name">args</span><span class="operator">.</span><span class="name">slices</span>
        <span class="name">circle_template</span> <span class="operator">=</span> <span class="name">CircleTemplate</span><span class="punctuation">(</span><span class="name">size</span><span class="punctuation">,</span> <span class="name">circle_count</span><span class="punctuation">,</span> <span class="name">slice_count</span><span class="punctuation">)</span>
        <span class="name">circle_template</span><span class="operator">.</span><span class="name">save</span><span class="punctuation">()</span>
</pre>
<pre class="code python literal-block">
<span class="keyword">def</span> <span class="name function">main</span><span class="punctuation">():</span>
    <span class="literal string doc">&quot;&quot;&quot;Create a circle template from command line options&quot;&quot;&quot;</span>
    <span class="comment single"># Get details from command line or use defaults</span>
    <span class="name">parser</span> <span class="operator">=</span> <span class="name">argparse</span><span class="operator">.</span><span class="name">ArgumentParser</span><span class="punctuation">()</span>
    <span class="name">parser</span><span class="operator">.</span><span class="name">add_argument</span><span class="punctuation">(</span><span class="literal string double">&quot;--size&quot;</span><span class="punctuation">,</span> <span class="name">help</span><span class="operator">=</span><span class="literal string double">&quot;length of image side in pixels&quot;</span><span class="punctuation">,</span>
                        <span class="name builtin">type</span><span class="operator">=</span><span class="name builtin">int</span><span class="punctuation">,</span> <span class="name">default</span><span class="operator">=</span><span class="name">DEFAULT_SIZE</span><span class="punctuation">)</span>
    <span class="name">parser</span><span class="operator">.</span><span class="name">add_argument</span><span class="punctuation">(</span><span class="literal string double">&quot;--circles&quot;</span><span class="punctuation">,</span> <span class="name">help</span><span class="operator">=</span><span class="literal string double">&quot;number of circles&quot;</span><span class="punctuation">,</span>
                        <span class="name builtin">type</span><span class="operator">=</span><span class="name builtin">int</span><span class="punctuation">,</span> <span class="name">default</span><span class="operator">=</span><span class="name">DEFAULT_CIRCLES</span><span class="punctuation">)</span>
    <span class="name">parser</span><span class="operator">.</span><span class="name">add_argument</span><span class="punctuation">(</span><span class="literal string double">&quot;--slices&quot;</span><span class="punctuation">,</span> <span class="name">help</span><span class="operator">=</span><span class="literal string double">&quot;number of slices&quot;</span><span class="punctuation">,</span>
                        <span class="name builtin">type</span><span class="operator">=</span><span class="name builtin">int</span><span class="punctuation">,</span> <span class="name">default</span><span class="operator">=</span><span class="name">DEFAULT_SLICES</span><span class="punctuation">)</span>
    <span class="name">args</span> <span class="operator">=</span> <span class="name">parser</span><span class="operator">.</span><span class="name">parse_args</span><span class="punctuation">()</span>
    <span class="name">size</span> <span class="operator">=</span> <span class="name">args</span><span class="operator">.</span><span class="name">size</span>
    <span class="name">circle_count</span> <span class="operator">=</span> <span class="name">args</span><span class="operator">.</span><span class="name">circles</span>
    <span class="name">slice_count</span> <span class="operator">=</span> <span class="name">args</span><span class="operator">.</span><span class="name">slices</span>
    <span class="name">circle_template</span> <span class="operator">=</span> <span class="name">CircleTemplate</span><span class="punctuation">(</span><span class="name">size</span><span class="punctuation">,</span> <span class="name">circle_count</span><span class="punctuation">,</span> <span class="name">slice_count</span><span class="punctuation">)</span>
    <span class="name">circle_template</span><span class="operator">.</span><span class="name">save</span><span class="punctuation">()</span>
</pre>
<p>Oh my.
I'm closing in on two thousand words.
That's far more than I intended.
Let's stop here, with the majority of my regular blog-writing needs covered.</p>
<p>Oh, fine.
One little section at least.</p>
</div>
</div>
<div class="section" id="bonus-csv-tables">
  <h3><a class="toc-backref" href="#id21">Bonus: CSV Tables</a></h3>

  <p>Hand-drawing a table can be labor-intenstive —
  especially when you get fancy.
  Sometimes that is too much.
  Sometimes you just want to stuff values in a table.</p>

  <p><a class="reference external" href="https://docutils.sourceforge.io/docs/ref/rst/directives.html#id4">csv-table</a> serves that perfectly.</p>

  <p>Let's say I have a CSV list of my most important <a class="reference external" href="/tags/taskwarrior">Taskwarrior</a> tasks for the site.</p>

  <p>Hang on.
  How do I get a CSV list of tasks?
  Give me a second here.</p>

  <p>The <a class="reference external" href="https://taskwarrior.org/docs/commands/export.html">export</a> command prints them as JSON.
  I don't see a <tt class="docutils literal"><span class="pre">json-table</span></tt> RST directive, though admittedly I haven't looked hard yet.
  Let's just pipe those to <a class="reference external" href="https://stedolan.github.io/jq/">jq</a>, and…</p>

  <pre class="code shell-session literal-block">
<span class="generic prompt">$</span> task <span class="name builtin">export</span> project:Site status:pending priority:H <span class="punctuation">|</span> <span class="literal string escape">\
</span>  jq -r <span class="literal string single">'.[] | [.id, .description, .urgency] | &#64;csv'</span>
<span class="generic output">227,&quot;rst basics for blogging&quot;,11.9
228,&quot;extract rst stylesheet&quot;,7.9</span>
</pre>

<p>Perfect!
Now where was I?
Oh yes!</p>

<p>Let's say I have a <a class="reference external" href="https://en.wikipedia.org/wiki/Comma-separated_values">CSV</a> list of my most important <a class="reference external" href="/tags/taskwarrior">Taskwarrior</a> tasks for the site.
I can paste that list under a <cite>csv-table</cite> directive, give it a caption and the <cite>header</cite> text —
maybe set the <tt class="docutils literal">widths</tt> option to <tt class="docutils literal">auto</tt>, because I dislike the default of equal-width columns.</p>

<pre class="code literal-block">
<span class="punctuation">..</span> <span class="operator word">csv-table</span><span class="punctuation">::</span> High priority site tasks
    <span class="name class">:header:</span> &quot;ID&quot;, &quot;Description&quot;, &quot;Urgency&quot;
    <span class="name class">:widths:</span> auto

    227,&quot;rst basics for blogging&quot;,11.9
    228,&quot;extract rst stylesheet&quot;,7.9
</pre>

<p>And it comes out not too bad!</p>
<table border="1" class="colwidths-auto docutils">
<caption>High priority site tasks</caption>
<thead valign="bottom">
<tr><th class="head">ID</th>
<th class="head">Description</th>
<th class="head">Urgency</th>
</tr>
</thead>
<tbody valign="top">
<tr><td>227</td>
<td>rst basics for blogging</td>
<td>11.9</td>
</tr>
<tr><td>228</td>
<td>extract rst stylesheet</td>
<td>7.9</td>
</tr>
</tbody>
</table>
</div>
<div class="section" id="another-bonus-list-tables">
<h3><a class="toc-backref" href="#id22">Another Bonus: List tables</a></h3>
<p>I feel bad.
A two row CVS table does not save <em>that</em> much time.
Maybe if I had 20 or 30 generated rows.
And while it may be easier for stuffing values into a table, CSV is not the most readable format.</p>
<p>I can make it up to you.
I <em>just</em> used <a class="reference external" href="https://docutils.sourceforge.io/docs/ref/rst/directives.html#list-table">list-table</a> while switching a recent post to reStructuredText.
It was a lifesaver.</p>
<pre class="code literal-block">
<span class="punctuation">..</span> <span class="operator word">list-table</span><span class="punctuation">::</span> Emacs text scale adjustment key bindings
    <span class="name class">:header-rows:</span> 1
    <span class="name class">:widths:</span> auto

    <span class="literal number">-</span> - Function
      <span class="literal number">-</span> Keys
      <span class="literal number">-</span> Description
    <span class="literal number">-</span> - <span class="literal string">``(text-scale-adjust 1)``</span>
      <span class="literal number">-</span> <span class="literal string">``C-x C-=``</span> or <span class="literal string">``C-x C-+``</span>
      <span class="literal number">-</span> Increase text size by one step
    <span class="literal number">-</span> - <span class="literal string">``(text-scale-adjust -1)``</span>
      <span class="literal number">-</span> <span class="literal string">``C-x C--``</span>
      <span class="literal number">-</span> Decrease text-size by one step
    <span class="literal number">-</span> - <span class="literal string">``(text-scale-adjust 0)``</span>
      <span class="literal number">-</span> <span class="literal string">``C-x C-0``</span>
      <span class="literal number">-</span> Reset text size to default
</pre>
<p>Use nested lists to construct your list table.
Each of the top list items represents a row in your table.
Each of the items in a row list is a cell in that row.
Because I specified <cite>:header-rows: 1</cite>, the first row gives use the table header.</p>
<table border="1" class="colwidths-auto docutils">
<caption>Emacs text scale adjustment key bindings</caption>
<thead valign="bottom">
<tr><th class="head">Function</th>
<th class="head">Keys</th>
<th class="head">Description</th>
</tr>
</thead>
<tbody valign="top">
<tr><td><tt class="docutils literal"><span class="pre">(text-scale-adjust</span> 1)</tt></td>
<td><tt class="docutils literal"><span class="pre">C-x</span> <span class="pre">C-=</span></tt> or <tt class="docutils literal"><span class="pre">C-x</span> <span class="pre">C-+</span></tt></td>
<td>Increase text size by one step</td>
</tr>
<tr><td><tt class="docutils literal"><span class="pre">(text-scale-adjust</span> <span class="pre">-1)</span></tt></td>
<td><tt class="docutils literal"><span class="pre">C-x</span> <span class="pre">C--</span></tt></td>
<td>Decrease text-size by one step</td>
</tr>
<tr><td><tt class="docutils literal"><span class="pre">(text-scale-adjust</span> 0)</tt></td>
<td><tt class="docutils literal"><span class="pre">C-x</span> <span class="pre">C-0</span></tt></td>
<td>Reset text size to default</td>
</tr>
</tbody>
</table>
<p>I like this.
Mind you, I get that simple and grid tables are easier to understanding when <em>reading</em> RST.
There are fancy editor extension to draw simple or grid tables.
Nevertheless, I'm writing this RST file with the intent of turning it into HTML.
In that context — for me — pasting CSV or lines of text is easier than polishing text tables.</p>
<p>Okay I have <strong>got</strong> to stop now.
Clearly I enjoy RST way too much.</p>
</div>
</div>
<div class="section" id="what-did-i-miss">
<h2><a class="toc-backref" href="#id23">What did I miss?</a></h2>
<p><a class="reference external" href="https://docutils.sourceforge.io/docs/ref/rst/roles.html">Roles</a> and <a class="reference external" href="https://docutils.sourceforge.io/docs/ref/rst/restructuredtext.html#substitution-definitions">substitutions</a>.
I wanted to cover them today, but no.
This will do for now.</p>
</div>
<div class="section" id="resources">
  <h2><a class="toc-backref" href="#id24">Resources</a></h2>

  <p>I referenced these quite a bit while putting this post together.
  Maybe they could be useful for you!</p>

  <ul class="simple">
    <li><a class="reference external" href="https://www.devdungeon.com/content/restructuredtext-rst-tutorial-0">DEV_DUNGEON reStructuredText (RST) Tutorial</a></li>
    <li><a class="reference external" href="https://docutils.sourceforge.io/docs/">Docutils project documentation</a>
      <ul>
        <li>especially the <a class="reference external" href="https://docutils.sourceforge.io/docs/user/rst/quickref.html">Quick reStructuredText</a> reference!</li>
      </ul>
    </li>
    <li><a class="reference external" href="https://docutils.readthedocs.io/en/sphinx-docs/user/rst/quickstart.html">ReStructuredText Primer</a></li>
  </ul>
</div>
