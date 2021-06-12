# DECIMATE
#
# Remove the "Dead frames" (duplicate frames) in a video
#
# Delete "still/dead frames" (frames that are the same as previous)
# ffmpeg -i {FILE} -vf mpdecimate,setpts=N/FRAME_RATE/TB -an {OUT}
