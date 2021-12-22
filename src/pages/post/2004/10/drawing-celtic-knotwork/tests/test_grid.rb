require "minitest/autorun"
require "../knotwork/grid"

class TestGrid < Minitest::Test
  def setup
    @source_string =<<~HERE.strip
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
  end

  def test_simple_grid
    grid = Grid.new 1, 1
    tile = Tile.new @source_string
    grid.set_tile 0, 0, tile
    assert_equal "x", grid.at(0, 0),
      "pixel_at fetches contents from pixel coordinates"

    assert_equal @source_string, grid.to_s
  end

  def test_large_grid
    grid = Grid.new 1, 2
    tile1 = Tile.new @source_string
    tile2 = Tile.new @source_string
    grid.set_tile 0, 0, tile1
    grid.set_tile 0, 1, tile2
    assert_equal "x", grid.at(0, 9),
      "pixel_at fetches from anywhere in the Grid."

    expected_output =<<~HERE.strip
      x . . . . . . . x x . . . . . . . x
      . x . . . . . x . . x . . . . . x .
      . . x . . . x . . . . x . . . x . .
      . . . x . x . . . . . . x . x . . .
      . . . . x . . . . . . . . x . . . .
      . . . x . x . . . . . . x . x . . .
      . . x . . . x . . . . x . . . x . .
      . x . . . . . x . . x . . . . . x .
      x . . . . . . . x x . . . . . . . x
    HERE

    assert_equal expected_output, grid.to_s
  end
end