import shutil
from pathlib import Path
import re
import sys

class FileSorter:
    def __init__(self, source_folder):
        self.source_folder = source_folder
        self.file_handlers = []

    def add_handler(self, handler):
        self.file_handlers.append(handler)

    def scan(self, folder):
        for item in folder.iterdir():
            if item.is_dir():
                if item.name not in ('архіви', 'відео', 'аудіо', 'документи', 'зображення', 'ІНШЕ'):
                    self.scan(item)
                continue

            for handler in self.file_handlers:
                if handler.can_handle(item):
                    handler.handle(item, self.source_folder)
                    break

    def core(self):
        self.scan(self.source_folder)

def start():
    if len(sys.argv) > 1:
        folder_process = Path(sys.argv[1])
        file_sorter = FileSorter(folder_process)

        file_sorter.add_handler(ImageHandler())
        file_sorter.add_handler(AudioHandler())
        file_sorter.add_handler(VideoHandler())
        file_sorter.add_handler(DocumentsHandler())
        file_sorter.add_handler(ArchiveHandler())
        file_sorter.add_handler(DefaultHandler())

        file_sorter.core()

class FileHandler:
    def can_handle(self, file):
        raise NotImplementedError

    def handle(self, file, target_folder):
        raise NotImplementedError

    def get_extension(self, name):
        return Path(name).suffix[1:].upper()

    def normalize(self, name):
        MAP = {}
        CYRILLIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
        TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
                       "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "je", "ji", "g")

        for cirilic, latin in zip(CYRILLIC_SYMBOLS, TRANSLATION):
            MAP[ord(cirilic)] = latin
            MAP[ord(cirilic.upper())] = latin.upper()

        string = name.translate(MAP)
        translated_name = re.sub(r'[^a-zA-Z.0-9_]', '_', string)
        return translated_name

class ImageHandler(FileHandler):
    def can_handle(self, file):
        return file.suffix[1:].upper() in ('JPEG', 'JPG', 'PNG', 'SVG')

    def handle(self, file, target_folder):
        target_folder.mkdir(exist_ok=True, parents=True)
        file.replace(target_folder / self.normalize(file.name))

class AudioHandler(FileHandler):
    AUDIO_EXTENSIONS = {'MP3', 'OGG', 'WAV', 'AMR'}

    def can_handle(self, file):
        return self.get_extension(file.name) in self.AUDIO_EXTENSIONS

    def handle(self, file, target_folder):
        target_folder.mkdir(exist_ok=True, parents=True)
        file.replace(target_folder / self.normalize(file.name))

class VideoHandler(FileHandler):
    VIDEO_EXTENSIONS = {'AVI', 'MP4', 'MOV', 'MKV'}

    def can_handle(self, file):
        return self.get_extension(file.name) in self.VIDEO_EXTENSIONS

    def handle(self, file, target_folder):
        target_folder.mkdir(exist_ok=True, parents=True)
        file.replace(target_folder / self.normalize(file.name))

class DocumentsHandler(FileHandler):
    DOCUMENT_EXTENSIONS = {'DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'}

    def can_handle(self, file):
        return self.get_extension(file.name) in self.DOCUMENT_EXTENSIONS

    def handle(self, file, target_folder):
        target_folder.mkdir(exist_ok=True, parents=True)
        file.replace(target_folder / self.normalize(file.name))

class ArchiveHandler(FileHandler):
    ARCHIVE_EXTENSIONS = {'ZIP', 'GZ', 'TAR'}

    def can_handle(self, file):
        return self.get_extension(file.name) in self.ARCHIVE_EXTENSIONS

    def handle(self, file, target_folder):
        target_folder.mkdir(exist_ok=True, parents=True)
        folder_for_file = target_folder / self.normalize(file.name.replace(file.suffix, ''))
        folder_for_file.mkdir(exist_ok=True, parents=True)
        try:
            shutil.unpack_archive(str(file.absolute()), str(folder_for_file.absolute()))
        except shutil.ReadError:
            folder_for_file.rmdir()
            return
        file.unlink()

class DefaultHandler(FileHandler):
    def can_handle(self, file):
        return True

    def handle(self, file, target_folder):
        target_folder.mkdir(exist_ok=True, parents=True)
        file.replace(target_folder / self.normalize(file.name))

if __name__ == "__main__":
    start()