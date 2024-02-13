from PIL import Image
from enum import Enum
import numpy as np
import cv2
import time

N_CONE_SAMPLES = 50
R_MAX = 400
THETA_MAX = 80 * np.pi / 180
THETA = np.linspace(-THETA_MAX, THETA_MAX, N_CONE_SAMPLES)

WIDTH = 400
HEIGHT = 400


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


# def get_target_direction(
#         theta: np.ndarray((N_CONE_SAMPLES), dtype=float),
#         r: np.ndarray((N_CONE_SAMPLES), dtype=float),
#         weight: np.ndarray((N_CONE_SAMPLES), dtype=float),
#         r_max: int = R_MAX
#         ) -> float:
#     ratio_sum = 0
#     r_total = 0
#     for i in range(N_CONE_SAMPLES):
#         r_total += r[i]
#         if (r[i] == 0) or (r[i] >= r_max):
#             continue
#         print(weight[i])
#         ratio_sum += weight[i].value[0] * theta[i] / r[i]
#     return ratio_sum * r_total / N_CONE_SAMPLES
def get_target_direction(
        theta: np.ndarray((N_CONE_SAMPLES), dtype=float),
        r: np.ndarray((N_CONE_SAMPLES), dtype=float),
        weight: np.ndarray((N_CONE_SAMPLES), dtype=float),
        r_max: int = R_MAX
        ) -> float:
    max_r = 0
    location = 0
    for i in range(N_CONE_SAMPLES - 15):
        local_avg = sum(r[i:i+15]) / 15
        if local_avg > max_r:
            max_r = local_avg
            location = i+2
    return theta[location]


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
            if r == R_MAX:
                radii[i].append(R_MAX)
                weight[i].append(PixelType.NULL)
                continue
            x = int(bot_xy[0] + r * np.cos(bot_dir + theta[i]))
            y = int(bot_xy[1] + r * np.sin(bot_dir + theta[i]))
            if track[y][x] == 188:
                continue
            w = Pixel.get_weight(track[y][x])
            if w == PixelType.NULL:
                # track[y][x] = 128
                continue
            radii.append(r)
            weight.append(w)
            break
    return np.array((radii, weight))


def traverse():
    STEP_SIZE = 5
    track = init_track("assets/frog.png")
    # bot_xy = (263, 144)
    bot_xy = [198, 116]
    bot_dir = 0
    while True:
        cv2.imshow("traversing", track)
        cv2.waitKey(0)
        polar = get_polar_coords(THETA, bot_xy, track, bot_dir)
        direction = get_target_direction(THETA, polar[0], polar[1])
        for i in range(STEP_SIZE):
            x = int(bot_xy[0] + i * np.cos(direction + bot_dir))
            y = int(bot_xy[1] + i * np.sin(direction + bot_dir))
            print(x, y)
            track[y][x] = 188
            track[y+1][x] = 188
        bot_xy[0] = bot_xy[0] + STEP_SIZE * np.cos(direction + bot_dir)
        bot_xy[1] = bot_xy[1] + STEP_SIZE * np.sin(direction + bot_dir)
        bot_dir += direction
        print(bot_dir)
    cv2.destroyAllWindows()


def main():
    traverse()
    # track = init_track("assets/frog.png")
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
