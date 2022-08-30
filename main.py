# -*- coding: utf-8 -*-

import requests.exceptions
from dbase import *
from order_candy import *
from cart_candy import *
from text_type import *
from call_back_c import *
import telebot
import config
from telebot import types

bot = telebot.TeleBot(config.TOKEN)

class telegramCommands:

	@bot.message_handler(commands=['start'])
	def contact(message):
		bd_users = set_data_base_id_user(message)
		phone = bd_users.test_phone()
		if phone == None:
			keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
			get_phone = types.KeyboardButton('Отправить телефон', request_contact=True)
			keyboard.add(get_phone)
			bot.send_message(message.chat.id,
							 'Для использования бота необходим Ваш номер телефона.\nБлагодарим за понимание)',
							 reply_markup=keyboard)
		elif phone != None:
			bd = cart_bd(message)
			set_data_base_id_user(message)
			keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
			button_shop = types.KeyboardButton('Меню')
			button_history = types.KeyboardButton('История заказов')
			button_cart = types.KeyboardButton('Корзина')
			keyboard.add(button_shop, button_history)
			keyboard.add(button_cart)
			bot.send_message(message.chat.id,
							 '{0.first_name}, привет!\nЭтот бот сделан для твоего удобства)\nЗаказывай где тебе удобно и когда тебе удобно!)'.format(
								 message.from_user), reply_markup=keyboard)

	@bot.message_handler(commands=['help'])
	def get_phone(message):
		print(message.text)
		bot.send_chat_action(message.chat.id, action='record_video')

	@bot.message_handler(commands=['smena'])
	def info_please(message):
		x = cart_bd(message)
		bot.send_message(message.chat.id, x.set_barista())

	@bot.message_handler(commands=['who_barista'])
	def info_please(message):
		x = cart_bd(message)
		try:
			barista = x.who_barista()
			bot.send_photo(message.chat.id,  barista[1], caption='Сегодня на смене: ' + barista[0], parse_mode='HTML')
		except TypeError:
			bot.send_message(message.chat.id, 'Хм....🤔\nЯ пока не в курсе кто бариста, пойду - узнаю, спросите меня позже ;)', parse_mode='HTML')

	@bot.message_handler(content_types=['text'])
	def starttext(message):
		textChat(message)

	@bot.message_handler(content_types=['contact'])
	def welcome(message):
		bd = cart_bd(message)
		users = set_data_base_id_user(message)
		users.phone(message.contact.phone_number)
		keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
		button_shop = types.KeyboardButton('Меню')
		button_history = types.KeyboardButton('История заказов')
		button_cart = types.KeyboardButton('Корзина')
		keyboard.add(button_shop, button_history)
		keyboard.add(button_cart)
		bot.send_message(message.chat.id,
						 '<u>Cпасибо!</u>\nЭтот бот сделан для твоего удобства)\nЗаказывай где тебе удобно и когда тебе удобно!)'.format(
							 message.from_user), reply_markup=keyboard, parse_mode='HTML')

	@bot.callback_query_handler(func=lambda call: True)
	def callback_candy(call):
		cb_candy(call)

while True:
	try:
		if __name__ == '__main__':
			bot.polling(none_stop=True)
	except requests.exceptions.ReadTimeout as e:
		print('candy_coffee', 'readtimeout')
	except requests.exceptions.ConnectionError as e:
		print('candy_coffee', 'ConnectionError')