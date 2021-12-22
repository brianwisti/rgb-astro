require "minitest/autorun"
require "../knotwork/knotwork_panel"

class TestKnotworkPanel < Minitest::Test
  def test_ascii
    panel = KnotworkPanel.new(1)
    expected_lines =<<~HERE.strip.split "\n"
      . . . . x x x x x x x . . . . . x x x x x x x . . . .
      . . . . x . . . . . . x x . x x . . . . . . x . . . .
      . . . . x . . . . . . . . x . . . . . . . . x . . . .
      . . . . x . . . x x x . . . x . x x x . . . x . . . .
      . . . . x . . x . . . x . . . x . . . x . . x . . . .
      . . . . x . . x . . x . x . . . x . . x . . x . . . .
      . . . . . x . . x x . . . x . . . x x . . x . . . . .
      . . . . . x . . x . . . x . x . . x . . . x . . . . .
      . . . . . . x x . . . x . . . x x . . . x . . . . . .
      . . . . . . x . . . . x . . . x . . . x x . . . . . .
      . . . . . x . . . . x . x . x . . . x . . x . . . . .
      . . . . . x . . . x . . . x . . . x x . . x . . . . .
      . . . . x . . . x . x . . . x . x . . x . . x . . . .
      . . . . x . . x . . . x . . . x . . . x . . x . . . .
      . . . . x . . x . . x . x . . . x . . x . . x . . . .
      . . . . . x . . x x . . . x . . . x x . . x . . . . .
      . . . . . x . . x . . . x . x . x . . . . x . . . . .
      . . . . . . x x . . . x . . . x . . . . x . . . . . .
      . . . . . . x . . . x x . . . x . . . x x . . . . . .
      . . . . . x . . . x . . x . x . . . x . . x . . . . .
      . . . . . x . . x x . . . x . . . x x . . x . . . . .
      . . . . x . . x . . x . . . x . x . . x . . x . . . .
      . . . . x . . x . . . x . . . x . . . x . . x . . . .
      . . . . x . . . x x x . x . . . x x x . . . x . . . .
      . . . . x . . . . . . . . x . . . . . . . . x . . . .
      . . . . x . . . . . . x x . x x . . . . . . x . . . .
      . . . . x x x x x x x . . . . . x x x x x x x . . . .
    HERE

    output_lines = panel.to_aa.split "\n"
    expected_lines.each_with_index do |line, i|
      assert_equal line, output_lines[i],
        "line #{i} doesn't match"
    end
  end

  def test_large_panels
    expected =<<~HERE.strip
      . . . . x x x x x x x . . . . . x x x x x x x . . . .
      . . . . x . . . . . . x x . x x . . . . . . x . . . .
      . . . . x . . . . . . . . x . . . . . . . . x . . . .
      . . . . x . . . x x x . . . x . x x x . . . x . . . .
      . . . . x . . x . . . x . . . x . . . x . . x . . . .
      . . . . x . . x . . x . x . . . x . . x . . x . . . .
      . . . . . x . . x x . . . x . . . x x . . x . . . . .
      . . . . . x . . x . . . x . x . . x . . . x . . . . .
      . . . . . . x x . . . x . . . x x . . . x . . . . . .
      . . . . . . x . . . . x . . . x . . . x x . . . . . .
      . . . . . x . . . . x . x . x . . . x . . x . . . . .
      . . . . . x . . . x . . . x . . . x x . . x . . . . .
      . . . . x . . . x . x . . . x . x . . x . . x . . . .
      . . . . x . . x . . . x . . . x . . . x . . x . . . .
      . . . . x . . x . . x . x . . . x . . x . . x . . . .
      . . . . . x . . x x . . . x . . . x x . . x . . . . .
      . . . . . x . . x . . . x . x . x . . . . x . . . . .
      . . . . . . x x . . . x . . . x . . . . x . . . . . .
      . . . . . . x . . . . x . . . x . . . x x . . . . . .
      . . . . . x . . . . x . x . x . . . x . . x . . . . .
      . . . . . x . . . x . . . x . . . x x . . x . . . . .
      . . . . x . . . x . x . . . x . x . . x . . x . . . .
      . . . . x . . x . . . x . . . x . . . x . . x . . . .
      . . . . x . . x . . x . x . . . x . . x . . x . . . .
      . . . . . x . . x x . . . x . . . x x . . x . . . . .
      . . . . . x . . x . . . x . x . x . . . . x . . . . .
      . . . . . . x x . . . x . . . x . . . . x . . . . . .
      . . . . . . x . . . x x . . . x . . . x x . . . . . .
      . . . . . x . . . x . . x . x . . . x . . x . . . . .
      . . . . . x . . x x . . . x . . . x x . . x . . . . .
      . . . . x . . x . . x . . . x . x . . x . . x . . . .
      . . . . x . . x . . . x . . . x . . . x . . x . . . .
      . . . . x . . . x x x . x . . . x x x . . . x . . . .
      . . . . x . . . . . . . . x . . . . . . . . x . . . .
      . . . . x . . . . . . x x . x x . . . . . . x . . . .
      . . . . x x x x x x x . . . . . x x x x x x x . . . .
    HERE

    output_lines = KnotworkPanel.new(2, 1).to_aa.split "\n"
    expected.split("\n").each_with_index do |line, i|
      assert_equal line, output_lines[i],
        "line #{i} doesn't match"
    end
  end
end