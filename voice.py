import speech_recognition as sr
import asyncio
import edge_tts
import pygame
import os
import threading

VOICE = "en-US-GuyNeural"

pygame.mixer.init()

# =========================
# AI STOP FLAG
# =========================

ai_stop = False


# =========================
# ASYNC SPEAK
# =========================

async def async_speak(text):

    global ai_stop

    file_name = "voice.mp3"

    communicate = edge_tts.Communicate(text, VOICE)

    await communicate.save(file_name)

    pygame.mixer.music.load(file_name)

    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():

        if ai_stop:
            pygame.mixer.music.stop()
            break

        await asyncio.sleep(0.1)

    pygame.mixer.music.unload()

    if os.path.exists(file_name):
        os.remove(file_name)


# =========================
# SPEAK
# =========================

def speak(text):

    global ai_stop

    ai_stop = False

    print("Assistant:", text)

    def run():
        asyncio.run(async_speak(text))

    threading.Thread(target=run, daemon=True).start()


# =========================
# STOP AI SPEAKING
# =========================

def stop_ai():

    global ai_stop

    ai_stop = True

    pygame.mixer.music.stop()


# =========================
# LISTEN
# =========================

def listen():

    recognizer = sr.Recognizer()

    with sr.Microphone() as source:

        print("Listening...")

        recognizer.adjust_for_ambient_noise(source, duration=0.5)

        audio = recognizer.listen(source)

    try:

        command = recognizer.recognize_google(audio)

        print("You:", command)

        return command.lower()

    except Exception as e:

        print("Voice Error:", e)

        return ""