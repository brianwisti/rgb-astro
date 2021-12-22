#!/usr/bin/env python3
"""
Utility script to draw concentric circle templates for drawing
"""

import argparse

from PIL import Image, ImageDraw

DEFAULT_SIZE = 600
DEFAULT_CIRCLES = 10
DEFAULT_SLICES = 12


class CircleTemplate:
    """
    Draws a circle template
    """

    def __init__(self, size, circle_count, slice_count):
        self.size = size
        self.circle_count = circle_count
        self.slice_count = slice_count
        self.midpoint = int(size / 2)
        self.image = Image.new(mode="L", size=(size, size), color=255)
        self._draw()

    def save(self):
        """Write my circle template image to file"""
        filename = "circle-{}-{}-{}.png".format(
            self.size, self.circle_count, self.slice_count
        )
        print("Saving {}".format(filename))
        self.image.save(filename)

    def show(self):
        """Display my circle template image on screen"""
        self.image.show()

    def _draw(self):
        """Create circles and slices in-memory"""
        draw = ImageDraw.Draw(self.image)
        largest_circle = self._draw_circles(draw)
        self._draw_slices(draw, largest_circle)
        del draw

    def _draw_circles(self, draw):
        if self.circle_count <= 0:
            return 0

        radius_step = int(self.midpoint / self.circle_count)
        last_radius = 0

        for radius in range(0, self.midpoint, radius_step):
            bounding_box = [
                (self.midpoint - radius, self.midpoint - radius),
                (self.midpoint + radius, self.midpoint + radius),
            ]
            draw.arc(bounding_box, 0, 360)
            last_radius = radius

        return last_radius

    def _draw_slices(self, draw, radius):
        if self.slice_count <= 0:
            return

        pie_box = [
            (self.midpoint - radius, self.midpoint - radius),
            (self.midpoint + radius, self.midpoint + radius),
        ]
        angle = 360 / self.slice_count
        start_angle = 0

        for pieslice in range(1, self.slice_count):
            end_angle = angle * pieslice
            draw.pieslice(pie_box, start_angle, end_angle)


def main():
    """Create a circle template from command line options"""
    # Get details from command line or use defaults
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--size", help="length of image side in pixels", type=int, default=DEFAULT_SIZE
    )
    parser.add_argument(
        "--circles", help="number of circles", type=int, default=DEFAULT_CIRCLES
    )
    parser.add_argument(
        "--slices", help="number of slices", type=int, default=DEFAULT_SLICES
    )
    args = parser.parse_args()
    size = args.size
    circle_count = args.circles
    slice_count = args.slices
    circle_template = CircleTemplate(size, circle_count, slice_count)
    circle_template.save()


if __name__ == "__main__":
    main()
