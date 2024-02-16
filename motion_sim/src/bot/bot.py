from src.config import Config


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
