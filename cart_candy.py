# -*- coding : utf-8 -*-
import config
import telebot
from telebot import types
from order_candy import *
from dbase import *

bot = telebot.TeleBot(config.TOKEN)

items_dict = {'amerikano_ob': {'name':'Американо', 'back_b': 'amerikano'},
			  'amerikano_hard': {'name': 'Крепкий Американо', 'back_b': 'amerikano'},
			  'latte250': {'name': 'Латте 250мл', 'back_b': 'latte'},
			  'latte350': {'name': 'Латте 350мл', 'back_b': 'latte'},
			  'latte450': {'name': 'Латте 450мл', 'back_b': 'latte'},
			  'capuchino250': {'name': 'Капучино 250мл', 'back_b': 'capuchino'},
			  'capuchino350': {'name': 'Капучино 350мл', 'back_b': 'capuchino'},
			  'capuchino450': {'name': 'Капучино 450мл', 'back_b': 'capuchino'},
			  'mokachino250': {'name': 'Мокачино 250мл', 'back_b': 'mokachino'},
			  'mokachino350': {'name': 'Мокачино 350мл', 'back_b': 'mokachino'},
			  'mokachino450': {'name': 'Мокачино 450мл', 'back_b': 'mokachino'},
			  'raf350': {'name': 'Раф 350мл', 'back_b': 'raf'},
			  'raf450': {'name': 'Раф 450мл', 'back_b': 'raf'},
			  'espresso': {'name': 'Эспрессо', 'back_b': 'clas_cof'},
			  'grilyajik': {'name': 'Грильяжик', 'back_b': 'aut_cof'},
			  'shafutinya': {'name': 'Шафутиня', 'back_b': 'aut_cof'},
			  'chizulya': {'name': 'Чизуля', 'back_b': 'aut_cof'},
			  'pinoli': {'name': 'Пиноли', 'back_b': 'aut_cof'},
			  'sherif': {'name': 'Шериф', 'back_b': 'aut_cof'}
  }

items_summer = {'tropic': 'Смузи Tropic', 'stroinyashka': 'Смузи Стройняшка', 'yagodka': 'Смузи Ягодка',
				'mohito': 'Лимонад Мохито', 'kivi_myata': 'Лимонад Киви-Мята'}

items_summer_ws = {'milk_coct': 'Молочный коктейль',
				'ice_coffee': 'Ice Coffee'}

item_an_menu = {'sandwich': 'Сэндвич', 'prime_blend': 'PRIME BLEND', 'house_blend': 'HOUSE BLEND',
				'candy_blend': 'CANDY BLEND'}

class item_buttons:
	inside = 0
	key = None
	def __init__(self, call):
		for keyword in items_dict.keys():
			if keyword in call.data:
				self.key = keyword
		self.call = call
		self.call.data = call.data
		try:
			self.item = items_dict[self.call.data]['name']
			self.back_b = items_dict[self.call.data]['back_b']
		except KeyError:
			try:
				self.item = items_dict[self.key]['name']
				self.back_b = items_dict[self.key]['back_b']
			except KeyError as e:
				pass
		self.item_btns()

	def item_btns(self):
		if self.call.data in items_dict:
			message = callback_buttons(self.call, self.item, self.call.data, self.back_b)
			message.callback_item()
		if self.call.data == 'plus_{0}'.format(self.key):
			message = callback_buttons(self.call, self.item, self.key, self.back_b, '2')
			message.callback_plus()
		if self.call.data == 'plus_{0}2'.format(self.key):
			message = callback_buttons(self.call, self.item, self.key, self.back_b, '2')
			message.callback_plus()
		if self.call.data == 'minus_{0}'.format(self.key):
			message = callback_buttons(self.call, self.item, self.key, self.back_b, '2')
			message.callback_minus()
		if self.call.data == 'minus_{0}2'.format(self.key):
			message = callback_buttons(self.call, self.item, self.key, self.back_b)
			message.callback_minus()
		if self.call.data == 'in_cart_{0}'.format(self.key):
			in_cart = callback_buttons(self.call, self.item, self.key, self.back_b)
			in_cart.in_cart()
			bot.answer_callback_query(callback_query_id=self.call.call.id, text='Товар добавлен в корзину')
		if self.call.data == 'clear_cart_{0}'.format(self.key):
			clear_cart = callback_buttons(self.call, self.item, self.key, self.back_b)
			clear_cart.clear_cart()
			bot.answer_callback_query(callback_query_id=self.call.id, text='Товар убран из корзины')
		if self.call.data == 'additive_{0}'.format(self.key):
			dop = callback_buttons(self.call, self.item, self.key, self.back_b)
			dop.additive()
		if self.call.data == 'cinnamon_{0}'.format(self.key):
			dop = callback_buttons(self.call, self.item, self.key, self.back_b)
			dop.cinnamon()
		if self.call.data == 'chocolate_{0}'.format(self.key):
			dop = callback_buttons(self.call, self.item, self.key, self.back_b)
			dop.chocolate()
		if self.call.data == 'cheese_{0}'.format(self.key):
			dop = callback_buttons(self.call, self.item, self.key, self.back_b)
			dop.cheese()
		if self.call.data == 'sugar_{0}'.format(self.key):
			dop = callback_buttons(self.call, self.item, self.key, self.back_b)
			dop.sugar()
		if self.call.data == 'syrup_{0}'.format(self.key):
			dop = callback_buttons(self.call, self.item, self.key, self.back_b)
			dop.syrup()
		if self.call.data == 'drop_additive_{0}'.format(self.key):
			dop = callback_buttons(self.call, self.item, self.key, self.back_b)
			dop.drop_additive()

class item_an_buttons:
	inside = 0
	key = None

	def __init__(self, call):
		for keyword in item_an_menu.keys():
			if keyword in call.data:
				self.key = keyword
		self.call = call
		self.call.data = call.data
		try:
			self.item = item_an_menu[self.key]
			self.back_b = 'an_menu'
		except KeyError:
			pass
		self.item_btns()

	def item_btns(self):
		if self.call.data in item_an_menu:
			message = callback_buttons_an(self.call, self.item, self.call.data, self.back_b)
			message.callback_item()
		if self.call.data == 'plus_{0}'.format(self.key):
			message = callback_buttons_an(self.call, self.item, self.key, self.back_b, '2')
			message.callback_plus()
		if self.call.data == 'plus_{0}2'.format(self.key):
			message = callback_buttons_an(self.call, self.item, self.key, self.back_b, '2')
			message.callback_plus()
		if self.call.data == 'minus_{0}'.format(self.key):
			message = callback_buttons_an(self.call, self.item, self.key, self.back_b, '2')
			message.callback_minus()
		if self.call.data == 'minus_{0}2'.format(self.key):
			message = callback_buttons_an(self.call, self.item, self.key, self.back_b)
			message.callback_minus()
		if self.call.data == 'in_cart_{0}'.format(self.key):
			in_cart = callback_buttons_an(self.call, self.item, self.key, self.back_b)
			in_cart.in_cart()
			bot.answer_callback_query(callback_query_id=self.call.call.id, text='Товар добавлен в корзину')
		if self.call.data == 'clear_cart_{0}'.format(self.key):
			clear_cart = callback_buttons_an(self.call, self.item, self.key, self.back_b)
			clear_cart.clear_cart()
			bot.answer_callback_query(callback_query_id=self.call.id, text='Товар убран из корзины')

class item_summer_buttons:
	inside = 0
	key = None

	def __init__(self, call):
		for keyword in items_summer.keys():
			if keyword in call.data:
				self.key = keyword
		self.call = call
		self.call.data = call.data
		try:
			self.item = items_summer[self.key]
			self.back_b = 'sum_cof'
		except KeyError:
			try:
				self.item = items_summer[self.key]
				self.back_b = 'sum_cof'
			except KeyError as e:
				pass
		self.item_btns()

	def item_btns(self):
		if self.call.data in items_summer:
			message = callback_buttons_summer(self.call, self.item, self.call.data, self.back_b)
			message.callback_item()
		if self.call.data == 'plus_{0}'.format(self.key):
			message = callback_buttons_summer(self.call, self.item, self.key, self.back_b, '2')
			message.callback_plus()
		if self.call.data == 'plus_{0}2'.format(self.key):
			message = callback_buttons_summer(self.call, self.item, self.key, self.back_b, '2')
			message.callback_plus()
		if self.call.data == 'minus_{0}'.format(self.key):
			message = callback_buttons_summer(self.call, self.item, self.key, self.back_b, '2')
			message.callback_minus()
		if self.call.data == 'minus_{0}2'.format(self.key):
			message = callback_buttons_summer(self.call, self.item, self.key, self.back_b)
			message.callback_minus()
		if self.call.data == 'in_cart_{0}'.format(self.key):
			in_cart = callback_buttons_summer(self.call, self.item, self.key, self.back_b)
			in_cart.in_cart()
			bot.answer_callback_query(callback_query_id=self.call.call.id, text='Товар добавлен в корзину')
		if self.call.data == 'clear_cart_{0}'.format(self.key):
			clear_cart = callback_buttons_summer(self.call, self.item, self.key, self.back_b)
			clear_cart.clear_cart()
			bot.answer_callback_query(callback_query_id=self.call.id, text='Товар убран из корзины')

class item_summer_buttons_ws:
	inside = 0
	key = None

	def __init__(self, call):
		for keyword in items_summer_ws.keys():
			if keyword in call.data:
				self.key = keyword
		self.call = call
		self.call.data = call.data
		try:
			self.item = items_summer_ws[self.key]
			self.back_b = 'sum_cof'
		except KeyError:
			try:
				self.item = items_summer_ws[self.key]
				self.back_b = 'sum_cof'
			except KeyError as e:
				pass
		self.item_btns()

	def item_btns(self):
		if self.call.data in items_summer_ws:
			message = callback_buttons_summer_ws(self.call, self.item, self.call.data, self.back_b)
			message.callback_item()
		if self.call.data == 'plus_{0}'.format(self.key):
			message = callback_buttons_summer_ws(self.call, self.item, self.key, self.back_b, '2')
			message.callback_plus()
		if self.call.data == 'plus_{0}2'.format(self.key):
			message = callback_buttons_summer_ws(self.call, self.item, self.key, self.back_b, '2')
			message.callback_plus()
		if self.call.data == 'minus_{0}'.format(self.key):
			message = callback_buttons_summer_ws(self.call, self.item, self.key, self.back_b, '2')
			message.callback_minus()
		if self.call.data == 'minus_{0}2'.format(self.key):
			message = callback_buttons_summer_ws(self.call, self.item, self.key, self.back_b)
			message.callback_minus()
		if self.call.data == 'in_cart_{0}'.format(self.key):
			in_cart = callback_buttons_summer_ws(self.call, self.item, self.key, self.back_b)
			in_cart.in_cart()
			bot.answer_callback_query(callback_query_id=self.call.call.id, text='Товар добавлен в корзину')
		if self.call.data == 'clear_cart_{0}'.format(self.key):
			clear_cart = callback_buttons_summer_ws(self.call, self.item, self.key, self.back_b)
			clear_cart.clear_cart()
			bot.answer_callback_query(callback_query_id=self.call.id, text='Товар убран из корзины')
		if self.call.data == 'syrup_{0}'.format(self.key):
			message = callback_buttons_summer_ws(self.call, self.item, self.key, self.back_b)
			message.syrup()

class callback_buttons:
	value = []
	text_order = '\n______\nЦена:\n{0} руб.\n______\nСумма: {1} руб.'
	text_price = '\n__________\nЦена: {0} руб.'
	def __init__(self, call, key, dicorate_key, back_call, dico2= ''):
		self.call = call
		try:
			self.chat_id = self.call.chat_id
		except AttributeError:
			self.chat_id = self.call.from_user.id
		try:
			self.message_id = self.call.message_id
		except AttributeError:
			self.message_id = self.call.message.id
		self.key = key
		self.d_key = dicorate_key
		self.back = back_call
		self.d_key2 = dico2
		self.price = item_catalog[self.key]['price']
		self.title = item_catalog[self.key]['title']
		self.description = item_catalog[self.key]['description']

	def callback_item(self):
		bd = cart_bd(self)
		c = bd.count_item_in_cart(self.key)
		cart_keyboard = types.InlineKeyboardMarkup(row_width=3)
		value = types.InlineKeyboardButton('☕ {0} ед.'.format(str(c)), callback_data='value')
		minus = types.InlineKeyboardButton('-1', callback_data='minus_{0}'.format(self.d_key))
		plus = types.InlineKeyboardButton('+1', callback_data='plus_{0}'.format(self.d_key))
		uppend_cart = types.InlineKeyboardButton('Добавить в корзину', callback_data='plus_{0}'.format(self.d_key))
		clear_cart = types.InlineKeyboardButton('Убрать из корзины', callback_data='clear_cart_{0}'.format(self.d_key))
		back_button = types.InlineKeyboardButton('<- назад', callback_data='{0}'.format(self.back))
		additive = types.InlineKeyboardButton('Добавки в напиток', callback_data='additive_{0}'.format(self.d_key))

		if bd.count_item_in_cart(self.key) > 0:
			cart_keyboard.add(minus, value, plus)
			cart_keyboard.add(additive, clear_cart, back_button, row_width=1)
			bot.edit_message_text('<u>' + self.title + '</u>' + '\n' + self.description + self.text_price.format(self.price)
								  + bd.cart_in_item(),	chat_id=self.chat_id, message_id=self.message_id,
								  reply_markup=cart_keyboard, parse_mode='HTML')
		if bd.count_item_in_cart(self.key) == 0:
			if bd.test_cart() > 0:
				cart_keyboard.add(uppend_cart, back_button, row_width=1)
				bot.edit_message_text(
						'<u>' + self.title + '</u>' + '\n' + self.description + self.text_price.format(self.price) + bd.cart_in_item(), chat_id=self.chat_id, message_id=self.message_id,
						reply_markup=cart_keyboard, parse_mode='HTML')
			else:
				cart_keyboard.add(uppend_cart, back_button, row_width=1)
				bot.edit_message_text(
						'<u>' + self.title + '</u>' + '\n' + self.description + self.text_price.format(
							self.price), chat_id=self.chat_id, message_id=self.message_id,
						reply_markup=cart_keyboard, parse_mode='HTML')

	def callback_plus(self):
		bd = cart_bd(self)
		if self.chat_id not in order:
			order.setdefault(self.chat_id, [self.key])
		else:
			order[self.chat_id].append(self.key)
		bd.in_cart_bd(self.key,bd.count_item_in_cart(self.key)+1)
		c = bd.count_item_in_cart(self.key)
		cart_keyboard = types.InlineKeyboardMarkup(row_width=3)
		value = types.InlineKeyboardButton('☕ {0} ед.'.format(str(c)), callback_data='value')
		minus = types.InlineKeyboardButton('-1', callback_data='minus_{0}'.format(self.d_key))
		plus = types.InlineKeyboardButton('+1', callback_data='plus_{0}{1}'.format(self.d_key, self.d_key2))
		in_cart = types.InlineKeyboardButton('Добавить в корзину', callback_data='in_cart_{0}'.format(self.d_key))
		additive = types.InlineKeyboardButton('Добавки в напиток', callback_data='additive_{0}'.format(self.d_key))
		clear_cart = types.InlineKeyboardButton('Убрать из корзины', callback_data='clear_cart_{0}'.format(self.d_key))
		back_button = types.InlineKeyboardButton('<- назад', callback_data='{0}'.format(self.back))
		if c > 0:
			cart_keyboard.add(minus, value, plus)
			cart_keyboard.add(additive, clear_cart, back_button, row_width=1)
			bot.edit_message_text('<u>' + self.title + '</u>' + '\n' + self.description + self.text_price.format(self.price) + bd.cart_in_item(),	chat_id=self.chat_id, message_id=self.message_id,
								  reply_markup=cart_keyboard, parse_mode='HTML')
		else:
			cart_keyboard.add(in_cart, back_button, row_width=1)
			bot.edit_message_text(
					'<u>' + self.title + '</u><b><i> ' + 'x ' + str(c) + ' ед.' + '</i></b>' + '\n' + self.description + self.text_price.format(self.price),
					chat_id=self.chat_id, message_id=self.message_id, reply_markup=cart_keyboard, parse_mode='HTML')

	def callback_minus(self):
		bd = cart_bd(self)
		count = None
		if bd.count_item_in_cart(self.key) > 0:
			count = bd.count_item_in_cart(self.key) - 1
			if count == 0:
				self.clear_cart()
				self.callback_item()
		cart_keyboard = types.InlineKeyboardMarkup(row_width=3)
		value = types.InlineKeyboardButton('☕ {0} ед.'.format(count), callback_data='value')
		minus = types.InlineKeyboardButton('-1', callback_data='minus_{0}{1}'.format(self.d_key, self.d_key2))
		plus = types.InlineKeyboardButton('+1', callback_data='plus_{0}'.format(self.d_key))
		in_cart = types.InlineKeyboardButton('Добавить в корзину', callback_data='in_cart_{0}'.format(self.d_key))
		additive = types.InlineKeyboardButton('Добавки в напиток', callback_data='additive_{0}'.format(self.d_key))
		clear_cart = types.InlineKeyboardButton('Убрать из корзины', callback_data='clear_cart_{0}'.format(self.d_key))
		back_button = types.InlineKeyboardButton('<- назад', callback_data='{0}'.format(self.back))
		cart_keyboard.add(minus, value, plus)
		if bd.test_cart() > 0:
			if bd.count_item_in_cart(self.key) > 0:
				bd.in_cart_bd(self.key, bd.count_item_in_cart(self.key) - 1)
				if bd.count_item_in_cart(self.key) == 0:
					self.clear_cart()
				cart_keyboard.add(additive, clear_cart, back_button, row_width=1)
				bot.edit_message_text('<u>' + self.title + '</u>' + '\n' + self.description + self.text_price.format(self.price)
									  + bd.cart_in_item(),	chat_id=self.chat_id, message_id=self.message_id,
									  reply_markup=cart_keyboard, parse_mode='HTML')
		else:
			self.callback_item()

	def in_cart(self):
		cart = cart_bd(self.call)
		cart.in_cart_bd(self.key, count(self.chat_id, self.key))
		c = cart.count_item_in_cart(self.key)
		cart_keyboard = types.InlineKeyboardMarkup(row_width=3)
		value = types.InlineKeyboardButton('☕ {0} ед.'.format(c), callback_data='value')
		minus = types.InlineKeyboardButton('-1', callback_data='minus_{0}{1}'.format(self.d_key, self.d_key2))
		plus = types.InlineKeyboardButton('+1', callback_data='plus_{0}'.format(self.d_key))
		clear_cart = types.InlineKeyboardButton('Убрать из корзины', callback_data='clear_cart_{0}'.format(self.d_key))
		additive = types.InlineKeyboardButton('Добавки в напиток', callback_data='additive_{0}'.format(self.d_key))
		back_button = types.InlineKeyboardButton('<- назад', callback_data='{0}'.format(self.back))
		cart_keyboard.add(minus, value, plus)
		cart_keyboard.add(additive, clear_cart, back_button, row_width=1)
		bot.edit_message_text('<u>' + self.title + '</u>' + '\n' + self.description + self.text_price.format(self.price) + cart.cart_in_item()
							  , chat_id=self.chat_id, message_id=self.call.message_id,
							  reply_markup=cart_keyboard, parse_mode='HTML')

	def clear_cart(self):
		try:
			for l in reversed(range(len(order[self.chat_id]))):
				if order[self.chat_id][l] == self.key:
					order[self.chat_id].pop(l)
		except KeyError: pass
		c = cart_bd(self)
		c.clear_cart_item(self.key)
		self.callback_item()

	def additive(self):
		bd = cart_bd(self)
		cart_keyboard = types.InlineKeyboardMarkup(row_width=3)
		chocolate = types.InlineKeyboardButton('Шоколад', callback_data='chocolate_{0}'.format(self.d_key))
		cheese = types.InlineKeyboardButton('Сыр', callback_data='cheese_{0}'.format(self.d_key, self.d_key2))
		syrup = types.InlineKeyboardButton('Сироп', callback_data='syrup_{0}'.format(self.d_key))
		cinnamon = types.InlineKeyboardButton('Корица', callback_data='cinnamon_{0}'.format(self.d_key))
		sugar = types.InlineKeyboardButton('Сахар', callback_data='sugar_{0}'.format(self.d_key))
		back_button = types.InlineKeyboardButton('<- назад', callback_data='{0}'.format(self.d_key))
		drop_additive = types.InlineKeyboardButton('Убрать добавки 🗑️', callback_data='drop_additive_{0}'.format(self.d_key))
		cart_keyboard.add(chocolate, cheese, syrup)
		cart_keyboard.add(cinnamon, sugar, row_width=2)
		cart_keyboard.add(drop_additive, back_button, row_width=1)
		bot.edit_message_text('Выберите желаемую добавку к напитку:' + '\n' + bd.cart_in_item(), chat_id=self.chat_id, message_id=self.message_id,
							  reply_markup=cart_keyboard, parse_mode='HTML')

	def drop_additive(self):
		bd = cart_bd(self)
		bd.drop_additive(self.key)
		self.additive()

	def cinnamon(self):
		bd = cart_bd(self)
		bd.cinnamon(self.key)
		self.additive()

	def chocolate(self):
		bd = cart_bd(self)
		bd.chocolate(self.key)
		self.additive()

	def cheese(self):
		bd = cart_bd(self)
		bd.cheese(self.key)
		self.additive()

	def sugar(self):
		bd = cart_bd(self)
		bd.sugar(self.key)
		self.additive()

	def syrup(self):
		bd = cart_bd(self)
		cart_keyboard = types.InlineKeyboardMarkup(row_width=1)
		back_button = types.InlineKeyboardButton('<- назад', callback_data='additive_{0}'.format(self.d_key))
		cart_keyboard.add(back_button, row_width=1)
		order_syrup_status.setdefault(self.chat_id, True)
		order_syrup.setdefault(self.chat_id, {'call': self.call, 'key': self.key, 'd_key': self.d_key, 'back': self.back})
		bot.edit_message_text('\n<b>Напишите вкус сиропа.</b>\n<i>Если такого сиропа не будет, бариста Вам сообщит о других, похожих вкусах)</i>' + '\n' + bd.cart_in_item() + '', chat_id=self.chat_id, message_id=self.message_id,
							  reply_markup=cart_keyboard, parse_mode='HTML')

class callback_buttons_an:
	value = []
	text_order = '\n------\nЦена:\n{0} руб.\n------\nСумма: {1} руб.'
	text_price = '\n------\nЦена: {0} руб.'
	def __init__(self, call, key, dicorate_key, back_call, dico2= ''):
		self.call = call
		try:
			self.chat_id = self.call.chat_id
		except AttributeError:
			self.chat_id = self.call.from_user.id
		try:
			self.message_id = self.call.message_id
		except AttributeError:
			self.message_id = self.call.message.id
		self.key = key
		self.d_key = dicorate_key
		self.back = back_call
		self.d_key2 = dico2
		self.price = item_catalog[self.key]['price']
		self.title = item_catalog[self.key]['title']
		self.description = item_catalog[self.key]['description']

	def callback_item(self):
		bd = cart_bd(self)
		c = bd.count_item_in_cart(self.key)
		cart_keyboard = types.InlineKeyboardMarkup(row_width=3)
		value = types.InlineKeyboardButton('☕ {0} ед.'.format(str(c)), callback_data='value')
		minus = types.InlineKeyboardButton('-1', callback_data='minus_{0}'.format(self.d_key))
		plus = types.InlineKeyboardButton('+1', callback_data='plus_{0}'.format(self.d_key))
		uppend_cart = types.InlineKeyboardButton('Добавить в корзину', callback_data='plus_{0}'.format(self.d_key))
		clear_cart = types.InlineKeyboardButton('Убрать из корзины', callback_data='clear_cart_{0}'.format(self.d_key))
		back_button = types.InlineKeyboardButton('<- назад', callback_data='{0}'.format(self.back))

		if bd.count_item_in_cart(self.key) > 0:
			cart_keyboard.add(minus, value, plus)
			cart_keyboard.add(clear_cart, back_button, row_width=1)
			bot.edit_message_text('<u>' + self.title + '</u>' + '\n' + self.description + self.text_price.format(self.price)
								  + bd.cart_in_item(),	chat_id=self.chat_id, message_id=self.message_id,
								  reply_markup=cart_keyboard, parse_mode='HTML')
		if bd.count_item_in_cart(self.key) == 0:
			if bd.test_cart() > 0:
				cart_keyboard.add(uppend_cart, back_button, row_width=1)
				bot.edit_message_text(
						'<u>' + self.title + '</u>' + '\n' + self.description + self.text_price.format(self.price) + bd.cart_in_item(), chat_id=self.chat_id, message_id=self.message_id,
						reply_markup=cart_keyboard, parse_mode='HTML')
			else:
				cart_keyboard.add(uppend_cart, back_button, row_width=1)
				bot.edit_message_text(
						'<u>' + self.title + '</u>' + '\n' + self.description + self.text_price.format(
							self.price), chat_id=self.chat_id, message_id=self.message_id,
						reply_markup=cart_keyboard, parse_mode='HTML')

	def callback_plus(self):
		bd = cart_bd(self)
		if self.chat_id not in order:
			order.setdefault(self.chat_id, [self.key])
		else:
			order[self.chat_id].append(self.key)
		bd.in_cart_bd(self.key,bd.count_item_in_cart(self.key)+1)
		c = bd.count_item_in_cart(self.key)
		cart_keyboard = types.InlineKeyboardMarkup(row_width=3)
		value = types.InlineKeyboardButton('☕ {0} ед.'.format(str(c)), callback_data='value')
		minus = types.InlineKeyboardButton('-1', callback_data='minus_{0}'.format(self.d_key))
		plus = types.InlineKeyboardButton('+1', callback_data='plus_{0}{1}'.format(self.d_key, self.d_key2))
		in_cart = types.InlineKeyboardButton('Добавить в корзину', callback_data='in_cart_{0}'.format(self.d_key))
		clear_cart = types.InlineKeyboardButton('Убрать из корзины', callback_data='clear_cart_{0}'.format(self.d_key))
		back_button = types.InlineKeyboardButton('<- назад', callback_data='{0}'.format(self.back))
		if c > 0:
			cart_keyboard.add(minus, value, plus)
			cart_keyboard.add(clear_cart, back_button, row_width=1)
			bot.edit_message_text('<u>' + self.title + '</u>' + '\n' + self.description + self.text_price.format(self.price) + bd.cart_in_item(),	chat_id=self.chat_id, message_id=self.message_id,
								  reply_markup=cart_keyboard, parse_mode='HTML')
		else:
			cart_keyboard.add(in_cart, back_button, row_width=1)
			bot.edit_message_text(
					'<u>' + self.title + '</u><b><i> ' + 'x ' + str(c) + ' ед.' + '</i></b>' + '\n' + self.description + self.text_price.format(self.price),
					chat_id=self.chat_id, message_id=self.message_id, reply_markup=cart_keyboard, parse_mode='HTML')

	def callback_minus(self):
		bd = cart_bd(self)
		count = None
		if bd.count_item_in_cart(self.key) > 0:
			count = bd.count_item_in_cart(self.key) - 1
			if count == 0:
				self.clear_cart()
				self.callback_item()
		cart_keyboard = types.InlineKeyboardMarkup(row_width=3)
		value = types.InlineKeyboardButton('☕ {0} ед.'.format(count), callback_data='value')
		minus = types.InlineKeyboardButton('-1', callback_data='minus_{0}{1}'.format(self.d_key, self.d_key2))
		plus = types.InlineKeyboardButton('+1', callback_data='plus_{0}'.format(self.d_key))
		in_cart = types.InlineKeyboardButton('Добавить в корзину', callback_data='in_cart_{0}'.format(self.d_key))
		clear_cart = types.InlineKeyboardButton('Убрать из корзины', callback_data='clear_cart_{0}'.format(self.d_key))
		back_button = types.InlineKeyboardButton('<- назад', callback_data='{0}'.format(self.back))
		cart_keyboard.add(minus, value, plus)
		if bd.test_cart() > 0:
			if bd.count_item_in_cart(self.key) > 0:
				bd.in_cart_bd(self.key, bd.count_item_in_cart(self.key) - 1)
				if bd.count_item_in_cart(self.key) == 0:
					self.clear_cart()
				cart_keyboard.add(clear_cart, back_button, row_width=1)
				bot.edit_message_text('<u>' + self.title + '</u>' + '\n' + self.description + self.text_price.format(self.price)
									  + bd.cart_in_item(),	chat_id=self.chat_id, message_id=self.message_id,
									  reply_markup=cart_keyboard, parse_mode='HTML')
		else:
			self.callback_item()

	def in_cart(self):
		cart = cart_bd(self.call)
		cart.in_cart_bd(self.key, count(self.chat_id, self.key))
		c = cart.count_item_in_cart(self.key)
		cart_keyboard = types.InlineKeyboardMarkup(row_width=3)
		value = types.InlineKeyboardButton('☕ {0} ед.'.format(c), callback_data='value')
		minus = types.InlineKeyboardButton('-1', callback_data='minus_{0}{1}'.format(self.d_key, self.d_key2))
		plus = types.InlineKeyboardButton('+1', callback_data='plus_{0}'.format(self.d_key))
		clear_cart = types.InlineKeyboardButton('Убрать из корзины', callback_data='clear_cart_{0}'.format(self.d_key))
		back_button = types.InlineKeyboardButton('<- назад', callback_data='{0}'.format(self.back))
		cart_keyboard.add(minus, value, plus)
		cart_keyboard.add(clear_cart, back_button, row_width=1)
		bot.edit_message_text('<u>' + self.title + '</u>' + '\n' + self.description + self.text_price.format(self.price) + cart.cart_in_item()
							  , chat_id=self.chat_id, message_id=self.call.message_id,
							  reply_markup=cart_keyboard, parse_mode='HTML')

	def clear_cart(self):
		try:
			for l in reversed(range(len(order[self.chat_id]))):
				if order[self.chat_id][l] == self.key:
					order[self.chat_id].pop(l)
		except KeyError: pass
		c = cart_bd(self)
		c.clear_cart_item(self.key)
		self.callback_item()


class callback_buttons_summer:
	value = []
	text_order = '\n------\nЦена:\n{0} руб.\n------\nСумма: {1} руб.'
	text_price = '\n------\nЦена: {0} руб.'
	def __init__(self, call, key, dicorate_key, back_call, dico2= ''):
		self.call = call
		try:
			self.chat_id = self.call.chat_id
		except AttributeError:
			self.chat_id = self.call.from_user.id
		try:
			self.message_id = self.call.message_id
		except AttributeError:
			self.message_id = self.call.message.id
		self.key = key
		self.d_key = dicorate_key
		self.back = back_call
		self.d_key2 = dico2
		self.price = item_catalog[self.key]['price']
		self.title = item_catalog[self.key]['title']
		self.description = item_catalog[self.key]['description']

	def callback_item(self):
		bd = cart_bd(self)
		c = bd.count_item_in_cart(self.key)
		cart_keyboard = types.InlineKeyboardMarkup(row_width=3)
		value = types.InlineKeyboardButton('☕ {0} ед.'.format(str(c)), callback_data='value')
		minus = types.InlineKeyboardButton('-1', callback_data='minus_{0}'.format(self.d_key))
		plus = types.InlineKeyboardButton('+1', callback_data='plus_{0}'.format(self.d_key))
		uppend_cart = types.InlineKeyboardButton('Добавить в корзину', callback_data='plus_{0}'.format(self.d_key))
		clear_cart = types.InlineKeyboardButton('Убрать из корзины', callback_data='clear_cart_{0}'.format(self.d_key))
		back_button = types.InlineKeyboardButton('<- назад', callback_data='{0}'.format(self.back))

		if bd.count_item_in_cart(self.key) > 0:
			cart_keyboard.add(minus, value, plus)
			cart_keyboard.add(clear_cart, back_button, row_width=1)
			bot.edit_message_text('<u>' + self.title + '</u>' + '\n' + self.description + self.text_price.format(self.price)
								  + bd.cart_in_item(),	chat_id=self.chat_id, message_id=self.message_id,
								  reply_markup=cart_keyboard, parse_mode='HTML')
		if bd.count_item_in_cart(self.key) == 0:
			if bd.test_cart() > 0:
				cart_keyboard.add(uppend_cart, back_button, row_width=1)
				bot.edit_message_text(
						'<u>' + self.title + '</u>' + '\n' + self.description + self.text_price.format(self.price) + bd.cart_in_item(), chat_id=self.chat_id, message_id=self.message_id,
						reply_markup=cart_keyboard, parse_mode='HTML')
			else:
				cart_keyboard.add(uppend_cart, back_button, row_width=1)
				bot.edit_message_text(
						'<u>' + self.title + '</u>' + '\n' + self.description + self.text_price.format(
							self.price), chat_id=self.chat_id, message_id=self.message_id,
						reply_markup=cart_keyboard, parse_mode='HTML')

	def callback_plus(self):
		bd = cart_bd(self)
		if self.chat_id not in order:
			order.setdefault(self.chat_id, [self.key])
		else:
			order[self.chat_id].append(self.key)
		bd.in_cart_bd(self.key,bd.count_item_in_cart(self.key)+1)
		c = bd.count_item_in_cart(self.key)
		cart_keyboard = types.InlineKeyboardMarkup(row_width=3)
		value = types.InlineKeyboardButton('☕ {0} ед.'.format(str(c)), callback_data='value')
		minus = types.InlineKeyboardButton('-1', callback_data='minus_{0}'.format(self.d_key))
		plus = types.InlineKeyboardButton('+1', callback_data='plus_{0}{1}'.format(self.d_key, self.d_key2))
		in_cart = types.InlineKeyboardButton('Добавить в корзину', callback_data='in_cart_{0}'.format(self.d_key))
		clear_cart = types.InlineKeyboardButton('Убрать из корзины', callback_data='clear_cart_{0}'.format(self.d_key))
		back_button = types.InlineKeyboardButton('<- назад', callback_data='{0}'.format(self.back))
		if c > 0:
			cart_keyboard.add(minus, value, plus)
			cart_keyboard.add(clear_cart, back_button, row_width=1)
			bot.edit_message_text('<u>' + self.title + '</u>' + '\n' + self.description + self.text_price.format(self.price) + bd.cart_in_item(),	chat_id=self.chat_id, message_id=self.message_id,
								  reply_markup=cart_keyboard, parse_mode='HTML')
		else:
			cart_keyboard.add(in_cart, back_button, row_width=1)
			bot.edit_message_text(
					'<u>' + self.title + '</u><b><i> ' + 'x ' + str(c) + ' ед.' + '</i></b>' + '\n' + self.description + self.text_price.format(self.price),
					chat_id=self.chat_id, message_id=self.message_id, reply_markup=cart_keyboard, parse_mode='HTML')

	def callback_minus(self):
		bd = cart_bd(self)
		count = None
		if bd.count_item_in_cart(self.key) > 0:
			count = bd.count_item_in_cart(self.key) - 1
			if count == 0:
				self.clear_cart()
				self.callback_item()
		cart_keyboard = types.InlineKeyboardMarkup(row_width=3)
		value = types.InlineKeyboardButton('☕ {0} ед.'.format(count), callback_data='value')
		minus = types.InlineKeyboardButton('-1', callback_data='minus_{0}{1}'.format(self.d_key, self.d_key2))
		plus = types.InlineKeyboardButton('+1', callback_data='plus_{0}'.format(self.d_key))
		in_cart = types.InlineKeyboardButton('Добавить в корзину', callback_data='in_cart_{0}'.format(self.d_key))
		clear_cart = types.InlineKeyboardButton('Убрать из корзины', callback_data='clear_cart_{0}'.format(self.d_key))
		back_button = types.InlineKeyboardButton('<- назад', callback_data='{0}'.format(self.back))
		cart_keyboard.add(minus, value, plus)
		if bd.test_cart() > 0:
			if bd.count_item_in_cart(self.key) > 0:
				bd.in_cart_bd(self.key, bd.count_item_in_cart(self.key) - 1)
				if bd.count_item_in_cart(self.key) == 0:
					self.clear_cart()
				cart_keyboard.add(clear_cart, back_button, row_width=1)
				bot.edit_message_text('<u>' + self.title + '</u>' + '\n' + self.description + self.text_price.format(self.price)
									  + bd.cart_in_item(),	chat_id=self.chat_id, message_id=self.message_id,
									  reply_markup=cart_keyboard, parse_mode='HTML')
		else:
			self.callback_item()

	def in_cart(self):
		cart = cart_bd(self.call)
		cart.in_cart_bd(self.key, count(self.chat_id, self.key))
		c = cart.count_item_in_cart(self.key)
		cart_keyboard = types.InlineKeyboardMarkup(row_width=3)
		value = types.InlineKeyboardButton('☕ {0} ед.'.format(c), callback_data='value')
		minus = types.InlineKeyboardButton('-1', callback_data='minus_{0}{1}'.format(self.d_key, self.d_key2))
		plus = types.InlineKeyboardButton('+1', callback_data='plus_{0}'.format(self.d_key))
		clear_cart = types.InlineKeyboardButton('Убрать из корзины', callback_data='clear_cart_{0}'.format(self.d_key))
		back_button = types.InlineKeyboardButton('<- назад', callback_data='{0}'.format(self.back))
		cart_keyboard.add(minus, value, plus)
		cart_keyboard.add(clear_cart, back_button, row_width=1)
		bot.edit_message_text('<u>' + self.title + '</u>' + '\n' + self.description + self.text_price.format(self.price) + cart.cart_in_item()
							  , chat_id=self.chat_id, message_id=self.call.message_id,
							  reply_markup=cart_keyboard, parse_mode='HTML')

	def clear_cart(self):
		try:
			for l in reversed(range(len(order[self.chat_id]))):
				if order[self.chat_id][l] == self.key:
					order[self.chat_id].pop(l)
		except KeyError: pass
		c = cart_bd(self)
		c.clear_cart_item(self.key)
		self.callback_item()

class callback_buttons_summer_ws:
	value = []
	text_order = '\n------\nЦена:\n{0} руб.\n------\nСумма: {1} руб.'
	text_price = '\n------\nЦена: {0} руб.'
	def __init__(self, call, key, dicorate_key, back_call, dico2= ''):
		self.call = call
		try:
			self.chat_id = self.call.chat_id
		except AttributeError:
			self.chat_id = self.call.from_user.id
		try:
			self.message_id = self.call.message_id
		except AttributeError:
			self.message_id = self.call.message.id
		self.key = key
		self.d_key = dicorate_key
		self.back = back_call
		self.d_key2 = dico2
		self.price = item_catalog[self.key]['price']
		self.title = item_catalog[self.key]['title']
		self.description = item_catalog[self.key]['description']

	def callback_item(self):
		bd = cart_bd(self)
		c = bd.count_item_in_cart(self.key)
		cart_keyboard = types.InlineKeyboardMarkup(row_width=3)
		value = types.InlineKeyboardButton('☕ {0} ед.'.format(str(c)), callback_data='value')
		minus = types.InlineKeyboardButton('-1', callback_data='minus_{0}'.format(self.d_key))
		plus = types.InlineKeyboardButton('+1', callback_data='plus_{0}'.format(self.d_key))
		plus_syrup = types.InlineKeyboardButton('Добавить сироп', callback_data='syrup_{0}'.format(self.d_key))
		uppend_cart = types.InlineKeyboardButton('Добавить в корзину', callback_data='plus_{0}'.format(self.d_key))
		clear_cart = types.InlineKeyboardButton('Убрать из корзины', callback_data='clear_cart_{0}'.format(self.d_key))
		back_button = types.InlineKeyboardButton('<- назад', callback_data='{0}'.format(self.back))

		if bd.count_item_in_cart(self.key) > 0:
			cart_keyboard.add(minus, value, plus)
			cart_keyboard.add(plus_syrup, clear_cart, back_button, row_width=1)
			bot.edit_message_text('<u>' + self.title + '</u>' + '\n' + self.description + self.text_price.format(self.price)
								  + bd.cart_in_item(),	chat_id=self.chat_id, message_id=self.message_id,
								  reply_markup=cart_keyboard, parse_mode='HTML')
		if bd.count_item_in_cart(self.key) == 0:
			if bd.test_cart() > 0:
				cart_keyboard.add(uppend_cart, back_button, row_width=1)
				bot.edit_message_text(
						'<u>' + self.title + '</u>' + '\n' + self.description + self.text_price.format(self.price) + bd.cart_in_item(), chat_id=self.chat_id, message_id=self.message_id,
						reply_markup=cart_keyboard, parse_mode='HTML')
			else:
				cart_keyboard.add(uppend_cart, back_button, row_width=1)
				bot.edit_message_text(
						'<u>' + self.title + '</u>' + '\n' + self.description + self.text_price.format(
							self.price), chat_id=self.chat_id, message_id=self.message_id,
						reply_markup=cart_keyboard, parse_mode='HTML')

	def callback_plus(self):
		bd = cart_bd(self)
		if self.chat_id not in order:
			order.setdefault(self.chat_id, [self.key])
		else:
			order[self.chat_id].append(self.key)
		bd.in_cart_bd(self.key,bd.count_item_in_cart(self.key)+1)
		c = bd.count_item_in_cart(self.key)
		cart_keyboard = types.InlineKeyboardMarkup(row_width=3)
		value = types.InlineKeyboardButton('☕ {0} ед.'.format(str(c)), callback_data='value')
		minus = types.InlineKeyboardButton('-1', callback_data='minus_{0}'.format(self.d_key))
		plus = types.InlineKeyboardButton('+1', callback_data='plus_{0}{1}'.format(self.d_key, self.d_key2))
		plus_syrup = types.InlineKeyboardButton('Добавить сироп', callback_data='syrup_{0}'.format(self.d_key))
		in_cart = types.InlineKeyboardButton('Добавить в корзину', callback_data='in_cart_{0}'.format(self.d_key))
		clear_cart = types.InlineKeyboardButton('Убрать из корзины', callback_data='clear_cart_{0}'.format(self.d_key))
		back_button = types.InlineKeyboardButton('<- назад', callback_data='{0}'.format(self.back))
		if c > 0:
			cart_keyboard.add(minus, value, plus)
			cart_keyboard.add(plus_syrup, clear_cart, back_button, row_width=1)
			bot.edit_message_text('<u>' + self.title + '</u>' + '\n' + self.description + self.text_price.format(self.price) + bd.cart_in_item(),	chat_id=self.chat_id, message_id=self.message_id,
								  reply_markup=cart_keyboard, parse_mode='HTML')
		else:
			cart_keyboard.add(in_cart, back_button, row_width=1)
			bot.edit_message_text(
					'<u>' + self.title + '</u><b><i> ' + 'x ' + str(c) + ' ед.' + '</i></b>' + '\n' + self.description + self.text_price.format(self.price),
					chat_id=self.chat_id, message_id=self.message_id, reply_markup=cart_keyboard, parse_mode='HTML')

	def callback_minus(self):
		bd = cart_bd(self)
		count = None
		if bd.count_item_in_cart(self.key) > 0:
			count = bd.count_item_in_cart(self.key) - 1
			if count == 0:
				self.clear_cart()
				self.callback_item()
		cart_keyboard = types.InlineKeyboardMarkup(row_width=3)
		value = types.InlineKeyboardButton('☕ {0} ед.'.format(count), callback_data='value')
		minus = types.InlineKeyboardButton('-1', callback_data='minus_{0}{1}'.format(self.d_key, self.d_key2))
		plus = types.InlineKeyboardButton('+1', callback_data='plus_{0}'.format(self.d_key))
		plus_syrup = types.InlineKeyboardButton('Добавить сироп', callback_data='syrup_{0}'.format(self.d_key))
		in_cart = types.InlineKeyboardButton('Добавить в корзину', callback_data='in_cart_{0}'.format(self.d_key))
		clear_cart = types.InlineKeyboardButton('Убрать из корзины', callback_data='clear_cart_{0}'.format(self.d_key))
		back_button = types.InlineKeyboardButton('<- назад', callback_data='{0}'.format(self.back))
		cart_keyboard.add(minus, value, plus)
		if bd.test_cart() > 0:
			if bd.count_item_in_cart(self.key) > 0:
				bd.in_cart_bd(self.key, bd.count_item_in_cart(self.key) - 1)
				if bd.count_item_in_cart(self.key) == 0:
					self.clear_cart()
				cart_keyboard.add(plus_syrup, clear_cart, back_button, row_width=1)
				bot.edit_message_text('<u>' + self.title + '</u>' + '\n' + self.description + self.text_price.format(self.price)
									  + bd.cart_in_item(),	chat_id=self.chat_id, message_id=self.message_id,
									  reply_markup=cart_keyboard, parse_mode='HTML')
		else:
			self.callback_item()

	def in_cart(self):
		cart = cart_bd(self.call)
		cart.in_cart_bd(self.key, count(self.chat_id, self.key))
		c = cart.count_item_in_cart(self.key)
		cart_keyboard = types.InlineKeyboardMarkup(row_width=3)
		value = types.InlineKeyboardButton('☕ {0} ед.'.format(c), callback_data='value')
		minus = types.InlineKeyboardButton('-1', callback_data='minus_{0}{1}'.format(self.d_key, self.d_key2))
		plus = types.InlineKeyboardButton('+1', callback_data='plus_{0}'.format(self.d_key))
		plus_syrup = types.InlineKeyboardButton('Добавить сироп', callback_data='syrup_{0}'.format(self.d_key))
		clear_cart = types.InlineKeyboardButton('Убрать из корзины', callback_data='clear_cart_{0}'.format(self.d_key))
		back_button = types.InlineKeyboardButton('<- назад', callback_data='{0}'.format(self.back))
		cart_keyboard.add(minus, value, plus)
		cart_keyboard.add(plus_syrup, clear_cart, back_button, row_width=1)
		bot.edit_message_text('<u>' + self.title + '</u>' + '\n' + self.description + self.text_price.format(self.price) + cart.cart_in_item()
							  , chat_id=self.chat_id, message_id=self.call.message_id,
							  reply_markup=cart_keyboard, parse_mode='HTML')

	def clear_cart(self):
		try:
			for l in reversed(range(len(order[self.chat_id]))):
				if order[self.chat_id][l] == self.key:
					order[self.chat_id].pop(l)
		except KeyError: pass
		c = cart_bd(self)
		c.clear_cart_item(self.key)
		self.callback_item()

	def syrup(self):
		bd = cart_bd(self)
		cart_keyboard = types.InlineKeyboardMarkup(row_width=1)
		back_button = types.InlineKeyboardButton('<- назад', callback_data='{0}'.format(self.d_key))
		cart_keyboard.add(back_button, row_width=1)
		order_syrup_status.setdefault(self.chat_id, True)
		order_syrup.setdefault(self.chat_id, {'call': self.call, 'key': self.key, 'd_key': self.d_key, 'back': self.back})
		bot.edit_message_text('\n<b>Напишите вкус сиропа.</b>\n<i>Если такого сиропа не будет, бариста Вам сообщит о других, похожих вкусах)</i>' + '\n' + bd.cart_in_item() + '', chat_id=self.chat_id, message_id=self.message_id,
							  reply_markup=cart_keyboard, parse_mode='HTML')

class order_status_class:

	def __init__(self, call, message = None):

		self.call = call
		try:
			self.call.data = call.data
		except AttributeError: pass
		try:
			self.orders = self.call.data.split('|')[1]
			self.call.data = self.call.data.split('|')[0]
		except IndexError:
			pass
		except AttributeError:
			pass
		self.chat_id = call.from_user.id
		self.message = message
		self.about_time()
		self.bd = cart_bd(self.call)
		self.text = self.bd.order_for_barista()
		try:
			self.status(self.call.data, self.orders)
		except AttributeError: pass

	def buy_ready(self):
		try:
			bd = cart_bd(self.call)
			order_status.pop(self.chat_id)
			id_orders = self.bd.order_done()
			keyboard = types.InlineKeyboardMarkup(row_width=1)
			seen = types.InlineKeyboardButton('ПРИНЯТО', callback_data='order_seen|{0}'.format(id_orders))
			cook = types.InlineKeyboardButton('ГОТОВЛЮ', callback_data='order_cook|{0}'.format(id_orders))
			well_done = types.InlineKeyboardButton('НАПИТОК ГОТОВ', callback_data='order_well_done|{0}'.format(id_orders))
			close_order = types.InlineKeyboardButton('ОПЛАТИЛИ/ЗАБРАЛИ', callback_data='order_close|{0}'.format(id_orders))
			keyboard.add(seen, cook, well_done, close_order)
			barista = bd.id_barista()
			bot.send_message(int(barista), self.text, parse_mode='HTML', reply_markup=keyboard)
			bot.send_message(self.chat_id,
									 'Отлично 🎉\n\nВаш <b>заказ передан</b> бариста!\n\nВам придёт <b>уведомление</b> по готовности напитка) ',
									 parse_mode='HTML')
		except KeyError:
			return False

	def status(self, call_data, orders):
		try:
			if self.call.data == 'order_seen':
				bd = cart_bd(self.call)
				status = bd.test_status(orders)
				if status == 'ready':
					id_us = bd.set_status('seen', orders)
					bot.send_message(id_us, '✔️ Бариста получил заказ ', disable_notification='True')
					keyboard = types.InlineKeyboardMarkup(row_width=1)
					cook = types.InlineKeyboardButton('ГОТОВЛЮ', callback_data='order_cook|{0}'.format(orders))
					well_done = types.InlineKeyboardButton('НАПИТОК ГОТОВ',
														   callback_data='order_well_done|{0}'.format(orders))
					close_order = types.InlineKeyboardButton('ОПЛАТИЛИ/ЗАБРАЛИ',
															 callback_data='order_close|{0}'.format(orders))
					keyboard.add(cook, well_done, close_order)
					bot.edit_message_reply_markup(chat_id=self.call.from_user.id, message_id=self.call.message.id,
												  reply_markup=keyboard)

			if self.call.data == 'order_cook':
				bd = cart_bd(self.call)
				status = bd.test_status(orders)
				if status == 'seen':
					id_us = bd.set_status('cook', orders)
					bot.send_message(id_us, '☕ Мы уже готовим')
					keyboard = types.InlineKeyboardMarkup(row_width=1)
					well_done = types.InlineKeyboardButton('НАПИТОК ГОТОВ',
														   callback_data='order_well_done|{0}'.format(orders))
					close_order = types.InlineKeyboardButton('ОПЛАТИЛИ/ЗАБРАЛИ',
															 callback_data='order_close|{0}'.format(orders))
					keyboard.add(well_done, close_order)
					bot.edit_message_reply_markup(chat_id=self.call.from_user.id, message_id=self.call.message.id,
												  reply_markup=keyboard)

			if self.call.data == 'order_well_done':
				bd = cart_bd(self.call)
				status = bd.test_status(orders)
				if status == 'cook':
					id_us = bd.set_status('done', orders)
					bot.send_message(id_us, '🎉 Всё готово! Мы Вас ждём!', )
					keyboard = types.InlineKeyboardMarkup(row_width=1)
					close_order = types.InlineKeyboardButton('ОПЛАТИЛИ/ЗАБРАЛИ',
															 callback_data='order_close|{0}'.format(orders))
					keyboard.add(close_order)
					bot.edit_message_reply_markup(chat_id=self.call.from_user.id, message_id=self.call.message.id,
												  reply_markup=keyboard)

			if self.call.data == 'order_close':
				bd = cart_bd(self.call)
				status = bd.test_status(orders)
				if status == 'done':
					id_us = bd.set_status('close', orders)
					keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
					button_shop = types.KeyboardButton('Меню')
					button_history = types.KeyboardButton('История заказов')
					button_cart = types.KeyboardButton('Корзина')
					keyboard.add(button_shop, button_history)
					keyboard.add(button_cart)
					name = bd.get_name_user(id_us)
					bot.send_message(id_us,
									 '{0}!\nCпасибо за то, что Ты есть! 💗'.format(name), reply_markup=keyboard)
					bot.delete_message(chat_id=self.call.from_user.id, message_id=self.call.message.id)

		except AttributeError: print('att_err')

	def about_time(self):
		bd = cart_bd(self.call)
		bd.about_time(self.message)
