from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler, CommandHandler, CallbackQueryHandler
from src.keyboards import lang_scope_keyboard, lang_keyboard
from src.utils import set_lang


SELECT_LANG_SCOPE, LANG_INTERFACE, LANG_VOICE = range(3)


# callbacks

async def handle_lang_command(update: Update, context=ContextTypes.DEFAULT_TYPE):
    markup = InlineKeyboardMarkup(inline_keyboard=lang_scope_keyboard)

    await update.message.reply_text(
        text='Change the language of the interface or voice messages?',
        reply_markup=markup)

    return SELECT_LANG_SCOPE


async def select_scope(update: Update, context=ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    match query.data:
        case 'interface':
            message = 'Select the interface language:'
            state = LANG_INTERFACE
            markup = InlineKeyboardMarkup(inline_keyboard=lang_keyboard)
        case 'voice':
            message = 'Select the language of voice messages:'
            state = LANG_VOICE
            markup = InlineKeyboardMarkup(inline_keyboard=lang_keyboard)
        case 'cancel':
            message = 'Cancelled'
            state = ConversationHandler.END
            markup = None

    await update.callback_query.edit_message_text(message, reply_markup=markup)

    return state


async def change_voice_lang(update: Update, context=ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    match query.data:
        case 'back':
            state = SELECT_LANG_SCOPE
            message = 'Change the language of the interface or voice messages?'
            markup = InlineKeyboardMarkup(inline_keyboard=lang_scope_keyboard)
        case 'cancel':
            state = ConversationHandler.END
            message = 'Cancelled'
            markup = None
        case _:
            user = update.effective_user
            await set_lang(user, query.data)
            state = ConversationHandler.END
            message = f'Language changed to {query.data}'
            markup = None

    await query.edit_message_text(message, reply_markup=markup)

    return state


async def cancel(update: Update, context=ContextTypes.DEFAULT_TYPE):
    return ConversationHandler.END


# handlers

lang_handler = ConversationHandler(
    conversation_timeout=60,
    entry_points=[CommandHandler("lang", handle_lang_command)],
    states={
        SELECT_LANG_SCOPE: [CallbackQueryHandler(select_scope, "^(voice|interface|cancel)$")],
        LANG_VOICE: [CallbackQueryHandler(change_voice_lang, "^(en|ru|back|cancel)$")]
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)
