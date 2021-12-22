---
aliases:
- /coolnamehere/2002/06/02_if-else-and-elsif.html
- /post/2002/if-else-and-elsif/
- /2002/06/02/pagetemplate-if-else-and-elsif/
category: coolnamehere
date: 2002-06-02 00:00:00
layout: layout:PublishedArticle
slug: pagetemplate-if-else-and-elsif
tags:
- pagetemplate
title: PageTemplate - If, Else, and Elsif
updated: 2009-07-11 00:00:00
uuid: c4352f20-abf8-4aca-9fa7-7194975f4fa7
---

## If

The `if` directive tells PageTemplate to only display a chunk of content
when some condition is true. PageTemplate will skip the block and move
on if the condition is false.

### Syntax

``` html
[%if condition %]
  chunk
[%end if %]
```

Here is an example of `if` in use.

``` html
[%if pageowner %]
<a href="admin.cgi">Admin View</a>
[%end if %]
```

In this example, if the application tells PageTemplate that `pageowner`
is true, PageTemplate inserts a link to an administrative page.
Otherwise, nothing happens here.

## Else

The `else` directive adds extra power to `if`, by indicating a chunk of
content to use when a condition is not true.

### Syntax

``` html
[%if value%]
  chunk
[%else%]
  alternate chunk
[%end if %]
```

### Example

``` html
[%if login%]
<p>Welcome back, [%var login %]!</p>
<p><a href="logout.cgi">Log Out</a></p>
[%else %]
<form name="login" method="post">
  Login: <input type="text" name="login" /><br />
  Password: <input type="password" name="passwd" /><br />
  <input type="submit" value="Login!" />
</form>
[%end if %]
```

This is the situation where I use `else` directives the most. If the
visitor is logged in to a Web application, she is shown a brief
welcoming message. If not, then she will see a login form.

This example also shows a convenient approach to `if` conditions. We
*could* make up a special `logged_in` variable, but since all we care
about here is the presence of a login, we have PageTemplate test that as
if it were a regular condition.

## Elsif

There are many cases where a simple “yes” or “no” doesn’t do enough. You
want to display something different in the same spot depending on
whether or not different conditions are true. PageTemplate makes that a
little easier with the `elsif` directive, which allows you to do exactly
that by testing the truth of different variables.

<aside class="admonition note">
<p class="admonition-title">Note</p>

See the `case` directive described in the [Other
Features](/post/2002/06/pagetemplate-other-features/) page for doing
multiple tests on the same variable.

</aside>

### Syntax

``` html
[%if condition1 %]
  Block 1
[%elsif condition2 %]
  Block 2
  ...
[%elsif conditionN> %]
  Block n
[%else %]
  Else Block
[%end if %]
```

### Example

``` html
[%if cart.items %]
  <p>You have [%var cart.count %] items in your cart.</p>
[%elsif cart.empty %]
  <p>Your cart is empty.</p>
[%else %]
  <p>You have no cart. <a href="register.rb">Register</a> and get one!</p>
[%end if %]
```

## Unless

Sometimes you want to ask if something is false. For example, you may
want to show a login form in one spot if the user is not logged in, but
nothing at all if he is logged in. That is exactly the sort of thing
`unless` was intended for.

### Syntax

``` html
[%unless condition %]
  Block
[%end unless %]
```

### Example

``` html
[%unless user.has_donated %]
<p><a href="pay_up.cgi">Donate money, chump!</a></p>
[%end unless %]
```