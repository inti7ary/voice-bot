def dummy_gettext(text: str):
    """
    Dummy function for marking strings as translatable for deferred translation.

    Example:
        from i18n.utils import dummy_gettext as _

        translatable_strings = [_("foo"), _("bar")]

    More: https://docs.python.org/3/library/gettext.html#deferred-translations
    """
    return text
