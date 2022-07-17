# Voice to text Telegram bot

Extensible Telegram bot for converting voice messages to text.

It uses Vosk API for speech recognition (https://alphacephei.com/vosk/)

## Start the bot using Docker compose

First create a bot using BotFather (https://core.telegram.org/bots#3-how-do-i-create-a-bot)

In the project root directory create `.env` file and put your bot token there:
```
TG_BOT_TOKEN=...
```
Then run:

```
docker compose up
```
## Working example
Working example can be found here: https://t.me/xiovbot  
Though it is hosted with a free plan and cannot process more then one voice message at a time due to low RAM.


## How to add a new language
Bot currently supports two languages: English and Russian.  
You can extend bot functionality by adding a new language.  
For example, suppose you want to add Spanish, then in the `conf.py` file add a new entry to `LANGUAGES` dict:
```
LANGUAGES = {
    ...,
    'es': {
        'full': _('spanish'),
        'emoji': '🇪🇸'
    },
}
```

Then specify name of the model you want to use in `MODELS`:
```
MODELS = {
    ...,
    'es': 'vosk-model-small-es-0.22',
}
```
List of all available models you can find here: https://alphacephei.com/vosk/models or https://alphacephei.com/vosk/models/model-list.json  
After that you need to create .po file in `locales/LANG/LC_MESSAGES/` where `LANG` is the language code, `es` in our example:
```
mkdir -p locales/es/LC_MESSAGES/
msginit --no-translator -i locales/bot.pot -o locales/es/LC_MESSAGES/bot.po
```
`msginit` command requires `gettext` package installed. You can install it with `apt-get update && apt-get install gettext` (Ubuntu)  

Then edit newly created `bot.po` manually to provide bot interface translation, you may keep it untouched and all interface will remain in English.  

And compile `bot.po` to `.mo`:
```
msgfmt locales/es/LC_MESSAGES/bot.po -o locales/es/LC_MESSAGES/bot.mo
```
