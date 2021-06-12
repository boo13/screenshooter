# _________________________ Imports  _________________________
# Local
from .timer import Timer

import subprocess
import numpy as np
from typing import List
from pathlib import Path, PurePath

# from pymediainfo import MediaInfo

# Kept getting error `RuntimeWarning: divide by zero encountered in log`
# This turns off that warning
np.seterr(divide="ignore")
from loguru import logger

# _________________________ Main Class  _________________________


class ProcessVideo:
    def __init__(self, input_folder, fps, overwrite, postprocess):
        # Import Vars to Self
        self.input_folder = input_folder
        self.fps = fps
        self.overwrite = overwrite
        self.postprocess = postprocess

        # Setup Internally used bits
        self.base_dir = Path(__file__).resolve().parent.parent
        self.timer = Timer()

        # Build video file list
        self.input_videos = self.build_input_video_list(input_folder)
        self.run(self.input_videos)

    def run(self, video_files):
        # For each of those videos we send a `subprocess` command
        for video in video_files:
            # Media Info
            # media_info = MediaInfo.parse(video)
            # for track in media_info.tracks:
            #     print(track)
            # Send Command
            self.build_cmd(video)

    def build_input_video_list(self, input):
        if input is None:
            # Get list of videos in the `input` folder
            video_file_list = self.get_video_files(
                input_dir=self.base_dir.joinpath("input")
            )
            logger.info(f"Video file List: {video_file_list}")
        else:
            video_file_list = [input]
            logger.info(f"Using command-line submitted video: {input}")

        return video_file_list

    def get_video_files(self, input_dir):
        """From a directory, return a list of video file paths, sorted based on common video file exstensions.

        Args:
            input_dir (Path): The folder in which we'll search for videos.

        Returns:
            List: Video file paths found in directory
        """

        # Get all files in folders and sub-folders
        files = self.get_all_files_in_dir(input_dir)

        vid_file_types = (
            ".avi",
            ".mp4",
            ".mkv",
            ".webm",
            ".mpeg",
            ".ogg",
            ".m4v",
            ".wmv",
            ".mov",
            ".flv",
        )

        video_files = []

        for f in files:
            if f.suffix in vid_file_types:
                video_files.append(f)

        return video_files

    def make_output_dirs(self, fileName):
        """[summary]

        Args:
            fileName ([type]): [description]

        Returns:
            Path: output_dir
        """
        output_dir = self.base_dir.joinpath("output")

        new_dir = output_dir.joinpath(fileName)
        selects_sub_dir = new_dir.joinpath("selects")
        rejects_sub_dir = new_dir.joinpath("rejects")
        dedeuplicate_sub_sub_dir = rejects_sub_dir.joinpath("dedeuplicate")
        blurry_sub_sub_dir = rejects_sub_dir.joinpath("blurry")

        try:
            Path.mkdir(new_dir)
            Path.mkdir(selects_sub_dir)
            Path.mkdir(rejects_sub_dir)
            Path.mkdir(dedeuplicate_sub_sub_dir)
            Path.mkdir(blurry_sub_sub_dir)
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

        return (output_dir, selects_sub_dir, rejects_sub_dir)

    # def build_cmd(self, input_video):
    #     """Build the Subprocess command and send it to `send_subprocess_cmd`"""

    #     # __________________ Set Output & Filename ___________________
    #     file_name = PurePath(input_video).stem
    #     (output_dir, selects_dir, rejects_dir) = self.make_output_dirs(file_name)

    #     logger.debug("Building command...")

    #     ouput_str = str(output_dir.joinpath(f"{file_name}_Screenshot-%04d.png"))

    #     # FFmpeg Commands
    #     # -i = input
    #     # input path as string
    #     # -an = strip out audio (may be unnecessary)
    #     # -sn = strip out subtitles (may be unnecessary)
    #     cmd: List[str] = ["ffmpeg", "-i", str(input_video), "-an", "-sn"]

    #     # Set fps part of the command
    #     if self.fps:
    #         cmd.append("-vf")
    #         cmd.append(f"fps=1/{self.fps}")

    #     # Last part of the command
    #     cmd.append(ouput_str)

    #     self.send_cmd(cmd, output_dir)

    # def send_cmd(self, cmd, output_dir):
    #     """Sends command to the shell via `subprocess`

    #     Args:
    #         cmd (List[str]): [description]
    #     """

    #     logger.debug(f"Sending subprocess command: {cmd}")
    #     self.timer.start()

    #     try:
    #         completed = subprocess.run(
    #             cmd,
    #             stdin=subprocess.PIPE,
    #             stdout=subprocess.PIPE,
    #             stderr=subprocess.PIPE,
    #             check=True,
    #             shell=False,
    #         )

    #         if completed.returncode == 0:
    #             logger.info("Capture complete...")
    #             logger.info("Initiating cleanup... ")
    #             # FileCleanup(dataset=output_dir)
    #             # Turned off FileCleanup temporarily

    #             self.timer.stop()
    #             logger.info("⭐️✨🌟🌈 Complete! 🏅🏆🎖\n")
    #         else:
    #             self.timer.stop()
    #             logger.info(f"🎃 Return code: {completed.returncode}\n")

    #         if self.verbose:
    #             self.timer.stop()
    #             logger.info(f"Bytes in stdout: {len(completed.stdout)}")
    #             _stdout = completed.stdout.decode("utf-8")
    #             logger.info(f"stdout: {_stdout}")

    #             _stderr = completed.stderr.decode("utf-8")
    #             logger.info(f"stderr: {_stderr}")

    #     except subprocess.CalledProcessError as err:
    #         self.timer.stop()
    #         logger.info("🎃    ‼️ Error in your subprocess command‼️    🎃\n")
    #         exit(err)

    #     return


class ShellCommand:
    def __init__(
        self, input_dir, output_dir, overwrite, captureFreq, postprocess
    ) -> None:

        if input_dir:
            print(input_dir)

        if postprocess:
            print(postprocess)

    def build_cmd(self, input_video):
        """Build the Subprocess command and send it to `send_subprocess_cmd`"""

        # __________________ Set Output & Filename ___________________
        file_name = PurePath(input_video).stem
        (output_dir, selects_dir, rejects_dir) = self.make_output_dirs(file_name)

        logger.debug("Building command...")

        ouput_str = str(output_dir.joinpath(f"{file_name}_Screenshot-%04d.png"))

        # FFmpeg Commands
        # -i = input
        # input path as string
        # -an = strip out audio (may be unnecessary)
        # -sn = strip out subtitles (may be unnecessary)
        cmd: List[str] = ["ffmpeg", "-i", str(input_video), "-an", "-sn"]

        # Set fps part of the command
        if self.fps:
            cmd.append("-vf")
            cmd.append(f"fps=1/{self.fps}")

        # Last part of the command
        cmd.append(ouput_str)

        self.send_cmd(cmd, output_dir)

    def send_cmd(self, cmd, output_dir):
        """Sends command to the shell via `subprocess`

        Args:
            cmd (List[str]): [description]
        """

        logger.debug(f"Sending subprocess command: {cmd}")
        self.timer.start()

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
                logger.info("Capture complete...")
                logger.info("Initiating cleanup... ")
                # FileCleanup(dataset=output_dir)
                # Turned off FileCleanup temporarily

                self.timer.stop()
                logger.info("⭐️✨🌟🌈 Complete! 🏅🏆🎖\n")
            else:
                self.timer.stop()
                logger.info(f"🎃 Return code: {completed.returncode}\n")

            if self.verbose:
                self.timer.stop()
                logger.info(f"Bytes in stdout: {len(completed.stdout)}")
                _stdout = completed.stdout.decode("utf-8")
                logger.info(f"stdout: {_stdout}")

                _stderr = completed.stderr.decode("utf-8")
                logger.info(f"stderr: {_stderr}")

        except subprocess.CalledProcessError as err:
            self.timer.stop()
            logger.info("🎃    ‼️ Error in your subprocess command‼️    🎃\n")
            exit(err)

        return
