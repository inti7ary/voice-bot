from telegram.ext import ContextTypes, ConversationHandler, CommandHandler, CallbackQueryHandler
from telegram import Update, InlineKeyboardMarkup
from src.i18n.translations import select_gettext
from src.i18n.utils import ensure_language
from src.keyboards import lang_scope_keyboard, lang_keyboard
from src.conf import LANGUAGES

SELECT_LANG_SCOPE, LANG_INTERFACE, LANG_VOICE = range(3)


# callbacks

@ensure_language
async def handle_lang_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Entry point of the /lang command"""

    lang = context.user_data['lang']
    voice_lang = context.user_data['voice_lang']
    _ = select_gettext(lang)

    markup = InlineKeyboardMarkup(inline_keyboard=lang_scope_keyboard(lang))

    text = _("Change the language of the interface or voice messages?\n"
             "Selected language of voice messages: {lang} {emoji}")\
        .format(lang=_(LANGUAGES[voice_lang].get('full')), emoji=LANGUAGES[voice_lang].get('emoji'))

    await update.message.reply_text(
        text=text,
        reply_markup=markup)

    return SELECT_LANG_SCOPE


async def select_scope(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data['lang']
    _ = select_gettext(lang)

    query = update.callback_query
    await query.answer()

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


async def back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data['lang']
    voice_lang = context.user_data['voice_lang']
    _ = select_gettext(lang)

    message = _("Change the language of the interface or voice messages?\n"
                "Selected language of voice messages: {lang} {emoji}") \
        .format(lang=_(LANGUAGES[voice_lang].get('full')), emoji=LANGUAGES[voice_lang].get('emoji'))
    markup = InlineKeyboardMarkup(inline_keyboard=lang_scope_keyboard(lang))

    await update.callback_query.edit_message_text(message, reply_markup=markup)

    return SELECT_LANG_SCOPE


async def change_interface_lang(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data['lang']
    _ = select_gettext(lang)

    query = update.callback_query
    await query.answer()

    match query.data:
        case 'back':
            return await back(update, context)
        case 'cancel':
            message = _('Cancelled')
        case _:
            new_lang = query.data
            _ = select_gettext(new_lang)
            lang_data = LANGUAGES[new_lang]

            context.user_data['lang'] = new_lang

            message = _('Interface language changed to {lang} {emoji}').format(
                lang=_(lang_data['full']),
                emoji=lang_data['emoji']
            )

    await query.edit_message_text(message, reply_markup=None)

    return ConversationHandler.END


async def change_voice_lang(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data['lang']
    _ = select_gettext(lang)

    query = update.callback_query
    await query.answer()

    match query.data:
        case 'back':
            return await back(update, context)
        case 'cancel':
            state = ConversationHandler.END
            message = _('Cancelled')
            markup = None
        case _:
            new_lang = query.data
            lang_data = LANGUAGES[new_lang]

            context.user_data['voice_lang'] = new_lang
            state = ConversationHandler.END

            message = _('Voice messages language changed to {lang} {emoji}').format(
                lang=_(lang_data['full']),
                emoji=lang_data['emoji']
            )

            markup = None

    await query.edit_message_text(message, reply_markup=markup)

    return state


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    return ConversationHandler.END


# handlers

_langs_regex_str = '|'.join(LANGUAGES)

lang_handler = ConversationHandler(
    conversation_timeout=60,
    entry_points=[CommandHandler("lang", handle_lang_command)],
    states={
        SELECT_LANG_SCOPE: [CallbackQueryHandler(select_scope, "^(voice|interface|cancel)$")],
        LANG_INTERFACE: [CallbackQueryHandler(change_interface_lang, f"^({_langs_regex_str}|back|cancel)$")],
        LANG_VOICE: [CallbackQueryHandler(change_voice_lang, f"^({_langs_regex_str}|back|cancel)$")]
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)
