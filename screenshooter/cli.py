# =========================================================================== #
# _____________________________    Imports     ______________________________ #
# =========================================================================== #
# ======            ====== #
# ======  Built-in  ====== #
# ======            ====== #
import os
import sys
from pathlib import Path

# ======            ====== #
# ======    Local   ====== #
# ======            ====== #
from .get_inputs import get_video_file_paths
from .main import get_video_info, ffmpegCommander

# ======            ====== #
# ======    PyPi    ====== #
# ======            ====== #
import click
import click_config_file
from loguru import logger
from single_source import get_version, VersionNotFoundError

# =========================================================================== #
# ______________________________ Logging setup  _____________________________ #
# =========================================================================== #
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


# ====== Used for getting the Package Version from Poetry's    ====== #
# ====== PyProject.toml file                                   ====== #
# ======                                                       ====== #
path_to_pyproject_dir = Path(__file__).parent.parent
try:
    __version__ = get_version(__name__, path_to_pyproject_dir, fail=True)
except VersionNotFoundError as v:
    logger.error(v)
    raise

# =========================================================================== #
# _______________________________      CLI       ____________________________ #
# =========================================================================== #


@click.command()
@click.option(
    "--input",
    "-i",
    default="input",
    help="📺 The folder in which to find input videos..",
)
@click.option(
    "--output",
    "-o",
    default="output",
    help="The folder to output to",
)
@click.option("--fps", "-f", default=1.0, help="⏰  Frames per second (float)...")
@click.option(
    "--overwrite",
    "-o",
    is_flag=True,
    help="If files already exist, overwrite them? [default: False]",
)
@click.option(
    "--postprocess",
    "-p",
    is_flag=True,
    help="Run post-processing to eliminate duplicates, blurry, etc.",
)
@click.option(
    "--version",
    "-v",
    is_flag=True,
    help="Print the Screenshooter version number",
)
@click.option(
    "--debug",
    "-d",
    is_flag=True,
    help="Print debug messages",
)
@click.option(
    "--video-info",
    is_flag=True,
    help="Print info for input video",
)
@click.option(
    "--audio-info",
    is_flag=True,
    help="Print info for input audio",
)
@click.option(
    "--decimate",
    is_flag=True,
    help="Decimate the video",
)
@click_config_file.configuration_option()
def CLI(
    input,
    output,
    fps,
    overwrite,
    postprocess,
    version,
    debug,
    video_info,
    audio_info,
    decimate,
):
    """
    The main function for parsing out the initial click (CLI) inputs.

    Click gets the file folder and desired output options for the
    screenshooter command, then sends it on its way.
    """
    # Display Version
    if version:
        # get_video_info(input)
        click.echo(f"Screenshooter Vers: {__version__}")
        sys.exit()

    # Directory
    root_dir = Path(input)
    if not root_dir.is_dir():
        print("The specified root directory doesn't exist")
        sys.exit()

    output_dir = Path(output)
    if not output_dir.is_dir():
        print("The specified root directory doesn't exist")
        sys.exit()

    # Get the video files
    videos = get_video_file_paths(root_dir)

    # Request to send
    request = {
        "file": {root_dir},
        "fps": {fps},
        "overwrite": {overwrite},
        "post-process": {postprocess},
    }

    # Debug
    if debug:
        logger.debug(f"Debug Mode is ON")
        logger.debug(f"Request: {request}")
        logger.debug(f"Video File List: {videos}")

    # Send the request
    # ProcessVideo(input, fps, overwrite, postprocess)
    for v in videos:

        # Video Info
        if video_info:
            get_video_info(v, audio_info)
        else:
            ffmpegCommander(v, output_dir, decimate=decimate)
