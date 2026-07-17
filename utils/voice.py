import pyttsx3

engine = pyttsx3.init()

engine.setProperty("rate",170)

spoken=set()

def speak(text):

    if text not in spoken:

        spoken.add(text)

        engine.say(text)

        engine.runAndWait()