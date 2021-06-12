# =========================================================================== #
# _____________________________    Imports     ______________________________ #
# =========================================================================== #
# ======            ====== #
# ======  Built-in  ====== #
# ======            ====== #
from pathlib import Path, PurePath
from typing import List
from pprint import pprint

# ======            ====== #
# ======    Local   ====== #
# ======            ====== #
from .timer import Timer

# ======            ====== #
# ======    PyPi    ====== #
# ======            ====== #
import subprocess
from loguru import logger
from pymediainfo import MediaInfo


# =========================================================================== #
# ______________________      Get Video Files       _________________________ #
# =========================================================================== #
def get_video_file_paths(input_dir):
    """From a directory, return a list of video file paths, sorted based
    on commonly used video file exstensions.

    Args:
        input_dir (Path): The folder in which we'll search for videos.

    Returns:
        List: Video file paths found in directory
    """

    # Get all files in folders and sub-folders
    # files = get_all_files_in_dir(input_dir)

    VIDEO_FILE_TYPES = (
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

    entries = input_dir.iterdir()
    # entries = sorted(entries, key=lambda entry: entry.is_file())

    for f in entries:
        if f.suffix in VIDEO_FILE_TYPES:
            video_files.append(f)

    return video_files


# =========================================================================== #
# ______________________       Get Media Info       _________________________ #
# =========================================================================== #
def get_video_info(video, audio=False):
    for track in MediaInfo.parse(video).tracks:
        if track.track_type == "Video":
            logger.info(f"Video Bit rate: {track.bit_rate}")
            logger.info(f"Video Frame rate: {track.frame_rate}")
            logger.info(f"Video Format: {track.format}")
            logger.info(f"Video Duration: {track.other_duration[4]}")
        elif track.track_type == "Audio":
            if audio:
                logger.info("Audio Track data:")
                pprint(track.to_data())


# =========================================================================== #
# ______________________ Subprocess > Shell Command   _______________________ #
# =========================================================================== #


class ffmpegCommander:
    """[summary]"""

    def __init__(
        self,
        input,
        output,
        decimate=False,
        strip_audio=True,
        strip_subtitles=True,
        verbose=False,
    ) -> None:
        self.i = input
        self.o = output
        self.d = decimate
        self.s_a = strip_audio
        self.s_s = strip_subtitles
        self.verbose = verbose

        # Function timer, just some FYI
        self.timer = Timer()

        # Start the FFmpeg Command
        self.cmd: List[str] = ["ffmpeg"]

        # Do the thing...
        self._cmd_builder()

    def _cmd_builder(self):
        # Input
        self._set_input()

        # Filters
        if self.d:
            self._append_video_filters()

        # Flags
        if self.s_a:
            # -an = strip out audio (may be unnecessary)
            self.cmd.append("-an")

        if self.s_s:
            # -sn = strip out subtitles (may be unnecessary)
            self.cmd.append("-sn")

        # Output
        self._append_output()

    def _set_input(self):
        # -i = input
        # input path as string
        self.cmd.extend(["-i", str(self.i)])

    def _append_video_filters(self):
        """=====================   FILTERS     ===============================
        SIMPLE FILTERGRAPHS
        https://ffmpeg.org/ffmpeg.html#toc-Simple-filtergraphs
        Simple filtergraphs are those that have exactly one input and
        output, both of the same type. Simple filtergraphs are configured
        with the per-stream -filter option (with -vf and -af aliases for
        video and audio respectively).
        ===================================================================
        """
        # Decimate
        logger.debug("Adding Video Filter: Decimate")
        self.cmd.extend(["-vf", "mpdecimate,setpts=N/FRAME_RATE/TB"])

    def _append_output(self):
        """Last part of the command is the output.

            We need to convert the Path to a String for
        We need to convert the Path to a String for
        subprocess to make sense of it.

        Note the `%04d` is a variable ffmpeg uses to indicate an
        incraminting number with 4 integers, such as:
            `Image-0001.png', `Image-0002.png`, etc.
        """

        file_name = PurePath(self.i).stem

        # Convert Path to string
        output_str = str(self.o.joinpath(f"{file_name}-%04d.png"))

        # Append it...
        self.cmd.append(output_str)

        # And send it...
        self.send()

    def send(self):
        """Sends command to the shell via `subprocess`

        Args:
            cmd (List[str]): [description]
        """

        logger.debug(f"Sending subprocess command: {self.cmd}")
        self.timer.start()

        try:
            completed = subprocess.run(
                self.cmd,
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
                logger.info("✨🌟  Complete! ⭐️✨\n")
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
            logger.error("🎃    ‼️ Error in your subprocess command‼️")
            exit(err)

        return
