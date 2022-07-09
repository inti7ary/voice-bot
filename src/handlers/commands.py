from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from src.i18n.translations import select_gettext
from src.utils import get_lang


# callbacks

async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = await get_lang(update.effective_user)
    _ = select_gettext(lang)

    context.user_data['started'] = 'who?'

    message = update.message

    await message.reply_text(_("Hi!"))


async def handle_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = await get_lang(update.effective_user)
    _ = select_gettext(lang)



    message = update.message
    await message.reply_text(_("I can't help you yet :("))


# handlers

start_handler = CommandHandler("start", handle_start)
help_handler = CommandHandler("help", handle_help)
