from pathlib import Path
import datetime
import aioredis
from telegram import File, User

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


async def set_lang(user: User, lang: str):
    redis = aioredis.from_url('redis://127.0.0.1')
    key = f'{user.id}:lang'
    await redis.set(key, lang)


async def get_lang(user: User):
    redis = aioredis.from_url('redis://127.0.0.1:6379/0', decode_responses=True)
    key = f'{user.id}:lang'
    return await redis.getset(key, 'ru')