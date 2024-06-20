import sys
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ChangeHandler(FileSystemEventHandler):
    def __init__(self, command):
        self.command = command
        self.process = None
        self.start_process()
    
    def on_any_event(self, event):
        print(f"Change detected: {event.src_path}")
        self.restart_process()
    
    def start_process(self):
        if self.process:
            self.process.kill()
        print("Starting process...")
        self.process = subprocess.Popen(self.command, shell=True)
    
    def restart_process(self):
        print("Restarting process...")
        self.start_process()

if __name__ == "__main__":
    path = "./src"
    command = "python test-https-server.py"
    
    event_handler = ChangeHandler(command)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    
    observer.join()