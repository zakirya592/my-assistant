import json
import os

MEMORY_FILE = "memory.json"

# =========================
# LOAD MEMORY
# =========================

def load_memory():

    if not os.path.exists(MEMORY_FILE):

        with open(MEMORY_FILE, "w") as file:
            json.dump({}, file)

    with open(MEMORY_FILE, "r") as file:

        return json.load(file)

# =========================
# SAVE MEMORY
# =========================

def save_memory(data):

    with open(MEMORY_FILE, "w") as file:

        json.dump(data, file, indent=4)

# =========================
# REMEMBER
# =========================

def remember(key, value):

    data = load_memory()

    data[key] = value

    save_memory(data)

# =========================
# RECALL
# =========================

def recall(key):

    data = load_memory()

    return data.get(key, None)