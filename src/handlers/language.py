from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler, CommandHandler, CallbackQueryHandler
from src.i18n.translations import select_gettext
from src.keyboards import lang_scope_keyboard, lang_keyboard
from src.conf import LANGUAGES
from src.utils import set_lang, get_lang

SELECT_LANG_SCOPE, LANG_INTERFACE, LANG_VOICE = range(3)


# callbacks

async def handle_lang_command(update: Update, context: ContextTypes.DEFAULT_TYPE):


    #
    lang = await get_lang(update.effective_user)
    _ = select_gettext(lang)
    #
    markup = InlineKeyboardMarkup(inline_keyboard=lang_scope_keyboard(lang))

    await update.message.reply_text(
        text=_('Change the language of the interface or voice messages?'),
        reply_markup=markup)

    return SELECT_LANG_SCOPE


async def select_scope(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    #
    lang = await get_lang(update.effective_user)
    _ = select_gettext(lang)
    #

    match query.data:
        case 'interface':
            message = _('Select the interface language:')
            state = LANG_INTERFACE
            markup = InlineKeyboardMarkup(inline_keyboard=lang_keyboard(lang))
        case 'voice':
            message = _('Select the language of voice messages:')
            state = LANG_VOICE
            markup = InlineKeyboardMarkup(inline_keyboard=lang_keyboard(lang))
        case 'cancel':
            message = _('Cancelled')
            state = ConversationHandler.END
            markup = None

    await update.callback_query.edit_message_text(message, reply_markup=markup)

    return state


async def change_voice_lang(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    #
    lang = await get_lang(update.effective_user)
    _ = select_gettext(lang)
    #

    match query.data:
        case 'back':
            state = SELECT_LANG_SCOPE
            message = _('Change the language of the interface or voice messages?')
            markup = InlineKeyboardMarkup(inline_keyboard=lang_scope_keyboard(lang))
        case 'cancel':
            state = ConversationHandler.END
            message = _('Cancelled')
            markup = None
        case _:
            user = update.effective_user
            new_lang = query.data
            await set_lang(user, query.data)
            state = ConversationHandler.END
            _ = select_gettext(new_lang)

            lang = LANGUAGES[query.data.lower()]
            message = _('Voice messages language changed to {lang} {emoji}').format(
                lang=_(lang['full']),
                emoji=lang['emoji']
            )
            markup = None

    await query.edit_message_text(message, reply_markup=markup)

    return state


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
