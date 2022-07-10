from functools import wraps
from telegram import User, Update
from telegram.ext import ContextTypes
from src import conf


def get_user_default_lang(user: User):
    """
    Get user's language depending on their system settings.

    If user's system language is not among supported languages,
    take the first supported language as default.
    """

    return user.language_code if user.language_code in conf.LANGUAGES else \
        list(conf.LANGUAGES.keys())[0]


def ensure_language(wrapped_callback):
    """
    Decorator that ensures that the language settings are present in the
    callback context.
     """

    @wraps(wrapped_callback)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not context.user_data.get('lang'):
            context.user_data['lang'] = get_user_default_lang(update.effective_user)

        if not context.user_data.get('voice_lang'):
            context.user_data['voice_lang'] = get_user_default_lang(update.effective_user)

        return await wrapped_callback(update, context)

    return wrapper
