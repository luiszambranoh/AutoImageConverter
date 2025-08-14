import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PIL import Image
from pathlib import Path

download_folder = r"C:\Users\Mimaki\Downloads"
destination_folder = r"C:\Users\Mimaki\Downloads\Converted_PNGs"

class ImageToPNGHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        
        if event.src_path.lower().endswith(('.webp', '.avif')):
            self.convert_to_png(event.src_path)

    def convert_to_png(self, file_path):
        file_path = Path(file_path)
        
        try:
            time.sleep(5)
            
            if file_path.exists() and not file_path.name.endswith(('.crdownload', '.part')):
                print(f"Checking file: {file_path}")
                
                img = Image.open(file_path)
                
                new_file_path = Path(destination_folder) / file_path.with_suffix(".png").name
                
                img.save(new_file_path, "PNG")
                
                print(f"Converted {file_path} to {new_file_path}")
                
            else:
                print(f"File not found or still being written: {file_path}")
        except Exception as e:
            print(f"Error converting {file_path}: {e}")

event_handler = ImageToPNGHandler()
observer = Observer()
observer.schedule(event_handler, download_folder, recursive=False)

observer.start()
print(f"Monitoring {download_folder} for new .webp and .avif files...")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()

observer.join()