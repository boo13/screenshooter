OVERWRITE_OUTPUT = True
INPUT_FPS = 1.0


# #______________________________ ffmpeg command ______________________________ #

# Global options (affect whole program instead of just one file:
#     -loglevel loglevel  set logging level
#     -v loglevel         set logging level
#     -report             generate a report
#     -max_alloc bytes    set maximum size of a single allocated block
#     -y                  overwrite output files
#     -n                  never overwrite output files
#     -ignore_unknown     Ignore unknown stream types
#     -filter_threads     number of non-complex filter threads
#     -filter_complex_threads  number of threads for -filter_complex
#     -stats              print progress report during encoding
#     -max_error_rate maximum error rate  ratio of errors (0.0: no errors, 1.0: 100% errors) above which ffmpeg returns an error instead of success.
#     -bits_per_raw_sample number  set the number of bits per raw sample
#     -vol volume         change audio volume (256=normal)

# -i = Input file
# -framerate = Framerate (values accepted ???)
# -q:v = Output Quality
# -vf select= The Video Filter
# -y    overwrite output files
# Video options:
#     -vframes number     set the number of video frames to output
# Audio options:
#     -an                 disable audio