# from face_login import authenticate_user
from voice import speak, listen,stop_ai
from commands import process
import subprocess
import command_queue
import threading
import time
import human_ai


result = subprocess.run(
    ["python", "face_login.py"],
    capture_output=True,
    text=True
)

# =========================
# LOGIN FIRST
# =========================
if "Login successful" in result.stdout:
    human_ai.human_ai.human_speak("Face verified. Initializing your personal assistant.")

    # speak("Login successful. Starting assistant")
    
    # Start the command queue worker
    command_queue.command_queue.start_worker()

    running = True
    
    def check_queue_status():
        """Check queue status periodically"""
        while running:
            status = command_queue.command_queue.get_queue_status()
            if status['queue_size'] > 0:
                print(f"\nQueue: {status['queue_size']} commands waiting")
                if status['current_task']:
                    print(f"Currently executing: {status['current_task']}")
            time.sleep(5)
    
    # Start queue status checker
    status_thread = threading.Thread(target=check_queue_status, daemon=True)
    status_thread.start()

    while running:

        command = listen()

        if command:
            stop_ai()
            # Check if current task is running and queue is empty
            status = command_queue.command_queue.get_queue_status()
            
            if status['current_task'] is None and status['queue_size'] == 0:
                # No current task, execute immediately
                running = process(command)
            else:
                # Task is running or queue has items, add to queue
                queue_size = command_queue.command_queue.add_command(command, process)
                speak(f"Command added to queue. Position: {queue_size}")
                print(f"Command queued: '{command}' (Position {queue_size})")
                
                # For exit commands, process immediately
                if "exit" in command or "stop" in command:
                    running = process(command)
                    command_queue.command_queue.stop()
                    break


else:
    print("Face Login Failed")
    speak("Face Login Failed")