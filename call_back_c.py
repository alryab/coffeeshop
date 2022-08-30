# -*- coding : utf-8 -*-

import telebot
import config
from telebot import types
from cart_candy import *
from order_candy import *

bot = telebot.TeleBot(config.TOKEN)

class cb_candy:
	def __init__(self, call):
		self.bd = cart_bd(call)
		self.how_many = 0
		self.call = call
		self.chat_id = self.call.message.chat.id
		self.message_id = self.call.message.message_id
		self.callback_candy()
		item_an_buttons(call)
		item_summer_buttons_ws(call)
		item_summer_buttons(call)
		item_buttons(call)
		order_status_class(call)

	def callback_candy(self):
		'''Меню Candy Coffee'''
		if self.call.data == 'clas_cof':
			classic_keyboard = types.InlineKeyboardMarkup(row_width=2)
			espresso = types.InlineKeyboardButton('Эспрессо', callback_data='espresso')
			amerikano = types.InlineKeyboardButton('Американо', callback_data='amerikano')
			latte = types.InlineKeyboardButton('Латте', callback_data='latte')
			capuchino = types.InlineKeyboardButton('Капучино', callback_data='capuchino')
			mokachino = types.InlineKeyboardButton('Мокачино', callback_data='mokachino')
			raf = types.InlineKeyboardButton('Раф', callback_data='raf')
			back = types.InlineKeyboardButton('<- назад', callback_data='main_menu')
			classic_keyboard.add(espresso, amerikano, latte, capuchino, mokachino, raf, back)
			if self.bd.test_cart() > 0:
				bot.edit_message_text('Классическое меню:\n' + self.bd.cart_in_item(), chat_id= self.chat_id, message_id=self.message_id, reply_markup=classic_keyboard, parse_mode='HTML')
			else:
				bot.edit_message_text('Классическое меню:\n', chat_id=self.chat_id,
									  message_id=self.message_id, reply_markup=classic_keyboard, parse_mode='HTML')
		if self.call.data == 'aut_cof':
			aut_keyboard = types.InlineKeyboardMarkup(row_width=2)
			grilyajik = types.InlineKeyboardButton('Грильяжик', callback_data='grilyajik')
			shafutinya = types.InlineKeyboardButton('Шафутиня', callback_data='shafutinya')
			chizulya = types.InlineKeyboardButton('Чизуля', callback_data='chizulya')
			pinoli = types.InlineKeyboardButton('Пиноли', callback_data='pinoli')
			sherif = types.InlineKeyboardButton('Шериф', callback_data='sherif')
			back = types.InlineKeyboardButton('<- назад', callback_data='main_menu')
			aut_keyboard.add(grilyajik, shafutinya, chizulya)
			aut_keyboard.add(pinoli, sherif, row_width=2)
			aut_keyboard.add(back, row_width=1)
			if self.bd.test_cart() > 0:
				bot.edit_message_text('Авторское меню:' + self.bd.cart_in_item(), chat_id=self.chat_id, message_id=self.message_id,
								  reply_markup=aut_keyboard, parse_mode='HTML')
			else:
				bot.edit_message_text('Авторское меню:', chat_id=self.chat_id, message_id=self.message_id,
								  reply_markup=aut_keyboard, parse_mode='HTML')
		if self.call.data == 'sum_cof':
			summer_keyboard = types.InlineKeyboardMarkup(row_width=2)
			tropic = types.InlineKeyboardButton('Смузи Tropic', callback_data='tropic')
			stroinyashka = types.InlineKeyboardButton('Смузи Стройняшка', callback_data='stroinyashka')
			yagodka = types.InlineKeyboardButton('Смузи Ягодка', callback_data='yagodka')
			mohito = types.InlineKeyboardButton('Лимонад Мохито', callback_data='mohito')
			kivi_myata = types.InlineKeyboardButton('Лимонад Киви-Мята', callback_data='kivi_myata')
			milk_coct = types.InlineKeyboardButton('Молочный коктейль', callback_data='milk_coct')
			ice_coffe = types.InlineKeyboardButton('Ice Coffee', callback_data='ice_coffee')
			back = types.InlineKeyboardButton('<- назад', callback_data='main_menu')
			summer_keyboard.add(tropic, yagodka)
			summer_keyboard.add(stroinyashka, mohito, kivi_myata, milk_coct, ice_coffe, back, row_width=1)
			if self.bd.test_cart() > 0:
				bot.edit_message_text('Летнее Меню:' + self.bd.cart_in_item(), chat_id=self.chat_id, message_id=self.message_id, reply_markup=summer_keyboard, parse_mode='HTML')
			else:
				bot.edit_message_text('Летнее Меню:', chat_id=self.chat_id, message_id=self.message_id,
								  reply_markup=summer_keyboard, parse_mode='HTML')
		if self.call.data == 'an_menu':
			an_menu_keyboard = types.InlineKeyboardMarkup(row_width=1)
			coffee = types.InlineKeyboardButton('Кофе свежей обжарки', callback_data='coffee')
			sandwich = types.InlineKeyboardButton('Сэндвич', callback_data='sandwich')
			'''ice_cream = types.InlineKeyboardButton('Мороженое', callback_data='ice_cream')
			water = types.InlineKeyboardButton('Вода', callback_data='water')'''
			back = types.InlineKeyboardButton('<- назад', callback_data='main_menu')
			an_menu_keyboard.add(coffee, sandwich)
			an_menu_keyboard.add(back, row_width=1)
			if self.bd.test_cart() > 0:
				bot.edit_message_text('Другое:' + self.bd.cart_in_item(), chat_id=self.chat_id, message_id=self.message_id,
								  reply_markup=an_menu_keyboard, parse_mode='HTML')
			else:
				bot.edit_message_text('Другое:', chat_id=self.chat_id, message_id=self.message_id,
									  reply_markup=an_menu_keyboard)

		'''Классическое меню:'''
		if self.call.data == 'amerikano':
			amerikano_keyboard = types.InlineKeyboardMarkup(row_width=1)
			amerikano_ob = types.InlineKeyboardButton('Американо', callback_data='amerikano_ob')
			amerikano_hard = types.InlineKeyboardButton('Крепкий Американо', callback_data='amerikano_hard')
			back = types.InlineKeyboardButton('<- назад', callback_data='clas_cof')
			amerikano_keyboard.add(amerikano_ob, amerikano_hard, back)
			if self.bd.test_cart() > 0:
				bot.edit_message_text('Американо - кофе по-американски, вода с эспрессо.\n------\nЦена:\nАмерикано, 250мл - 110 руб.\nКрепкий Американо, 250мл - 130 руб.' + self.bd.cart_in_item(), chat_id=self.chat_id,
				message_id=self.message_id, reply_markup=amerikano_keyboard, parse_mode='HTML')
			else:
				bot.edit_message_text(
					'Американо - кофе по-американски, вода с эспрессо.\n------\nЦена:\nАмерикано, 250мл - 110 руб.\nКрепкий Американо, 250мл - 130 руб.',
					chat_id=self.chat_id,
					message_id=self.message_id, reply_markup=amerikano_keyboard)
		if self.call.data == 'latte':
			latte_keyboard = types.InlineKeyboardMarkup(row_width=1)
			l250 = types.InlineKeyboardButton('Латте 250мл', callback_data='latte250')
			l350 = types.InlineKeyboardButton('Латте 350мл', callback_data='latte350')
			l450 = types.InlineKeyboardButton('Латте 450мл', callback_data='latte450')
			back = types.InlineKeyboardButton('<- назад', callback_data='clas_cof')
			latte_keyboard.add(l250, l350, l450, back)
			if self.bd.test_cart() > 0:
				bot.edit_message_text('Латте - кофейный напиток на основе молока, представлющий собой смесь из молочной пенки, молока и эспрессо.\n------\nЦена:\n250мл - 140 руб.\n350мл - 160 руб.\n450мл - 180 руб' + self.bd.cart_in_item(), chat_id=self.chat_id, message_id=self.message_id,
				reply_markup=latte_keyboard, parse_mode='HTML')
			else:
				bot.edit_message_text(
				'Латте - кофейный напиток на основе молока, представлющий собой смесь из молочной пенки, молока и эспрессо.\n------\nЦена:\n250мл - 140 руб.\n350мл - 160 руб.\n450мл - 180 руб',
				chat_id=self.chat_id, message_id=self.message_id,
				reply_markup=latte_keyboard)
		if self.call.data == 'capuchino':
			capuchino_keyboard = types.InlineKeyboardMarkup(row_width=1)
			c250 = types.InlineKeyboardButton('Капучино 250мл', callback_data='capuchino250')
			c350 = types.InlineKeyboardButton('Капучино 350мл', callback_data='capuchino350')
			c450 = types.InlineKeyboardButton('Капучино 450мл', callback_data='capuchino450')
			back = types.InlineKeyboardButton('<- назад', callback_data='clas_cof')
			capuchino_keyboard.add(c250, c350, c450, back)
			if self.bd.test_cart() > 0:
				bot.edit_message_text('Капучино - кофейный напиток на основе эспрессо с добавлением в него подогретого вспененного молока.\n------\nЦена:\n250мл - 140 руб.\n350мл - 160 руб.\n450мл - 180 руб' + self.bd.cart_in_item(),
								  chat_id=self.chat_id, message_id=self.message_id,	reply_markup=capuchino_keyboard, parse_mode='HTML')
			else:
				bot.edit_message_text(
				'Капучино - кофейный напиток на основе эспрессо с добавлением в него подогретого вспененного молока.\n------\nЦена:\n250мл - 140 руб.\n350мл - 160 руб.\n450мл - 180 руб',
				chat_id=self.chat_id, message_id=self.message_id, reply_markup=capuchino_keyboard)
		if self.call.data == 'mokachino':
			mokachino_keyboard = types.InlineKeyboardMarkup(row_width=1)
			m250 = types.InlineKeyboardButton('Мокачино 250мл', callback_data='mokachino250')
			m350 = types.InlineKeyboardButton('Мокачино 350мл', callback_data='mokachino350')
			m450 = types.InlineKeyboardButton('Мокачино 450мл', callback_data='mokachino450')
			back = types.InlineKeyboardButton('<- назад', callback_data='clas_cof')
			mokachino_keyboard.add(m250, m350, m450, back)
			if self.bd.test_cart() > 0:
				bot.edit_message_text('Мокачино - кофейный напиток на основе эспрессо с растопленным в нём натуральным молочным шоколадом и добавленным в него подогретого вспененного молока.\n------\nЦена:\n250мл - 160 руб.\n350мл - 180 руб.\n450мл - 200 руб' + self.bd.cart_in_item(), chat_id=self.chat_id, message_id=self.message_id,
				reply_markup=mokachino_keyboard, parse_mode='HTML')
			else:
				bot.edit_message_text(
					'Мокачино - кофейный напиток на основе эспрессо с растопленным в нём натуральным молочным шоколадом и добавленным в него подогретого вспененного молока.\n------\nЦена:\n250мл - 160 руб.\n350мл - 180 руб.\n450мл - 200 руб',
					chat_id=self.chat_id, message_id=self.message_id, reply_markup=mokachino_keyboard, parse_mode='HTML')
		if self.call.data == 'raf':
			raf_keyboard = types.InlineKeyboardMarkup(row_width=1)
			raf350 = types.InlineKeyboardButton('Раф 350мл', callback_data='raf350')
			raf450 = types.InlineKeyboardButton('Раф 450мл', callback_data='raf450')
			back = types.InlineKeyboardButton('<- назад', callback_data='clas_cof')
			raf_keyboard.add(raf350, raf450, back)
			if self.bd.test_cart() > 0:
				bot.edit_message_text('Раф - нежнейший кофейный напиток, представляющий собой вспененную смесь из эспрессо и сливок.\n------\nЦена:\n350мл - 180 руб.\n450мл - 200 руб.' + self.bd.cart_in_item(),
								  chat_id=self.chat_id,	message_id=self.message_id, reply_markup=raf_keyboard, parse_mode='HTML')
			else:
				bot.edit_message_text(
					'Раф - нежнейший кофейный напиток, представляющий собой вспененную смесь из эспрессо и сливок.\n------\nЦена:\n350мл - 180 руб.\n450мл - 200 руб.',chat_id=self.chat_id, message_id=self.message_id, reply_markup=raf_keyboard, parse_mode='HTML')

		'''Кофейные зёрна'''
		if self.call.data == 'coffee':
			keyboard = types.InlineKeyboardMarkup(row_width=1)
			button_prime = types.InlineKeyboardButton('PRIME BLEND', callback_data='prime_blend')
			button_house = types.InlineKeyboardButton('HOUSE BLEND', callback_data='house_blend')
			button_candy = types.InlineKeyboardButton('CANDY BLEND', callback_data='candy_blend')
			button_back = types.InlineKeyboardButton('<- назад', callback_data='an_menu')
			keyboard.add(button_candy, button_prime, button_house, button_back)
			if self.bd.test_cart() > 0:
				bot.edit_message_text('Кофе свежей обжарки.\n------\nВ Candy Coffee, мы помолим зёрна именно под Ваш метод приготовления!' + self.bd.cart_in_item(),
								  chat_id=self.chat_id,	message_id=self.message_id, reply_markup=keyboard, parse_mode='HTML')
			else:
				bot.edit_message_text('Кофе свежей обжарки.\n------\nВ Candy Coffee, мы помолим зёрна именно под Ваш метод приготовления!',
								  chat_id=self.chat_id,	message_id=self.message_id, reply_markup=keyboard, parse_mode='HTML')

		'''Вода'''

		if self.call.data == 'water':
			keyboard = types.InlineKeyboardMarkup(row_width=1)
			button_still = types.InlineKeyboardButton(' + Вода негазированная', callback_data='still_water')
			button_soda = types.InlineKeyboardButton(' + Вода газированная', callback_data='soda_water')
			button_back = types.InlineKeyboardButton('<- назад', callback_data='an_menu')
			keyboard.add(button_still, button_soda, button_back)
			if self.bd.test_cart() > 0:
				bot.edit_message_text('Вода питьевая, 0,5л.\n------\nЦена: 30 руб.' + self.bd.cart_in_item(),
								  chat_id=self.chat_id,	message_id=self.message_id, reply_markup=keyboard, parse_mode='HTML')
			else:
				bot.edit_message_text('Вода питьевая, 0,5л.\n------\nЦена: 30 руб.',
								  chat_id=self.chat_id,	message_id=self.message_id, reply_markup=keyboard, parse_mode='HTML')

		'''Очистка корзины'''
		if self.call.data == 'clear_cart':
			c = cart_bd(self)
			c.clear_cart()
			keyboard = types.InlineKeyboardMarkup(row_width=1)
			back_mm = types.InlineKeyboardButton('Назад в меню', callback_data= 'main_menu')
			keyboard.add(back_mm)
			bot.edit_message_text('Корзина очищена', chat_id=self.chat_id, message_id=self.message_id,
					reply_markup=keyboard, parse_mode='HTML')
		'''Заказ'''
		if self.call.data == 'buy':
			order_status.setdefault(self.chat_id, True)
			keyboard = types.InlineKeyboardMarkup(row_width=1)
			timer_button = types.InlineKeyboardButton('По готовности', callback_data='buy_ready')
			back = types.InlineKeyboardButton('<- Назад', callback_data='cart')
			keyboard.add(timer_button, back)
			bot.edit_message_text('Мы почти готовим!\n😋\nУточните, пожалуйста через какое время напиток должен быть готов?\n__________________\n<i>*нажмите <b>по готовности</b>\nтак же вы можете написать через какое время или во сколько Вы хотели бы придти за напитком\n</i>', chat_id=self.chat_id, message_id=self.message_id,
					reply_markup=keyboard, parse_mode='HTML')

		if self.call.data == 'buy_ready':
			orstat = order_status_class(self.call, 'По готовности')
			orstat.buy_ready()

		if self.call.data == 'order_seen':
			pass

		if self.call.data == 'cart':
			try:
				order_comment.pop(self.chat_id)
				order_status.pop(self.chat_id)
			except KeyError: pass
			keyboard = types.InlineKeyboardMarkup(row_width=1)
			clear_cart = types.InlineKeyboardButton('Очистить корзину 🗑', callback_data='clear_cart')
			buy = types.InlineKeyboardButton('Заказать', callback_data='buy')
			comment = types.InlineKeyboardButton('Добавить комментарий', callback_data='comment')
			back_mm = types.InlineKeyboardButton('Назад в меню', callback_data='main_menu')
			c = cart_bd(self.call)
			show_cart = c.cart()
			if show_cart != False:
				keyboard.add(buy, comment, clear_cart, back_mm)
				bot.edit_message_text('{0}'.format(c.cart()),  chat_id=self.chat_id, message_id=self.message_id,
					reply_markup=keyboard, parse_mode='HTML')
			else:
				keyboard.add(back_mm)
				bot.edit_message_text('<b>Вы пока ничего не добавили в корзину :(</b>', chat_id=self.chat_id,
									  message_id=self.message_id, parse_mode='HTML', reply_markup=keyboard)

		if self.call.data == 'comment':
			order_comment.setdefault(self.chat_id, True)
			keyboard = types.InlineKeyboardMarkup(row_width=1)
			delete_com = types.InlineKeyboardButton('Удалить комментарий', callback_data='del_comment')
			back = types.InlineKeyboardButton('Назад в меню', callback_data='cart')
			c = cart_bd(self.call)
			show_cart = c.cart()
			if show_cart != False:
				keyboard.add(delete_com, back)
				bot.edit_message_text('Следующее сообщение будет записано в комментарий', chat_id=self.chat_id, message_id=self.message_id,
									  reply_markup=keyboard, parse_mode='HTML')
		'''Меню Candy Coffee'''
		if self.call.data == 'main_menu':
			menu_keyboard = types.InlineKeyboardMarkup(row_width=1)
			classic_coffee = types.InlineKeyboardButton('Класcический кофе', callback_data='clas_cof')
			author_coffee = types.InlineKeyboardButton('Авторский кофе', callback_data='aut_cof')
			summer_coffee = types.InlineKeyboardButton('Летние напитки', callback_data='sum_cof')
			anuwer = types.InlineKeyboardButton('Другое', callback_data='an_menu')
			menu_keyboard.add(classic_coffee, author_coffee, summer_coffee, anuwer)
			if self.bd.test_cart() > 0:
				bot.edit_message_text('* * * МЕНЮ Candy Coffee * * *' + self.bd.cart_in_item(),
									  chat_id=self.chat_id, message_id=self.message_id,
									  reply_markup=menu_keyboard, parse_mode='HTML')
			else:
				bot.edit_message_text('* * * МЕНЮ Candy Coffee * * *', chat_id=self.chat_id, message_id=self.message_id,
								  reply_markup=menu_keyboard)
