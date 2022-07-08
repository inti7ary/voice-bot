from telegram import InlineKeyboardButton

lang_scope_keyboard = [
    [InlineKeyboardButton('Interface', callback_data='interface'), InlineKeyboardButton('Voice', callback_data='voice')],
    [InlineKeyboardButton('Cancel', callback_data='cancel')],
]

lang_keyboard = [
    [InlineKeyboardButton('En 🇺🇸', callback_data='en'), InlineKeyboardButton('Ru 🇷🇺', callback_data='ru')],
    [InlineKeyboardButton('Cancel', callback_data='cancel')],
    [InlineKeyboardButton('Back', callback_data='back')]
]


