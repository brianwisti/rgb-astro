---
aliases:
- /blogspot/2006/09/22_ive-been-experimenting-with-cakephp.html
- /post/2006/ive-been-experimenting-with-cakephp/
- /2006/09/22/ive-been-experimenting-with-cakephp/
category: blogspot
date: 2006-09-22 00:00:00
layout: layout:PublishedArticle
slug: ive-been-experimenting-with-cakephp
tags:
- php
title: I've Been Experimenting With CakePHP
uuid: 4fdbeb2a-9d90-482e-bfbe-c3ce550714ab
---

I've been experimenting with <a href="http://cakephp.org/">CakePHP</a> over the last couple of weeks for a project. It's definitely not <a href="http://rubyonrails.com/">Ruby on Rails</a>, but it has a lot of charm. This library provides a MVC system for PHP applications, but the really interesting thing is that you can just drop it onto your Web server space with no fuss or bother. You don't even have to worry about clever mod_rewrite rules if you don't want to.
<!--more-->

Since CakePHP is so accessible, I thought it would be fun to explore the framework a little bit more, and document what's going on here. Now, I'm not the greatest at remembering to update this blog, but I'll do my best.

My goal is straightforward: create a forum application, similar in purpose to <a href="http://www.phpbb.com/">phpBB</a>. I'm sure it has already been done, but I'm in this strictly for the educational exercise.

The first task - assuming you already have Web space with support for PHP and MySQL - is to get CakePHP. That's easy enough. Just grab the latest archive from the download section of the CakePHP site, and unpack it to your server space. I'm fond of using my personal machine as a development site, so I won't be worrying about issues like uploading or editing remote files.

    $ cd /var/www
    $ sudo tar xfvz ~/cake_1.1.7.3363.tar.gz
    ...
    $ mv cake_1.1.7.3363.tar.gz cakebb
    $ sudo chown --recursive brianwisti cakebb

Okay, there are much safer approaches to setting things up, but I am only doing quick and dirty development on my home machine.

Next I need to manage the database connections. CakePHP uses PHP code for configuration, following along with the Rails idea of "convention over configuration." The theory is that a handful of PHP files are easier to sort through than a handful of XML configuration files.

Configuration files are kept in <tt>cakebb/app/config</tt>. The first one I'll be looking at is database.php, except that there is no <tt>database.php</tt> when Cake is first extracted. We have a file <tt>database.php.default</tt> instead. I'll move it over to <tt>database.php</tt> so that Cake has something to look at on startup.

    $ mv database.php.default database.php

Of course now I need to edit the file to establish the database connection details. I'll also need to set up the appropriate databases on my local MySQL server.

So here's the important part of <tt>database.php</tt>:

~~~php
class DATABASE_CONFIG
{
    var $default = array('driver' => 'mysql',
                                'connect' => 'mysql_connect',
                                'host' => 'localhost',
                                'login' => 'cakebb',
                                'password' => 'cakebb_user',
                                'database' => 'my secret password',
                                'prefix' => '');

    var $test = array('driver' => 'mysql',
                            'connect' => 'mysql_connect',
                            'host' => 'localhost',
                            'login' => 'cakebb_user',
                            'password' => 'my secret password',
                            'database' => 'cakebb_test',
                            'prefix' => '');
}
~~~

Then I go into the MySQL shell to create the databases and accounts needed by CakeBB.

    $ mysql -uroot -p
    Enter password:
    Welcome to the MySQL monitor.  Commands end with ; or \g.
    Your MySQL connection id is 6 to server version: 5.0.22-Debian_0ubuntu6.06.2-log
    Type 'help;' or '\h' for help. Type '\c' to clear the buffer.

    mysql> create database cakebb;
    Query OK, 1 row affected (0.01 sec)

    mysql> create database cakebb_test;
    Query OK, 1 row affected (0.00 sec)

    mysql> grant all on cakebb.* to 'cakebb_user'@'%' identified by 'my secret password';
    Query OK, 0 rows affected (0.00 sec)

    mysql> grant all on cakebb_test.* to 'cakebb_user'@'%' identified by 'my secret password';
    Query OK, 0 rows affected (0.00 sec)

I feel like skipping mod_rewrite for now, so I'll uncomment the following line (around line 40 of <tt>app/config/core.php</tt>):

~~~php
//  define ('BASE_URL', env('SCRIPT_NAME'));
~~~

All I've got at this point is the basic setup, but I should test it just to make sure everything is connecting. I send my browser to http://localhost/cakebb/ and get a lovely status page telling me that CakePHP is installed and able to connect to the database.

Great. I'm set up and functional. The next step will be to build the application models. But that will have to wait until tomorrow, because I need to get to work now.