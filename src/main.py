import os

import conf
import handlers
from telegram.ext import Application
from persistence import RedisPersistence


def main():
    application = Application.builder() \
        .token(conf.API_TOKEN) \
        .persistence(RedisPersistence(redis_url=conf.REDIS_URL)) \
        .concurrent_updates(True) \
        .build()

    for handler in conf.HANDLERS:
        application.add_handler(getattr(handlers, handler))

    application.run_polling()


if __name__ == "__main__":
    main()