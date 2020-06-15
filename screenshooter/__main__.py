"""
Usage:
    screnshooter  [options] [FILE]
    screnshooter -h | --help
    screnshooter --version

Arguments:
    FILE       📄 optional input file

Options:
    -h --help                               👷 show this message and exit
    --version                               🎱 show version and exit
    -i                                      📺 input video
    -v                                      🚧 verbose mode [default: True]
    -r                                      ⏰ framerate
    --overwrite_output                      If files already exist, overwrite them? [default: False]


🐍(python) takes 🎬(video) from 📥(input) 📂(folder) and makes 📸 🎆🎇🌅🌄🌆🌇🌉🌌🌠(screenshots).

All the while... trying to maxmize the screenshot quality behind-the-scenes-like.

🎃____________________🎃
 :Python: >= python 3.6
 :Updated: 06.14.2020
"""

# _________________________ Imports  _________________________
import sys
from version import __version__
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
            "format": "{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
        },
        {
            "sink": "screenshooter.log",
            "format": "{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
        },
    ],
    "extra": {"user": "someone"},
}
logger.configure(**config)

# _________________________ Main Class  _________________________


class Shooter:
    def __init__(self, fps=1, overwrite_output=False):
        # __________________ Class Vars  ___________________
        self.fps = fps
        self.overwrite = overwrite_output

        logger.info(
            f"Shooter starting with:\n\t\t\tVersion:{__version__}\n\t\t\tfps:{fps}\n\t\t\toverwrite output:{overwrite_output}"
        )

        # __________________ Set Paths  ___________________
        self.base_dir = Path(__file__).resolve().parent.parent
        self.input_dir = self.base_dir.joinpath("input")

        # __________________ Input Video  ___________________

        if args["FILE"] is None:
            for vid_file in self.input_dir.glob("*.avi"):
                self.input_video = vid_file
                logger.info(f"Video found inside of input folder: {self.input_video}")
                self.build_cmd()

            # self.input_video = self.input_dir.joinpath(
            #     "Big_Buck_Bunny_1080p_surround.avi"
            # )

        else:
            self.input_video = args["FILE"]
            logger.info(f"Using command-line submitted video: {self.input_video}")
            self.build_cmd()

    def make_output_dir(self, fileName):
        """[summary]

        Args:
            fileName ([type]): [description]

        Returns:
            Path: output_dir
        """
        output_dir = self.base_dir.joinpath("output")

        new_dir = output_dir.joinpath(fileName)

        try:
            Path.mkdir(new_dir)
            output_dir = output_dir.joinpath(fileName)

        except FileNotFoundError as e:
            logger.debug("A missing parent folder - problem in the path.")
            exit(e)

        except FileExistsError as e:
            logger.debug("The output folder already exists")

            if self.overwrite:
                Path.mkdir(new_dir, exist_ok=True)
                output_dir = output_dir.joinpath(fileName)
            else:
                logger.info("Exiting...")
                exit(e)

        return output_dir

    def build_cmd(self):
        """Build the Subprocess command and send it to 1send_subprocess_cmd`
        """

        # __________________ Set Output & Filename ___________________
        self.file_name = PurePath(self.input_video).stem
        self.output_dir = self.make_output_dir(self.file_name)

        logger.debug("Building command...")

        ouput_str = str(
            self.output_dir.joinpath(f"{self.file_name}_Screenshot-%04d.png")
        )

        cmd: List[str] = [
            "ffmpeg",
            "-i",
            str(self.input_video),
            # "-framerate",
            # str(self.fps),
            ## "-vcodec",
            ## "libx264",
            ## "-preset",
            ## "ultrafast",
            ouput_str,
            # "-an",
            # "-y",
        ]

        if args["-v"]:
            # These are ffmpeg verbose commands
            cmd.append("-report")
            cmd.append("-stats")

        self.send_subprocess_cmd(cmd)

    def send_subprocess_cmd(self, cmd):
        logger.debug(f"Sending subprocess command: {cmd}")

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
                logger.info("\n🎯⭐️✨🌟🌈 Complete! 🏅🏆🥇🎖\n")
            else:
                logger.info(f"\n🎃 Return code: {completed.returncode}")

            if args["-v"]:
                logger.info(f"Bytes in stdout: {len(completed.stdout)}")
                _stdout = completed.stdout.decode("utf-8")
                logger.info(f"stdout: {_stdout}")

                _stderr = completed.stderr.decode("utf-8")
                logger.info(f"stderr: {_stderr}")

        except subprocess.CalledProcessError as err:
            logger.info("\n🎃    ‼️ Error in your subprocess command‼️    🎃\n")
            exit(err)

        return


# _________________________ Run It  _________________________

if __name__ == "__main__":
    args = docopt(__doc__, version=__version__)

    logger.debug("\nStarting New Session..")

    shoot = Shooter(overwrite_output=args["--overwrite_output"])
