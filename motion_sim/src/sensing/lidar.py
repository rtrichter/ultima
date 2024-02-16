from src.config import Config as conf

class Lidar:

    __slots__ = [
        "__RPM",
        "__resolution"
    ]

    RPM2RESOLUTION = {
        300: 0.1,
        600: 0.2,
        900: 0.3,
        1200: 0.4
    }

    def __init__(self, RPM=None, resolution=None):
        if (RPM is None) and (resolution is None):
            raise ValueError("""Must pass exactly one of either
                RPM or resolution: Received neither""")
        if (RPM is None) and (resolution is None):
            raise ValueError("""Must pass exactly one of either
                RPM or resolution: Received both""")
        if not (RPM is None):
            self.RPM = RPM
            self.resolution = Lidar.RMP2RESOLUTION[RPM]
        elif not (resolution is None):
            keys = list(Lidar.RPM2RESOLUTION.keys())
            index = Lidar.RPM2RESOLUTION.values().index(resolution)
            self.RPM = keys[index]
            self.resolution = resolution

    def get_polar_coordinates(
            self, x: int, y: int, heading: float, track: np.ndarray, config: dict
            ) -> np.ndarray:
        radii = []
        weight = []
        theta = np.linspace(-np.pi, np.pi, self.resolution)
        for i in range(theta.size):
            for r in range(config[conf.R_MAX])
