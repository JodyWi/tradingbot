import os
import datetime
import pygame
import torch
from TTS.api import TTS


# Directory to save the generated audio file
tts_directory = "data\\tts_data"
# ~\tradingbot_st\data\tts_data
os.makedirs(tts_directory, exist_ok=True)  # Ensure the directory exists



def run_tts_tts(text):


    # Check if GPU is available

    device = "cuda" if torch.cuda.is_available() else "cpu"

    # Initialize pygame mixer for audio playback
    pygame.mixer.init()

    # Create an instance of the TTS class
    tts = TTS()

    # List available 🐸TTS models
    # print("Available models:", tts.list_models())

    # Initialize TTS with a multilingual model
    tts = TTS(model_name="tts_models/en/jenny/jenny", progress_bar=False).to(device)

    # Define the text you want to synthesize
    text = f"{text}"

    # Create a filename with a unique timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    output_file = os.path.join(tts_directory, f"{timestamp}.wav")

    # Save the speech to the file with the timestamped filename
    tts.tts_to_file(text=text, file_path=output_file)

    # Play the generated audio automatically using pygame
    pygame.mixer.music.load(output_file)
    pygame.mixer.music.play()

    # Keep the script alive while the audio is playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)


    print(f"Speech synthesis complete. Audio saved to {output_file}")