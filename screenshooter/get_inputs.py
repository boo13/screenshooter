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
