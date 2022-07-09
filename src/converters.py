import asyncio
import concurrent.futures
import json
from functools import partial
from vosk import Model, KaldiRecognizer
import subprocess
from src import conf


def _transcribe_voice_sync(file_path, lang='en'):
    sample_rate = 16000
    model = Model(lang=lang, model_name=conf.MODELS.get(lang))
    rec = KaldiRecognizer(model, sample_rate)

    process = subprocess.Popen(['ffmpeg', '-loglevel', 'quiet', '-i',
                                file_path,
                                '-ar', str(sample_rate), '-ac', '1', '-f', 's16le', '-'],
                               stdout=subprocess.PIPE)

    while data := process.stdout.read(4000):
        rec.AcceptWaveform(data)

    result = rec.FinalResult()
    text = json.loads(result).get('text')

    return text


async def transcribe_voice(file_path, lang='en'):
    func = partial(_transcribe_voice_sync, file_path=file_path, lang=lang)
    loop = asyncio.get_running_loop()

    with concurrent.futures.ProcessPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, func)

    return result
