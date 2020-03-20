from telegram.ext import Updater, CommandHandler, MessageHandler, ConversationHandler, Filters, InlineQueryHandler, CallbackContext
import logging
from datetime import datetime, timedelta
import pytz


def reminder(context):
    context.bot.send_message(chat_id=context.job.context, text="Type /daily to start your daily.")

def start(update, context):
    #update.message.reply_text("Type /daily to start your daily.")
    dt = datetime.today()
    context.job_queue.run_repeating(reminder, 
                                    interval=timedelta(days=1), 
                                    first=pytz.timezone("Europe/Berlin").localize(datetime(dt.year,dt.month,dt.day,10)),
                                    context=update.message.chat_id)


def daily(update, context):
    weekdays = ["Monday","Tuesdy","Wednesday","Thursday","Friday","Saturday","Sunday"]
    today = datetime.today()
    update.message.reply_text(f"{weekdays[today.weekday()]} - {today.day}/{today.month}/{today.year}. \nWas schaffst du diese Woche?")
    return QUESTION2

def second_question(update, context):
    update.message.reply_text("Woran arbeitest du Heute?")
    return QUESTION3

def third_question(update, context):
    update.message.reply_text("Wofür bist du dankbar?")
    return DONE

def done(update, context):
    update.message.reply_text("Thanks!")
    return ConversationHandler.END


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

QUESTION2, QUESTION3, DONE = range(3)
bot_token = 'Token'

updater = Updater(bot_token, use_context=True)
dp = updater.dispatcher

start_handler = CommandHandler("start", start)
dp.add_handler(start_handler)
# Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
conv_handler = ConversationHandler(
    entry_points=[CommandHandler("daily", daily)],

    states={
        QUESTION2: [MessageHandler(Filters.text, second_question)],

        QUESTION3: [MessageHandler(Filters.text, third_question)],

        DONE: [MessageHandler(Filters.text,done)],
    },
    fallbacks = [MessageHandler(Filters.regex('^Done$'), done)]
)
    
dp.add_handler(conv_handler)
# Start the Bot
updater.start_polling()
    
# Run the bot until you press Ctrl-C or the process receives SIGINT,
# SIGTERM or SIGABRT. This should be used most of the time, since
# start_polling() is non-blocking and will stop the bot gracefully.
updater.idle()
