from telegram import InlineKeyboardButton
from src.conf import LANGUAGES

lang_scope_keyboard = [
    [InlineKeyboardButton('Interface', callback_data='interface'), InlineKeyboardButton('Voice', callback_data='voice')],
    [InlineKeyboardButton('Cancel', callback_data='cancel')],
]

lang_keyboard = [
    [InlineKeyboardButton('{short} {emoji}'.format(
        short=lang.capitalize(),
        emoji=LANGUAGES[lang].get('emoji')), callback_data=lang) for lang in LANGUAGES],
    [InlineKeyboardButton('Cancel', callback_data='cancel')],
    [InlineKeyboardButton('Back', callback_data='back')]
]


