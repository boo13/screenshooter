"""
Usage:
    screnshooter  [options] [FILE]
    screnshooter -h | --help
    screnshooter --version

Arguments:
    FILE       📄 optional input file

Options:
    -h --help                       👷 show this message and exit
    --version                       🎱 show version and exit
    -i                              📺 input video
    -v                              🚧 verbose mode
    --framerate=<n>                 1 is a frame a second, 60 is a frame a minute, 0 disables the video filter and outputs every frame [default: 1]
    -r                              ⏰ framerate
    --overwrite_output              If files already exist, overwrite them? [default: False]
    --add_to_output                 If an output folder for the video already exists, create a new folder [default: False]


🐍(python) takes 🎬(video) from 📥(input) 📂(folder) and makes 📸 🎆🎇🌅🌄🌆🌇🌉🌌🌠(screenshots).

All the while... trying to maxmize the screenshot quality behind-the-scenes-like.

🎃____________________🎃
 :Python: >= python 3.6
 :Updated: 06.14.2020
"""

# _________________________ Imports  _________________________
import sys

# Local
from version import __version__
from timer import Timer
import screenshooter

#
import subprocess
from docopt import docopt
from typing import List
from pathlib import Path, PurePath

# _________________________ Logging setup  _________________________
from loguru import logger

config = {
    "handlers": [
        {
            "sink": sys.stdout,
            # "level": 'DEBUG'
            "format": "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
            # "format": "<green>{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}</green>",
        },
        {
            "sink": "screenshooter.log",
            "format": "{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
        },
    ],
    "extra": {"user": "someone"},
}
logger.configure(**config)


# _________________________ Run It  _________________________

if __name__ == "__main__":
    args = docopt(__doc__, version=__version__)

    screenshooter.Screenshooter(
        input_video=args["FILE"],
        verbose=args["-v"],
        fps=float(args["--framerate"]),
        overwrite_output=args["--overwrite_output"],
    )
