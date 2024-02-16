import numpy as np
import cv2
import json


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
    THETA = "THETA"

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
        config[Config.TRACK_FILENAME] = loaded[Config.TRACK_FILENAME]
        config[Config.TRACK] = Config.get_track(loaded[Config.TRACK_FILENAME])
