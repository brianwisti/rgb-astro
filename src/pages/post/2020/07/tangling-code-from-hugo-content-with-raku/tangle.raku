sub MAIN() {
  my $filename = "index.md";
  my $opener = '{{< ';
  my $closer = ' >}}';
  my regex shortcode {
    $opener
      code \s
      'file="' $<filename> = .+? '"'  # Remember the filename
      .*?
    $closer
    \n                # Ignore leading newline
    $<content> = .+?  # Remember everything else in the block
    \n                # Ignore leading newline
    $opener '/code' $closer
  }

  my $markdown = slurp $filename;

  if $markdown.match(/ <shortcode> /) {
    my $tangle-file = $/<shortcode><filename>;
    my $tangle-content = $/<shortcode><content>;
    spurt $tangle-file, $tangle-content;
    say "Tangled to $tangle-file";
  }
}