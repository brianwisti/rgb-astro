use v6.d;

sub MAIN(Str $filename) {
  my regex params {
      'file="' $<filename> = .+? '"'
      ||
      'name="' $<fragment> = .+? '"'
  }
  my $opener = '{{< ';
  my $closer = ' >}}';

  my regex shortcode {
    $opener code \s <params> .*? $closer
    \n                # Ignore leading newline
    $<content> = .+?  # Remember everything else in the block
    \n                # Ignore trailing newline
    $opener '/code' $closer
  }

    my %fragment-for;
    my @filenames;
    my $markdown = slurp $filename;

    for $markdown.match(/<shortcode>/, :global) -> $block {
      my $tangle-content = $block<shortcode><content>;
      my $params = $block<shortcode><params>;
      my $fragment = $params<fragment> || $params<filename>;

      if $fragment {
        say "fragment: $fragment";
        %fragment-for{ $fragment.Str } = $tangle-content;
      }

      if my $filename = $params<filename> {
        @filenames.push($filename.Str);
      }
    }

    my regex fragment { ^^ \h*? "«" $<name> = .+? "»" $$ }
    my %tangle-for;

    sub tangle(Str $name) {
      return "" unless $name;

      if %tangle-for{ $name } {
        return %tangle-for{ $name }.Str;
      }

      my $content = %fragment-for{ $name };
      unless $content {
        die "«$name» is not a valid fragment";
      }

      for $content.match(/ <fragment> /, :global) -> $match {
        my $fragment-ref = $match.Str;
        my $fragment-name = $match<fragment><name>.Str;
        say "$name ← «$fragment-name»";
        $content.subst-mutate(/$fragment-ref/, tangle( $fragment-name));
      }

      %tangle-for{ $name } = $content;
    }

    for %fragment-for.keys -> $name { tangle($name); }

  my $commented-opener = '{{' ~ '</* ';
  my $commented-closer = ' */>' ~ '}}';

    for @filenames -> $tangle-file {
      my $tangle-content = %tangle-for{ $tangle-file }
        .subst(:global, / $commented-opener /, $opener)
        .subst(:global, / $commented-closer /, $closer);
      spurt $tangle-file, $tangle-content;
      say "Tangled to $tangle-file";
    }
}