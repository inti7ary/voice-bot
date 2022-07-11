from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from src.i18n.translations import select_gettext
from src.i18n.utils import ensure_language

# callbacks


@ensure_language
async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data['lang']
    _ = select_gettext(lang)

    # this set is never persisted though...
    bot_users = context.bot_data.setdefault('users', set())
    bot_users.add(update.effective_user.id)

    text = _("Hi!\nSend me a voice message and I'll convert it to text.\n\n"
             "🌎 You can also change the language by typing /lang")

    await update.message.reply_text(text)


@ensure_language
async def handle_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data['lang']
    _ = select_gettext(lang)

    text = _("Just send me a message if you want to convert it to text.\n"
             "If you need to change the language, type /lang")

    await update.message.reply_text(text)


# handlers

start_handler = CommandHandler("start", handle_start)
help_handler = CommandHandler("help", handle_help)
