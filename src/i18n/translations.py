import gettext
from src import conf
from src.errors import LanguageNotSupportedError


# dict of the available translation formed from ``conf.LANGUAGES``
translations = {
    lang: gettext.translation('bot', conf.LOCALEDIR, languages=[lang]) for lang in conf.LANGUAGES
}


def select_gettext(lang: str):
    """
    Get appropriate ``gettext`` method depending on provided ``lang``.

    This function is needed for installing ``gettext`` into local namespace
    in contrast to NullTranslations.install which installs it into builtins.

    Example:
        _ = select_gettext('en')
    """

    if lang not in conf.LANGUAGES:
        raise LanguageNotSupportedError

    translation = translations[lang]
    return translation.gettext
