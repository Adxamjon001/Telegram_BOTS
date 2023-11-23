

import telebot
from pyowm import OWM

# Botni tokeni
TOKEN = '6743702064:AAH0APP9F2vumxFX2U9WYgQit65qTrfmPPI'

# OpenWeatherMap API klyuchi
OWM_API_KEY = 'ff6aef17fcfafcd4d7145ff1bc9a6dcb'
owm = OWM(OWM_API_KEY)
mgr = owm.weather_manager()

# Botni yaratish
bot = telebot.TeleBot(TOKEN)

# /start buyrug'i
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Salom! Ob-havo ma'lumotlari uchun /obhavo buyrug'ini bosing.")

# /obhavo buyrug'i
@bot.message_handler(commands=['obhavo'])
def handle_obhavo(message):
    # Manzil so'rovi
    msg = bot.send_message(message.chat.id, "Qaysi shahar ob-havoni bilmoqchisiz?")
    bot.register_next_step_handler(msg, process_city_step)

def process_city_step(message):
    try:
        # Manzilni olish
        city = message.text
        # Ob-havo malumotlarini so'rovi
        observation = mgr.weather_at_place(city)
        w = observation.weather

        # Ma'lumotlarni tayyorlash
        status = w.detailed_status
        temp = w.temperature('celsius')["temp"]
        humidity = w.humidity
        speed=w.wind
        

        # Foydalanuvchiga javob
        reply = f"Hozir {city} shaharida ob-havo:\nHavo: {status}\nTemperatura: {temp}°C\nNamlik: {humidity}%\nShamol tezligi:  {w.wind()['speed']} m/s m/s 💨"
        bot.send_message(message.chat.id, reply)

    except Exception as e:
        bot.send_message(message.chat.id, f"Xatolik yuz berdi: {e}")

# Botni ishga tushirish
if __name__ == '__main__':
    bot.polling(none_stop=True)
