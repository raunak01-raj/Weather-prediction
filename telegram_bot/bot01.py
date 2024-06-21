import pyowm
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from newsapi import NewsApiClient

# API keys
OWM_API_KEY = 'dced1079e66785e94ac5827a3215410e'
NEWS_API_KEY = '5d17b0593c62456992daa613eeee9967'

# Telegram Bot Token
TOKEN = '6732164277:AAHJm0d0U0gDkQ-k1rUqAArIOy2mlHbW5Fk'

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Welcome to WeatherBot! Use \n'
                              '/weather <city> to get current weather,\n '
                              '/forecast <city> to get a 3-hour forecast,\n '
                              'and /news to get the latest weather news.\n')

def weather(update: Update, context: CallbackContext) -> None:
    city = ' '.join(context.args)
    if not city:
        update.message.reply_text('Please provide a city name')
        return

    try:
        # Initialize pyowm with your API key
        owm = pyowm.OWM(OWM_API_KEY)

        # Search for current weather in the specified city
        observation = owm.weather_manager().weather_at_place(city)
        w = observation.weather

        # Parse weather information
        weather_description = w.detailed_status.capitalize()
        temperature = w.temperature('celsius')['temp']
        humidity = w.humidity

        # Format the response
        reply_text = f'Weather in {city}: {weather_description}\nTemperature: {temperature}°C\nHumidity: {humidity}%'

        update.message.reply_text(reply_text)

    except pyowm.commons.exceptions.NotFoundError:
        update.message.reply_text('City not found. Please enter a valid city name.')
    except Exception as e:
        update.message.reply_text('Sorry, something went wrong.')

def forecast(update: Update, context: CallbackContext) -> None:
    city = ' '.join(context.args)
    if not city:
        update.message.reply_text('Please provide a city name')
        return

    try:
        # Initialize pyowm with your API key
        owm = pyowm.OWM(OWM_API_KEY)

        # Search for weather forecast in the specified city
        forecast = owm.weather_manager().forecast_at_place(city, '3h')

        # Get the next 5 forecasts
        forecasts = forecast.forecast
        reply_text = f'3-Hour Forecast for {city}:\n'

        for weather in forecasts:
            time = weather.reference_time('iso')[11:16]
            description = weather.detailed_status.capitalize()
            temperature = weather.temperature('celsius')['temp']
            reply_text += f'{time}: {description}, {temperature}°C\n'

        update.message.reply_text(reply_text)

    except pyowm.commons.exceptions.NotFoundError:
        update.message.reply_text('City not found. Please enter a valid city name.')
    except Exception as e:
        update.message.reply_text(f'Sorry, something went wrong: {str(e)}')

# Example usage (not part of the function)
# Replace with actual Update and CallbackContext objects when running in a bot environment
# update = Update
# context = CallbackContext
# forecast(update, context)


def news(update: Update, context: CallbackContext) -> None:
    try:
        # Initialize NewsApiClient with your API key
        newsapi = NewsApiClient(api_key=NEWS_API_KEY)

        # Fetch top headlines related to weather
        top_headlines = newsapi.get_top_headlines(q='weather', language='en', country='us')

        if top_headlines['totalResults'] > 0:
            articles = top_headlines['articles'][:5]  # Limit to 5 articles

            reply_text = 'Latest Weather News:\n\n'
            for article in articles:
                title = article['title']
                url = article['url']
                reply_text += f'{title}\n{url}\n\n'

            update.message.reply_text(reply_text)
        else:
            update.message.reply_text('No news found related to weather.')

    except Exception as e:
        update.message.reply_text('Sorry, something went wrong.')

def main() -> None:
    updater = Updater(TOKEN, use_context=True)

    # Commands
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('weather', weather))
    updater.dispatcher.add_handler(CommandHandler('forecast', forecast))
    updater.dispatcher.add_handler(CommandHandler('news', news))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()