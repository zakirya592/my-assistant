import os
import subprocess
import threading
import task_manager
import auto_background

# ==========================================
# SEARCH FILE OR FOLDER
# ==========================================

def search_pc(item_name):

    drives = []

    # --------------------------------------
    # CHECK DRIVES
    # --------------------------------------

    for drive_letter in "CDEFGHIJKLMNOPQRSTUVWXYZ":

        drive = f"{drive_letter}:\\"

        if os.path.exists(drive):

            drives.append(drive)

    # --------------------------------------
    # SEARCH
    # --------------------------------------

    for drive in drives:

        for root, dirs, files in os.walk(drive):

            # SEARCH FOLDERS
            for folder in dirs:

                if item_name.lower() in folder.lower():

                    path = os.path.join(root, folder)

                    open_location(path)

                    return f"Folder found at {path}"

            # SEARCH FILES
            for file in files:

                if item_name.lower() in file.lower():

                    path = os.path.join(root, file)

                    open_location(path)

                    return f"File found at {path}"

    return "Item not found"


# ==========================================
# OPEN LOCATION
# ==========================================

def open_location(path):

    subprocess.run(
        f'explorer /select,"{path}"',
        shell=True
    )


# ==========================================
# BACKGROUND SEARCH
# ==========================================

def search_pc_background(item_name):
    """Start search in background and return task ID"""
    task_id = task_manager.task_manager.run_task_in_background(
        search_pc, 
        f"Search for {item_name}", 
        item_name
    )
    return task_id