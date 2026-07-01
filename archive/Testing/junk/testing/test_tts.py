import pyttsx3
engine = pyttsx3.init(driverName='espeak')  # Specify espeak
engine.say("Hello World")
engine.runAndWait()
