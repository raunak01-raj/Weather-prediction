# bot name - WeatherWise
# username = @weather_wise247_bot

import telegram.ext

Token = "6732164277:AAHJm0d0U0gDkQ-k1rUqAArIOy2mlHbW5Fk"

updater = telegram.ext.updater("6732164277:AAHJm0d0U0gDkQ-k1rUqAArIOy2mlHbW5Fk", use_context=True)
dispatcher = updater.dispatcher

def start(update, context):
    update.message.reply_text("Hello! Welcome to WeatherWise")

def help(update, context):
    update.message.reply_text(
        """
/start -> Welcome to the channel
/help -> This message
/content -> About current weather prediction
"""
    )

def content(update, context):
    update.message.reply_text(" We will provide you the weather update")

dispatcher.add_handler(telegram.ext.CommandHandler('start', start))
dispatcher.add_handler(telegram.ext.CommandHandler('help', help))
dispatcher.add_handler(telegram.ext.CommandHandler('content', content))

updater.start_polling
updater.idle()