# ================================================================== #
# _________________________    Imports     _________________________ #
# ================================================================== #
# ======            ====== #
# ======  Built-in  ====== #
# ======            ====== #


# ======            ====== #
# ======    Local   ====== #
# ======            ====== #

# ======            ====== #
# ======    PyPi    ====== #
# ======            ====== #
import subprocess
from loguru import logger



# ================================================================== #
# _________________________   Commands     _________________________ #
# ================================================================== #

# DECIMATE
#
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


def get_codecs():
    cmd = "ffmpeg -codecs"
    x = subprocess.check_output(cmd, shell=True)
    x = x.split(b"\n")
    for e in x:
        print(e)


def get_formats():
    cmd = "ffmpeg -formats"
    x = subprocess.check_output(cmd, shell=True)
    x = x.split(b"\n")
    for e in x:
        print(e)


def convert_seq_to_mov():
    input = r"C:\Users\HP\Desktop\FFMPEG\smoke\dense_smoke_p001.%03d.png"
    output = r"C:\Users\HP\Desktop\FFMPEG\out.mp4"
    frame_rate = 24
    cmd = f'ffmpeg -framerate {frame_rate} -i "{input}" "{output}"'
    print(cmd)
    subprocess.check_output(cmd, shell=True)


def convert_mov_to_seq():
    input = r"C:\Users\HP\Desktop\FFMPEG\playblast.mov"
    output = r"C:\Users\HP\Desktop\FFMPEG\v001\car_scene_v001.%03d.png"

    cmd = f'ffmpeg  -i "{input}" "{output}"'
    print(cmd)
    subprocess.check_output(cmd, shell=True)


def get_thumbnail():
    input = r"C:\Users\HP\Desktop\FFMPEG\comp.mov"
    output = r"C:\Users\HP\Desktop\FFMPEG\thumb.png"
    cmd = f'ffmpeg -i "{input}" -ss 00:00:01.000 -vframes 1  -s 640x360  "{output}"'
    print(cmd)
    subprocess.check_output(cmd, shell=True)


# Get FPS
# From here: https://stackoverflow.com/questions/27792934/get-video-fps-using-ffprobe
# ffprobe -v error -select_streams v -of default=noprint_wrappers=1:nokey=1 -show_entries stream=r_frame_rate file.mp4


def get_fps():
    cmd = f"ffprobe -v error -select_streams v -of default=noprint_wrappers=1:nokey=1 -show_entries stream=r_frame_rate ../input/FBIAgent.m4v"
    subprocess.check_output(cmd, shell=True)


if __name__ == "__main__":
    # get_codecs()
    # get_formats()
    # get_thumbnail()
    get_fps()
