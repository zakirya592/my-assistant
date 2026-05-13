import pyautogui
import pytesseract
from PIL import Image
import os
import cv2
import numpy as np

# ==========================================
# TESSERACT PATH
# ==========================================

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    
)

# ==========================================
# CREATE SCREENSHOT FOLDER
# ==========================================

if not os.path.exists("screenshots"):

    os.makedirs("screenshots")


# ==========================================
# TAKE SCREENSHOT
# ==========================================

def take_screenshot():

    image = pyautogui.screenshot()

    path = "screenshots/screen.png"

    image.save(path)

    return path


# ==========================================
# READ SCREEN TEXT
# ==========================================

def read_screen():

    path = take_screenshot()

    image = Image.open(path)

    text = pytesseract.image_to_string(image)

    if text.strip() == "":

        return "No text detected on screen"

    return text


# ==========================================
# FIND TEXT ON SCREEN
# ==========================================

def find_text(target_text):

    path = take_screenshot()

    image = cv2.imread(path)

    data = pytesseract.image_to_data(
        image,
        output_type=pytesseract.Output.DICT
    )

    for i, word in enumerate(data["text"]):

        if target_text.lower() in word.lower():

            x = data["left"][i]
            y = data["top"][i]
            w = data["width"][i]
            h = data["height"][i]

            center_x = x + w // 2
            center_y = y + h // 2

            return (
                center_x,
                center_y
            )

    return None


# ==========================================
# CLICK BUTTON/TEXT
# ==========================================

def click_text(target_text):

    position = find_text(target_text)

    if position:

        pyautogui.click(position)

        return f"Clicked {target_text}"

    return f"{target_text} not found"


# ==========================================
# TYPE TEXT
# ==========================================

def type_text(text):

    pyautogui.write(
        text,
        interval=0.05
    )

    return "Typing completed"


# ==========================================
# PRESS KEY
# ==========================================

def press_key(key):

    pyautogui.press(key)

    return f"{key} pressed"


# ==========================================
# SCROLL
# ==========================================

def scroll_up():

    pyautogui.scroll(500)

    return "Scrolled up"


def scroll_down():

    pyautogui.scroll(-500)

    return "Scrolled down"


# ==========================================
# OPEN SCREENSHOT
# ==========================================

def open_last_screenshot():

    path = "screenshots/screen.png"

    if os.path.exists(path):

        os.startfile(path)

        return "Opening screenshot"

    return "No screenshot found"