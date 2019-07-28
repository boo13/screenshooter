"""
Tests for `screenshooter` module.
"""
import pytest


class TestScreenshooter(object):
    @classmethod
    def setup_class(cls):
        pass

    def test_metadata(self):
        from screenshooter import __version__, __email__, __author__

        assert __version__
        assert __author__
        assert __email__ == "boo13bot@gmail.com"

    def test_python_version(self):
        import sys

        assert sys.version_info[0] >= 3
        assert sys.version_info[1] >= 6

    def test_filepaths_exist(self):

        import pathlib
        from pathlib import Path

        # Check we're on a Unix system
        p = pathlib.PurePath()
        assert type(p) is pathlib.PurePosixPath

        # Check for the base directory
        BASE_DIR = Path(__file__).resolve().parent.parent
        assert type(BASE_DIR) is pathlib.PosixPath
        assert BASE_DIR.exists()
        assert BASE_DIR.is_dir()
        assert BASE_DIR.is_absolute()

        # Check for the input folder
        INPUT_DIR = BASE_DIR.joinpath("input")
        assert INPUT_DIR.is_dir()

        # Check for the output folder
        OUTPUT_DIR = BASE_DIR.joinpath("output")
        assert OUTPUT_DIR.is_dir()

        # If we have the default video, perform extra tests
        # Allow for no default video, for travis tests to pass
        # # Check for the default video
        INPUT_VID = INPUT_DIR.joinpath("test_input.mp4")

        if INPUT_VID.exists():
            vidName = pathlib.PurePath(INPUT_VID).stem
            assert vidName == "test_input"

            # Is it an .mp4
            vidExt = pathlib.PurePath(INPUT_VID).suffix
            assert vidExt == ".mp4"

    def test_make_ouput_dir(self):
        import pathlib
        from pathlib import Path
        from screenshooter import path_handler

        #    _res = path_handler.make_output_dir("test")
        #    assert _res.is_dir()

        assert path_handler.BASE_DIR.is_absolute()

    @classmethod
    def teardown_class(cls):
        pass
