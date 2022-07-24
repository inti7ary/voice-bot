import asyncio
import json
from functools import partial
from vosk import Model, KaldiRecognizer
import subprocess
from src import conf
from src.errors import LanguageNotSupportedError


def _transcribe_voice_sync(file_path, lang='en'):
    if lang not in conf.LANGUAGES:
        supported_langs = list(conf.MODELS)
        message = f"Language '{lang}' is not supported, supported languages are: {repr(supported_langs).strip('[]')}"
        raise LanguageNotSupportedError(message)

    sample_rate = 16000
    model = Model(lang=lang, model_name=conf.MODELS.get(lang))
    rec = KaldiRecognizer(model, sample_rate)

    command = ['ffmpeg', '-loglevel', 'quiet', '-i', file_path,
               '-ar', str(sample_rate), '-ac', '1', '-f', 's16le', '-']
    process = subprocess.Popen(command, stdout=subprocess.PIPE)

    while data := process.stdout.read(4000):
        rec.AcceptWaveform(data)

    result = rec.FinalResult()
    text = json.loads(result).get('text')

    return text


async def transcribe_voice(file_path, lang='en', pool=None):
    """Convert audio file at file_path to text."""

    func = partial(_transcribe_voice_sync, file_path=file_path, lang=lang)
    loop = asyncio.get_running_loop()

    result = await loop.run_in_executor(pool, func)

    return result
