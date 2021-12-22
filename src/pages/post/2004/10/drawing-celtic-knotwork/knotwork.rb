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

def main
  rows = 1
  columns = 1

  opts = OptionParser.new do |opts|
    opts.banner = "Usage #{$0} |opts|"
    opts.separator ""
    opts.separator "Specific Options"

    opts.on("-r", "--rows [ROWS]",
            "Number of rows for this panel (default 1)") do |r|
      rows = r.to_i
      columns = rows
    end

    opts.on("-c", "--columns [COLUMNS]",
            "Number of columns for this panel (default ROWS)") do |c|
      columns = c.to_i
    end

    opts.on_tail("-h", "--help",
                 "Show this message") do
      puts opts
      exit
    end
  end

  opts.parse!

  panel = KnotworkPanel.new(rows, columns)
  panel.to_image()
end

main