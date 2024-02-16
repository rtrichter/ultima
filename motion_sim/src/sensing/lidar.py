# from src.config import Config as conf
from src.track.pixel_type import PixelTypes, PixelType
import numpy as np


class Lidar:

    __slots__ = [
        "__RPM",            # rpm
        "__resolution",     # degrees
        "__range"           # pixels
        "__thetas"          # array of angles in radians
    ]

    RPM2RESOLUTION = {
        300: 0.1,
        600: 0.2,
        900: 0.3,
        1200: 0.4
    }

    def __init__(self, range, RPM=None, resolution=None):
        if (RPM is None) and (resolution is None):
            raise ValueError("""Must pass exactly one of either
                RPM or resolution: Received neither""")
        if (RPM is None) and (resolution is None):
            raise ValueError("""Must pass exactly one of either
                RPM or resolution: Received both""")
        if not (RPM is None):
            self.__RPM = RPM
            self.__resolution = Lidar.RMP2RESOLUTION[RPM]
        elif not (resolution is None):
            keys = list(Lidar.RPM2RESOLUTION.keys())
            index = Lidar.RPM2RESOLUTION.values().index(resolution)
            self.__RPM = keys[index]
            self.__resolution = resolution
        self.__thetas = np.linspace(-np.pi, np.pi, self.__resolution)

    def get_polar_coords(
            self,
            x: int,
            y: int,
            heading: float,
            track: np.ndarray,
            config: dict
            ) -> np.ndarray:
        radii = []
        weight = []
        for i in range(self.__thetas.size):
            for r in range(self.__range):
                if r == self.__range - 1:
                    radii.append(self.__range)
                    weight.append(PixelTypes.TARGET)
                    break

                x = int(x + r * np.cos(heading + self.__thetas[i]))
                y = int(y + r * np.sin(heading + self.__thetas[i]))

                if abs(x) >= track[0].size or abs(y) >= track.size:
                    radii.append(r)
                    weight.append(PixelTypes.OBSTACLE)
                    break

                w = PixelType.get_weight(track[y][x])

                if w == PixelType.NULL:
                    continue

                radii.append(r)
                weight.append(w)
                break
