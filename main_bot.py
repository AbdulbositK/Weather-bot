import requests
import datetime
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

open_weather_token = '62d2cf4aa1b0692cc1aa30f934dcc487'
tg_bot = '2101328705:AAEBmQKrblO8UXospr0xLcGYNEaiPgZXH1Q'

bot = Bot(token=tg_bot)
dp = Dispatcher(bot)

btn_weather_Tashkent = KeyboardButton('Tashkent')
btn_weather_Samarkand = KeyboardButton('Samarkand')
btn_weather_Andijan = KeyboardButton('Andijan')
btn_weather_Bukhara = KeyboardButton('Bukhara')
btn_weather_Fergana = KeyboardButton('Fergana')
city_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_weather_Tashkent, btn_weather_Andijan,
                                                          btn_weather_Bukhara, btn_weather_Samarkand,
                                                          btn_weather_Fergana)


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Привет! Выберите город который вы хотите проверить", reply_markup=city_menu)


@dp.message_handler()
async def get_weather(message: types.Message):
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B",

    }

    r = requests.get(
        f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric")
    data = r.json()

    city = data["name"]
    cur_weather = data["main"]["temp"]

    weather_description = data["weather"][0]["main"]
    if weather_description in code_to_smile:
        wd = code_to_smile[weather_description]
    else:
        wd = "Посмотрите в окно"

    humidity = data["main"]["humidity"]
    pressure = data["main"]["pressure"]
    wind = data["wind"]["speed"]
    sunrise = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
    sunset = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
    length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
        data["sys"]["sunrise"])

    await message.reply(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                        f"Погода в городе: {city}\nТемпература: {cur_weather}C° {wd}\nВлажность: {humidity}%\n"
                        f"Давление: {pressure} мм.рт.ст\nВетер: {wind} м/с\nВосход солнца: {sunrise}\n"
                        f"Закат солнца: {sunset}\n"
                        f"Продолжительность дня: {length_of_the_day}\n"
                        f"***Хорошего дня!***")


if __name__ == '__main__':
    executor.start_polling(dp)
