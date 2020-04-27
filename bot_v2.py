from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, CallbackQueryHandler, 
                        MessageHandler, ConversationHandler,  
                        InlineQueryHandler, Filters, CallbackContext)
import logging
from datetime import datetime, timedelta
from tzlocal import get_localzone
import pytz

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def start(update, context):
    dt = datetime.today()
    daily_time = 10
    first = pytz.timezone(str(get_localzone())).localize(datetime(dt.year,dt.month,dt.day,daily_time))
    #context.job_queue.run_repeating( daily_reminder, 
    #                                interval=timedelta(days=1), 
    #                                first=first,
    #                                context=update.message.chat_id)

    language_keyboard = [[InlineKeyboardButton("Deutsch", callback_data='de'),
                        InlineKeyboardButton("English", callback_data='eng')]]
    update.message.reply_text('Please choose:', reply_markup=InlineKeyboardMarkup(language_keyboard))
    language_keyboard2 = [[InlineKeyboardButton("2", callback_data='2'),
                        InlineKeyboardButton("3", callback_data='3')]]
    update.message.reply_text('Please choose:', reply_markup=InlineKeyboardMarkup(language_keyboard2))
    
def language_button(update, context):
    query = update.callback_query
    query.answer()
    context.user_data["language"] = query.data
    query.edit_message_text(f"Your language is set to: {query.data}")

def get_language(update, context):
    update.message.reply_text(context.user_data["language"])

def main():
    bot_token = 'token'
    updater = Updater(bot_token, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(language_button))
    dp.add_handler(CommandHandler("get_language", get_language))
    #Start Bot
    updater.start_polling()

    #Stop Bot with Ctrl+C
    updater.idle()

if __name__ == '__main__':
    main()