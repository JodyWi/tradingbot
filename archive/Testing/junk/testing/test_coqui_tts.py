import pygame
import torch
from TTS.api import TTS

# Check if GPU is available
device = "cuda" if torch.cuda.is_available() else "cpu"


# Initialize pygame mixer for audio playback
pygame.mixer.init()

# Create an instance of the TTS class
tts = TTS()

# List available 🐸TTS models
print("Available models:", tts.list_models())

# Initialize TTS with a multilingual model
tts = TTS(model_name="tts_models/en/jenny/jenny", progress_bar=False).to(device)

# Define the text you want to synthesize
text = "Hello, this is a test of the Coqui TTS system. How are you today?"

# Generate the speech and save it to a file
output_path = "output_test.wav"
tts.tts_to_file(text=text, file_path=output_path)

# Load the audio file with pygame
pygame.mixer.music.load(output_path)

# Play the audio file
pygame.mixer.music.play()

# Keep the script alive while the audio is playing
while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)


print(f"Speech synthesis complete. Audio saved to {output_path}")
