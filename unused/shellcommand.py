

# ================================================================== #
# _________________           Decimate         _____________________ #
# ================================================================== #
# ffmpeg -i {FILE} -vf mpdecimate,setpts=N/FRAME_RATE/TB -an {OUT}


def decimate(input_video, output=None):
    """Remove the "Dead frames" (duplicate frames) in a video

    Args:
        input_video ([type]): [description]
    """

    if output is None:
        output = f"converted-{input_video}"
    print(input_video)

    cmd = f"ffmpeg -i {input_video} -vf mpdecimate,setpts=N/FRAME_RATE/TB -an {output}"
    # cmd()


# ================================================================== #
# __________________ Subprocess > Shell Command  ___________________ #
# ================================================================== #
class ShellCommand:
    def __init__(
        self,
        input_vid,
        output_dir,
        overwrite=False,
        captureFreq=1,
        postprocess=False,
        verbose=True,
    ) -> None:

        self.timer = Timer()

        self.build_cmd(input_vid, output_dir, captureFreq)

        # if postprocess:
        #     print(postprocess)

    def build_cmd(self, input_vid, output_dir, captureFreq):
        """Build the Subprocess command and send it to `send_subprocess_cmd`"""

        # __________________ Set Output & Filename ___________________
        file_name = PurePath(input_vid).stem
        # (output_dir, selects_dir, rejects_dir) = self.make_output_dirs(file_name)

        logger.debug("Building command...")
        logger.debug(f"Output dir: {output_dir}")
        logger.debug(f"File Name: {file_name}")

        ouput_str = str(output_dir.joinpath(f"{file_name}_Screenshot-%04d.png"))

        # FFmpeg Commands
        # -i = input
        # input path as string
        # -an = strip out audio (may be unnecessary)
        # -sn = strip out subtitles (may be unnecessary)
        cmd: List[str] = ["ffmpeg", "-i", str(input_vid), "-an", "-sn"]

        # Set fps part of the command
        if captureFreq:
            cmd.append("-vf")
            # cmd.append(f"fps=1")
            cmd.append(f"fps=1/{captureFreq}")

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
                logger.info("🌟🌈 Complete! ⭐️✨\n")
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
