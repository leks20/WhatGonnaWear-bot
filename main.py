import os
import time

from dotenv import load_dotenv
import requests
from requests.exceptions import RequestException
import telebot
from telebot import types


load_dotenv()
telegram_token = os.getenv('telegram_token')
weather_token = os.getenv('weather_token')

bot = telebot.TeleBot(telegram_token)
URL = 'http://api.openweathermap.org/data/2.5/forecast'


def get_weather(city):
    weather_parameters = {
            'q': city,
            'appid': weather_token,
            'units': 'metric',
            'lang': 'ru'
        }

    try:
        response = requests.get(url=URL, params=weather_parameters)

        temp = round(response.json()['list'][0]['main']['temp'])
        feels_like = round(response.json()['list'][0]['main']['feels_like'])
        humidity = response.json()['list'][0]['main']['humidity']
        description = response.json()['list'][0]['weather'][0]['description'].capitalize()
        wind_speed = round(response.json()['list'][0]['wind']['speed'])
        time = response.json()['list'][0]['dt_txt'].split(' ')[1].split(':')[0]

        if feels_like < -25:
            advice = 'В такой мороз лучше сидеть дома... Ну или очень тепло одеваться!'
        elif -25 <= feels_like < -20:
            advice = 'Не забудьте про термобелье! Зима выдалась холодная...'
        elif -20 <= feels_like < -15:
            advice = 'Пуховик и тёплая обувь - обязательные атрибуты Вашей прогулки'
        elif -15 <= feels_like < -10:
            advice = 'Тёплый шарф и свитер заменят кружку горячего чая'
        elif -10 <= feels_like < -5:
            advice = 'Прохладно... Не забудьте перчатки и шапку!'
        elif -5 <= feels_like < 0:
            advice = 'Пальто и стильный шарф сегодня как никогда кстати!'
        elif 0 <= feels_like < 5:
            advice = 'Любимый свитшот или тёплый спортивный костюм не дадут замерзнуть'
        elif 5 <= feels_like < 10:
            advice = 'Лёгкая куртка сегодня не помешает'
        elif 10 <= feels_like < 15:
            advice = 'Выгуливаем новые кеды и худи'
        elif 15 <= feels_like < 20:
            advice = 'Долой верхнюю одежду! Время лёгких пиджаков и платьев'
        elif 20 <= feels_like < 25:
            advice = 'Шорты и майка сегодня - отличный выбор'
        elif 25 <= feels_like:
            advice = 'Минимум одежды - максимум загара'

        res = f'{advice}\n\nПогода в г. {city} в {time}:00\n{description}. Температура воздуха: {temp}°, по ощущениям: {feels_like}°. Влажность {humidity} %, скорость ветра {wind_speed} м/с.'

        temp2 = round(response.json()['list'][2]['main']['temp'])
        feels_like2 = round(response.json()['list'][2]['main']['feels_like'])
        humidity2 = response.json()['list'][2]['main']['humidity']
        description2 = response.json()['list'][2]['weather'][0]['description'].capitalize()
        wind_speed2 = round(response.json()['list'][2]['wind']['speed'])
        time2 = response.json()['list'][2]['dt_txt'].split(' ')[1].split(':')[0]
        res2 = f'Погода в г. {city} в {time2}:00\n{description2}. Температура воздуха: {temp2}°, по ощущениям: {feels_like2}°. Влажность {humidity2} %, скорость ветра {wind_speed2} м/с.'

        temp3 = round(response.json()['list'][4]['main']['temp'])
        feels_like3 = round(response.json()['list'][4]['main']['feels_like'])
        humidity3 = response.json()['list'][4]['main']['humidity']
        description3 = response.json()['list'][4]['weather'][0]['description'].capitalize()
        wind_speed3 = round(response.json()['list'][4]['wind']['speed'])
        time3 = response.json()['list'][4]['dt_txt'].split(' ')[1].split(':')[0]
        res3 = f'Погода в г. {city} в {time3}:00\n{description3}. Температура воздуха: {temp3}°, по ощущениям: {feels_like3}°. Влажность {humidity3} %, скорость ветра {wind_speed3} м/с.'

        final_message = f'{res}\n\n{res2}\n\n{res3}'
    except KeyError:
        final_message = 'Мы честно искали, но такого города нет 😟'
    except RequestException:
        final_message = 'Что-то пошло не так...'

    return final_message


def main():

    while True:
        try:
            @bot.message_handler(commands=['start'])
            def start(message):
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
                btn1 = types.KeyboardButton('Москва')
                btn2 = types.KeyboardButton('Санкт-Петербург')
                btn3 = types.KeyboardButton('Новосибирск')
                btn4 = types.KeyboardButton('Екатеринбург')
                btn5 = types.KeyboardButton('Нижний Новгород')
                btn6 = types.KeyboardButton('Казань')
                btn7 = types.KeyboardButton('Челябинск')
                btn8 = types.KeyboardButton('Омск')
                btn9 = types.KeyboardButton('Самара')
                btn10 = types.KeyboardButton('Ростов-на-Дону')
                markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9, btn10)
                text = f'<b>Привет, {message.from_user.first_name}!</b>\nНапишите название города или выберите из списка'
                bot.send_message(message.chat.id, text, parse_mode='html', reply_markup=markup)

            @bot.message_handler(content_types=['text'])
            def mess(message):
                final_message = get_weather(message.text)
                bot.send_message(message.chat.id, final_message, parse_mode='html')

            bot.polling(none_stop=True)

        except KeyboardInterrupt:
            finish = input(
                'Вы действительно хотите прервать работу бота? Y/N: '
                )
            if finish in ('Y', 'y'):
                print('До встречи!')        
            elif finish in ('N', 'n'):
                print('Продолжаем работать!')

        except Exception as e:
            print(f'Бот упал с ошибкой: {e}')
            time.sleep(5)


if __name__ == '__main__':
    main()
