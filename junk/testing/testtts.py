import ChatTTS
import torch
import torchaudio

# Initialize ChatTTS
chat = ChatTTS.Chat()
chat.load(compile=False)  # Set to True for better performance if needed

# Texts to convert to audio
texts = ["PUT YOUR 1st TEXT HERE", "PUT YOUR 2nd TEXT HERE"]

# Infer the text-to-speech conversion
wavs = chat.infer(texts)

# Save each wav file
for i in range(len(wavs)):
    try:
        # Try saving with unsqueeze (1 channel audio)
        torchaudio.save(f"basic_output{i}.wav", torch.from_numpy(wavs[i]).unsqueeze(0), 24000, format="wav")
    except:
        # Fallback in case the first method fails (without unsqueeze)
        torchaudio.save(f"basic_output{i}.wav", torch.from_numpy(wavs[i]), 24000, format="wav")
