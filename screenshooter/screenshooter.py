"""
Usage:
    screnshooter  [options] [FILE]

Arguments:
    FILE       📄 optional input file

Options:
    -h --help   👷 show this message and exit
    --version   🎱 show version and exit
    -i          📺 input video
    -v          🚧 verbose mode
    -r          ⏰ framerate


🐍(python) takes 🎬(video) from 📥(input) 📂(folder) ... makes 📸 🎆🎇🌅🌄🌆🌇🌉🌌🌠(screenshots)...

All the while... trying to maxmize the screenshot quality behind-the-scenes-like.

🎃____________________🎃
 :Python: >= python 3.6
 :Updated: 10.30.2019

"""

# from docopt import docopt
import argparse
import subprocess
import datetime
from typing import List
from pathlib import Path, PurePath

# _________________________ Logging setup  _________________________
import sys
from loguru import logger

# For scripts
config = {
    "handlers": [
        {"sink": sys.stdout, "format": "{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}"},
        {"sink": "screenshooter.log",
            "format": "{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}"},
    ],
    "extra": {"user": "someone"}
}
logger.configure(**config)

# For libraries
logger.disable("my_library")
logger.info("No matter added sinks, this message is not displayed")
logger.enable("my_library")
logger.info("This message however is propagated to the sinks")


BASE_DIR = Path(__file__).resolve().parent.parent



class shooter:
    def __init__(self):
        self.BASE_DIR = Path(__file__).resolve().parent.parent
        self.INPUT_VID = self.vidInput(args["FILE"])
        self.fileName = PurePath(self.INPUT_VID).stem

    def main(self):
        logger.info("\n🚀\n...\nHere we go\n...\n")

        OUTPUT_DIR = make_output_dir(self.fileName)

        ouput_str = str(OUTPUT_DIR.joinpath(
            f"{self.fileName}_Screenshot-%04d.jpg"))

        cmd: List[str] = [
            "ffmpeg",
            "-i",
            str(self.INPUT_VID),
            "-framerate",
            str(INPUT_FPS),
            ouput_str,
            "-an",
            "-y",
        ]

        if args["-v"]:
            # These are ffmpeg verbose commands
            cmd.append("-report")
            cmd.append("-stats")

        try:
            completed = subprocess.run(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
                shell=False,
            )

            if completed.returncode == 0:
                print("\n🎯⭐️✨🌟🌈 Complete! 🏅🏆🥇🎖\n")
            else:
                print(f"\n🎃 Return code: {completed.returncode}")

            if args["-v"]:
                print(f"Bytes in stdout: {len(completed.stdout)}")
                _stdout = completed.stdout.decode("utf-8")
                print(f"stdout: {_stdout}")

                _stderr = completed.stderr.decode("utf-8")
                print(f"stderr: {_stderr}")

        except subprocess.CalledProcessError as err:
            print("\n🎃    ‼️ Error in your subprocess command‼️    🎃\n")
            exit(err)

    def vidInput(self, file):
        INPUT_DIR = self.BASE_DIR.joinpath("input")

        if args["FILE"] is None:
            INPUT_VID = INPUT_DIR.joinpath("test_input_30frames.mp4")
            print(
                "\n🏴‍☠️ 🏴‍☠️ 🏴‍☠️ ☠️  Argh!.. Aye Captain, using default video...  ☠️  🏴‍☠️ 🏴‍☠️ 🏴‍☠️"
            )
        else:
            INPUT_VID = INPUT_DIR.joinpath(args["FILE"])

        fileName = PurePath(INPUT_VID).stem
        fileExt = PurePath(INPUT_VID).suffix
        print(f"\n      📃 {fileName}       🔖 {fileExt}\n")
        print(f"\n      ↪  {INPUT_VID}\n")

        return INPUT_VID


def make_output_dir(fileName):

    OUTPUT_DIR = BASE_DIR.joinpath("output")
    new_dir = OUTPUT_DIR.joinpath(fileName)

    try:
        Path.mkdir(new_dir)
        OUTPUT_DIR = OUTPUT_DIR.joinpath(fileName)

    except FileNotFoundError as e:
        print("A missing parent folder - problem in the path.")
        exit(e)

    except FileExistsError as e:
        print("The file already exists")

        if OVERWRITE_OUTPUT:
            Path.mkdir(new_dir, exist_ok=True)
            OUTPUT_DIR = OUTPUT_DIR.joinpath(fileName)
        else:
            exit(e)

    return OUTPUT_DIR


if __name__ == "__main__":
    # args = docopt(__doc__)
    ses = shooter()
    ses.main()
