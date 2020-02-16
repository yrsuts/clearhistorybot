import os
from telegram.ext import CallbackContext
from telegram.ext.dispatcher import Update, run_async
import time
import pickle
import gc


def start(update: Update, context: CallbackContext):
    bot = context.bot
    message = update.message
    chat_id = message.chat_id
    message_id = message.message_id
    delete_message(bot, chat_id, message_id, delay=1.0)
    text = 'Enjoy !'
    message_sent = bot.send_message(
        chat_id=chat_id,
        text=text,
    )
    message_id = message_sent.message_id
    from_user_id = bot.id
    record_for_deletion(chat_id, message_id, from_user_id)


def clear_all(update: Update, context: CallbackContext):
    bot = context.bot
    message = update.message
    chat_id = message.chat_id
    message_id = message.message_id
    delete_message(bot, chat_id, message_id, delay=1.0)

    target_messages = get_target_messages(chat_id)
    for message_id in target_messages:
        delete_message(bot, chat_id, message_id)


def clear_mine(update: Update, context: CallbackContext):
    bot = context.bot
    message = update.message
    chat_id = message.chat_id
    message_id = message.message_id
    from_user_id = message.from_user.id
    delete_message(bot, chat_id, message_id, delay=1.0)

    target_messages = get_target_messages(chat_id, from_user_id)
    for message_id in target_messages:
        delete_message(bot, chat_id, message_id)


def clear_bot(update: Update, context: CallbackContext):
    bot = context.bot
    message = update.message
    chat_id = message.chat_id
    message_id = message.message_id
    from_user_id = bot.id
    delete_message(bot, chat_id, message_id, delay=1.0)

    target_messages = get_target_messages(chat_id, from_user_id)
    for message_id in target_messages:
        delete_message(bot, chat_id, message_id)


def record(update: Update, context: CallbackContext):
    bot = context.bot
    message = update.message
    chat_id = message.chat_id
    message_id = message.message_id
    from_user_id = message.from_user.id
    text = message.text
    if text:
        if text[0] == '/':
            delete_message(bot, chat_id, message_id, delay=0.5)
            return
    record_for_deletion(chat_id, message_id, from_user_id)


def auto_delete(context):
    record_for_deletion_file = './messages_to_delete.pkl'
    bot = context.bot
    chat_ids = []
    for message in generate_message(record_for_deletion_file):
        chat_ids.append(message[0])
    chat_ids = list(set(chat_ids))
    for chat_id in chat_ids:
        target_messages = get_target_messages(chat_id)
        for message_id in target_messages:
            delete_message(bot, chat_id, message_id)
    try:
        os.remove('subscriptions_content.pkl')
    except Exception:
        pass
    gc.collect()


@run_async
def delete_message(bot, chat_id, message_id, delay=0.0):
    if delay:
        time.sleep(delay)
    try:
        bot.delete_message(chat_id, message_id)
    except Exception:
        pass


def record_for_deletion(chat_id, message_id, from_user_id):
    record_for_deletion_file = './messages_to_delete.pkl'
    if os.path.exists(record_for_deletion_file):
        with open(record_for_deletion_file, 'ab') as f:
            pickle.dump([chat_id, message_id, from_user_id], f)
    else:
        with open(record_for_deletion_file, 'wb') as f:
            _ = [pickle.dump([chat_id, message_id, from_user_id], f)]


def get_target_messages(chat_id, from_user_id=0):
    record_for_deletion_file = './messages_to_delete.pkl'
    tartget_messages = []
    all_messages = \
        [message for message in generate_message(record_for_deletion_file)]
    if from_user_id:
        for message in generate_message(record_for_deletion_file):
            if message[0] == chat_id and message[2] == from_user_id:
                tartget_messages.append(message[1])
                all_messages.remove(message)
    else:
        for message in generate_message(record_for_deletion_file):
            if message[0] == chat_id:
                tartget_messages.append(message[1])
                all_messages.remove(message)

    with open(record_for_deletion_file, 'wb') as f:
        _ = [pickle.dump(message, f) for message in all_messages]
    return tartget_messages


def generate_message(record_file):
    try:
        with open(record_file, 'rb') as f:
            while True:
                try:
                    message = pickle.load(f)
                    yield message
                except Exception:
                    raise StopIteration
    except FileNotFoundError:
        raise StopIteration
