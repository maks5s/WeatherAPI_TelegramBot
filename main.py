import os
import requests
import telebot
from telebot import types
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')

bot = telebot.TeleBot(BOT_TOKEN)


def get_weather(city_name):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={WEATHER_API_KEY}"
    response = requests.get(url)
    weather_data = response.json()

    weather_text = ""

    if weather_data['cod'] == 200:
        weather_text += f"City : {weather_data['name']}, {weather_data['sys']['country']}\n"
        weather_text += f"Coordinate : {weather_data['coord']['lon']} °N, {weather_data['coord']['lat']} °E\n"
        weather_text += f"Weather : {weather_data['weather'][0]['main']}\n"
        weather_text += f"Temperature : {weather_data['main']['temp'] - 273.15:.2f} °C\n"
        weather_text += f"Humidity : {weather_data['main']['humidity']} %\n"
        weather_text += f"Wind Speed : {weather_data['wind']['speed']} m/s\n"
    else:
        weather_text += f"Error: {weather_data['message']}"

    return weather_text


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Hello, I`m WeatherAPI_Bot. To find out the weather, please enter command \"/weather\"")


@bot.message_handler(commands=['weather'])
def ask_city(message):
    msg = bot.reply_to(message, "Please enter the city name:")
    bot.register_next_step_handler(msg, send_weather)


def send_weather(message):
    city_name = message.text
    weather_text = get_weather(city_name)

    bot.send_message(message.chat.id, f"The current weather details in {city_name}:\n\n{weather_text}")


bot.infinity_polling()
