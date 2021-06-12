from pymediainfo import MediaInfo

media_info = MediaInfo.parse("sample_videos/Big_Buck_Bunny_1080p_surround.avi")

for track in media_info.tracks:
    print(track)
    # if track.track_type == "Video":
    #     print(track.bit_rate, track.bit_rate_mode, track.codec)
