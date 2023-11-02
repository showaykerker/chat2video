import json
import os
import subprocess

from typing import List, Tuple, Union

import numpy as np
from PIL import Image
from moviepy.audio.AudioClip import CompositeAudioClip
from moviepy.editor import AudioClip
from moviepy.editor import AudioFileClip
from moviepy.editor import VideoClip
from moviepy.editor import CompositeVideoClip
from moviepy.editor import ImageClip
from moviepy.editor import clips_array
from moviepy.editor import concatenate_audioclips
from moviepy.editor import concatenate_videoclips
from moviepy.video.fx.all import margin


def get_config() -> List[dict]:
    if os.path.isfile("config.json"):
        use_config = "config.json"
    else:
        assert os.path.isfile("example.config.json"), ""\
            "Must include either config.json or "\
            "example.config.json in the directory."
        use_config = "example.config.json"

    with open(use_config, "r") as f:
        config = json.load(f)
    return config


def get_audio_clip() -> AudioFileClip:
    assert os.path.isfile("discord-notification.mp3"), ""\
        "Must have discord-notification.mp3 in the directory."
    return AudioFileClip("discord-notification.mp3").subclip(0.0, 0.5)


def get_max_img_height(config: List[str]) -> float:
    max_height = -1
    for frame in config:
        height = sum([Image.open(os.path.join("images", img)).height
                      for img in frame["img"]])
        max_height = max(max_height, height)

    print(f"max height: {max_height}")
    assert max_height > 0, max_height

    return max_height * 1.05


def build_video_clips(
        config: List[dict],
        max_height: float) -> Tuple[VideoClip, List[float]]:
    clips = []
    timestamps = [0.0]

    for i, frame in enumerate(config):
        if i != len(config)-1:
            timestamps.append(timestamps[-1] + frame["duration"] - 0.1)

        img_files = [os.path.join("images", f) for f in frame["img"]]

        if len(img_files) == 1:
            # Single image => center
            clip = ImageClip(img_files[0]).set_position(
                'center').set_duration(frame['duration'])
        else:
            # Multiple images => concatenate vertically
            imgs = [ImageClip(f).set_position('center').set_duration(
                frame['duration']) for f in img_files]
            clip = clips_array([[im] for im in imgs])

        w, h = clip.size
        padding = int((max_height-h) / 2.)
        clip = margin(clip, top=padding, bottom=padding)
        clips.append(clip)

    # Concatenate clips
    final = concatenate_videoclips(clips)

    return final, timestamps


def get_empty_audio_clip(duration: float) -> AudioClip:
    def _make_frame(t):
        numpy_array = np.array([0, 0])
        return numpy_array
    return AudioClip(_make_frame, duration=duration)


def mix_audio(
        empty_audio: Union[AudioClip, AudioFileClip],
        sound: Union[AudioClip, AudioFileClip],
        timestamps: List[float]) -> AudioClip:
    return CompositeAudioClip(
        [empty_audio] +
        [sound.set_start(t).set_duration(0.5) for t in timestamps])

if __name__ == '__main__':

    config = get_config()
    discord_notification_clip = get_audio_clip()

    max_height = get_max_img_height(config)
    video_clip, timestamps = build_video_clips(config, max_height)

    empty_audio = get_empty_audio_clip(duration=video_clip.duration)
    mixed = mix_audio(empty_audio, discord_notification_clip, timestamps)

    video_clip.audio = mixed
    video_clip.write_videofile('output.mp4', fps=6, audio_codec='aac')




