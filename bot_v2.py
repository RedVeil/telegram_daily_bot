from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (Updater, CommandHandler, CallbackQueryHandler, 
                        MessageHandler, ConversationHandler,  
                        InlineQueryHandler, Filters, CallbackContext)
import logging
from datetime import datetime, timedelta

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)



#!!! TODO Implement Payment and Demo
#Either in Telegram or check DB for key in db



messages = {
    "Deutsch":{
        "inital_standup_time": 'Alles klar, lass uns in deutsch weiter machen.\nWann soll ich dich an dein tägliches Standup erinnern?',
        "inital_retro_time": ['Ich werde dich von nun an um ', ' an dein Standup erinnern.\nWann soll ich dich an deine tägliche Retro erinnern?' ],
        "end_inital_configuration": ['Ok, täglich um ',' werde ich dich an deine Retro erinnern.'
                                    '\n/standup startet dein erstes Standup.' 
                                    '\n/help erklärt dir alle Befehle.'],
        "cancel": 'Tschüss, ich hoffe wir reden bald wieder.',
        "change_language": 'Alles klar, lass uns in deutsch weiter machen.',
        "change_standup_time": 'Wann soll ich dich an dein tägliches Standup erinnern?',
        "end_standup_time": ['Ich werde dich von nun an um ', ' an dein Standup erinnern.'],
        "change_retro_time":'Wann soll ich dich an deine tägliche Retro erinnern?',
        "end_retro_time":['Ok, täglich um ',' werde ich dich an deine Retro erinnern.'],
        "standup_reminder":"Hallo, ich soll dich an dein /standup erinnern.",
        "weekly_goal_reminder":"Text /weekly um mir von deinem Ziel für diese Woche zu berichten.",
        "retro_reminder":"Schreibe /retro um deine Retro zu starten.",
        "weekly_goal": "Also, was ist dein Ziel für diese Woche? Ich bin ganz Ohr.",
        "standup_inital":"Guten Morgen :)\nWas ist dein Ziel für Heute?",
        "standup_placeholder": "Danke :)",
        "retro_inital": "Wie war dein Tag?",
        "retro_accomplished": "Was hast du heute geschafft?",
        "retro_placeholder": "Gute Nacht :)",
        "helper":"Es gibt einige Befehle mit denen du mich kontrollieren kannst."
                    "\n"
                    "\n/language ändert meine Sprache zu Englisch."
                    "\n/standuptime ändert die Zeit zu der ich dich an dein Standup erinnere."
                    "\n/retrotime ändert wann ich dich an deine Retro erinnere."
                    "\n/changestandup erlaubt dir Fragen im Standup zu ändern oder zu löschen."
                    "\n/changeretro erlaubt dir ebenso die Fragen der Retro zu ändern oder zu löschen."
                    "\n"
                    "\n/standup startet zu jedem Zeitpunkt dein Standup."
                    "\n/weekly startet die die Frage nach deinem Ziel der Woche."
                    "\n/retro startet die Retro.",
        "change_standup_inital":'''Wenn du eine Frage ändern möchtest, sag mir was ich dich fragen soll.
                                \nWenn du eine Frage löschen möchtest, schreibe "DELETE".
                                \nSchreibe "SKIP" wenn du diese Frage nicht ändern möchtest.
                                \nWas soll ich zuerst fragen?''',
        "change_standup_placeholder":["Ich werde im Standup dir folgende Frage stellen: ","\nSoll ich dich noch etwas fragen?"],
        "change_standup_end": ["Meine zweite Frage lautet: ", "\nIst vermerkt."],
        "change_retro_inital":"Was soll ich dich als erstes fragen?",
        "change_retro_accomplished":["Meine erste Frage lautet: ", "\nWie lautet meine zweite Frage?"],
        "change_retro_placeholder":["Ich werde dich als zweites das folgende fragen: ","\nWenn ich dich noch etwas fragen soll, was wäre es?"],
        "change_retro_end":["Meine letzte Frage ist: ", "\nIch hab alles notiert."],
    },
    "English":{
        "inital_standup_time": "Alright, let's continue in english. When shall I remind you of your daily standup?",
        "inital_retro_time": ['I will remind you from now on ', ' about your standup.\nWhen shall I remind you of your daily retro?'],
        "end_inital_configuration": ["Okay, I'll remind you daily at "," about your retro."
                                    "\n/standup starts your first standup."
                                    "\n/help explains all available commands."],
        "cancel": "Bye, I hope we talk again soon.",
        "change_language": "Alright, let's continue in english.",
        "change_standup_time": 'When should I remind you of your daily standup?',
        "end_standup_time": ['I will remind you from now on at ', ' about your standup.'],
        "change_retro_time": 'When should I remind you of your daily retro?',
        "end_retro_time":["Okay, I'll remind you daily at "," about your retro."],
        "standup_reminder": "Hello, I'm here to remind you about your /standup.",
        "weekly_goal_reminder": "Text /weekly to tell me about your goal for this week.",
        "retro_reminder": "Write /retro to start your retro.",
        "weekly_goal": "So what is your goal for this week? I'm all ears.",
        "standup_inital": "Good morning :)\nWhat is your goal for today?",
        "standup_placeholder": "Have a good day :)",
        "retro_inital": "How was your day?",
        "retro_accomplished": "What did you do today?",
        "retro_placeholder": "Good Night :)",
        "helper":"There are some commands you can use to control me."
                    "\n"
                    "\n/language changes my language to English."
                    "\n/standuptime changes the time I remind you of your standup."
                    "\n/retrotime changes when I remind you of your retro."
                    "\n/changestandup allows you to change or delete questions in the standup."
                    "\n/changeretro also allows you to change or delete retro questions."
                    "\n"
                    "\n/standup starts your standup at any time."
                    "\n/weekly starts the question for your goal of the week."
                    "\n/retro starts the retro.",
        "change_standup_inital":"If you want to change a question type the question that i shall ask you."
                                '\nIf you want to delete the question write "DELETE" and "SKIP" if you dont want to change this question.'
                                '\nWhat shall i ask first?',
        "change_standup_placeholder":["I will ask you this question in the standup: ","\nDo you want me to ask you something else?"],
        "change_standup_end": ["My second question is ",". Noted."],
        "change_retro_inital": "What should I ask you first?",
        "change_retro_accomplished":["My first question is: ", "\nWhat's my second question?"],
        "change_retro_placeholder": ["I will ask you the following second question: ","\nIf I should ask you something else, what would it be?"],
        "change_retro_end": ["My last question is: ", "\nGot it."],
    }
}

#---Utility Functions---
def parse_time(message):
    divider = [",",".",":"]
    for i in divider:
        if i in message:
            hour, minute = message.split(i)
            return str(hour), str(minute)
    return str(message), "00"

def change_question(message, question, context):
    if message.upper() == "SKIP":
        return
    elif message.upper() == "DELETE":
        context.user_data["messages"][context.user_data["language"]][question] = ""
    else:
        context.user_data["messages"][context.user_data["language"]][question] = message

def payment_check(update, context):
    dt = datetime.today()
    today = datetime(dt.year,dt.month,dt.day)
    if not context.user_data["premium"]:
        if  context.user_data["demo"]+timedelta(days=8) >= today:
            update.message.reply_text("demo in the future")
            #Block interaction and tell people to pay
    else:
        if today >= context.user_data["premium"]+timedelta(days=32):
            return
            # how to check for subscription?
            #Block interaction and tell people to pay
#----------------------------------------------------------------------------------------

#---Start Configuration---
def start(update, context):
    dt = datetime.today()
    context.user_data["messages"] = messages
    context.user_data["language"] = "English"
    context.user_data["standup_time"] = 10
    context.user_data["retro_time"] = 19
    context.user_data["demo"] = datetime(dt.year,dt.month,dt.day)
    context.user_data["premium"] = False
    #payment_check(update, context)
    language_keyboard = [['Deutsch', 'English']]
    update.message.reply_text('What language shall i use?', reply_markup=ReplyKeyboardMarkup(language_keyboard, one_time_keyboard=True))
    return "inital_standup_time"

def inital_standup_time(update, context):
    context.user_data["language"] = update.message.text  
    update.message.reply_text(context.user_data["messages"][context.user_data["language"]][ "inital_standup_time"])
    return "inital_retro_time"

def inital_retro_time(update, context):
    context.user_data["standup_time"] = update.message.text
    hour, minute = parse_time(update.message.text)
    dt = datetime.today()
    first = datetime(dt.year,dt.month,dt.day,int(hour),int(minute))
    if first <= datetime.now():
        first = datetime(dt.year,dt.month,dt.day+1,int(hour),int(minute))

    context.job_queue.run_repeating(standup_reminder, 
                                    interval=timedelta(days=1), 
                                    first=first,
                                    context=[update.message.chat_id,context.user_data["language"]])
    context.job_queue.run_repeating(weekly_goal_reminder, 
                                    interval=timedelta(days=7), 
                                    first=first,
                                    context=[update.message.chat_id,context.user_data["language"]])
    update.message.reply_text(context.user_data["messages"][context.user_data["language"]]["inital_retro_time"][0] 
                                + hour + ":" + minute
                                + messages[context.user_data["language"]]["inital_retro_time"][1])
    return "end_inital_configuration"

def end_inital_configuration(update, context):
    context.user_data["retro_time"] = update.message.text
    hour, minute = parse_time(update.message.text)
    dt = datetime.today()
    first = datetime(dt.year,dt.month,dt.day,int(hour),int(minute))
    if first <= datetime.now():
        first = datetime(dt.year,dt.month,dt.day+1,int(hour),int(minute))

    context.job_queue.run_repeating(retro_reminder, 
                                    interval=timedelta(days=1), 
                                    first=first,
                                    context=[update.message.chat_id,context.user_data["language"]])

    update.message.reply_text(context.user_data["messages"][context.user_data["language"]]["end_inital_configuration"][0] 
                                + hour + ":" + minute
                                + messages[context.user_data["language"]]["end_inital_configuration"][1])
    return ConversationHandler.END

#----------------------------------------------------------------------------------------


#---Change Functions---
def change_language(update, context):
    if context.user_data["language"] == "Deutsch":
        context.user_data["language"] = "English"
    else:
        context.user_data["language"] = "Deutsch"

    update.message.reply_text(context.user_data["messages"][context.user_data["language"]]["change_language"])

def change_standup_time(update, context):
    update.message.reply_text(context.user_data["messages"][context.user_data["language"]]["change_standup_time"])
    return "end_standup_time"

def end_standup_time(update, context):
    context.user_data["standup_time"] = update.message.text
    hour, minute = parse_time(update.message.text)
    update.message.reply_text(context.user_data["messages"][context.user_data["language"]]["end_standup_time"][0]
                                + hour + ":" + minute
                                + messages[context.user_data["language"]]["end_standup_time"][1])
    return ConversationHandler.END

def change_retro_time(update, context):
    update.message.reply_text(context.user_data["messages"][context.user_data["language"]]["change_retro_time"])
    return "end_retro_time"

def end_retro_time(update, context):
    context.user_data["retro_time"] = update.message.text
    hour, minute = parse_time(update.message.text)
    update.message.reply_text(context.user_data["messages"][context.user_data["language"]]["end_retro_time"][0]
                                + hour + ":" + minute
                                + messages[context.user_data["language"]]["end_retro_time"][1])
    return ConversationHandler.END
#----------------------------------------------------------------------------------------

#---Weekly Conversation---
def weekly(update, context):
    update.message.reply_text(context.user_data["messages"][context.user_data["language"]]["weekly_goal"])
#----------------------------------------------------------------------------------------

#---Standup Conversation---
def standup_inital(update, context):
    #payment_check(update, context)
    weekdays = {"English":["Monday","Tuesdy","Wednesday","Thursday","Friday"], "Deutsch":["Montag","Dienstag","Mittwoch","Donnerstag","Freitag"]}
    today = datetime.today()
    update.message.reply_text(f"""{weekdays[context.user_data["language"]][today.weekday()]} - {today.day}/{today.month}/{today.year}.
                                \n{context.user_data["messages"][context.user_data["language"]]["standup_inital"]}""")
    return "standup_placeholder"

def standup_placeholder(update, context):
    update.message.reply_text(context.user_data["messages"][context.user_data["language"]]["standup_placeholder"])
    return ConversationHandler.END
#----------------------------------------------------------------------------------------


#---Retro Conversation---
def retro_inital(update, context):
    update.message.reply_text(context.user_data["messages"][context.user_data["language"]]["retro_inital"])
    return "retro_accomplished"

def retro_accomplished(update, context):
    update.message.reply_text(context.user_data["messages"][context.user_data["language"]]["retro_accomplished"])
    return "retro_placeholder"

def retro_placeholder(update, context):
    update.message.reply_text(context.user_data["messages"][context.user_data["language"]]["retro_placeholder"])
    return ConversationHandler.END
#----------------------------------------------------------------------------------------


#---Reminder---
def standup_reminder(context):
    context.bot.send_message(chat_id=context.job.context[0], text=messages[context.job.context[1]]["standup_reminder"])

def weekly_goal_reminder(context):
    context.bot.send_message(chat_id=context.job.context[0], text=messages[context.job.context[1]]["weekly_goal_reminder"])

def retro_reminder(context):
    context.bot.send_message(chat_id=context.job.context[0], text=messages[context.job.context[1]]["retro_reminder"])
#----------------------------------------------------------------------------------------



#---Helper Functions---
def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def cancel(update, context):
    update.message.reply_text(context.user_data["messages"][context.user_data["language"]]["cancel"],
                                reply_markup=ReplyKeyboardRemove())

def reset_questions(update, context):
    context.user_data["messages"] = messages
    update.message.reply_text(context.user_data["messages"][context.user_data["language"]]["reset_question"])

def helper(update, context):
    update.message.reply_text(context.user_data["messages"][context.user_data["language"]]["helper"])
#----------------------------------------------------------------------------------------


#---Change Standup Conversation---
def change_standup_inital(update, context):
    update.message.reply_text(context.user_data["messages"][context.user_data["language"]]["change_standup_inital"])
    return "change_standup_placeholder"

def change_standup_placeholder(update, context):
    change_question(update.message.text, "standup_inital", context)
    update.message.reply_text(context.user_data["messages"][context.user_data["language"]]["change_standup_placeholder"][0]
                                + update.message.text
                                + context.user_data["messages"][context.user_data["language"]]["change_standup_placeholder"][1])
    return "change_standup_end"

def change_standup_end(update, context):
    change_question(update.message.text, "standup_placeholder", context)
    update.message.reply_text(context.user_data["messages"][context.user_data["language"]]["change_standup_end"][0]
                                + update.message.text
                                + context.user_data["messages"][context.user_data["language"]]["change_standup_end"][1])
    return ConversationHandler.END
#----------------------------------------------------------------------------------------


#---Change Retro Conversation---
def change_retro_inital(update, context):
    update.message.reply_text(context.user_data["messages"][context.user_data["language"]]["change_retro_inital"])
    return "change_retro_accomplished"

def change_retro_accomplished(update, context):
    change_question(update.message.text, "retro_inital", context)
    update.message.reply_text(context.user_data["messages"][context.user_data["language"]]["change_retro_accomplished"][0]
                                + update.message.text
                                + context.user_data["messages"][context.user_data["language"]]["change_retro_accomplished"][1])
    return "change_retro_placeholder"

def change_retro_placeholder(update, context):
    change_question(update.message.text, "retro_anything_else", context)
    update.message.reply_text(context.user_data["messages"][context.user_data["language"]]["change_retro_placeholder"][0]
                                + update.message.text
                                + context.user_data["messages"][context.user_data["language"]]["change_retro_placeholder"][1])
    return "change_retro_end"

def change_retro_end(update, context):
    change_question(update.message.text, "retro_placeholder", context)
    update.message.reply_text(context.user_data["messages"][context.user_data["language"]]["change_retro_end"][0]
                                + update.message.text
                                + context.user_data["messages"][context.user_data["language"]]["change_retro_end"][1])
    return ConversationHandler.END
#----------------------------------------------------------------------------------------







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
        entry_points=[CommandHandler('standuptime', change_standup_time)],
        states={
            "end_standup_time": [MessageHandler(Filters.text, end_standup_time)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    retro_time_handler = ConversationHandler(
        entry_points=[CommandHandler('retrotime', change_retro_time)],
        states={
            "end_retro_time": [MessageHandler(Filters.text, end_retro_time)],
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
            "retro_accomplished": [MessageHandler(Filters.text, retro_accomplished)],
            "retro_placeholder": [MessageHandler(Filters.text, retro_placeholder)],
        },
        fallbacks = [CommandHandler('cancel', cancel)]
    )

    change_standup_handler = ConversationHandler(
        entry_points=[CommandHandler("changestandup", change_standup_inital)],
        states={
            "change_standup_placeholder": [MessageHandler(Filters.text, change_standup_placeholder)],
            "change_standup_end": [MessageHandler(Filters.text, change_standup_end)],
        },
        fallbacks = [CommandHandler('cancel', cancel)]
    )

    change_retro_handler = ConversationHandler(
        entry_points=[CommandHandler("changeretro", change_retro_inital)],
        states={
            "change_retro_accomplished": [MessageHandler(Filters.text, change_retro_accomplished)],
            "change_retro_placeholder": [MessageHandler(Filters.text, change_retro_placeholder)],
            "change_retro_end": [MessageHandler(Filters.text, change_retro_end)],
        },
        fallbacks = [CommandHandler('cancel', cancel)]
    )



    dp.add_handler(start_handler)
    dp.add_handler(standup_time_handler)
    dp.add_handler(retro_time_handler)
    dp.add_handler(standup_handler)
    dp.add_handler(retro_handler)
    dp.add_handler(change_standup_handler)
    dp.add_handler(change_retro_handler)
    dp.add_handler(CommandHandler("language", change_language))
    dp.add_handler(CommandHandler("weekly", weekly))
    dp.add_handler(CommandHandler("help", helper))
    dp.add_handler(CommandHandler("default", reset_questions))
    dp.add_error_handler(error)

    #Start Bot
    updater.start_polling()

    #Stop Bot with Ctrl+C
    updater.idle()

if __name__ == '__main__':
    main()