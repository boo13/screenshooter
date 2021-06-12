# ================================================================== #
# _________________________    Imports     _________________________ #
# ================================================================== #
# ======            ====== #
# ======  Built-in  ====== #
# ======            ====== #
import sys
from pathlib import Path

# ======            ====== #
# ======    Local   ====== #
# ======            ====== #
from .commands import get_video_info
from .process import ProcessVideo

# ======            ====== #
# ======    PyPi    ====== #
# ======            ====== #
import click
import click_config_file
from loguru import logger
from single_source import get_version, VersionNotFoundError

# ================================================================== #
# _________________________ Logging setup  _________________________ #
# ================================================================== #
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

# ================================================================== #
# _________________________      CLI       _________________________ #
# ================================================================== #


@click.command()
@click.option(
    "--input",
    "-i",
    default="input",
    help="📺 The folder in which to find input videos..",
)
@click.option("--fps", "-f", default=1.0, help="⏰ Frames per second (float)...")
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
        get_video_info(input)

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
