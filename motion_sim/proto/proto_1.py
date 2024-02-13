# FROZEN ON 2/13
# DO NOT EDIT

from enum import Enum
import numpy as np
import cv2
import time
import json

import sys

N_CONE_SAMPLES = 50
R_MAX = 100
THETA_MAX = 100 * np.pi / 180
THETA = np.linspace(-THETA_MAX, THETA_MAX, N_CONE_SAMPLES)

WIDTH = 400
HEIGHT = 400

STEP_SIZE = 5
DIR_SCALAR = 5


class PixelType(Enum):
    OBSTACLE = -1,
    NULL = 0,
    TARGET = 1


# maybe unecessary encapsulation
class Pixel:

    HEX2PIXELTYPE = {
        0: PixelType.OBSTACLE,
        255: PixelType.NULL,
        129: PixelType.OBSTACLE,
        117: PixelType.TARGET,
        99: PixelType.OBSTACLE,
        127: PixelType.OBSTACLE,
        188: PixelType.NULL
    }

    @classmethod
    def get_weight(cls, rgb: int) -> PixelType:
        return cls.HEX2PIXELTYPE[rgb]


# def init_track(filename: str) -> np.ndarray:
#     img = Image.open(filename)
#     hex = img.convert("RGB")
#     img.show()
#     return np.asarray(hex).copy()
#

def init_track(filename: str) -> np.ndarray:
    return cv2.imread(filename, cv2.IMREAD_UNCHANGED)


def get_target_direction(
        theta: np.ndarray((N_CONE_SAMPLES), dtype=float),
        r: np.ndarray((N_CONE_SAMPLES), dtype=float),
        weight: np.ndarray((N_CONE_SAMPLES), dtype=float),
        r_max: int = R_MAX
        ) -> float:
    ratio_sum = 0
    r_total = 0
    for i in range(N_CONE_SAMPLES):
        r_total += r[i]
        if (r[i] == 0) or (r[i] >= r_max):
            continue
        sign = theta[i] / abs(theta[i])
        angle_part = sign / N_CONE_SAMPLES
        ratio_sum += angle_part * r[i] / R_MAX
        # ratio_sum += weight[i].value[0] * theta[i] / r[i]
    # print(ratio_sum)
    return ratio_sum * DIR_SCALAR

# def get_target_direction(
#         theta: np.ndarray((N_CONE_SAMPLES), dtype=float),
#         r: np.ndarray((N_CONE_SAMPLES), dtype=float),
#         weight: np.ndarray((N_CONE_SAMPLES), dtype=float),
#         r_max: int = R_MAX
#         ) -> float:
#     max_r = 0
#     location = 0
#     for i in range(N_CONE_SAMPLES - 15):
#         local_avg = sum(r[i:i+15]) / 15
#         if local_avg > max_r:
#             max_r = local_avg
#             location = i+2
#     return theta[location]


def get_polar_coords(
        theta: np.ndarray((N_CONE_SAMPLES)),
        bot_xy: tuple[int, int],
        track: np.ndarray((HEIGHT, WIDTH)),
        bot_dir: float
        ) -> np.ndarray((2, N_CONE_SAMPLES)):
    radii = []
    weight = []
    for i in range(theta.size):
        # cv2.imshow("title", track)
        # cv2.waitKey(0)
        for r in range(R_MAX):
            if r == R_MAX-1:
                radii.append(R_MAX)
                weight.append(PixelType.TARGET)
                break
            x = int(bot_xy[0] + r * np.cos(bot_dir + theta[i]))
            y = int(bot_xy[1] + r * np.sin(bot_dir + theta[i]))
            if abs(x) >= WIDTH or abs(y) >= HEIGHT:
                radii.append(r)
                weight.append(PixelType.NULL)
                break
            if track[y][x] == 188:
                continue
            w = Pixel.get_weight(track[y][x])
            if w == PixelType.NULL:
                # track[y][x] = 128
                continue
            radii.append(r)
            weight.append(w)
            break
        # print(f"{i}: {r}, {R_MAX}")
    return np.array((radii, weight))


def traverse(bot_xy, bot_dir):
    track = init_track("assets/frog.png")
    while True:
        cv2.imshow("traversing", track)
        cv2.waitKey(0)
        polar = get_polar_coords(THETA, bot_xy, track, bot_dir)
        direction = get_target_direction(THETA, polar[0], polar[1])
        for i in range(STEP_SIZE):
            x = int(bot_xy[0] + i * np.cos(direction + bot_dir))
            y = int(bot_xy[1] + i * np.sin(direction + bot_dir))
            # print(x, y)
            track[y][x] = 188
            track[y+1][x] = 188
        bot_xy[0] = bot_xy[0] + STEP_SIZE * np.cos(direction + bot_dir)
        bot_xy[1] = bot_xy[1] + STEP_SIZE * np.sin(direction + bot_dir)
        bot_dir += direction
        # print(bot_dir)
    cv2.destroyAllWindows()


def show_cone(track, bot_xy, bot_dir, theta):
    STEP_SIZE = 5
    while True:
        cv2.imshow("traversing", track)
        polar = get_polar_coords(THETA, bot_xy, track, bot_dir)
        direction = get_target_direction(THETA, polar[0], polar[1])

        track[bot_xy[0]][bot_xy[1]] = 0
        track[bot_xy[0]+1][bot_xy[1]] = 0
        track[bot_xy[0]][bot_xy[1]+1] = 0
        track[bot_xy[0]+1][bot_xy[1]+1] = 0

        for angle in (-THETA_MAX, direction, THETA_MAX):
            for i in range(STEP_SIZE):
                x = int(bot_xy[0] + i * np.cos(angle + bot_dir))
                y = int(bot_xy[1] + i * np.sin(angle + bot_dir))
                track[y][x] = 188
                track[y+1][x] = 188
        cv2.imshow("traversing", track)
        time.sleep(0.1)
        cv2.waitKey(0)
        track[bot_xy[0]][bot_xy[1]] = 255
        track[bot_xy[0]+1][bot_xy[1]] = 255
        track[bot_xy[0]][bot_xy[1]+1] = 255
        track[bot_xy[0]+1][bot_xy[1]+1] = 255
        for angle in (-THETA_MAX, direction, THETA_MAX):
            for i in range(STEP_SIZE*5):
                x = int(bot_xy[0] + i * np.cos(angle + bot_dir))
                y = int(bot_xy[1] + i * np.sin(angle + bot_dir))
                track[y][x] = 255
                track[y+1][x] = 255
        bot_xy[0] = int(bot_xy[0] + STEP_SIZE * np.cos(direction + bot_dir))
        bot_xy[1] = int(bot_xy[1] + STEP_SIZE * np.sin(direction + bot_dir))
        bot_dir += direction
    cv2.destroyAllWindows()


# ugly function but lets me freeze this file and run everything from config
def traverse_with_config(config):
    global WIDTH
    global HEIGHT
    global N_CONE_SAMPLES
    global R_MAX
    global THETA_MAX
    global STEP_SIZE
    global THETA
    global DIR_SCALAR
    WIDTH = config["WIDTH"]
    HEIGHT = config["HEIGHT"]
    N_CONE_SAMPLES = config["N_CONE_SAMPLES"]
    R_MAX = config["R_MAX"]
    THETA_MAX = config["THETA_MAX"] * np.pi / 180
    STEP_SIZE = config["STEP_SIZE"]
    DIR_SCALAR = config["DIR_SCALAR"]
    THETA = np.linspace(-THETA_MAX, THETA_MAX, N_CONE_SAMPLES)
    traverse([config["bot_x"], config["bot_y"]], config["bot_dir"] * np.pi / 180)


def main():
    filename = sys.argv[-1]
    with open(filename) as f:
        config = json.load(f)
    traverse_with_config(config)

    # traverse([200, 120], 0)

    # track = init_track("assets/frog.png")
    # show_cone(track, [198, 116], 0)
    # # cv2.imshow("initial", track)
    # # cv2.waitKey(0)
    # # bot_xy = (263, 144)
    # bot_xy = (198, 116)
    # polar = get_polar_coords(THETA, bot_xy, track)
    # direction = get_target_direction(THETA, polar[0], polar[1])
    # print(direction)
    # cv2.imshow("initial", track)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # # img = Image.fromarray(track).convert("RGB")
    # # img.show()


if __name__ == "__main__":
    main()
