require './knotwork/knotwork_panel.rb'

require 'rmagick'
include Magick

class KnotworkPanel
  def to_image()
    filename = "panel-#{@row_size}x#{@col_size}.png"

    max_x = 9 * @row_size
    max_y = 9 * @col_size

    image = Image.new(max_x, max_y) { self.background_color = "white" }
    (0...max_y).each do |y|
      (0...max_x).each do |x|
        pixel = @grid.at(x, y)
        if pixel == "x" then
          image.pixel_color(x, y, "black")
        end
      end
    end
    image.write(filename)
  end
end

panel = KnotworkPanel.new(8, 18)
panel.to_image()