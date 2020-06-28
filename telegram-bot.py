# -*- coding: utf-8 -*-
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, InlineQueryHandler, CallbackContext, ConversationHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
import logging
import random

from serializers import serialize_sleep, serialize_event
from commenters import *

MYSELF = int(os.environ['TELE_ID'])
TOKEN = os.environ['SYL_KEY']

FIRST, SECOND = range(2)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(update: Update, context: CallbackContext):
    print(update.message.chat_id)
    context.bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")

def hi(update: Update, context: CallbackContext):
    if update.message.from_user.id == MYSELF:
        context.bot.send_message(chat_id=update.message.chat_id, text="Hi!")
    else:
        context.bot.send_message(chat_id=update.message.chat_id, text="You are not allowed to use that function!")

def eventKb(update: Update, context: CallbackContext):
    if update.message.from_user.id != MYSELF:
        context.bot.send_message(chat_id=update.message.chat_id, text="You are not allowed to use that function!")
        return

    keyboard = [[InlineKeyboardButton("1", callback_data="1"),
                 InlineKeyboardButton("2", callback_data="2")],
                [InlineKeyboardButton("3", callback_data="3"),
                InlineKeyboardButton("4", callback_data="4")],
                [InlineKeyboardButton("5", callback_data="5")]
                ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose event intensity:', reply_markup=reply_markup)
    return FIRST

def eventCb(update, context):
    query = update.callback_query

    intensity = query.data

    status, values = serialize_event(intensity)
    time, typ = values[0], values[1]

    msg = "{} wurde um erfasst um: {} ".format(typ, time)

    query.answer()

    query.edit_message_text(text=msg)
    return ConversationHandler.END


def sleepKb(update, context):
    if update.message.from_user.id != MYSELF:
        context.bot.send_message(chat_id=update.message.chat_id, text="You are not allowed to use that function!")
        return

    keyboard = [[InlineKeyboardButton("Wakeup", callback_data='wakeup'),
                 InlineKeyboardButton("Standup", callback_data='standup')],
                [InlineKeyboardButton("Go to bed", callback_data='gotobed'),
                InlineKeyboardButton("Handy away", callback_data='handyaway')],
                [InlineKeyboardButton("Toothbrush (m)", callback_data='toothbrush_morning'),
                InlineKeyboardButton("Shower", callback_data='shower')],
                [InlineKeyboardButton("Breakfast", callback_data='breakfast'),
                InlineKeyboardButton("Lunch", callback_data='lunch')],
                [InlineKeyboardButton("Dinner", callback_data='dinner'),
                InlineKeyboardButton("Toothbrush (e)", callback_data='toothbrush_evening')],
                ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose:', reply_markup=reply_markup)
    return FIRST

def sleepCb(update, context):
    query = update.callback_query

    sleep_type = query.data

    status, values = serialize_sleep(sleep_type)
    time, typ = values[0], values[1]


    _, comment = get_time_comment(time, typ)
    msg = "{} wurde um erfasst um: {} ".format(typ, time)
    msg += "\n" + comment

    query.answer()

    query.edit_message_text(text=msg)
    return ConversationHandler.END

def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END

sleepH = ConversationHandler(
    entry_points=[CommandHandler('sleep', sleepKb)],
    states={
        FIRST: [CallbackQueryHandler(sleepCb)],
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)

eventH = ConversationHandler(
    entry_points=[CommandHandler('event', eventKb)],
    states={
        FIRST: [CallbackQueryHandler(eventCb)],
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)



def main():

    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(CommandHandler('hi', hi))

    updater.dispatcher.add_handler(sleepH)
    updater.dispatcher.add_handler(eventH)

    updater.start_polling()

if __name__ == '__main__':
    main()
