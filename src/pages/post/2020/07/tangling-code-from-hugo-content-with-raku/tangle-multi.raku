sub MAIN() {
  my $filename = "index.md";
  my $opener = '{{< ';
  my $closer = ' >}}';

  my regex shortcode {
    $opener
      code \h
      'file="' $<filename> = .+? '"'  # Remember the filename
      .*?
    $closer
    \n                # Ignore leading newline
    $<content> = .+?  # Remember everything else in the block
    \n                # Ignore trailing newline
    $opener '/code' $closer
  }

  my $commented-opener = '{{' ~ '</* ';
  my $commented-closer = ' */>' ~ '}}';

  my $markdown  = slurp $filename;
  my @fragments = $markdown.match(/<shortcode>/, :global);

  for @fragments -> $block {
    my $tangle-file = $block<shortcode><filename>;
      my $tangle-content = $block<shortcode><content>
        .subst(:global, / $commented-opener /, $opener)
        .subst(:global, / $commented-closer /, $closer);
    spurt $tangle-file, $tangle-content;
    say "Tangled to $tangle-file";
  }
}