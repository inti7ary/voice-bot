import os

import conf
import handlers
from telegram.ext import Application
from persistence import RedisPersistence


def main():
    builder = Application.builder() \
        .token(conf.API_TOKEN) \
        .concurrent_updates(True)

    if conf.REDIS_URL:
        builder.persistence(RedisPersistence(redis_url=conf.REDIS_URL)) \

    application = builder.build()

    for handler in conf.HANDLERS:
        application.add_handler(getattr(handlers, handler))

    application.run_polling()


if __name__ == "__main__":
    main()