import os
import datetime
import pyttsx3


# Directory to save the generated audio file
tts_directory = "data\\tts_data"
# ~\tradingbot_st\data\tts_data
os.makedirs(tts_directory, exist_ok=True)  # Ensure the directory exists


def run_tts_pyttsx3(text):
    """Run TTS engine once on app startup."""

    # Initialize the TTS engine (only once)
    engine = pyttsx3.init()

    # Select the voice index
    engine.setProperty("voice", "english")
    engine.setProperty("rate", 150)

    # Run TTS engine once
    engine.say(text)
    engine.runAndWait()
    engine.stop()  # Stop after running once

    # Save the generated audio file
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    output_file = os.path.join(tts_directory, f"pyttsx3{timestamp}.wav")
    engine.save_to_file(text, output_file)

    
