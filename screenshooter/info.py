from pprint import pprint
from pymediainfo import MediaInfo
from loguru import logger


def video_info(video):
    media_info = MediaInfo.parse(video)
    for track in media_info.tracks:
        if track.track_type == "Video":
            logger.info(f"Video Bit rate: {track.bit_rate}")
            logger.info(f"Video Frame rate: {track.frame_rate}")
            logger.info(f"Video Format: {track.format}")
            logger.info(f"Video Duration: {track.other_duration[4]}")
            # print(
            #     "Bit rate: {t.bit_rate}, Frame rate: {t.frame_rate}, "
            #     "Format: {t.format}".format(t=track)
            # )
            # print("Duration (raw value):", track.duration)
            # print("Duration (other values:")
            # pprint(track.other_duration)
        elif track.track_type == "Audio":
            logger.info("Audio Track data:")
            pprint(track.to_data())
