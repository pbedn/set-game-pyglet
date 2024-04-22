# Colors from https://flatuicolors.com/palette/defo

from typing import Tuple


class Pixel(int):
    pass


class RGB(Tuple[int, int, int, int | None]):
    pass


class RGB01(Tuple[int, int, int, int | None]):
    pass


class HEX(str):
    pass


class CornerMargin:
    x: Pixel = 125
    y: Pixel = 50


class OutlineBox:
    size: Pixel = 1
    thickness: Pixel = 6
    # Color Peter River
    color: RGB = (52, 152, 219)


class BackgroundColor:
    # Color Wet Asphalt
    hex: HEX = '2c3e50'
    color: RGB = (44, 62, 80)
    rgb01: RGB01 = (0.204, 0.286, 0.369, 1.0)


class FontColor:
    # Color Clouds
    rgb: RGB = (236, 240, 241)


class Configuration:
    corner_margin: CornerMargin = CornerMargin()
    outline_box: OutlineBox = OutlineBox()
    font_color: FontColor = FontColor()


config = Configuration()
