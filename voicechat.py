import pyttsx3
import threading

engine = pyttsx3.init()
engine.setProperty("rate", 170)

stop_speaking_flag = False

def speakchat(text):
    global stop_speaking_flag
    stop_speaking_flag = False

    def run():
        global stop_speaking_flag
        print("Assistant:", text)
        engine.say(text)
        engine.runAndWait()

    thread = threading.Thread(target=run)
    thread.start()

def stop_speaking():
    global stop_speaking_flag
    stop_speaking_flag = True
    engine.stop()