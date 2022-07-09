from telegram import Update
from telegram.ext import CommandHandler, ContextTypes


# callbacks

async def handle_start(update: Update, context=ContextTypes.DEFAULT_TYPE):
    message = update.message
    await message.reply_text('Hi!')


async def handle_help(update: Update, context=ContextTypes.DEFAULT_TYPE):
    message = update.message
    await message.reply_text("I can't help you yet :(")


# handlers

start_handler = CommandHandler("start", handle_start)
help_handler = CommandHandler("help", handle_help)
