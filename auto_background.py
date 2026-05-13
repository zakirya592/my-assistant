import threading
import time
import functools
from voice import speak
from datetime import datetime

class AutoBackgroundManager:
    def __init__(self):
        self.background_tasks = {}
        self.lock = threading.Lock()
        self.timeout_threshold = 10  # seconds
    
    def auto_background(self, func_name=None):
        """Decorator to automatically run functions in background if they take > 10 seconds"""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                # Create a unique task ID
                task_id = f"{func.__name__}_{int(time.time())}"
                
                def run_with_timeout():
                    start_time = time.time()
                    try:
                        result = func(*args, **kwargs)
                        execution_time = time.time() - start_time
                        
                        with self.lock:
                            self.background_tasks[task_id] = {
                                'name': func_name or func.__name__,
                                'status': 'completed',
                                'start_time': start_time,
                                'end_time': time.time(),
                                'execution_time': execution_time,
                                'result': result
                            }
                        
                        if execution_time > self.timeout_threshold:
                            speak(f"Task {func_name or func.__name__} completed in {execution_time:.1f} seconds")
                        
                        return result
                        
                    except Exception as e:
                        execution_time = time.time() - start_time
                        with self.lock:
                            self.background_tasks[task_id] = {
                                'name': func_name or func.__name__,
                                'status': 'failed',
                                'start_time': start_time,
                                'end_time': time.time(),
                                'execution_time': execution_time,
                                'error': str(e)
                            }
                        
                        if execution_time > self.timeout_threshold:
                            speak(f"Task {func_name or func.__name__} failed after {execution_time:.1f} seconds")
                        
                        raise e
                
                # Start the function in a thread with timeout detection
                thread = threading.Thread(target=run_with_timeout, daemon=True)
                thread.start()
                
                # Wait for up to 10 seconds
                thread.join(timeout=self.timeout_threshold)
                
                if thread.is_alive():
                    # Task is taking longer than 10 seconds, continue in background
                    with self.lock:
                        self.background_tasks[task_id] = {
                            'name': func_name or func.__name__,
                            'status': 'running_background',
                            'start_time': time.time(),
                            'thread': thread
                        }
                    
                    speak(f"Task {func_name or func.__name__} is running in background")
                    return None  # Return None for background tasks
                
                # Task completed within 10 seconds, get result
                with self.lock:
                    if task_id in self.background_tasks:
                        task = self.background_tasks[task_id]
                        if task['status'] == 'completed':
                            return task['result']
                        elif task['status'] == 'failed':
                            raise Exception(task['error'])
                
                return None
            
            return wrapper
        return decorator
    
    def get_background_tasks(self):
        """Get all background tasks"""
        with self.lock:
            return self.background_tasks.copy()
    
    def clear_completed_tasks(self):
        """Clear completed background tasks"""
        with self.lock:
            completed_ids = [tid for tid, task in self.background_tasks.items() 
                           if task['status'] in ['completed', 'failed']]
            for tid in completed_ids:
                del self.background_tasks[tid]

# Global auto background manager
auto_bg = AutoBackgroundManager()
