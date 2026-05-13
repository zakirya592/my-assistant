import threading
import time
import queue
from voice import speak

class CommandQueue:
    def __init__(self):
        self.command_queue = queue.Queue()
        self.current_task = None
        self.task_lock = threading.Lock()
        self.worker_thread = None
        self.running = False
        self.long_task_threshold = 10  # seconds
        
    def start_worker(self):
        """Start the background worker thread"""
        if not self.running:
            self.running = True
            self.worker_thread = threading.Thread(target=self._process_queue, daemon=True)
            self.worker_thread.start()
    
    def add_command(self, command, process_func):
        """Add a command to the queue"""
        self.command_queue.put((command, process_func))
        return len(self.command_queue.queue)
    
    def _process_queue(self):
        """Process commands from the queue"""
        while self.running:
            try:
                if not self.command_queue.empty():
                    command, process_func = self.command_queue.get()
                    
                    with self.task_lock:
                        self.current_task = command
                        start_time = time.time()
                    
                    try:
                        # Execute the command with timeout detection
                        result = self._execute_with_timeout(command, process_func)
                        
                        with self.task_lock:
                            execution_time = time.time() - start_time
                            if execution_time > self.long_task_threshold:
                                speak(f"Long task completed in {execution_time:.1f} seconds")
                        
                    except Exception as e:
                        print(f"Error executing command '{command}': {e}")
                        speak(f"Error executing command")
                    
                    finally:
                        with self.task_lock:
                            self.current_task = None
                        self.command_queue.task_done()
                
                else:
                    time.sleep(0.1)  # Small delay to prevent busy waiting
                    
            except Exception as e:
                print(f"Queue worker error: {e}")
    
    def _execute_with_timeout(self, command, process_func, timeout=30):
        """Execute a command with timeout detection"""
        def target():
            return process_func(command)
        
        result_container = []
        exception_container = []
        
        def wrapper():
            try:
                result = target()
                result_container.append(result)
            except Exception as e:
                exception_container.append(e)
        
        thread = threading.Thread(target=wrapper)
        thread.daemon = True
        thread.start()
        
        # Wait for completion or timeout
        thread.join(timeout)
        
        if thread.is_alive():
            # Task is taking too long, but we'll let it continue in background
            speak("Task is taking longer than expected, continuing in background")
            return None
        
        if exception_container:
            raise exception_container[0]
        
        return result_container[0] if result_container else None
    
    def get_queue_status(self):
        """Get current queue status"""
        with self.task_lock:
            status = {
                'queue_size': self.command_queue.qsize(),
                'current_task': self.current_task,
                'running': self.running
            }
        return status
    
    def stop(self):
        """Stop the queue worker"""
        self.running = False
        if self.worker_thread:
            self.worker_thread.join(timeout=5)

# Global command queue instance
command_queue = CommandQueue()
