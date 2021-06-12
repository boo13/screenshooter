from process import ProcessVideo
import click
import click_config_file
from loguru import logger

# ======            ====== #
# ======    Local   ====== #
# ======            ====== #
from info import video_info

# ====== Used for getting the Package Version from Poetry's    ====== #
# ====== PyProject.toml file                                   ====== #
# ======                                                       ====== #
from pathlib import Path
from single_source import get_version, VersionNotFoundError

path_to_pyproject_dir = Path(__file__).parent.parent
try:
    __version__ = get_version(__name__, path_to_pyproject_dir, fail=True)
except VersionNotFoundError as v:
    logger.error(v)
    raise

# ======    ====== #
# ======    ====== #
# ======    ====== #


@click.command()
@click.option(
    "--input",
    "-i",
    default="input",
    help="📺 The folder in which to find input videos..",
)
@click.option(
    "--fps", "-f", default=1.0, help="⏰ Frames per second (float)..."
)
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
    help="Run the post-processing scripts to eliminate duplicates, blurry, etc. images. [default: False]",
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
@click_config_file.configuration_option()
def CLI(input, fps, overwrite, postprocess, version, debug):
    """
    The main function for parsing out the initial click (CLI) inputs.

    Click gets the file folder and desired output options for the
    screenshooter command, then sends it on its way.
    """

    if version:
        # print(f"version: {__version__}")
        video_info(input)

    else:
        request = {
            "file": {input},
            "fps": {fps},
            "overwrite": {overwrite},
            "post-process": {postprocess},
        }

        if debug:
            logger.debug(f"Request: {request}")

        ProcessVideo(input, fps, overwrite, postprocess)
