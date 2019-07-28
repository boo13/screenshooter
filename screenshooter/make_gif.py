mkdir frames
ffmpeg -i input -vf scale=320:-1:flags=lanczos,fps=10 frames/ffout%03d.png

import config

# cmd: List[str] = [
#             "ffmpeg",
#             "-i",
#             str(config.INPUT_VID),
#             "-framerate",
#             str(config.INPUT_FPS),
#             ouput_str,
#             "-an",
#             "-y",
#         ]

# try:

#     OUTPUT_DIR = make_output_dir(self.fileName) 

#     ouput_str = str(OUTPUT_DIR.joinpath(f"{self.fileName}_Screenshot-%04d.jpg"))

#     completed = subprocess.run(
#         cmd,
#         stdin=subprocess.PIPE,
#         stdout=subprocess.PIPE,
#         stderr=subprocess.PIPE,
#         check=True,
#         shell=False,
#     )

#     if completed.returncode == 0:
#         print("\n🎯⭐️✨🌟🌈 Complete! 🏅🏆🥇🎖\n")
#     else:
#         print(f"\n🎃 Return code: {completed.returncode}")

#     except subprocess.CalledProcessError as err:
#         print("\n🎃    ‼️ Error in your subprocess command‼️    🎃\n")
#         exit(err)