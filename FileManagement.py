from os import scandir, rename
from os.path import splitext, exists, join
from shutil import move
from time import sleep

import logging

from watchdog.observers import Observer
from watchdog.events import DirModifiedEvent, FileModifiedEvent, FileSystemEventHandler

source_dir = "D:\Documents/"
dest_dir_music = "D:\Documents\music/"
dest_dir_video = "D:\Documents\videos/"
dest_dir_image = "D:\Documents\images/"
dest_dir_documents = "D:\Documents\docs/"
  
# ? supported image types
image_extensions = [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp", ".tiff", ".tif", ".psd", ".raw", ".arw", ".cr2", ".nrw",
                    ".k25", ".bmp", ".dib", ".heif", ".heic", ".ind", ".indd", ".indt", ".jp2", ".j2k", ".jpf", ".jpf", ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ai", ".eps", ".ico"]
# ? supported Video types
video_extensions = [".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg",
                    ".mp4", ".mp4v", ".m4v", ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd"]
# ? supported Audio types
audio_extensions = [".m4a", ".flac", "mp3", ".wav", ".wma", ".aac"]
# ? supported Document types
document_extensions = [".doc", ".docx", ".odt",
                       ".pdf", ".xls", ".xlsx", ".ppt", ".pptx"]

def make_unique(name, dest):
    filename, extension = splitext(name)
    counter = 1
    while exists(f"{dest}/{name}"):
        name = f"{filename({str(counter)})}{extension}"
        counter += 1
    return name

def move_file(dest, entry, name):
    if exists(f"{dest}/{name}"):
        unique_name = make_unique(name, dest)
        oldName = join(dest, name)
        newName = join(dest, unique_name)
        rename(oldName, newName)
    move(entry, dest)
    


class MoverHandler(FileSystemEventHandler):
    def on_modified(self, event):
        with scandir(source_dir) as entries:
            for entry in entries:
                name = entry.name
                self.check_doc_files(entry, name)
                self.check_image_files(entry, name)
                self.check_music_files(entry, name)
                self.check_video_files(entry, name)

    def check_doc_files(self, entry, name):
        filename, extension = splitext(name)
        if extension.lower() in document_extensions:
            move_file(dest_dir_documents, entry, name)
            logging.info(f"Moved document file: {name}")

    def check_image_files(self, entry, name):
        filename, extension = splitext(name)
        if extension.lower() in image_extensions:
            move_file(dest_dir_image, entry, name)
            logging.info(f"Moved image file: {name}")
    
    def check_video_files(self, entry, name):
        filename, extension = splitext(name)
        if extension.lower() in video_extensions:
            move_file(dest_dir_video, entry, name)
            logging.info(f"Moved video file: {name}")

    def check_music_files(self, entry, name):
        filename, extension = splitext(name)
        if extension.lower() in audio_extensions:
            move_file(dest_dir_music, entry, name)
            logging.info(f"Moved audio file: {name}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = source_dir
    event_handler = MoverHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()