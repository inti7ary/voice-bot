import conf
from src import handlers
from telegram.ext import Application


def main():
    application = Application.builder().token(conf.API_TOKEN).build()

    for handler in conf.HANDLERS:
        application.add_handler(getattr(handlers, handler))

    application.run_polling()


if __name__ == "__main__":
    main()