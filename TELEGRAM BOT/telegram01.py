# bot name - WeatherWise
# username = @weather_wise247_bot

from telegram import Bot
from telegram.ext import Updater, CommandHandler

token = "6732164277:AAHJm0d0U0gDkQ-k1rUqAArIOy2mlHbW5Fk"

bot = Bot(token='6732164277:AAHJm0d0U0gDkQ-k1rUqAArIOy2mlHbW5Fk')
updater = Updater(bot=bot, update_queue=True)
dispatcher = updater.dispatcher


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! Welcome to WeatherWise.")

def help(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=
        """
/start -> Hello! Welcome to WeatherWise.
/help -> This message 
/content -> This will will be updated soon
"""
)
        
def content(update, context):
    update.message.reply_text(" We will provide you the weather update")

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('help', help))
dispatcher.add_handler(CommandHandler('content', content))

updater.start_polling()
updater.idle()