import shutil
import asyncio
import yt_dlp as youtube_dl
import os
import math
import subprocess
import re
import json

pwd = os.getcwd()
# download_subdirectory = os.getenv("downloads_subdirectory")
# download_path = os.path.join(pwd, download_subdirectory)
download_path = os.path.join(pwd)

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': os.path.join(download_path, '%(title)s.mp3'),
    'restrictfilenames': True,
    'noplaylist': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',  # bind to ipv4 since ipv6 addresses cause issues sometimes
    'before_options': "-reconnect 1 -reconnect_streamed 1  -reconnect_on_network_error 1 -reconnect_on_http_error 1 -reconnect_delay_max 5"
    # https://ffmpeg.org/ffmpeg-protocols.html#http
}

ffmpeg_options = {
    'options': '-vn',
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


def executable_found(executable_name: str) -> bool:
    return shutil.which(executable_name) is not None


def validate_required_executables() -> None:
    required_executables = ["yt-dlp", "ffmpeg"]
    for executable in required_executables:
        if not executable_found(executable):
            print(f"Executable {executable} not found!\nPlease install requirements.txt and external dependencies first!")
            exit(1)


def get_most_replayed_start_in_seconds(heatmap) -> int:
    highest_value = 0
    index = 0
    for i in range(len(heatmap) - 2):
        total_value = heatmap[i]['value'] + heatmap[i + 1]['value'] + heatmap[i + 2]['value']
        if total_value > highest_value:
            highest_value = total_value
            index = i
    return math.floor(heatmap[index]["start_time"])


async def download_song(url: str):
    loop = asyncio.get_event_loop()
    data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=True))

    if 'entries' in data:
        data = data['entries'][0]
    return data


def clip_song(song_data, clip_length=10):
    start = get_most_replayed_start_in_seconds(song_data['heatmap'])

    full_mp3_file = ytdl.prepare_filename(song_data)
    clipped_mp3_file = re.sub("(\.mp3)$", "-clipped.mp3", full_mp3_file)
    subprocess.run(
        ["ffmpeg", "-y", "-ss", f"{start}", "-i", f"{full_mp3_file}", "-t", f"{clip_length}", f"{clipped_mp3_file}"]
    )

    os.remove(full_mp3_file)


async def download_clip(song: str) -> None:
    validate_required_executables()
    song_data = await download_song(song)
    clip_song(song_data)


if __name__ == "__main__":
    print("File is not meant to be run directly!")
    exit(1)
