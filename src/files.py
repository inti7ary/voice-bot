from pathlib import Path
import datetime
from telegram import File
from src import conf


def generate_filename(file: File):
    file_unique_id = file.file_unique_id
    extension = Path(file.file_path).suffix
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

    new_file_name = f'{timestamp}-{file_unique_id}{extension}'
    return new_file_name


async def download(file: File):
    filename = generate_filename(file)
    file_path = conf.VOICE_DIR / filename

    await file.download(custom_path=file_path)

    return file_path
