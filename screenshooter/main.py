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
from yaspin import yaspin, Spinner

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
# _____________________       Make Output Dirs       ________________________ #
# =========================================================================== #
def make_output_dirs(fileName):
    """[summary]

    Args:
        fileName ([type]): [description]

    Returns:
        Path: output_dir
    """
    output_dir = self.base_dir.joinpath("output")

    new_dir = output_dir.joinpath(fileName)
    # selects_sub_dir = new_dir.joinpath("selects")
    # rejects_sub_dir = new_dir.joinpath("rejects")
    # dedeuplicate_sub_sub_dir = rejects_sub_dir.joinpath("dedeuplicate")
    # blurry_sub_sub_dir = rejects_sub_dir.joinpath("blurry")

    try:
        Path.mkdir(new_dir)
        # Path.mkdir(selects_sub_dir)
        # Path.mkdir(rejects_sub_dir)
        # Path.mkdir(dedeuplicate_sub_sub_dir)
        # Path.mkdir(blurry_sub_sub_dir)
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

    # return (output_dir, selects_sub_dir, rejects_sub_dir)


# =========================================================================== #
# ______________________ Subprocess > Shell Command   _______________________ #
# =========================================================================== #


class ffmpegCommander:
    """[summary]"""

    def __init__(
        self,
        input,
        output,
        ss=False,
        ss_h=0,
        ss_m=0,
        ss_s=0,
        ss_mi=0,
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

        # Seek start
        if ss:
            self._seek_start(ss_h, ss_m, ss_s, ss_mi)

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

    def _seek_start(self, hours, mins, secs, mils):
        self.cmd.extend(["-ss", f"{hours}:{mins}:{secs}.{mils}"])

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
        ======================================================================
        """
        # Decimate
        logger.debug("Adding Video Filter: Decimate")
        self.cmd.extend(["-vf", "mpdecimate,setpts=N/FRAME_RATE/TB"])

    def _append_output(self):
        """=====================    OUTPUT     ===============================
        Last part of the command is the output.

        We need to convert the Path to a String for
        We need to convert the Path to a String for
        subprocess to make sense of it.

        Note the `%04d` is a variable ffmpeg uses to indicate an
        incraminting number with 4 integers, such as:
            `Image-0001.png', `Image-0002.png`, etc.
        ======================================================================
        """
        # Get the video filename (minus the extension)
        file_name = PurePath(self.i).stem

        # Make output directory, using the name of the video file
        new_dir = self.o.joinpath(file_name)

        try:
            Path.mkdir(new_dir)
            self.o = self.o.joinpath(file_name)

        except FileNotFoundError as e:
            logger.error("A missing parent folder - problem in the path.")
            exit(e)

        # except FileExistsError as e:
        #     logger.debug("The output folder already exists")

        #     if self.overwrite:
        #         Path.mkdir(new_dir, exist_ok=True)
        #         output_dir = output_dir.joinpath(fileName)
        #     else:
        #         logger.info("Exiting...")
        #         exit(e)

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
            # Compose new spinners with custom sequence and interval value
            sp = Spinner(
                ["😸", ". 😹", ".. 😼", "... 😻", ".... 😾", "..... 😿", "...... 😽", "....... 🙀"], 500
            )

            with yaspin(sp, text="Cats at work!!!"):  # cats consuming code :)
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
