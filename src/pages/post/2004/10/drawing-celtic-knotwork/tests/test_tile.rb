require "minitest/autorun"
require "../knotwork/tile.rb"

class TestTile < Minitest::Test
  def setup
    @tile = Tile.new
  end

  def test_pixels
    refute @tile.is_set?(0, 0),
      "By default, any pixel in a Tile is blank"

    assert @tile.set(0, 0),
      "Use Tile#set(row, col) to set a pixel at coordinates (row, col)"

    assert @tile.is_set?(0, 0),
      "A pixel (row, col) is set after Tile#set(row, col) has been called"

    @tile.unset 0, 0
    refute @tile.is_set?(0, 0),
      "An unset pixel has no set value"

    @tile.set(1, 1)
    refute @tile.is_set?(0, 0),
      "Setting one pixel has no effect on other pixels in a Tile"

    assert @tile.is_set?(1, 1),
      "Tile remembers the set status of each pixel in its confines."
  end

  def test_set_from_string
    source_string =<<~HERE.strip
      x . . . . . . . x
      . x . . . . . x .
      . . x . . . x . .
      . . . x . x . . .
      . . . . x . . . .
      . . . x . x . . .
      . . x . . . x . .
      . x . . . . . x .
      x . . . . . . . x
    HERE

    assert @tile.set_from_string(source_string),
      "You can use ASCII art strings to set the pixels in a Tile"

    assert @tile.is_set?(0, 0)
    assert @tile.is_set?(1, 0)

    assert_equal 'x', @tile.at(0, 0),
      "A Tile remembers the value assigned, if given, during Tile#set(row, col, val)"
  end
end