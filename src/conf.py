import os
from pathlib import Path

API_TOKEN = os.getenv('TG_BOT_API_TOKEN')

BASE_DIR = Path(__file__).resolve().parent.parent

VOICE_DIR = BASE_DIR / 'voice/'

HANDLERS = [
    'start_handler',
    'help_handler',
    'voice_handler',
    'lang_handler',
    'text_handler',
]

MODELS = {
    'en': 'vosk-model-en-us-0.22-lgraph',
    'ru': 'vosk-model-ru-0.10-lgraph',
}

LANGUAGES = {
    'en': {
        'full': 'english',
        'emoji': '🇺🇸'
    },
    'ru': {
        'full': 'russian',
        'emoji': '🇷🇺'
    },
}
