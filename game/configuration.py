from game.custom import *


class CornerMargin:
    x: Pixel = 125
    y: Pixel = 50


class OutlineBox:
    size: Pixel = 1
    thickness: Pixel = 5
    color: RGBA = (67, 137, 194)


class Configuration:
    corner_margin: CornerMargin = CornerMargin()
    outline_box: OutlineBox = OutlineBox()


config = Configuration()
