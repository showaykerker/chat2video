from moviepy.editor import ImageClip, concatenate_videoclips, clips_array, AudioFileClip, AudioClip, CompositeVideoClip, concatenate_audioclips
from moviepy.audio.AudioClip import CompositeAudioClip
from moviepy.video.fx.resize import resize
from moviepy.video.fx.all import margin
import os
import json 
from PIL import Image
import numpy as np
import subprocess

# Configure frames
config = [
    {"img": ["img1.jpg"], "duration": 2},
    {"img": ["img1.jpg", "img2.jpg"], "duration": 2}, 
    {"img": ["img2.jpg", "img3.jpg"], "duration": 4}
]

audioclip = AudioFileClip("discord-notification.mp3").subclip(0.0, 0.5)

# Get max height of images
max_height = -1
max_width = -1
for frame in config:
    height = -1
    for img in frame["img"]:
        im = Image.open(os.path.join("images", img))
        height += im.height
        max_width = max(max_width, im.width)
    max_height = max(max_height, height)

print(f"max height: {max_height}, max width: {max_width}")
assert max_height > 0, max_height
assert max_width > 0, max_width
max_height *= 1.05

# Build video clips
clips = []
timestamps = [0.0]

for i, frame in enumerate(config):
    if i != len(config)-1:
        timestamps.append(timestamps[-1] + frame["duration"] - 0.1)
    img_files = [os.path.join("images", f) for f in frame["img"]]
    
    if len(img_files) == 1:
        # Single image => center 
        clip = ImageClip(img_files[0]).set_position('center').set_duration(frame['duration'])
    else:
        # Multiple images => concatenate vertically
        imgs = [ImageClip(f).set_position('center').set_duration(frame['duration']) for f in img_files]
        clip = clips_array([[im] for im in imgs])

    w, h = clip.size
    padding = int((max_height-h)/2.)    
    clip = margin(clip, mar=None, left=0, right=0, top=padding, bottom=padding, color=(0, 0, 0), opacity=1.0)
    clips.append(clip)

# Concatenate clips     
final = concatenate_videoclips(clips)

def make_frame(t):
    numpy_array = np.array([0, 0])
    return numpy_array
 
# creating audio clip
empty_audio = AudioClip(make_frame, duration = final.duration)

mixed = CompositeAudioClip([empty_audio] + [audioclip.set_start(t).set_duration(0.5) for t in timestamps])

final.audio = mixed

final.write_videofile('output.mp4', fps=6, audio_codec='aac')




