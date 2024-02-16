import numpy as np
import cv2
import json
from enum import Enum


class Config:

    WIDTH = "WIDTH"
    HEIGHT = "HEIGHT"
    N_CONE_SAMPLES = "N_CONE_SAMPLES"
    R_MAX = "R_MAX"
    THETA_MAX = "THETA_MAX"
    STEP_SIZE = "STEP_SIZE"
    DIR_SCALAR = "DIR_SCALAR"
    X_INITIAL = "X_INITIAL"
    Y_INITIAL = "Y_INITIAL"
    THETA_INITIAL = "THETA_INITIAL"
    TRACK_FILENAME = "TRACK_FILENAME"
    TRACK = "TRACK"

    @staticmethod
    def get_track(filename: str) -> np.ndarray:
        return cv2.imread(filename, cv2.IMREAD_UNCHANGED)

    @staticmethod
    def load_config(filename: str, config: dict()) -> None:
        with open(filename) as f:
            loaded = json.load(f)
        config[Config.WIDTH] = loaded[Config.WIDTH]
        config[Config.HEIGHT] = loaded[Config.HEIGHT]
        config[Config.N_CONE_SAMPLES] = loaded[Config.N_CONE_SAMPLES]
        config[Config.R_MAX] = loaded[Config.R_MAX]
        config[Config.THETA_MAX] = loaded[Config.THETA_MAX] * np.pi / 180
        config[Config.STEP_SIZE] = loaded[Config.STEP_SIZE]
        config[Config.DIR_SCALAR] = loaded[Config.DIR_SCALAR]
        config[Config.X_INITIAL] = loaded[Config.X_INITIAL]
        config[Config.Y_INITIAL] = loaded[Config.Y_INITIAL]
        config[Config.THETA_INITIAL] = loaded[Config.THETA_INITIAL] * np.pi / 180
        config[Config.TRACK_FILENAME] = loaded[Config.TRACK_FILENAME] * np.pi / 180
        config[Config.TRACK] = Config.get_track(loaded[Config.TRACK_FILENAME])


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
    def get_weight(cls, bgr: int) -> PixelTypes:
        return cls.INT_2_PIXEL_TYPE[bgr]

class Lidar:
    
    __slots__ = [
        
    ]


class Bot:

    __slots__ = [
        "__x", "__y", "__heading"
    ]

    @classmethod
    def from_config(cls, config: dict):
        return cls(config[Config.X_INITIAL],
                   config[Config.Y_INITIAL],
                   config[Config.HEADING_INITIAL])

    def __init__(self, x: int, y: int, heading: float) -> None:
        self.__x = x
        self.__y = y
        self.__heading = heading

    def get_polar_coordinates() -> np.ndarray:
        pass


if __name__ == '__main__':
    # config = {}
    # Config.load_config("assets/proto_1.config.json", config)
    # print(config)
    b = Bot(10, 10, 0)
    b.Sensing.speak()
