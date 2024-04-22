from typing import Tuple


class Pixel(int):
    pass


class RGB(Tuple[int, int, int, int | None]):
    pass


class RGB01(Tuple[int, int, int, int | None]):
    pass


class HEX(str):
    pass
