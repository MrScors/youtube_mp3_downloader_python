import os
import string
import random

from flask import Flask, request
from pytube import YouTube

from moviepy.editor import VideoFileClip


app = Flask(__name__)


def random_string(string_length=10):
    """Generate a random string of fixed length """
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=string_length))


def get_extension(filename):
    return filename[filename.rindex("."):]  # rindex() -> java lastIndexOf()


def mp4_to_mp3(input_file_name):
    output_file_dir = input_file_name[:input_file_name.rindex("/")]
    output_file_name = input_file_name[(input_file_name.rindex("/")+1):].replace("mp4", "mp3")
    video = VideoFileClip(os.path.join(input_file_name))
    video.audio.write_audiofile(os.path.join(output_file_dir, output_file_name))
    os.remove(input_file_name)
    return output_file_name


@app.route('/download')
def download_youtube_video():
    url = request.args.get('url')
    local_uri = "/resources"

    if url.startswith("https://www.youtube.com/watch?v="):
        yt = YouTube(url)
        video = yt.streams.first().download(local_uri)

        new_video_name = random_string(20) + get_extension(video)
        mp4_file_location = local_uri + "/" + new_video_name
        os.rename(video, mp4_file_location)

        mp3_file_location = mp4_to_mp3(mp4_file_location)

        return mp3_file_location, 200

    return "Invalid YouTube link", 400


if __name__ == '__main__':
    app.run(host='0.0.0.0')
