
from flask import Flask, request
import os
import telebot
import bot_ironchief


server = Flask(__name__)
bot = bot_ironchief.bot
bot_ironchief.main()


@server.route('/' + bot.token, methods=['POST'])
def get_message():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return '!', 200


@server.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://bot-ironchief.herokuapp.com/' + bot.token)
    return 'Hello from bot', 200


@server.route('/admin')
def helloadmin():
    return 'Hello admin', 200


@server.route('/rwh')
def remove_webhook():
    bot.remove_webhook()
    return 'webhook delete - ok', 200


if __name__ == '__main__':
    server.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))