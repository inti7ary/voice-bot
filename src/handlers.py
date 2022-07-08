from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters, CommandHandler
from src.utils import download, set_lang, get_lang
from src.converters import transcribe_voice


class UnsupportedLanguageError(Exception):
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)
        self.message = message


# callbacks

async def handle_voice(update: Update, context=ContextTypes.DEFAULT_TYPE):
    message = update.message
    file = await message.voice.get_file()
    file_path = await download(file)

    lang = await get_lang(update.effective_user)

    text = transcribe_voice(file_path=file_path, lang=lang) or\
        "Sorry, I failed to detect any voice here :("

    await message.reply_text(text, reply_to_message_id=message.id)


async def handle_start(update: Update, context=ContextTypes.DEFAULT_TYPE):
    message = update.message
    await message.reply_text('Hi!')


async def handle_help(update: Update, context=ContextTypes.DEFAULT_TYPE):
    message = update.message
    await message.reply_text("I can't help you yet :(")


async def handle_lang_change(update: Update, context=ContextTypes.DEFAULT_TYPE):
    try:
        lang = context.args.pop(0)
        supported_langs = ['ru', 'en']
        if lang not in supported_langs:
            raise UnsupportedLanguageError(f'Currently supported languages: {supported_langs}')
        await set_lang(update.effective_user, lang)
        await update.message.reply_text(f'Language changed to {lang}')

    except IndexError:
        ...
    except UnsupportedLanguageError as e:
        await update.message.reply_text(e.message)


# handlers

voice_handler = MessageHandler(filters.VOICE, handle_voice)
start_handler = CommandHandler("start", handle_start)
help_handler = CommandHandler("help", handle_help)
lang_change_handler = CommandHandler("lang", handle_lang_change)
