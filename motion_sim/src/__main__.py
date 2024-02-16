from src.config import Config as conf
import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        filename = "assets/config/default.json"
    else:
        filename = "assets/config/" + sys.argv[1]
    config = {}
    conf.load_config(filename, config)
    # print(config)
