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

    my %fragment_for;
    my @filenames;
    my $markdown = slurp $filename;

    for $markdown.match(/<shortcode>/, :global) -> $block {
      my $tangle_content = $block<shortcode><content>;
      my $params = $block<shortcode><params>;
      my $fragment = $params<fragment> || $params<filename>;

      if $fragment {
        say "fragment: $fragment";
        %fragment_for{ $fragment.Str } = $tangle_content;
      }

      if my $filename = $params<filename> {
        @filenames.push($filename.Str);
      }
    }

    my regex fragment { ^^ \h*? "«" $<name> = .+? "»" $$ }
    my %tangle_for;

    sub tangle(Str $name) {
      return "" unless $name;

      if %tangle_for{ $name } {
        return %tangle_for{ $name }.Str;
      }

      my $content = %fragment_for{ $name };
      unless $content {
        die "«$name» is not a valid fragment";
      }

      for $content.match(/ <fragment> /, :global) -> $match {
        my $fragment_ref = $match.Str;
        my $fragment_name = $match<fragment><name>.Str;
        say "$name ← «$fragment_name»";
        $content.subst-mutate(/$fragment_ref/, tangle( $fragment_name));
      }

      %tangle_for{ $name } = $content;
    }

    for %fragment_for.keys -> $name { tangle($name); }

  my $commented_opener = '{{' ~ '</* ';
  my $commented_closer = ' */>' ~ '}}';

    for @filenames -> $tangle_file {
      my $tangle_content = %tangle_for{ $tangle_file }
        .subst(:global, / $commented_opener /, $opener)
        .subst(:global, / $commented_closer /, $closer);
      spurt $tangle_file, $tangle_content;
      say "Tangled to $tangle_file";
    }
}
