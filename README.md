# clip-songs

Small python project that uses `yt-dlp` and `ffmpeg` to download and clip the most replayed 10 seconds of a song.

## Install
Needs both `yt-dlp` (which will be installed by pip) and [ffmpeg](https://ffmpeg.org/).

```bash
python -m venv .venv
. ./venv/bin/activate
pip install -r requirements.txt
chmod +x main.py
./main.py "<song>" # This will generate a 10 second clip of the most replayed part of the song
```

## Customisation
The length of the clip can be customised by changing the `clip_length` variable in the 
`clip_song(song_data, clip_length=10)` function of the file [clip.py](clip.py).