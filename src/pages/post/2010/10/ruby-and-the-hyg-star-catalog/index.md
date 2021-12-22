---
aliases:
- /coolnamehere/2010/10/05_ruby-and-the-hyg-star-catalog.html
- /post/2010/ruby-and-the-hyg-star-catalog/
- /2010/10/05/ruby-and-the-hyg-star-catalog/
category: coolnamehere
date: 2010-10-05 00:00:00
layout: layout:PublishedArticle
slug: ruby-and-the-hyg-star-catalog
tags:
- ruby
title: Ruby and the HYG Star Catalog
uuid: 57815f1d-2eb8-4cfd-a857-6afccf9f4417
---

[Parrot Babysteps]: /post/2009/07/parrot-babysteps

[reading a CSV file in Parrot]: /post/2009/10/parrot-babysteps-06-files-and-hashes
[HYG Star Catalog]: http://www.astronexus.com/node/34
[Parrot]: /tags/parrot/
[Ruby]: /tags/ruby/

One of my big projects over the last year has been a [Parrot Babysteps][] tutorial. One of the more
interesting tasks in that tutorial was [reading a CSV file in Parrot][]. I used the [HYG Star Catalog][] as a
sample CSV file that was large enough to present some interesting data. This was fun in [Parrot][], but
obviously I thought quite a bit about how I would tackle the problem in a higher level language such as
[Ruby][]. Today seems like a good day to find out.
<!--more-->

[Sequel]: http://sequel.rubyforge.org/

I am emphasizing the *Moderately* in this Moderately Interesting Ruby Exercise. After exploring the `csv`
library for Ruby, we'll use [Sequel][] to build a database that can be quickly queried. Even though I have an
unhealthy love for making projects larger and more complex than they need to be, I want to keep this short and
sweet.

### What I'm Using

[MacPorts]: http://macports.org
[rvm]: http://rvm.beginrescueend.com/

My primary machine for these projects is the happy home iMac. It is running OS X 10.6 plus
[MacPorts][]. My default Ruby is 1.9.2, installed via [rvm][].

I may revisit this exercise with other Ruby installations on other platforms to double-check that things work,
but your results *should* be similar to mine as long as you are using Ruby 1.9.2.

## Exploration

[wget]: http://www.gnu.org/software/wget/

We will start by poking at the Ruby standard `csv` library a little bit, just to see how we use it.
I already have a copy of the [HYG Star Catalog][] from my previous efforts, but for this exercise I'll pretend
I do not. We'll just download it using our favorite downloading technique. Mine is GNU [wget][].

    $ wget http://www.astronexus.com/files/downloads/hygxyz.csv.gz
    $ tar xfvz hygxyz.csv.gz

[editor]: /tags/editors/

If we open `hygxyz.csv` in our favorite [editor][], we will see that the file is large and bewildering.

    StarID,HIP,HD,HR,Gliese,BayerFlamsteed,ProperName,RA,Dec,Distance,PMRA,PMDec,RV,Mag,AbsMag,Spectrum,ColorIndex,X,Y,Z,VX,VY,VZ
    0,,,,,,Sol,0,0,0.000004848,0,0,0,-26.73,4.85,G2V,0.656,0,0,0,0,0,0
    1,1,224700,,,,,6.079e-05,01.08901332,282.485875706215,-5.20,-1.88,,9.10,1.84501631012894,F5,0.482,282.43485,0.00449,5.36884,4.9e-08,-7.12e-06,-2.574e-06
    ... and so on for 119,618 lines

There are many fields. Some of them are strings, others are numbers. Quite a few are empty.

### Parsing the CSV

Let's start with the simplest and dumbest CSV parsing code we can manage.

``` ruby
require 'csv'

CSV.open('hygxyz.csv').each { |row| p row }
```

How does that look?

    $ ruby stellar
    ["StarID", "HIP", "HD", "HR", "Gliese", "BayerFlamsteed", "ProperName", "RA", "Dec", "Distance", "PMRA",
    "PMDec", "RV", "Mag", "AbsMag", "Spectrum", "ColorIndex", "X", "Y", "Z", "VX", "VY", "VZ"]
    ["0", nil, nil, nil, nil, nil, "Sol", "0", "0", "0.000004848", "0", "0", "0", "-26.73", "4.85", "G2V",
    "0.656", "0", "0", "0", "0", "0", "0"]
    ["1", "1", "224700", nil, nil, nil, nil, "6.079e-05", "01.08901332", "282.485875706215", "-5.20", "-1.88",
    nil, "9.10", "1.84501631012894", "F5", "0.482", "282.43485", "0.00449", "5.36884", "4.9e-08", "-7.12e-06",
    "-2.574e-06"]
    ["2", "2", "224690", nil, nil, nil, nil, "0.00025315", "-19.49883745", "45.662100456621", "181.21",
    "-0.93", nil, "9.27", "5.97222057420059", "K3V", "0.999", "43.04329", "0.00285", "-15.24144", "-7.1e-08",
    "4.0112e-05", "-1.94e-07"]
    ["3", "3", "224699", nil, nil, nil, nil, "0.00033386", "38.85928608", "355.871886120996", "5.24", "-2.91",
    nil, "6.61", "-1.1464684004746", "B9", "-0.019", "277.11358", "0.02422", "223.27753", "3.148e-06",
    "9.04e-06", "-3.909e-06"]
    ...

Okay, wow. That is a lot of stuff going by. I don't know about you, but I'm going to hit Control-C and make an
adjustment to the code.

``` ruby
require 'csv'

filename = 'hygxyz.csv'
CSV.open(filename).first(3).each { |row| p row }
```

There. Now we will only look at the first three entries. That should be a little easier to digest. I also
shuffled the filename into its own variable. That's just how I like to do things. I tell myself that it will
be easier to read and edit later.

    $ ruby stellar
    ["StarID", "HIP", "HD", "HR", "Gliese", "BayerFlamsteed", "ProperName", "RA", "Dec", "Distance", "PMRA",
    "PMDec", "RV", "Mag", "AbsMag", "Spectrum", "ColorIndex", "X", "Y", "Z", "VX", "VY", "VZ"]
    ["0", nil, nil, nil, nil, nil, "Sol", "0", "0", "0.000004848", "0", "0", "0", "-26.73", "4.85", "G2V",
    "0.656", "0", "0", "0", "0", "0", "0"]
    ["1", "1", "224700", nil, nil, nil, nil, "6.079e-05", "01.08901332", "282.485875706215", "-5.20", "-1.88",
    nil, "9.10", "1.84501631012894", "F5", "0.482", "282.43485", "0.00449", "5.36884", "4.9e-08", "-7.12e-06",
    "-2.574e-06"]

The default behavior for `csv` is reasonable. It split up the fields correctly, and set the empty fields to
`nil`. Next we need to deal with the fact that the first row is supposed to be the header, providing names for
fields in the corresponding columns.

``` ruby
require 'csv'

filename = 'hygxyz.csv'
CSV.open(filename, headers: true).first(3).each { |row| p row }
```

One small change has a big impact.

    $ ruby stellar.rb
    #<CSV::Row "StarID":"0" "HIP":nil "HD":nil "HR":nil "Gliese":nil "BayerFlamsteed":nil "ProperName":"Sol"
    "RA":"0" "Dec":"0" "Distance":"0.000004848" "PMRA":"0" "PMDec":"0" "RV":"0" "Mag":"-26.73" "AbsMag":"4.85"
    "Spectrum":"G2V" "ColorIndex":"0.656" "X":"0" "Y":"0" "Z":"0" "VX":"0" "VY":"0" "VZ":"0">
    #<CSV::Row "StarID":"1" "HIP":"1" "HD":"224700" "HR":nil "Gliese":nil "BayerFlamsteed":nil "ProperName":nil
    "RA":"6.079e-05" "Dec":"01.08901332" "Distance":"282.485875706215" "PMRA":"-5.20" "PMDec":"-1.88" "RV":nil
    "Mag":"9.10" "AbsMag":"1.84501631012894" "Spectrum":"F5" "ColorIndex":"0.482" "X":"282.43485" "Y":"0.00449"
    "Z":"5.36884" "VX":"4.9e-08" "VY":"-7.12e-06" "VZ":"-2.574e-06">
    #<CSV::Row "StarID":"2" "HIP":"2" "HD":"224690" "HR":nil "Gliese":nil "BayerFlamsteed":nil "ProperName":nil
    "RA":"0.00025315" "Dec":"-19.49883745" "Distance":"45.662100456621" "PMRA":"181.21" "PMDec":"-0.93" "RV":nil
    "Mag":"9.27" "AbsMag":"5.97222057420059" "Spectrum":"K3V" "ColorIndex":"0.999" "X":"43.04329" "Y":"0.00285"
    "Z":"-15.24144" "VX":"-7.1e-08" "VY":"4.0112e-05" "VZ":"-1.94e-07">

Now `csv` is generating something that looks vaguely like a hash. Nice. However, every field is handled as a
String when some of them are obviously numbers. The `converters` option should fix that.

``` ruby
CSV.open(filename, headers: true, converters: :numeric).first(5).each do |row|
  p row
end
```

Setting the `converters` option to `:numeric` tells CSV to convert anything that looks like a number to a
Number. That is useful for comparing values, because Ruby won't automatically convert a String into a Number.
You must tell it to convert. Anyways - I'm babbling. It is really amazing how hard it is to pad the content of
these little essays out when you are talking about Ruby code. That's probably why there are so many silly
cartoons and insane gibberish accompanying the best Ruby tutorials.

    $ ruby stellar.rb
    #<CSV::Row "StarID":0 "HIP":nil "HD":nil "HR":nil "Gliese":nil "BayerFlamsteed":nil "ProperName":"Sol" "RA":0
    "Dec":0 "Distance":4.848e-06 "PMRA":0 "PMDec":0 "RV":0 "Mag":-26.73 "AbsMag":4.85 "Spectrum":"G2V"
    "ColorIndex":0.656 "X":0 "Y":0 "Z":0 "VX":0 "VY":0 "VZ":0>
    #<CSV::Row "StarID":1 "HIP":1 "HD":224700 "HR":nil "Gliese":nil "BayerFlamsteed":nil "ProperName":nil
    "RA":6.079e-05 "Dec":1.08901332 "Distance":282.485875706215 "PMRA":-5.2 "PMDec":-1.88 "RV":nil "Mag":9.1
    "AbsMag":1.84501631012894 "Spectrum":"F5" "ColorIndex":0.482 "X":282.43485 "Y":0.00449 "Z":5.36884
    "VX":4.9e-08 "VY":-7.12e-06 "VZ":-2.574e-06>
    #<CSV::Row "StarID":2 "HIP":2 "HD":224690 "HR":nil "Gliese":nil "BayerFlamsteed":nil "ProperName":nil
    "RA":0.00025315 "Dec":-19.49883745 "Distance":45.662100456621 "PMRA":181.21 "PMDec":-0.93 "RV":nil "Mag":9.27
    "AbsMag":5.97222057420059 "Spectrum":"K3V" "ColorIndex":0.999 "X":43.04329 "Y":0.00285 "Z":-15.24144
    "VX":-7.1e-08 "VY":4.0112e-05 "VZ":-1.94e-07>

Let's do something with those Numbers. How about counting the number of stars within ten light years of Earth?

``` ruby
# count-neighbors.rb
require 'csv'
filename = 'hygxyz.csv'
neighbor_count = 0

CSV.open(filename, headers: true, converters: :numeric).each do |row|
  if row['Distance'] < 10
    neighbor_count += 1
  end
end

puts "There are #{neighbor_count} stars within 10 light years of Earth."
```

How many are there?

    $ ruby count-neighbors.rb
    There are 320 stars within 10 light years of Earth.

That's a lot of neighbors. It took a while to count them, though. That probably has something to do with the
20 Megabyte CSV file. We are not ready to speed things up, though. Let's try one more task: looking for a
specific star.

``` ruby
# find-sol.rb
require 'csv'
filename = 'hygxyz.csv'
CSV.open(filename, headers: true, converters: :numeric).each do |row|
  if row['ProperName'] == "Sol"
    p row
  end
end
```
It better find our own Sun. It's the first entry, after all.

    $ ruby find-sol.rb
    #<CSV::Row "StarID":0 "HIP":nil "HD":nil "HR":nil "Gliese":nil "BayerFlamsteed":nil "ProperName":"Sol" "RA":0
    "Dec":0 "Distance":4.848e-06 "PMRA":0 "PMDec":0 "RV":0 "Mag":-26.73 "AbsMag":4.85 "Spectrum":"G2V"
    "ColorIndex":0.656 "X":0 "Y":0 "Z":0 "VX":0 "VY":0 "VZ":0>

Sorry, I got sleepy. Is it done? I should have put a `break` in that code after printing out the star details. 
Of course, that is just cheating around the fact that parsing a large CSV file is *slow*. Perhaps it is time
to try a database.

### Creating a Database

[SQLite]: http://sqlite.org

I would imagine that stuffing these values into a database should make simple questions like "show me the star
named 'Sol'" or "count the stars within 10 light years" pretty straightforward. We can use a lightweight
database such as [SQLite][]. There may be nearly 120,000 stars in the catalog, but that is trivial for SQLite.
I have heard anecdotal reports of it being used for tables with millions of rows. 

First, I want to install `sqlite3`.

    $ port install sqlite3

[Ubuntu]: http://ubuntu.com

I'm not doing this on my [Ubuntu][] Linux machine, but if I was I'd install both the `sqlite3` shell and the
development libraries.

    $ sudo apt-get install sqlite3 libsqlite3-dev

#### The Sequel Library

[sqlite3-ruby]: http://rubyforge.org/projects/sqlite-ruby/

I have already chosen [Sequel][] as my preferred Ruby database library, so I need to install that. Oh, and I
should also install [sqlite3-ruby][]. Sequel provides a nice layer of abstraction, but it does not contain the
code which actually speaks to the database.

    $ gem install sequel
    $ gem install sqlite3-ruby

[Sequel migrations]: http://sequel.rubyforge.org/rdoc/files/doc/migration_rdoc.html

We can use the `create_table` database method described on the [Sequel migrations][] page to build the table,
rather than relying on my rather lightweight knowledge of SQLite schema definition. The dump of star data from
our earlier CSV parsing code provides the hints we need to build a usable schema.

``` ruby
require 'csv'
require 'sequel'

filename = 'hygxyz.csv'

DB = Sequel.sqlite('hyg.db')

if DB.table_exists? :stars
    DB.drop_table :stars
end

DB.create_table :stars do
    primary_key :id
    Integer :StarID
    Integer :HIP
    Integer :HD
    Integer :HR
    Integer :Gliese
    Integer :BayerFlamsteed
    String  :ProperName
    Float   :RA
    Float   :Dec
    Float   :Distance
    Float   :PMRA
    Float   :PMDec
    Float   :RV
    Float   :Mag
    Float   :AbsMag
    String  :Spectrum
    Float   :ColorIndex
    Float   :X
    Float   :Y
    Float   :Z
    Float   :VX
    Float   :VY
    Float   :VZ
end

CSV.open(filename, headers: true, converters: :numeric).each do |row|
    print "."
    DB[:stars].insert(row.to_hash)
end
puts
```

This script will set up the database and fill it with values from the CSV file. Each row is converted to a
Hash, which makes the database `insert` method happy. There is also a little check and cleanup near the
beginning. This is just in case there is a typo that messes up your code later on. It doesn't hurt to be
cautious.

    $ ruby stellar.rb
    .......

Go take a break. Make some coffee, catch up with your family, or play one more turn of Civilization. This is
going to take a while. Me, I went for some more coffee.

### Searching the Database

[Sequel querying API]: http://sequel.rubyforge.org/rdoc/files/doc/querying_rdoc.html

We will look at the [Sequel querying API][] in a moment, but first let us make sure that the database returns
plausible results to direct queries.

    $ sqlite3 hyg.db
    sqlite> select count(*) from stars where distance < 10;
    320
    sqlite> select * from stars where propername = 'Sol';
    1|0||||||Sol|0.0|0.0|4.848e-06|0.0|0.0|0.0|-26.73|4.85|G2V|0.656|0.0|0.0|0.0|0.0|0.0|0.0
    sqlite> .quit

Hopefully you noticed a big improvement in the speed of your searches by switching to a database. I sure did.

What if we tried the same queries with Ruby and Sequel? Let's open an `irb` prompt and test it out.

    $ irb
    ruby-1.9.2-p0 > require 'sequel'
     => true
    ruby-1.9.2-p0 > DB = Sequel.sqlite('hyg.db')
     => #<Sequel::SQLite::Database: "sqlite:/hyg.db">
    ruby-1.9.2-p0 > DB[:stars].first(ProperName: 'Sol')
     => {:id=>1, :StarID=>0, :HIP=>nil, :HD=>nil, :HR=>nil, :Gliese=>nil, :BayerFlamsteed=>nil,
    :ProperName=>"Sol", :RA=>0.0, :Dec=>0.0, :Distance=>4.848e-06, :PMRA=>0.0, :PMDec=>0.0, :RV=>0.0,
    :Mag=>-26.73, :AbsMag=>4.85, :Spectrum=>"G2V", :ColorIndex=>0.656, :X=>0.0, :Y=>0.0, :Z=>0.0, :VX=>0.0,
    :VY=>0.0, :VZ=>0.0}
    ruby-1.9.2-p0 > DB[:stars].filter { distance < 10 }.count
     => 320

Yes indeed. That was much faster. Let's close with something a little bit fancier: showing a table of
information about all the stars in the catalog that are G Spectrum and have a proper name, ordered by their
distance from Earth.

    ruby-1.9.2-p0 > DB[:stars].filter(:Spectrum.like('G%')).filter('ProperName not null').order(:Distance).each { |row|
    ruby-1.9.2-p0 >     printf("%20s\t%4.2f\t%s\n", row[:ProperName], row[:Distance], row[:Spectrum])
    ruby-1.9.2-p0 ?>  }
                  Sol    0.00    G2V
    Rigel Kentaurus A    1.35    G2V
            82 G. Eri    6.06    G8V
     Groombridge 1830    9.16    G8Vp
         Vindemiatrix    31.35   G8IIIvar
                Nihal    48.80   G5II
    => #<Sequel::SQLite::Dataset: "SELECT * FROM `stars` WHERE ((Spectrum like 'G%') AND (ProperName not null))">

I encourage you to explore the [Sequel querying API][] more on your own, but I need to wrap this up.

## Conclusion

All right. You've got 119,617 stars with various characteristics, all sitting there waiting for you to think
of something interesting to do with them. I just wanted to see how much easier it would be to parse a CSV in a
high level language. Turns out, it's pretty easy. Explore the Ruby standard library and the *many* Rubygems
that are available out in the big world. You'll probably have fun, and you'll almost definitely learn
something.