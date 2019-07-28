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
 :Updated: 07.28.2019

"""
import subprocess
from typing import List
from config import INPUT_FPS


class shooter:
    def __init__(self):
        from pathlib import Path, PurePath

        self.BASE_DIR = Path(__file__).resolve().parent.parent
        self.INPUT_VID = self.vidInput(args["FILE"])
        self.fileName = PurePath(self.INPUT_VID).stem

    def main(self):
        print("\n🚀\n...\nHere we go\n...\n")
        print("⏳\n")

        OUTPUT_DIR = make_output_dir(self.fileName)

        ouput_str = str(OUTPUT_DIR.joinpath(f"{self.fileName}_Screenshot-%04d.jpg"))

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

    def cli(self):
        pass

    def vidIn(self, file):
        return file


if __name__ == "__main__":

    from docopt import docopt

    args = docopt(__doc__)

    from pathlib import Path, PurePath

    from path_handler import make_output_dir

    ses = shooter()

    ses.main()

