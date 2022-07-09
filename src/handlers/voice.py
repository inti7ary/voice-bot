from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters
from src.utils import download, get_lang
from src.converters import transcribe_voice


# callbacks

async def handle_voice(update: Update, context=ContextTypes.DEFAULT_TYPE):
    message = update.message
    file = await message.voice.get_file()
    file_path = await download(file)

    lang = await get_lang(update.effective_user)

    text = await transcribe_voice(file_path=file_path, lang=lang) or\
        "Sorry, I failed to detect any voice here :("

    await message.reply_text(text, reply_to_message_id=message.id)


# handlers

voice_handler = MessageHandler(filters.VOICE, handle_voice)
