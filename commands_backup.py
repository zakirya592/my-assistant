from voice import speak
import system
from ai import ask_ai
import json
import subprocess
from memory import remember, recall
import search_ai
import task_manager
import command_queue
import auto_background
from datetime import datetime
import pyautogui
import vision_ai
import human_ai

def process(command):

    if not command:
        return True

    # =========================
    # EXIT
    # =========================

    if "exit" in command or "stop" in command:
        human_ai.human_ai.human_speak("Alright, I'm shutting down now. Take care!")
        return False

    # =========================
    # OPEN APPS
    # =========================

    elif "open" in command:
        # Extract the app name after "open "
        app_name = command.replace("open ", "").strip()
        
        # Handle special cases first
        if app_name == "youtube":
            human_ai.human_ai.acknowledge_command(command)
            system.open_youtube()
            human_ai.human_ai.human_speak("Opening YouTube for you!")
        elif app_name == "google":
            human_ai.human_ai.acknowledge_command(command)
            system.open_google()
            human_ai.human_ai.human_speak("Let me open Google for you.")
        else:
            # Try to open any application by name
            human_ai.human_ai.acknowledge_command(command)
            success = system.open_app(app_name)
            if success:
                human_ai.human_ai.human_speak(f"Okay, opening {app_name} now.")
            else:
                human_ai.human_ai.human_speak(f"Hmm, I couldn't find {app_name} on your system. Sorry about that!")

    # =========================
    # CLOSE APPS
    # =========================

    elif "close" in command:
        # Extract the app name after "close "
        app_name = command.replace("close ", "").strip()
        
        # Try to close the application
        human_ai.human_ai.acknowledge_command(command)
        success = system.close_app(app_name)
        if success:
            human_ai.human_ai.human_speak(f"Okay, I'm closing {app_name} now.")
        else:
            human_ai.human_ai.human_speak(f"I don't see {app_name} running right now.")

    # =========================
    # SYSTEM CONTROL
    # =========================

    elif "shutdown" in command:
        human_ai.human_ai.human_speak("Okay, I'm shutting down your system now. Make sure you've saved everything!")
        system.shutdown()

    elif "restart" in command:
        human_ai.human_ai.human_speak("Alright, restarting your system now. I'll be back in a moment!")
        system.restart()

    # =========================
    # VOLUME CONTROL
    # =========================

    elif "volume up" in command:
        system.volume_up()
        speak("Volume increased")

    elif "volume down" in command:
        system.volume_down()
        speak("Volume decreased")

    # =========================
    # SCREENSHOT
    # =========================

    elif "screenshot" in command:
        system.screenshot()
        speak("Screenshot taken")

    # =========================
    # SEARCH
    # =========================

    elif "search" in command:
        query = command.replace("search", "")
        system.search_google(query)
        speak("Searching Google")
     

     # ==========================================
    # SEARCH FILES/FOLDERS
    # ==========================================

    elif "find" in command or "search for" in command:

        text = command

        text = text.replace("find", "")
        text = text.replace("search for", "")

        item_name = text.strip()

        # Check if background search is requested
        if "background" in command or "in background" in command:
            speak(f"Starting background search for {item_name}")
            task_id = search_ai.search_pc_background(item_name)
            speak(f"Search started with task ID: {task_id}")
        else:
            speak(f"Searching for {item_name}")
            
            # Use manual background detection for search
            import time
            start_time = time.time()
            
            def run_search():
                return search_ai.search_pc(item_name)
            
            # Start search in background thread
            import threading
            search_thread = threading.Thread(target=run_search, daemon=True)
            search_thread.start()
            
            # Wait for up to 10 seconds
            search_thread.join(timeout=10)
            
            if search_thread.is_alive():
                # Search is taking too long, let it continue in background
                task_id = task_manager.task_manager.run_task_in_background(
                    search_ai.search_pc, 
                    f"Search for {item_name}", 
                    item_name
                )
                speak(f"Search is taking longer than expected, continuing in background with ID: {task_id}")
            else:
                # Search completed quickly
                execution_time = time.time() - start_time
                if execution_time > 10:
                    speak(f"Search completed in {execution_time:.1f} seconds")
                # The result will be spoken by the search function itself
    # =========================
    # APP MANAGEMENT
    # =========================

    elif "refresh apps" in command or "update apps" in command:
        speak("Refreshing application cache...")
        if system.refresh_executable_cache():
            speak("Application cache updated successfully")
        else:
            speak("Error refreshing application cache")

    elif "refresh" in command or "reload" in command:

        pyautogui.press("f5")

        speak("Page refreshed")

    elif "list apps" in command or "installed apps" in command or "show apps" in command:
        speak("Listing available applications...")
        try:
            with open("installed_executables.json", "r") as f:
                executables = json.load(f)
            
            if executables:
                speak(f"Found {len(executables)} applications")
                print(f"\nAvailable Applications ({len(executables)}):")
                print("=" * 50)
                for i, (exe_name, exe_path) in enumerate(sorted(executables.items())[:20], 1):
                    print(f"{i}. {exe_name}")
                
                if len(executables) > 20:
                    print(f"... and {len(executables) - 20} more")
                
                print(f"\nFull list saved to 'available_apps.txt'")
                
                # Save full list to file
                with open("available_apps.txt", "w", encoding="utf-8") as f:
                    f.write("Available Applications:\n")
                    f.write("=" * 50 + "\n")
                    for i, (exe_name, exe_path) in enumerate(sorted(executables.items()), 1):
                        f.write(f"{i}. {exe_name}\n")
            else:
                speak("No applications found. Try refreshing the cache first")
        except Exception:
            speak("No application cache found. Say 'refresh apps' to create one")

    elif "running apps" in command or "list running" in command or "show running" in command:
        speak("Listing running applications...")
        try:
            result = subprocess.run('tasklist', shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                running_apps = []
                for line in lines[3:]:  # Skip header lines
                    if line.strip():
                        parts = line.split()
                        if len(parts) >= 2:
                            app_name = parts[0].replace('.exe', '')
                            running_apps.append(app_name)
                
                if running_apps:
                    speak(f"Found {len(running_apps)} running applications")
                    print(f"\nRunning Applications ({len(running_apps)}):")
                    print("=" * 50)
                    for i, app in enumerate(sorted(running_apps)[:20], 1):
                        print(f"{i}. {app}")
                    
                    if len(running_apps) > 20:
                        print(f"... and {len(running_apps) - 20} more")
                    
                    # Save to file
                    with open("running_apps.txt", "w", encoding="utf-8") as f:
                        f.write("Running Applications:\n")
                        f.write("=" * 50 + "\n")
                        for i, app in enumerate(sorted(running_apps), 1):
                            f.write(f"{i}. {app}\n")
                    
                    print(f"\nFull list saved to 'running_apps.txt'")
                else:
                    speak("No running applications found")
            else:
                speak("Error getting running applications")
        except Exception as e:
            speak("Error listing running applications")
            print(f"Error: {e}")
    
        # =========================
    # MEMORY SYSTEM
    # =========================
    elif "remember" in command:

        text = command.replace("remember", "").strip()

        if " is " in text:

            key, value = text.split(" is ", 1)

            remember(key.strip(), value.strip())

            speak("I will remember that")

    elif "what is my" in command:

        key = command.replace("what is my", "").strip()

        value = recall(key)

        if value:

            speak(f"Your {key} is {value}")

        else:

            speak("I do not remember")
    # =========================
    # AI CHAT
    # =========================
    elif "EZ" in command:
        try:
            answer = ask_ai(command)
            speak(answer)
        except Exception as e:
            print("AI Error:", e)
            speak("AI is currently unavailable")
    # =========================
    # TASK MANAGEMENT
    # =========================
    elif "task status" in command or "check task" in command:
        tasks = task_manager.task_manager.get_all_tasks()
        if tasks:
            speak(f"Found {len(tasks)} tasks")
            print("\nTask Status:")
            print("=" * 60)
            for task_id, task in tasks.items():
                status = task['status']
                name = task['name']
                start_time = task['start_time'].strftime("%H:%M:%S")
                print(f"ID: {task_id} | {name} | {status} | Started: {start_time}")
                if status == 'failed' and 'error' in task:
                    print(f"  Error: {task['error']}")
        else:
            speak("No tasks found")

    elif "clear tasks" in command:
        task_manager.task_manager.clear_completed_tasks()
    # =========================
    # QUEUE MANAGEMENT
    # =========================

    elif "queue status" in command or "check queue" in command:
        status = command_queue.command_queue.get_queue_status()
        speak(f"Queue has {status['queue_size']} commands waiting")
        print(f"\nQueue Status:")
        print("=" * 40)
        print(f"Commands in queue: {status['queue_size']}")
        if status['current_task']:
            print(f"Currently executing: {status['current_task']}")
        else:
            print("No command currently executing")

    elif "clear queue" in command:
        # Clear all pending commands from queue
        while not command_queue.command_queue.command_queue.empty():
            command_queue.command_queue.command_queue.get()
            command_queue.command_queue.command_queue.task_done()
        speak("Queue cleared")

    elif "background tasks" in command or "running background" in command:
        tasks = auto_background.auto_bg.get_background_tasks()
        if tasks:
            speak(f"Found {len(tasks)} background tasks")
            print("\nBackground Tasks:")
            print("=" * 60)
            for task_id, task in tasks.items():
                status = task['status']
                name = task['name']
                start_time = task.get('start_time', 0)
                if start_time:
                    start_str = f"{datetime.fromtimestamp(start_time).strftime('%H:%M:%S')}"
                else:
                    start_str = "Unknown"
                
                print(f"Task: {name} | Status: {status} | Started: {start_str}")
                if 'execution_time' in task:
                    print(f"  Execution time: {task['execution_time']:.1f}s")
                if 'error' in task:
                    print(f"  Error: {task['error']}")
        else:
            speak("No background tasks found")
    
    # =========================
# MEMORY SYSTEM
# =========================
elif "remember" in command:

    text = command.replace("remember", "").strip()

    if " is " in text:

        key, value = text.split(" is ", 1)

        remember(key.strip(), value.strip())
    elif "click" in command:
        human_ai.human_ai.acknowledge_command(command)
        target = command.replace(
            "click",
            ""
        ).strip()
        result = vision_ai.click_text(target)
        human_ai.human_ai.human_speak(result)


    # ==========================================
    # TYPE TEXT
    # ==========================================

    elif "type" in command:
        human_ai.human_ai.acknowledge_command(command)
        text = command.replace(
            "type",
            ""
        ).strip()
        result = vision_ai.type_text(text)
        human_ai.human_ai.human_speak(result)


    # ==========================================
    # PRESS KEY
    # ==========================================

    elif "press" in command:
        human_ai.human_ai.acknowledge_command(command)
        key = command.replace(
            "press",
            ""
        ).strip()
        result = vision_ai.press_key(key)
        human_ai.human_ai.human_speak(result)


    # ==========================================
    # SCROLL DOWN
    # ==========================================

    elif "scroll down" in command:
        human_ai.human_ai.acknowledge_command(command)
        result = vision_ai.scroll_down()
        human_ai.human_ai.human_speak(result)


    # ==========================================
    # SCROLL UP
    # ==========================================

    elif "scroll up" in command:
        human_ai.human_ai.acknowledge_command(command)
        result = vision_ai.scroll_up()
        human_ai.human_ai.human_speak(result)


    # ==========================================
    # OPEN SCREENSHOT
    # ==========================================

    elif "open screenshot" in command:
        human_ai.human_ai.acknowledge_command(command)
        result = vision_ai.open_last_screenshot()
        human_ai.human_ai.human_speak(result)



    else:
        human_ai.human_ai.human_speak("Hmm, I'm not sure what you mean by that. Could you try saying it differently?")
    

    return True
