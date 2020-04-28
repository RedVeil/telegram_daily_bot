from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
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




messages = {
    "Deutsch":{
        "inital_standup_time": 'Alles klar, lass uns in Deutsch weiter machen. \nWann soll ich dich an dein tägliches Standup erinnern?',
        "inital_retro_time": ['Ich werde dich von nun an um ', 'Uhr an dein Standup erinnern. \nWann soll ich dich an deine tägliche Retro erinnern?' ],
        "end_inital_configuration": ['Ok, täglich um ','Uhr werde ich dich an deine Retro erinnern.'
                                    '\nMit /standup kannst du dein erstes Standup starten.' 
                                    '\nWenn du mehr wissen willst schreibe /help.'],
        "cancel": 'Tschüss, ich hoffe wir reden bald wieder.',
        "change_language": 'Alles klar, lass uns in Deutsch weiter machen.',
        "change_standup_time": 'Wann soll ich dich an dein tägliches Standup erinnern?',
        "end_standup_time": ['Ich werde dich von nun an um ', 'Uhr an dein Standup erinnern.'],
        "change_retro_time":'Wann soll ich dich an deine tägliche Retro erinnern?',
        "end_retro_time":['Ok, täglich um ','Uhr werde ich dich an deine Retro erinnern.'],
        "standup_reminder":"Hallo, ich soll dich an dein /standup erinnern.",
        "weekly_goal_reminder":"Text /weekly um mir von deinem Ziel für diese Woche zu berichten.",
        "retro_reminder":"Schreibe /retro um deine Retro zu starten.",
        "weekly_goal": "Also, was ist dein Ziel für diese Woche? Ich bin ganz Ohr.",
        "standup_inital":"Guten Morgen :) \n Was ist dein Ziel für Heute?",
        "standup_placeholder": "",
        "retro_inital": "",
        "retro_how_do_you_feel": "",
        "retro_placeholder": "",
        "retro_anything_else": "",
    },
    "English":{
        "inital_standup_time": 'Very well, i will speak in english than.\nWhen would you like to get notified about your daily standup?',
        "inital_retro_time": ['Ok, i will remind you about daily about your standup at ', '.\nWhen would you like to get notified about your daily retro?'],
        "end_inital_configuration": ['I will remind you about daily about your retro at ', '.'
                                    '\nYou can start your first standup now with /standup'
                                    '\nIf you wanna learn more type /help.'],
        "cancel": 'Bye! I hope we can talk again some day.',
        "change_language": 'Very well, i will speak in english than.',
        "change_standup_time":'When would you like to get notified about your daily standup?',
        "end_standup_time": ['Ok, i will remind you about daily about your standup at ', '.'],
        "change_retro_time":'When would you like to get notified about your daily retro?',
        "end_retro_time":['I will remind you about daily about your retro at ', '.']
        "standup_reminder":"Hello, i shall remind you of your /standup.",
        "weekly_goal_reminder":"Text /weekly to tell me about your goal for this week.",
        "retro_reminder":"Text me /retro to start your retro.",
        "weekly_goal": "So, what is your goal for the week?",
        "standup_inital":"Good Day :)",
        "standup_placeholder": "",
        "retro_inital": "",
        "retro_how_do_you_feel": "",
        "retro_placeholder": "",
        "retro_anything_else": "",

    }
}













def start(update, context):
    context.user_data["language"] = "English"
    context.user_data["standup_time"] = 10
    context.user_data["retro_time"] = 19
    language_keyboard = [['Deutsch', 'English']]
    update.message.reply_text('What language shall i use?', reply_markup=ReplyKeyboardMarkup(language_keyboard, one_time_keyboard=True))
    return "inital_standup_time"

def inital_standup_time(update,context):
    context.user_data["language"] = update.message.text  
    update.message.reply_text(messages[context.user_data["language"]][ "inital_standup_time"])
    return "inital_retro_time"

def inital_retro_time(update,context):
    context.user_data["standup_time"] = update.message.text
    dt = datetime.today()
    first = pytz.timezone(str(get_localzone())).localize(datetime(dt.year,dt.month,dt.day,update.message.text))
    context.job_queue.run_repeating(standup_reminder, 
                                    interval=timedelta(days=1), 
                                    first=first,
                                    context=update.message.chat_id)
    context.job_queue.run_repeating(weekly_goal_reminder, 
                                    interval=timedelta(days=7), 
                                    first=first,
                                    context=update.message.chat_id)
    update.message.reply_text(messages[context.user_data["language"]]["inital_retro_time"][0] 
                                + update.message.text 
                                + messages[context.user_data["language"]]["inital_retro_time"][1])
    return "end_inital_configuration"

def end_inital_configuration(update,context):
    context.user_data["retro_time"] = update.message.text
    dt = datetime.today()
    first = pytz.timezone(str(get_localzone())).localize(datetime(dt.year,dt.month,dt.day,update.message.text))
    context.job_queue.run_repeating(retro_reminder, 
                                    interval=timedelta(days=1), 
                                    first=first,
                                    context=update.message.chat_id)

    update.message.reply_text(messages[context.user_data["language"]]["end_inital_configuration"][0] 
                                + update.message.text 
                                + messages[context.user_data["language"]]["end_inital_configuration"][1])
    return "end_inital_configuration"

def cancel(update, context):
    update.message.reply_text(messages[context.user_data["language"]]["cancel"],
                                reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END

def change_language(update, context):
    if context.user_data["language"] == "Deutsch":
        context.user_data["language"] = "English"
    else:
        context.user_data["language"] = "Deutsch"

    update.message.reply_text(messages[context.user_data["language"]]["change_language"])
    

def change_standup_time(update, context):
    update.message.reply_text(messages[context.user_data["language"]]["change_standup_time"])

def end_standup_time(update,context):
    context.user_data["standup_time"] = update.message.text
    update.message.reply_text(messages[context.user_data["language"]]["end_standup_time"][0]
                                + update.message.text
                                + messages[context.user_data["language"]]["end_standup_time"][1])



def change_retro_time(update,context):
    update.message.reply_text(messages[context.user_data["language"]]["change_retro_time"])

def end_retro_time(update, context):
    context.user_data["retro_time"] = update.message.text
    update.message.reply_text(messages[context.user_data["language"]]["end_retro_time"][0]
                                + update.message.text
                                + messages[context.user_data["language"]]["end_retro_time"][1])

def standup_reminder(context):
        context.bot.send_message(chat_id=context.job.context, text=messages[context.user_data["language"]]["standup_reminder"])

def weekly_goal_reminder(context):
        context.bot.send_message(chat_id=context.job.context, text=messages[context.user_data["language"]]["weekly_goal_reminder"])

def retro_reminder(context):
        context.bot.send_message(chat_id=context.job.context, text=messages[context.user_data["language"]]["retro_reminder"])



def weekly(context, update):
    update.message.reply_text(messages[context.user_data["language"]]["weekly_goal"])


def standup_inital(context,update):
    weekday = {"English":["Monday","Tuesdy","Wednesday","Thursday","Friday"], "Deutsch":["Montag","Dienstag","Mittwoch","Donnerstag","Freitag"]}
    today = datetime.today()
    update.message.reply_text(f"""{weekdays[context.user_data["language"]][today.weekday()]} - {today.day}/{today.month}/{today.year}.
                                \n{messages[context.user_data["language"]]["standup_inital"]}""")
    return "standup_placeholder"

def standup_placeholder(context,update):
    update.message.reply_text(messages[context.user_data["language"]]["standup_placeholder"])


def retro_inital(context,update):
    update.message.reply_text(messages[context.user_data["language"]]["retro_inital"])
    return "retro_how_do_you_feel"

def retro_how_do_you_feel(context,update):
    update.message.reply_text(messages[context.user_data["language"]]["retro_how_do_you_feel"])
    return "retro_anything_else"

def retro_anything_else(context,update):
    update.message.reply_text(messages[context.user_data["language"]]["retro_anything_else"])
    return "retro_placeholder"

def retro_placeholder(context,update):
    update.message.reply_text(messages[context.user_data["language"]]["retro_placeholder"])
    



def main():
    bot_token = 'token'
    updater = Updater(bot_token, use_context=True)
    dp = updater.dispatcher

    

    start_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            "inital_standup_time": [MessageHandler(Filters.regex('^(Deutsch|English)$'), inital_standup_time)],
            "inital_retro_time": [MessageHandler(Filters.text, inital_retro_time)],
            "end_inital_configuration": [MessageHandler(Filters.text, end_inital_configuration)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    standup_time_handler = ConversationHandler(
        entry_points=[CommandHandler('standup_time', change_standup_time)],
        states={
            "end_standup_time": [MessageHandler(Filters.text), end_standup_time)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    retro_time_handler = ConversationHandler(
        entry_points=[CommandHandler('retro_time', change_retro_time)],
        states={
            "end_retro_time": [MessageHandler(Filters.text), end_retro_time)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    standup_handler = ConversationHandler(
    entry_points=[CommandHandler("standup", standup_inital)],
    states={
        "standup_placeholder": [MessageHandler(Filters.text, standup_placeholder)]
    },
    fallbacks = [CommandHandler('cancel', cancel)]
    )

    retro_handler = ConversationHandler(
    entry_points=[CommandHandler("retro", retro_inital)],
    states={
        "retro_how_do_you_feel": [MessageHandler(Filters.text, retro_how_do_you_feel)],

        "retro_placeholder": [MessageHandler(Filters.text, retro_placeholder)],

        "retro_anything_else": [MessageHandler(Filters.text,retro_anything_else)],
    },
    fallbacks = [CommandHandler('cancel', cancel)]
    )



    dp.add_handler(start_handler)
    dp.add_handler(standup_time_handler)
    dp.add_handler(retro_time_handler)
    dp.add_handler(standup_handler)
    df.add_handler(retro_handler)
    dp.add_handler(CommandHandler("language", change_language))
    dp.add_handler(CommandHandler("weekly", weekly))

    #Start Bot
    updater.start_polling()

    #Stop Bot with Ctrl+C
    updater.idle()

if __name__ == '__main__':
    main()