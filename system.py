import os
import subprocess
import pyautogui
from voice import speak
import webbrowser
import shutil
import glob
import json

def open_notepad():
    subprocess.Popen("notepad.exe")

def shutdown():
    speak("Shutting down system")
    os.system("shutdown /s /t 1")

def restart():
    speak("Restarting system")
    os.system("shutdown /r /t 1")

def volume_up():
    pyautogui.press("volumeup", presses=5)

def volume_down():
    pyautogui.press("volumedown", presses=5)

def screenshot():
    img = pyautogui.screenshot()
    img.save("screen.png")
    speak("Screenshot taken")

def open_google():
    webbrowser.open("https://google.com")
    speak("Opening Google")

def open_youtube():
    webbrowser.open("https://youtube.com")
    speak("Opening YouTube")

def search_google(query):
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)
    speak("Searching Google")

def open_app(app_name):
    """Open an application if it's installed"""
    try:
        # First try direct execution
        try:
            subprocess.Popen(app_name)
            return True
        except FileNotFoundError:
            pass
        
        # Try with .exe extension
        try:
            subprocess.Popen(f"{app_name}.exe")
            return True
        except FileNotFoundError:
            pass
        
        # Try common Windows applications
        windows_apps = {
            "control panel": "control",
            "control": "control",
            "calculator": "calc",
            "calc": "calc",
            "task manager": "taskmgr",
            "taskmgr": "taskmgr",
            "this pc": "explorer",
            "file explorer": "explorer",
            "explorer": "explorer",
            "recycle bin": "explorer ::{645FF040-5081-101B-9F08-00AA002F954E}",
            "ms word": "winword",
            "word": "winword",
            "microsoft word": "winword",
            "excel": "excel",
            "ms excel": "excel",
            "microsoft excel": "excel",
            "powerpoint": "powerpnt",
            "ms powerpoint": "powerpnt",
            "microsoft powerpoint": "powerpnt"
        }
        
        # Check if app name matches any Windows app
        lower_app = app_name.lower()
        if lower_app in windows_apps:
            subprocess.Popen(windows_apps[lower_app])
            return True
        
        # Check if executable exists in PATH
        if shutil.which(app_name.lower()):
            subprocess.Popen(app_name.lower())
            return True
        
        # Search for executable
        exe_path = find_app_by_name(app_name)
        if exe_path:
            subprocess.Popen(exe_path)
            return True
        
        return False
        
    except Exception:
        return False

def find_installed_executables():
    """Find all executable files in common installation directories"""
    executables = {}
    
    # Common installation directories
    search_paths = [
        "C:\\Program Files\\*",
        "C:\\Program Files (x86)\\*",
        f"C:\\Users\\{os.getenv('USERNAME')}\\AppData\\Local\\*",
        f"C:\\Users\\{os.getenv('USERNAME')}\\AppData\\Roaming\\*"
    ]
    
    for path_pattern in search_paths:
        try:
            for root_dir in glob.glob(path_pattern):
                if os.path.isdir(root_dir):
                    # Search for .exe files
                    for exe_path in glob.glob(f"{root_dir}\\*.exe"):
                        exe_name = os.path.basename(exe_path).replace('.exe', '').lower()
                        executables[exe_name] = exe_path
                    
                    # Search in subdirectories (up to 2 levels deep)
                    for subdir in glob.glob(f"{root_dir}\\*"):
                        if os.path.isdir(subdir):
                            for exe_path in glob.glob(f"{subdir}\\*.exe"):
                                exe_name = os.path.basename(exe_path).replace('.exe', '').lower()
                                executables[exe_name] = exe_path
                            
                            # One more level deep
                            for subsubdir in glob.glob(f"{subdir}\\*"):
                                if os.path.isdir(subsubdir):
                                    for exe_path in glob.glob(f"{subsubdir}\\*.exe"):
                                        exe_name = os.path.basename(exe_path).replace('.exe', '').lower()
                                        executables[exe_name] = exe_path
        except Exception:
            continue
    
    return executables

def find_app_by_name(app_name):
    """Find an application executable by searching through installed programs"""
    app_name = app_name.lower()
    
    # First, try to find from cached executables
    try:
        if os.path.exists("installed_executables.json"):
            with open("installed_executables.json", "r") as f:
                cached_executables = json.load(f)
                
            # Check exact match
            if app_name in cached_executables:
                return cached_executables[app_name]
            
            # Check partial matches
            for exe_name, exe_path in cached_executables.items():
                if app_name in exe_name or exe_name in app_name:
                    return exe_path
    except Exception:
        pass
    
    # If not found in cache, search fresh
    executables = find_installed_executables()
    
    # Cache for future use
    try:
        with open("installed_executables.json", "w") as f:
            json.dump(executables, f)
    except Exception:
        pass
    
    # Check exact match
    if app_name in executables:
        return executables[app_name]
    
    # Check partial matches
    for exe_name, exe_path in executables.items():
        if app_name in exe_name or exe_name in app_name:
            return exe_path
    
    return None

def refresh_executable_cache():
    """Refresh the cache of installed executables"""
    executables = find_installed_executables()
    try:
        with open("installed_executables.json", "w") as f:
            json.dump(executables, f)
        print(f"Cache refreshed with {len(executables)} executables")
        return True
    except Exception as e:
        print(f"Error refreshing cache: {e}")
        return False

def close_app(app_name):
    """Close an application by name"""
    try:
        app_name = app_name.lower()
        
        # Map common app names to process names
        process_names = {
            "chrome": "chrome.exe",
            "google chrome": "chrome.exe",
            "firefox": "firefox.exe",
            "mozilla firefox": "firefox.exe",
            "edge": "msedge.exe",
            "microsoft edge": "msedge.exe",
            "notepad": "notepad.exe",
            "calculator": "calculator.exe",
            "calc": "calculator.exe",
            "word": "winword.exe",
            "microsoft word": "winword.exe",
            "excel": "excel.exe",
            "microsoft excel": "excel.exe",
            "powerpoint": "powerpnt.exe",
            "microsoft powerpoint": "powerpnt.exe",
            "vlc": "vlc.exe",
            "media player": "wmplayer.exe",
            "spotify": "spotify.exe",
            "discord": "discord.exe",
            "steam": "steam.exe",
            "task manager": "taskmgr.exe",
            "explorer": "explorer.exe",
            "file explorer": "explorer.exe",
            "postman": "postman.exe",
            "postman copy": "postman.exe",
            "zoom": "zoom.exe",
            "zoom workspace": "zoom.exe"
        }
        
        # Get the process name
        process_name = process_names.get(app_name, f"{app_name}.exe")
        
        # Try to close by process name first
        try:
            result = subprocess.run(f'taskkill /f /im "{process_name}"', shell=True, capture_output=True, text=True)
            if "SUCCESS" in result.stdout:
                return True
        except Exception:
            pass
        
        # Try to find process by partial name matching
        try:
            result = subprocess.run('tasklist', shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if app_name.replace(' ', '') in line.replace(' ', '').lower():
                        parts = line.split()
                        if len(parts) >= 2 and parts[1].isdigit():
                            pid = parts[1]
                            try:
                                kill_result = subprocess.run(f'taskkill /f /pid {pid}', shell=True, capture_output=True, text=True)
                                if "SUCCESS" in kill_result.stdout:
                                    return True
                            except Exception:
                                continue
        except Exception:
            pass
        
        # Try WMIC for more robust process finding
        try:
            wmic_result = subprocess.run(f'wmic process where "name like \'%{app_name}%\'" get processid', shell=True, capture_output=True, text=True)
            if wmic_result.returncode == 0:
                lines = wmic_result.stdout.strip().split('\n')
                for line in lines[1:]:  # Skip header
                    line = line.strip()
                    if line and line.isdigit():
                        pid = line
                        try:
                            kill_result = subprocess.run(f'taskkill /f /pid {pid}', shell=True, capture_output=True, text=True)
                            if "SUCCESS" in kill_result.stdout:
                                return True
                        except Exception:
                            continue
        except Exception:
            pass
        
        return False
        
    except Exception:
        return False