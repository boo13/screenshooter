import cv2
from loguru import logger
from pathlib import Path


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

            # This 'if' statement prevents 'FileNotFoundError's by making sure we have an image
            if image is not None:

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
            (fig, ax) = plt.subplots(
                1,
                2,
            )
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
        """Detect duplicate images in the same folder based on Image Hash.

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
