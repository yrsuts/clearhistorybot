#! /root/venv/bin/python
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram.ext import MessageHandler, Filters
from datetime import time
import handler
import logging


logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def main():
    token = '875316307:AAGe7mmyjP3Rz3wvugxj-PSuZJ41B9-Nc8I'
    updater = Updater(token=token, use_context=True)
    allhandlers = [CommandHandler('start', handler.start),
                   CommandHandler('clearall', handler.clear_all),
                   CommandHandler('clearmine', handler.clear_mine),
                   CommandHandler('clearbot', handler.clear_bot),
                   MessageHandler(Filters.all, handler.record)]

    _ = [updater.dispatcher.add_handler(handler_) for handler_ in allhandlers]
    job = updater.job_queue
    job.run_daily(handler.auto_delete, time=time(0, 0, 0, 0),
                  days=(0, 2, 4, 6))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
