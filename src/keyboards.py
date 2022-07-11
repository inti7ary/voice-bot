from typing import List
from telegram import InlineKeyboardButton
from src.conf import LANGUAGES
from src.i18n.translations import select_gettext


def lang_scope_keyboard(lang: str) -> List[List[InlineKeyboardButton]]:
    """
    Factory function for inline language scope keyboard.

    Return the keyboard with buttons translated to specific language.
    """

    _ = select_gettext(lang)

    keyboard = [
        [InlineKeyboardButton(_('Interface'), callback_data='interface'),
         InlineKeyboardButton(_('Voice'), callback_data='voice')],

        [InlineKeyboardButton(_('Cancel'), callback_data='cancel')],
    ]

    return keyboard


def lang_keyboard(lang: str) -> List[List[InlineKeyboardButton]]:
    """
    Factory function for inline language keyboard.

    Create keyboard containing all languages specified in ``conf.LANGUAGES``.
    Return the keyboard with buttons translated to specific language.
    """

    _ = select_gettext(lang)

    keyboard = [
        [InlineKeyboardButton('{short} {emoji}'.format(
            short=lang.capitalize(),
            emoji=LANGUAGES[lang].get('emoji')), callback_data=lang) for lang in LANGUAGES],
        [InlineKeyboardButton(_('Back'), callback_data='back')],
        [InlineKeyboardButton(_('Cancel'), callback_data='cancel')],
    ]

    return keyboard
