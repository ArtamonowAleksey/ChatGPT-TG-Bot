import openai as openai
import telebot
from telebot import types

# Параметры подключения к Телеграм

TG_token = ''
bot = telebot.TeleBot(TG_token)

# Параметры подключения к ChatGPT

openai_token = ''
openai.api_key = openai_token

# Параметры подключения к БД

host = ''
database = ''
user = 'user'
password = ''
port = ''

# Приветственное сообщение

hi_message = "Спрашивай и я расскажу тебе все,что знаю"


# Стартовое сообщение бота.

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, hi_message)


@bot.message_handler(content_types=['text'])
def get_text_message(message):
    if message.content_type == 'text':
        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                                  messages=[{"role": "user", "content": message.text}]
                                                  )
        openai_answer = completion.choices[0].message.content
        bot.send_message(message.from_user.id,openai_answer)

bot.polling(none_stop=True, interval=1)
