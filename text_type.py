# -*- coding : utf-8 -*-

import telebot
import config
import order_candy
from telebot import types
from call_back_c import *

bot = telebot.TeleBot(config.TOKEN)

class textChat:
	message = None

	def __init__(self, message):
		self.message = message
		self.bd = cart_bd(message)
		bd_users = set_data_base_id_user(self.message)
		phone = bd_users.test_phone()
		if phone == None:
			self.get_contact()
		elif phone != None:
			self.main()

	def get_contact(self):
		keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
		get_phone = types.KeyboardButton('Отправить телефон', request_contact=True)
		keyboard.add(get_phone)
		bot.send_message(self.message.chat.id,
						 'Для использования бота необходим Ваш номер телефона.\nБлагодарим за понимание)',
						 reply_markup=keyboard)

	def main(self):
		if self.message.chat.id == 1064692141:
			bot.send_message(self.message.chat.id,
							 '{0.first_name} {1.last_name}, завали своё ебало!'.format(self.message.from_user,
																					   self.message.from_user))
		else:
			if self.message.text == 'Меню':
				try:
					order_syrup_status.pop(self.message.chat.id)
					order_comment.pop(self.message.chat.id)
				except KeyError: pass
				self.menu()
			if self.message.text == 'История заказов':
				try:
					order_syrup_status.pop(self.message.chat.id)
					order_comment.pop(self.message.chat.id)
				except KeyError:
					pass
				bot.send_message(self.message.chat.id,
								 self.bd.order_history(), parse_mode='HTML')
			if self.message.text == 'Корзина':
				try:
					order_syrup_status.pop(self.message.chat.id)
					order_comment.pop(self.message.chat.id)
				except KeyError:
					pass
				self.cart()
			'''Комментарий'''
			try:
				if order_comment[self.message.chat.id] == True:
					order_comment.pop(self.message.chat.id)
					self.bd.comment()
					self.cart()
			except KeyError: pass
			'''Ответ на вопрос о времени'''
			try:
				if self.bd.test_cart() > 0 and order_status[self.message.chat.id] == True:
					osc = order_status_class(self.message, self.message.text)
					osc.buy_ready()

				else:
					pass
			except KeyError as e:
				pass
			except ValueError:
				pass
			'''Выбор сиропа'''
			try:
				if order_syrup_status[self.message.chat.id] == True:
					order_syrup_status.pop(self.message.chat.id)
					call = order_syrup[self.message.chat.id]['call']
					key = order_syrup[self.message.chat.id]['key']
					d_key = order_syrup[self.message.chat.id]['d_key']
					back = order_syrup[self.message.chat.id]['back']
					self.bd.syrup()
					if d_key in items_dict.keys():
						cb = callback_buttons(call, key, d_key, back)
						cb.additive()
					if d_key in items_summer_ws.keys():
						cb = callback_buttons_summer_ws(call, key, d_key, back)
						cb.callback_item()
					bot.delete_message(self.message.chat.id, self.message.id)
			except KeyError: pass

	def cart(self):
		try:
			order_status.pop(self.message.from_user.id)
		except KeyError: pass
		keyboard = types.InlineKeyboardMarkup(row_width=1)
		clear_cart = types.InlineKeyboardButton('Очистить корзину 🗑', callback_data= 'clear_cart')
		buy = types.InlineKeyboardButton('Заказать', callback_data= 'buy')
		comment = types.InlineKeyboardButton('Добавить комментарий', callback_data='comment')
		back_mm = types.InlineKeyboardButton('Назад в меню', callback_data= 'main_menu')
		c = cart_bd(self.message)
		show_cart = c.cart()
		if show_cart != False:
			keyboard.add(buy, comment, clear_cart, back_mm)
			bot.send_message(self.message.chat.id,'{0}'.format(c.cart()), reply_markup= keyboard,
							 parse_mode='HTML')
		else:
			keyboard.add(back_mm)
			bot.send_message(self.message.chat.id, '<b>Вы пока ничего не добавили в корзину :(</b>', parse_mode='HTML', reply_markup= keyboard)

	def menu(self):
		bd = cart_bd(self.message)
		message = self.message
		menu_keyboard = types.InlineKeyboardMarkup(row_width=1)
		classic_coffee = types.InlineKeyboardButton('Класcический кофе', callback_data='clas_cof')
		author_coffee = types.InlineKeyboardButton('Авторский кофе', callback_data='aut_cof')
		summer_coffee = types.InlineKeyboardButton('Летние напитки', callback_data='sum_cof')
		anuwer = types.InlineKeyboardButton('Другое', callback_data='an_menu')
		menu_keyboard.add(classic_coffee, author_coffee, summer_coffee, anuwer)
		if bd.test_cart() > 0:
			bot.send_message(message.chat.id,'* * * МЕНЮ Candy Coffee * * *\n' + bd.cart_in_item(), reply_markup=menu_keyboard,  parse_mode='HTML')
		else:
			bot.send_message(message.chat.id, '* * * МЕНЮ Candy Coffee * * *', reply_markup=menu_keyboard, parse_mode='HTML')

	def orders_duty_barista(self):
		text = ''
		keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
		bd = cart_bd(self.message)
		orders_db = bd.orders_duty_barista()
		for x in orders_db:
			text += '-----\n{0}:\n{1}\n'.format(x, orders_db[x])
			button = types.KeyboardButton('/order {0}'.format(orders_db[x]))
			keyboard.add(button)
		bot.send_message(self.message.chat.id, 'Заказы\n' + text + '\n', reply_markup=keyboard)