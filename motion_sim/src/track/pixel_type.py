from enum import Enum


class PixelTypes(Enum):
    OBSTACLE = -1,
    NULL = 0,
    TARGET = 1


class PixelType:
    INT_2_PIXEL_TYPE = {
        (0, 0, 0): PixelTypes.OBSTACLE,
        (255, 255, 255): PixelTypes.NULL
    }

    @classmethod
    def get_weight(cls, bgr: tuple) -> PixelTypes:
        if type(bgr) is not tuple:
            bgr = tuple(bgr)
        return cls.INT_2_PIXEL_TYPE[bgr]
