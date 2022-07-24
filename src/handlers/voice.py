from concurrent.futures import ProcessPoolExecutor
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ContextTypes, MessageHandler, filters
from src import conf
from src.files import download
from src.converters import transcribe_voice
from src.i18n.translations import select_gettext
from src.i18n.utils import ensure_language

process_pool = ProcessPoolExecutor()


# callbacks

@ensure_language
async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang, voice_lang = context.user_data['lang'], context.user_data['voice_lang']
    _ = select_gettext(lang)

    file = await update.message.voice.get_file()
    file_path = await download(file) if conf.SAVE_VOICE_FILES else file.file_path

    await update.effective_chat.send_action(ChatAction.TYPING)

    text = await transcribe_voice(file_path=file_path, lang=voice_lang, pool=process_pool) or\
        _("Sorry, I failed to detect any voice here :(")

    await update.message.reply_text(text, reply_to_message_id=update.message.id)


# handlers

voice_handler = MessageHandler(filters.VOICE, handle_voice)
