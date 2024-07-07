import speech_recognition as sr
import pyttsx3


recognizer = sr.Recognizer()
engine = pyttsx3.init()

voice_id = r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_PT-BR_MARIA_11.0"
engine.setProperty('voice', voice_id)