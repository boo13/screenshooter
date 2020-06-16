# _________________________ Imports  _________________________
# Local
from version import __version__
from timer import Timer

#
import os
import sys
import subprocess
from typing import List
from pathlib import Path, PurePath
import matplotlib.pyplot as plt
from imutils import paths
import numpy as np

# Kept getting error `RuntimeWarning: divide by zero encountered in log`
# This turns off that warning
np.seterr(divide="ignore")
import cv2
from loguru import logger

# _________________________ Main Class  _________________________


class Screenshooter:
    def __init__(self, input_video, verbose, fps, overwrite_output=False):
        self.fps = fps
        self.overwrite = overwrite_output
        self.base_dir = Path(__file__).resolve().parent.parent
        self.verbose = verbose

        self.timer = Timer()

        TABS = "\t\t\t\t"
        logger.debug(
            f"""Starting New Session...
            {TABS}Screenshooter Version: {__version__}
            {TABS}Input Video: {input_video}
            {TABS}Verbose: {verbose}
            {TABS}fps: {fps}
            {TABS}overwrite output: {overwrite_output}
            """
        )

        self.input_videos = self.build_input_video_list(input_video)

        self.run(self.input_videos)

    def run(self, video_files):
        # For each of those videos we send a `subprocess` command
        for video in video_files:
            self.build_cmd(video)

    def build_input_video_list(self, input_video):
        if input_video is None:
            # Get list of videos in the `input` folder
            video_file_list = self.get_video_files(
                input_dir=self.base_dir.joinpath("input")
            )
            logger.info(f"Video file List: {video_file_list}")
        else:
            video_file_list = [input_video]
            logger.info(f"Using command-line submitted video: {input_video}")

        return video_file_list

    def get_all_files_in_dir(self, input_dir):
        """From a directory return a list of paths for the files contained within it.

        Args:
            input_dir (Path): The folder in which we'll search for files.

        Returns:
            List: File paths found in directory
        """

        # Directory containg files
        dir_path = Path(input_dir)
        assert dir_path.is_dir()

        # Empty list
        file_list = []

        for f in dir_path.iterdir():
            if f.is_file():
                file_list.append(f)
            elif f.is_dir():
                file_list.extend(self.get_all_files_in_dir(f))

        return file_list

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

    def build_cmd(self, input_video):
        """Build the Subprocess command and send it to `send_subprocess_cmd`
        """

        # __________________ Set Output & Filename ___________________
        file_name = PurePath(input_video).stem
        (output_dir, selects_dir, rejects_dir) = self.make_output_dirs(file_name)

        logger.debug("Building command...")

        ouput_str = str(output_dir.joinpath(f"{file_name}_Screenshot-%04d.png"))

        cmd: List[str] = [
            "ffmpeg",
            "-i",
            str(input_video),
        ]

        # Set fps part of the command
        if self.fps:
            cmd.append("-vf")
            cmd.append(f"fps=1/{self.fps}")

        # Last part of the command
        cmd.append(ouput_str)

        if self.verbose:
            # These are ffmpeg verbose commands
            cmd.append("-report")
            cmd.append("-stats")

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
                # DeDuplicate(dataset=output_dir)
                FileCleanup(dataset=output_dir)

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


class FileCleanup:
    def __init__(self, dataset, dryrun=False, deduplicate=True, remove_blurry=True):
        self.dataset = dataset
        self.dryrun = dryrun

        self.image_paths = list(paths.list_images(self.dataset))

        if deduplicate:
            logger.info("Starting to remove duplicate images...")
            self.DeDuplicate()

        if remove_blurry:
            logger.info("Starting to remove blurry images...")
            self.remove_blurry_images()
            # detect_blur_fft()

    def remove_blurry_images(self):
        # loop over our image paths
        for image_path in self.image_paths:
            # Load image and make grayscale
            image = cv2.imread(image_path)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            (mean, blurry) = self.detect_blur_fft(gray)
            text = "Blurry ({:.2f})" if blurry else "Not Blurry ({:.2f})"
            text = text.format(mean)

            # Not sure why the list is coming through as strings, so here I'm just converting it back to a Path object
            img_path = Path(image_path)
            img_name = img_path.name

            logger.debug(f"{img_name} is {text}")

            reject = (
                Path(self.dataset)
                .joinpath("rejects")
                .joinpath("blurry")
                .joinpath(img_name)
            )
            select = Path(self.dataset).joinpath("selects").joinpath(img_name)

            if blurry:
                # Thanks to guidance from https://realpython.com/python-pathlib/
                with reject.open(mode="xb") as f:
                    f.write(img_path.read_bytes())
                    img_path.unlink()
            else:
                with select.open(mode="xb") as f:
                    f.write(img_path.read_bytes())
                    img_path.unlink()

    def detect_blur_fft(self, image, size=60, thresh=5, vis=False):
        """Find blurry images
        
        Based on code from: https://www.pyimagesearch.com/2020/06/15/opencv-fast-fourier-transform-fft-for-blur-detection-in-images-and-video-streams/?__s=sizjqdkszyoej5pbk9sf

        Args:
            image ([type]): [description]
            size (int, optional): [description]. Defaults to 60.
            thresh (int, optional): [description]. Defaults to 10.
            vis (bool, optional): [description]. Defaults to False.

        Returns:
            [type]: [description]
        """

        # grab the dimensions of the image and use the dimensions to
        # derive the center (x, y)-coordinates
        (h, w) = image.shape
        (cX, cY) = (int(w / 2.0), int(h / 2.0))

        # compute the FFT to find the frequency transform, then shift
        # the zero frequency component (i.e., DC component located at
        # the top-left corner) to the center where it will be more
        # easy to analyze
        fft = np.fft.fft2(image)
        fftShift = np.fft.fftshift(fft)

        # check to see if we are visualizing our output
        if vis:
            # compute the magnitude spectrum of the transform
            magnitude = 20 * np.log(np.abs(fftShift))
            # display the original input image
            (fig, ax) = plt.subplots(1, 2,)
            ax[0].imshow(image, cmap="gray")
            ax[0].set_title("Input")
            ax[0].set_xticks([])
            ax[0].set_yticks([])
            # display the magnitude image
            ax[1].imshow(magnitude, cmap="gray")
            ax[1].set_title("Magnitude Spectrum")
            ax[1].set_xticks([])
            ax[1].set_yticks([])
            # show our plots
            plt.show()

        # zero-out the center of the FFT shift (i.e., remove low
        # frequencies), apply the inverse shift such that the DC
        # component once again becomes the top-left, and then apply
        # the inverse FFT
        fftShift[cY - size : cY + size, cX - size : cX + size] = 0
        fftShift = np.fft.ifftshift(fftShift)
        recon = np.fft.ifft2(fftShift)

        # compute the magnitude spectrum of the reconstructed image,
        # then compute the mean of the magnitude values
        magnitude = 20 * np.log(np.abs(recon))
        mean = np.mean(magnitude)

        # the image will be considered "blurry" if the mean value of the
        # magnitudes is less than the threshold value
        return (mean, mean <= thresh)

    def DeDuplicate(self):
        """ Detect duplicate images in the same folder based on Image Hash.

        Based on code from: https://www.pyimagesearch.com/2020/04/20/detect-and-remove-duplicate-images-from-a-dataset-for-deep-learning/

        """
        # grab the paths to all images in our input dataset directory and
        # then initialize our hashes dictionary
        logger.debug("Computing image hashes...")

        hashes = {}

        # loop over our image paths
        for image_path in self.image_paths:
            # load the input image and compute the hash
            image = cv2.imread(image_path)
            h = self.dhash(image)
            # grab all image paths with that hash, add the current image
            # path to it, and store the list back in the hashes dictionary
            p = hashes.get(h, [])
            p.append(image_path)
            hashes[h] = p

        imgs_deleted = 0
        # loop over the image hashes
        for (h, hashed_paths) in hashes.items():
            # check to see if there is more than one image with the same hash
            if len(hashed_paths) > 1:
                # check to see if this is a dry run
                if self.dryrun:
                    # initialize a montage to store all images with the same
                    # hash
                    montage = None
                    # loop over all image paths with the same hash
                    for p in hashed_paths:
                        # load the input image and resize it to a fixed width
                        # and heightG
                        image = cv2.imread(p)
                        image = cv2.resize(image, (150, 150))
                        # if our montage is None, initialize it
                        if montage is None:
                            montage = image
                        # otherwise, horizontally stack the images
                        else:
                            montage = np.hstack([montage, image])
                    # show the montage for the hash
                    logger.info(f"Hash: {h}")
                    cv2.imshow("Montage", montage)
                    cv2.waitKey(0)

                    # otherwise, we'll be removing the duplicate images
                else:
                    # loop over all image paths with the same hash *except*
                    # for the first image in the list (since we want to keep
                    # one, and only one, of the duplicate images)

                    for p in hashed_paths[1:]:
                        os.remove(p)
                        imgs_deleted += 1

        logger.info(f"DeDuplication complete!\n{imgs_deleted} images deleted")

    def dhash(self, image, hash_size=8):
        # convert the image to grayscale and resize the grayscale image,
        # adding a single column (width) so we can compute the horizontal
        # gradient
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        resized = cv2.resize(gray, (hash_size + 1, hash_size))
        # compute the (relative) horizontal gradient between adjacent
        # column pixels
        diff = resized[:, 1:] > resized[:, :-1]
        # convert the difference image to a hash and return it
        return sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])

    # def find_blurry_images(self, img):
    #     """
    #     Based on code from: https://www.youtube.com/watch?v=5YP7OoMhXbM

    #     Args:
    #         img ([type]): [description]
    #     """
    #     img = cv2.imread(img, cv2.IMREAD_GRAYSCALE)

    #     # Low values, closer to 0, mean a blurrier image
    #     # Higher values, near 100, mean our image has a high pixel variance
    #     # which we use as a way to determine if it is in focus
    #     laplacian_var = cv2.Laplacian(img, cv2.CV_64F).var()

    #     print(laplacian_var)

    #     if laplacian_var < 5:
    #         print("Image is blurry")
