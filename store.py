import os

import numpy as np
import parselmouth
from tqdm import tqdm


def save_pitch_values_to_npy(directory, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Iterate over files in the directory
    for file_name in tqdm(os.listdir(directory)):
        if file_name.endswith(".wav"):
            file_path = os.path.join(directory, file_name)
            # Load the sound file and extract pitch values
            sound = parselmouth.Sound(file_path)
            pitch = sound.to_pitch()
            pitch_values = pitch.selected_array["frequency"]

            # Save pitch values to .npy file
            output_file = os.path.join(
                output_directory, os.path.splitext(file_name)[0] + ".npy"
            )
            np.save(output_file, pitch_values)


# Example usage
input_directory = "./data/songs_clean/"
output_directory = "./data/pitch_values/"

save_pitch_values_to_npy(input_directory, output_directory)
