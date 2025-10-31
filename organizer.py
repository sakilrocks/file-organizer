
import os
import json
import shutil
import time

from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

CONFIG_PATH = "config/categories.json"
LOG_FILE = "logs/activity.log"


def log_action(message):
    os.makedirs("logs", exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now()}] {message}\n")


def load_categories():
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)


def get_category(extension, categories):
    for category, exts in categories.items():
        if extension.lower() in exts:
            return category
    return "others"


def move_file(file_path, target_dir):
    os.makedirs(target_dir, exist_ok=True)
    file_name = os.path.basename(file_path)
    dest_path = os.path.join(target_dir, file_name)
    if os.path.exists(dest_path):
        base, ext = os.path.splitext(file_name)
        dest_path = os.path.join(target_dir, f"{base}_{int(time.time())}{ext}")
    shutil.move(file_path, dest_path)
    log_action(f"moved: {file_name} -> {target_dir}")


def organize_folder(folder_path):
    categories = load_categories()
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            _, ext = os.path.splitext(file_name)
            category = get_category(ext, categories)
            target_dir = os.path.join(folder_path, category)
            move_file(file_path, target_dir)
    print("folder organized successfully")



class Watcher(FileSystemEventHandler):
    def __init__(self, folder):
        self.folder = folder

    def on_created(self, event):
        if not event.is_directory:
            time.sleep(1) 
            organize_folder(self.folder)


def watch_folder(folder_path):
    event_handler = Watcher(folder_path)
    observer = Observer()
    observer.schedule(event_handler, folder_path, recursive=False)
    observer.start()
    print(f"watching folder: {folder_path} (press Ctrl+C to stop)")

    try:
        while True:
            time.sleep(2)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()




if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="file organizer")
    parser.add_argument("folder", help="folder path to organize")
    parser.add_argument("--watch", action="store_true", help="enable continuous watch mode")
    args = parser.parse_args()

    if not os.path.exists(args.folder):
        print("error: folder not found.")
        exit(1)

    organize_folder(args.folder)

    if args.watch:
        watch_folder(args.folder)