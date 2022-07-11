import os
from pathlib import Path
from i18n.gettext import dummy_gettext as _


API_TOKEN = os.getenv('TG_BOT_API_TOKEN')

BASE_DIR = Path(__file__).resolve().parent.parent

VOICE_DIR = BASE_DIR / 'voice/'

LOCALEDIR = BASE_DIR / 'locales/'

REDIS_URL = os.getenv('REDIS_URL')

HANDLERS = [
    'start_handler',
    'help_handler',
    'voice_handler',
    'lang_handler',
]

LANGUAGES = {
    'en': {
        'full': _('english'),
        'emoji': '🇺🇸'
    },
    'ru': {
        'full': _('russian'),
        'emoji': '🇷🇺'
    },
}

MODELS = {
    'en': 'vosk-model-en-us-0.22-lgraph',
    'ru': 'vosk-model-ru-0.10-lgraph',
}
