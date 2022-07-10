from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from src.i18n.translations import select_gettext
from src.i18n.utils import ensure_language

# callbacks


@ensure_language
async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data['lang']
    _ = select_gettext(lang)

    bot_users = context.bot_data.setdefault('users', [])
    bot_users.append(update.effective_user.id)

    await update.message.reply_text(_("Hi!"))


@ensure_language
async def handle_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data['lang']
    _ = select_gettext(lang)

    await update.message.reply_text(_("I can't help you yet :("))


# handlers

start_handler = CommandHandler("start", handle_start)
help_handler = CommandHandler("help", handle_help)
