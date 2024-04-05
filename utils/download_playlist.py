import os

from pytube import Playlist

# Specify the URL of the YouTube playlist
playlist_url = (
    "https://www.youtube.com/playlist?list=PLgneFNebuPpeH8RVvHxVinWTioZCuhMAD"
)

# Create a Playlist object
playlist = Playlist(playlist_url)

# Create a directory to save the audio files if it doesn't exist
save_directory = "songs"
if not os.path.exists(save_directory):
    os.makedirs(save_directory)

# Download each video in the playlist
for i, video in enumerate(playlist.videos):
    if i == 100:
        break
    print(f"Downloading: {video.title}")
    # Get the audio stream and download it
    audio_stream = video.streams.filter(only_audio=True).first()
    if audio_stream:
        # Download the audio stream and save it in the "songs" directory with the .wav extension
        audio_stream.download(output_path=save_directory, filename_prefix="audio_")
        # Rename the downloaded file with the video title
        downloaded_file = os.path.join(
            save_directory, f"audio_{audio_stream.default_filename}"
        )
        new_file = os.path.join(save_directory, f"{video.title}.wav")
        os.rename(downloaded_file, new_file)
        print(f"Downloaded and saved as: {new_file}")
    else:
        print(f"No audio stream found for: {video.title}")
