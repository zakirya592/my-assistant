import threading
import time
import uuid
from datetime import datetime
from voice import speak

class TaskManager:
    def __init__(self):
        self.tasks = {}
        self.task_results = {}
        self.lock = threading.Lock()
    
    def run_task_in_background(self, task_func, task_name, *args, **kwargs):
        """Run a task in background thread"""
        task_id = str(uuid.uuid4())[:8]
        
        with self.lock:
            self.tasks[task_id] = {
                'name': task_name,
                'status': 'running',
                'start_time': datetime.now(),
                'thread': None
            }
        
        def task_wrapper():
            try:
                result = task_func(*args, **kwargs)
                with self.lock:
                    self.tasks[task_id]['status'] = 'completed'
                    self.tasks[task_id]['end_time'] = datetime.now()
                    self.task_results[task_id] = result
                speak(f"Task '{task_name}' completed")
            except Exception as e:
                with self.lock:
                    self.tasks[task_id]['status'] = 'failed'
                    self.tasks[task_id]['error'] = str(e)
                    self.tasks[task_id]['end_time'] = datetime.now()
                speak(f"Task '{task_name}' failed")
        
        thread = threading.Thread(target=task_wrapper)
        with self.lock:
            self.tasks[task_id]['thread'] = thread
        
        thread.start()
        speak(f"Started background task: {task_name}")
        return task_id
    
    def get_task_status(self, task_id):
        """Get status of a specific task"""
        with self.lock:
            if task_id in self.tasks:
                task = self.tasks[task_id]
                status_info = {
                    'id': task_id,
                    'name': task['name'],
                    'status': task['status'],
                    'start_time': task['start_time']
                }
                if 'end_time' in task:
                    status_info['end_time'] = task['end_time']
                if 'error' in task:
                    status_info['error'] = task['error']
                return status_info
            return None
    
    def get_all_tasks(self):
        """Get status of all tasks"""
        with self.lock:
            return self.tasks.copy()
    
    def get_task_result(self, task_id):
        """Get result of a completed task"""
        with self.lock:
            return self.task_results.get(task_id)
    
    def clear_completed_tasks(self):
        """Clear completed tasks from memory"""
        with self.lock:
            completed_ids = [tid for tid, task in self.tasks.items() 
                           if task['status'] in ['completed', 'failed']]
            for tid in completed_ids:
                del self.tasks[tid]
                if tid in self.task_results:
                    del self.task_results[tid]
        speak("Completed tasks cleared")

# Global task manager instance
task_manager = TaskManager()
