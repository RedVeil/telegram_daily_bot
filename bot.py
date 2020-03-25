from telegram.ext import Updater, CommandHandler, MessageHandler, ConversationHandler, Filters, InlineQueryHandler, CallbackContext
import logging
from datetime import datetime, timedelta
import pytz


def daily_reminder(context):
    context.bot.send_message(chat_id=context.job.context, text="Type /daily to start your daily.")

def retro_reminder(context):
    context.bot.send_message(chat_id=context.job.context, text="Type /retro to start your retro.")

def start(update, context):
    #update.message.reply_text("Type /daily to start your daily.")
    dt = datetime.today()
    context.job_queue.run_repeating(daily_reminder, 
                                    interval=timedelta(days=1), 
                                    first=pytz.timezone("Europe/Berlin").localize(datetime(dt.year,dt.month,dt.day,10)),
                                    context=update.message.chat_id)
    context.job_queue.run_repeating(retro_reminder, 
                                    interval=timedelta(days=1), 
                                    first=pytz.timezone("Europe/Berlin").localize(datetime(dt.year,dt.month,dt.day,20)),
                                    context=update.message.chat_id)


def daily(update, context):
    weekdays = ["Monday","Tuesdy","Wednesday","Thursday","Friday","Saturday","Sunday"]
    today = datetime.today()
    update.message.reply_text(f"{weekdays[today.weekday()]} - {today.day}/{today.month}/{today.year}. \nWas ist dein Ziel für diese Woche?")
    return DAILY2

def second_daily(update, context):
    update.message.reply_text("Welches Module-Todo erledigst du heute?")
    return DAILY3

def third_daily(update, context):
    update.message.reply_text("Was ist dein Ziel für heute?")
    return DONE_DAILY

def retro(update, context):
    update.message.reply_text("Wie war der Tag?")
    return RETRO2

def second_retro(update, context):
    update.message.reply_text("Wie produktiv hast du dich heute gefühlt?")
    return RETRO3

def third_retro(update, context):
    update.message.reply_text("Was hast du heute geschafft?")
    return DONE_RETRO

#def fourth_retro(update, context):
#    update.message.reply_text("Gibt es etwas ?")
#    return DONE_RETRO

def done_daily(update, context):
    update.message.reply_text("Thanks!")
    return ConversationHandler.END

def done_retro(update, context):
    update.message.reply_text("Good Night")
    return ConversationHandler.END


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

DAILY2, DAILY3, DONE_DAILY = range(3)
RETRO2, RETRO3, DONE_RETRO = range(3)
bot_token = 'Token'

updater = Updater(bot_token, use_context=True)
dp = updater.dispatcher

start_handler = CommandHandler("start", start)
dp.add_handler(start_handler)
# Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
daily_handler = ConversationHandler(
    entry_points=[CommandHandler("daily", daily)],

    states={
        DAILY2: [MessageHandler(Filters.text, second_daily)],

        DAILY3: [MessageHandler(Filters.text, third_daily)],

        DONE_DAILY: [MessageHandler(Filters.text,done_daily)],
    },
    fallbacks = [MessageHandler(Filters.regex('^Done$'), done_daily)]
)

retro_handler = ConversationHandler(
    entry_points=[CommandHandler("retro", retro)],

    states={
        RETRO2: [MessageHandler(Filters.text, second_retro)],

        RETRO3: [MessageHandler(Filters.text, third_retro)],

        DONE_RETRO: [MessageHandler(Filters.text,done_retro)],
    },
    fallbacks = [MessageHandler(Filters.regex('^Done$'), done_retro)]
)
    
dp.add_handler(daily_handler)
dp.add_handler(retro_handler)
# Start the Bot
updater.start_polling()
    
# Run the bot until you press Ctrl-C or the process receives SIGINT,
# SIGTERM or SIGABRT. This should be used most of the time, since
# start_polling() is non-blocking and will stop the bot gracefully.
updater.idle()
