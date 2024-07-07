import speech_recognition as sr
import datetime
import wikipedia
import pywhatkit
import pyautogui

from llm import generate_content
from voice import engine, recognizer


def execute_command():
    try:
        with sr.Microphone() as source:
            print("Listening..")
            audio = recognizer.listen(source)
            command = recognizer.recognize_google(audio, language="pt-BR").lower()
            print(f"Command: {command}")
            return command        
    except sr.UnknownValueError as e:
        print(f"Could not understand the audio; {e}")
    except sr.RequestError as e:
        print(f"Error requesting speech recognition service results; {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def user_voice_command():
    engine.say("Estou ouvindo!")
    while True:
        engine.runAndWait()
        command = execute_command()
        if command:
            engine.say("Um momento, estou pensando...")
            engine.runAndWait()
            result = generate_content(command)
            print(result)
            engine.say(result)
            engine.runAndWait()

            if "desligar" in command:
                print("Até logo!")
                engine.say("Até logo!")
                engine.runAndWait()
                break
"""
def user_voice_command():
    while True:
        command = execute_command()
        #command = input("Command: ")
        if command:
            result = generate_content(command)
            engine.say(result)
            engine.runAndWait()

            
               
            if "horas" in command:
                print("buscando horas...")
                current_time = datetime.datetime.now().strftime("%H:%M")
                engine.say("Agora são " + current_time)
                engine.runAndWait()
            elif "procure por" in command:
                print("procurando informação...")
                search_query = command.replace("procure por", "")
                wikipedia.set_lang("pt")
                result = wikipedia.summary(search_query, 2)
                print(result)
                engine.say(result)
                engine.runAndWait()
            elif "tocar" in command:
                print("tocando...")
                song = command.replace("toque", "")
                result = pywhatkit.playonyt(song)
                print(result)
                engine.say("Tocando música")
                engine.runAndWait()
            elif "fechar guia" in command:
                print("fechando...")
                pyautogui.hotkey('ctrl', 'w')
            elif "olá" in command:
                print("Olá")
                engine.say("Olá, tudo bem?")
                engine.runAndWait()
            elif "curiosidade" in command:
                print("buscando uma curiosidade...")
                result = generate_content("Me retorne uma curiosidade (em portugues)").replace("*", "")
                engine.say(result)
                engine.runAndWait()
            elif "inteligencia" in command:
                print("inteligencia...")
                result = generate_content(command)
                engine.say(result)
                engine.runAndWait()
            elif "desligar" in command:
                print("Até logo!")
                engine.say("Até logo!")
                engine.runAndWait()
                break
                
""" 

user_voice_command()
