import argparse
import os

from pydub import AudioSegment
from pytube import YouTube

AUDIO_DOWNLOAD_DIR = "../songs"
OUTPUT_FORMAT = "wav"


def YoutubeAudioDownload(video_url):
    video = YouTube(video_url)
    audio = video.streams.filter(only_audio=True).first()

    try:
        audio_file_path = audio.download(output_path=AUDIO_DOWNLOAD_DIR)
        convert_to_wav(audio_file_path)
        os.remove(
            audio_file_path
        )  # Remove the original downloaded file after conversion
    except Exception:
        print("Failed to download audio")

    print("Audio was downloaded and converted to WAV successfully")


def convert_to_wav(input_file):
    # Load the audio file
    audio = AudioSegment.from_file(input_file)

    # Define the output file path with WAV extension
    output_file = os.path.splitext(input_file)[0] + ".wav"

    # Export the audio to WAV format
    audio.export(output_file, format=OUTPUT_FORMAT)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video", required=True, help="Youtube video URL")
    ap.add_argument(
        "-a",
        "--audio",
        required=False,
        help="Audio only",
        action=argparse.BooleanOptionalAction,
    )
    args = vars(ap.parse_args())

    if args["audio"]:
        YoutubeAudioDownload(args["video"])
