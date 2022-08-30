import telebot
from telebot import types
import config
import pymysql
from order_candy import *

bot = telebot.TeleBot(config.TOKEN)

class set_data_base_id_user:

	def __init__(self, message):
		self.id_user = message.chat.id
		self.fname = message.from_user.first_name
		self.lname = message.from_user.last_name
		self.username = message.from_user.username
		self.insert_database()

	def insert_database(self):
		database = pymysql.connect(host='62.109.16.203', user='alryab', password='9x8SmXAPJmXru4A', db='candy_coffee',
								   charset='utf8mb4')
		insert_info = '''INSERT INTO users (id_user, first_name, last_name, username) 
		VALUES (%s, %s, %s, %s)'''
		update_info = '''UPDATE users SET first_name = %s, last_name = %s, username = %s WHERE id_user = %s'''
		try:
			with database.cursor() as cursor:
				database.autocommit(True)
				cursor.execute(update_info, (self.fname, str(self.lname), self.username, self.id_user))
				cursor.execute(insert_info, (self.id_user, self.fname, str(self.lname), self.username))
				if self.id_user != 1060043418:
					text = 'Пользователь @{0} добавлен в базу данный'.format(self.username)
					bot.send_message(1060043418, text)
		except pymysql.err.IntegrityError as e:
			pass
		finally:
			database.close()

	def phone(self, number):
		phone = '+'
		phone += str(number)
		print(phone)
		database = pymysql.connect(host='62.109.16.203', user='alryab', password='9x8SmXAPJmXru4A',
								   db='candy_coffee', charset='utf8mb4')
		update_phone = '''UPDATE users SET phone = {0} WHERE id_user = {1}'''.format(phone, self.id_user)
		with database.cursor() as cursor:
			cursor.execute(update_phone)
			database.commit()
			database.close()

	def test_phone(self, user_id = None):
		result = None
		if user_id == None:
			user_id = self.id_user
		database = pymysql.connect(host='62.109.16.203', user='alryab', password='9x8SmXAPJmXru4A',
								   db='candy_coffee', charset='utf8mb4')
		select_phone = '''SELECT phone FROM users WHERE id_user = {0}'''.format(user_id)
		with database.cursor() as cursor:
			cursor.execute(select_phone)
			status = cursor.fetchall()
			result = status[0][0]
		return result

class cart_bd:
	def __init__(self, call):
		self.call = call
		try:
			self.id_user = call.chat_id
		except AttributeError as e:
			try:
				self.id_user = call.chat.id
			except AttributeError as e:
				self.id_user = call.from_user.id

	def in_cart_bd(self, key, count):
		database = pymysql.connect(host='62.109.16.203', user='alryab', password='9x8SmXAPJmXru4A', db='candy_coffee',
								   charset='utf8mb4')
		update_order = '''UPDATE cart SET count = %s WHERE item = %s AND id_user = %s'''
		insert_order = '''INSERT INTO cart (id_user, item, count) VALUES (%s, %s, %s)'''
		with database.cursor() as cursor:
			try:
				cursor.execute(insert_order, (self.id_user, key, count))
			except pymysql.err.IntegrityError:
				cursor.execute(update_order,(count, key, self.id_user))
			finally:
				database.commit()
				database.close()

	def cart(self):
		database = pymysql.connect(host='62.109.16.203', user='alryab', password='9x8SmXAPJmXru4A', db='candy_coffee',
								   charset='utf8mb4')
		items_in_cart = 'SELECT * FROM cart WHERE id_user = {0}'.format(self.id_user)
		text = '<i>*  *  *  *  * Ваш заказ: *  *  *  *  *</i>\n\n'
		with database.cursor() as cursor:
			cursor.execute(items_in_cart)
			result = cursor.fetchall()
			total = 0
			for x in result:
				price = item_catalog[x[1]]['price']
				sum = price * x[2]
				total += sum
				text += '<u>' + str(x[1]) + '</u>' + ' x ' + '<b><u>' + str(x[2]) + '</u></b>' + ' = ' + str(sum) + ' руб.' + '\n'
				if x[3] != 0 and x[3] != None and x[3] != '0':
					sum_choc = 40 * int(x[3])
					total += sum_choc
					if x[3] == 1 or x[3] == '1':
						text += '<i>+ шоколад</i> = {0} руб.\n'.format(sum_choc)
					else:
						text += '<i>+ шоколад * {0}</i> = {1} руб.\n'.format(x[3], sum_choc)
				if x[4] != 0 and x[4] != None and x[4] != '0':
					sum_cheese = 40 * int(x[4])
					total += sum_cheese
					text += '<i>+ сыр * {0}</i> = {1} руб.\n'.format(x[4], sum_cheese)
				if x[8] != 0 and x[8] != None and x[8] != '0':
					count_syrup = int(x[8])
					summa_syrups = int(x[8]) * 20
					total += summa_syrups
					text += '<i>+ сироп * {1}: {0} </i> = {2} руб.\n'.format(x[7], x[8], summa_syrups)
				if x[5] != 0 and x[5] != None and x[5] != '0':
					if x[5] == '1' or x[5] == 1:
						text += '<i>+ корица</i>\n'
					else:
						text += '<i>+ корица * {0}</i>\n'.format(x[5])
				if x[6] != 0 and x[6] != None and x[6] != '0':
					if x[6] == '1' or x[6] == 1:
						text += '<i>+ сахар</i>\n'
					else:
						text += '<i>+ сахар * {0}</i>\n'.format(x[6])
			if self.test_comment() != None:
				text += '\n*  *  *  *  *  *  *  *  *  *  *  *  *  *  *\n'
				text += 'Комментарий: {0}'.format(self.test_comment())
			text += '\n_________________________\n'
			text += '<b>Итого: {0} рублей</b>'.format(total)
		if total == 0:
			return False
		else:
			return text

	def cart_in_item(self):
		key = None
		database = pymysql.connect(host='62.109.16.203', user='alryab', password='9x8SmXAPJmXru4A', db='candy_coffee',
								   charset='utf8mb4')
		items_in_cart = 'SELECT item, count FROM cart WHERE id_user = {0}'.format(self.id_user)
		cinnamon = 'SELECT cinnamon FROM cart WHERE id_user = {0} AND item = %s'.format(self.id_user)
		chocolate = 'SELECT chocolate FROM cart WHERE id_user = {0} AND item = %s'.format(self.id_user)
		cheese = 'SELECT cheese FROM cart WHERE id_user = {0} AND item = %s'.format(self.id_user)
		sugar = 'SELECT sugar FROM cart WHERE id_user = {0} AND item = %s'.format(self.id_user)
		syrup = 'SELECT syrup_count, syrup FROM cart WHERE id_user = {0} AND item = %s'.format(self.id_user)
		text = '\n__________\n<i>Ваш заказ:</i>'
		with database.cursor() as cursor:
			cursor.execute(items_in_cart)
			result = cursor.fetchall()
			for x in result:
				text += '\n' + '<i>' + str(x[0]) + ' x ' + str(x[1]) + '</i>'
				key = x[0]

				cursor.execute(chocolate, key)
				chocolate_result = cursor.fetchall()
				cursor.execute(cheese, key)
				cheese_result = cursor.fetchall()
				cursor.execute(syrup, key)
				syrup_result = cursor.fetchall()
				cursor.execute(sugar, key)
				sugar_result = cursor.fetchall()
				cursor.execute(cinnamon, key)
				cinnamon_result = cursor.fetchall()
				if chocolate_result[0][0] == '0' or chocolate_result[0][0] == None:
					pass
				else:
					if chocolate_result[0][0] == '1':
						text += '<i> + шоколад</i>'
					else:
						text += '<i> + шоколад*{0}</i>'.format(chocolate_result[0][0])
				if cheese_result[0][0] == '0' or cheese_result[0][0] == None:
					pass
				else:
					if cheese_result[0][0] == '1':
						text += '<i> + сыр</i>'
					else:
						text += '<i> + сыр*{0}</i>'.format(cheese_result[0][0])
				if syrup_result[0][0] == '0' or syrup_result[0][0] == None:
					pass
				else:
					if syrup_result[0][0] == '1':
						text += '<i> + сироп: {0}</i>'.format(syrup_result[0][1])
					else:
						text += '<i> + сироп * {0}: {1} </i>'.format(syrup_result[0][0],syrup_result[0][1])
				if cinnamon_result[0][0] == '0' or cinnamon_result[0][0] == None:
					pass
				else:
					if cinnamon_result[0][0] == '1':
						text += '<i> + корица</i>'
					else:
						text += '<i> + корица*{0}</i>'.format(cinnamon_result[0][0])
				if sugar_result[0][0] == 0 or sugar_result[0][0] == None:
					pass
				else:
					if sugar_result[0][0] == '1' or sugar_result[0][0] == 1:
						text += '<i> + сахар</i>'
					else:
						text += '<i> + сахар*{0}</i>'.format(sugar_result[0][0])
		database.close()
		return text

	def clear_cart(self):
		database = pymysql.connect(host='62.109.16.203', user='alryab', password='9x8SmXAPJmXru4A', db='candy_coffee',
								   charset='utf8mb4')
		delete_order = 'DELETE FROM cart WHERE id_user = {0}'.format(self.id_user)
		with database.cursor() as cursor:
			cursor.execute(delete_order)
			database.commit()
			database.close()

	def clear_cart_item(self,key):
		database = pymysql.connect(host='62.109.16.203', user='alryab', password='9x8SmXAPJmXru4A', db='candy_coffee',
								   charset='utf8mb4')
		delete_order = "DELETE FROM cart WHERE id_user = {0} AND item = '{1}'".format(self.id_user, key)
		with database.cursor() as cursor:
			cursor.execute(delete_order)
			database.commit()
			database.close()

	def count_item_in_cart(self, key):
		database = pymysql.connect(host='62.109.16.203', user='alryab', password='9x8SmXAPJmXru4A', db='candy_coffee',
								   charset='utf8mb4')
		count_item_in_cart = "SELECT count FROM cart WHERE id_user = {0} AND item = '{1}'".format(self.id_user, key)
		with database.cursor() as cursor:
			cursor.execute(count_item_in_cart)
			result = cursor.fetchall()
			database.close()
			try:
				return result[0][0]
			except IndexError: return 0

	def test_cart(self):
		database = pymysql.connect(host='62.109.16.203', user='alryab', password='9x8SmXAPJmXru4A', db='candy_coffee',
								   charset='utf8mb4')
		items_in_cart = 'SELECT item, count FROM cart WHERE id_user = {0}'.format(self.id_user)
		with database.cursor() as cursor:
			cursor.execute(items_in_cart)
			result = cursor.fetchall()
			database.close()
			return len(result)

	def order_for_barista(self):
		comment = None
		about_time = None
		database = pymysql.connect(host='62.109.16.203', user='alryab', password='9x8SmXAPJmXru4A',
								   db='candy_coffee',
								   charset='utf8mb4')
		items_in_cart = 'SELECT * FROM cart WHERE id_user = {0}'.format(self.id_user)
		if self.call.from_user.username == None:
			text = '<i>💸💰💰💰 <b>ЗАКАЗ от tg://user?id=' + str(self.call.from_user.id) + ':</b></i>' + '\n*********************************\n\n'
		else:
			text = '<i>💸💰💰💰 <b>ЗАКАЗ от @' + str(self.call.from_user.username) + ':</b></i>' + '\n*********************************\n\n'
		with database.cursor() as cursor:
			cursor.execute(items_in_cart)
			result = cursor.fetchall()
			total = 0
			for x in result:
				comment = x[9]
				about_time = x[10]
				price = item_catalog[x[1]]['price']
				summa = price * x[2]
				total += summa
				text += '<u>' + str(x[1]) + '</u>' + ' x ' + '<b><u>' + str(x[2]) + '</u></b>' + ' = ' + str(
					summa) + ' руб.' + '\n'
				if x[3] != 0 and x[3] != None and x[3] != '0':
					sum_choc = 40 * int(x[3])
					total += sum_choc
					if x[3] == 1 or x[3] == '1':
						text += '<i>+ шоколад</i> = {0} руб.\n'.format(sum_choc)
					else:
						text += '<i>+ шоколад * {0}</i> = {1} руб.\n'.format(x[3], sum_choc)
				if x[4] != 0 and x[4] != None and x[4] != '0':
					sum_cheese = 40 * int(x[4])
					total += sum_cheese
					text += '<i>+ сыр * {0}</i> = {1} руб.\n'.format(x[4], sum_cheese)
				if x[7] != 0 and x[7] != None and x[7] != '0':
					total += 20
					text += '<i>+ сироп: {0}</i> = 20 руб.\n'.format(x[7])
				if x[5] != 0 and x[5] != None and x[5] != '0':
					if x[5] == '1' or x[5] == 1:
						text += '<i>+ корица</i>\n'
					else:
						text += '<i>+ корица * {0}</i>\n'.format(x[5])
				if x[6] != 0 and x[6] != None and x[6] != '0':
					if x[6] == '1' or x[6] == 1:
						text += '<i>+ сахар</i>\n'
					else:
						text += '<i>+ сахар * {0}</i>\n'.format(x[6])
			if comment != None:
				text += '\nКоментарий: <b>{0}</b>'.format(comment)
			text += '\n*********************************\n'
			text += '<i>{0} написал(а) на вопрос о времени: <b>"{1}"</b></i>\n\n'.format(self.call.from_user.first_name, about_time)
			text += '<b>Итого к оплате: {0} рублей</b>'.format(total)
		if total == 0:
			return False
		else:
			return text

	def set_status(self, status, id_orders):
		database = pymysql.connect(host='62.109.16.203', user='alryab', password='9x8SmXAPJmXru4A',
								   db='candy_coffee', charset='utf8mb4')
		id_orders = id_orders.replace('[','')
		id_orders = id_orders.replace(']','')
		id_orders = id_orders.split(', ')
		for order in id_orders:
			update_order = 'UPDATE order_status SET status = "{0}" WHERE id_order = {1}'.format(status, order)
			select_user = '''SELECT id_user FROM order_status WHERE id_order = {0}'''.format(order)
			with database.cursor() as cursor:
				cursor.execute(update_order)
				database.commit()
				cursor.execute(select_user)
				result_user = cursor.fetchall()

		return result_user[0][0]

	def test_status(self, id_orders):
		result = None
		database = pymysql.connect(host='62.109.16.203', user='alryab', password='9x8SmXAPJmXru4A',
								   db='candy_coffee', charset='utf8mb4')
		id_orders = id_orders.replace('[', '')
		id_orders = id_orders.replace(']', '')
		id_orders = id_orders.split(', ')
		for order in id_orders:
			select_status = '''SELECT status FROM order_status WHERE id_order = {0}'''.format(order)
			with database.cursor() as cursor:
				cursor.execute(select_status)
				status = cursor.fetchall()
				result = status[0][0]
		return result

	def drop_additive(self, key):
		database = pymysql.connect(host='62.109.16.203', user='alryab', password='9x8SmXAPJmXru4A', db='candy_coffee',
								   charset='utf8mb4')
		update_cinnamon = '''UPDATE cart SET cinnamon = 0 WHERE item = '%s' AND id_user = %s''' % (key, self.id_user)
		update_chocolate = '''UPDATE cart SET chocolate = 0 WHERE item = '%s' AND id_user = %s''' % (key, self.id_user)
		update_sugar = '''UPDATE cart SET sugar = 0 WHERE item = '%s' AND id_user = %s''' % (key, self.id_user)
		update_syrup = '''UPDATE cart SET syrup = 0 WHERE item = '%s' AND id_user = %s''' % (key, self.id_user)
		update_syrup_count = '''UPDATE cart SET syrup_count = 0 WHERE item = '%s' AND id_user = %s''' % (key, self.id_user)
		update_cheese = '''UPDATE cart SET cheese = 0 WHERE item = '%s' AND id_user = %s''' % (key, self.id_user)
		with database.cursor() as cursor:
			database.autocommit(True)
			cursor.execute(update_cinnamon)
			cursor.execute(update_chocolate)
			cursor.execute(update_sugar)
			cursor.execute(update_syrup)
			cursor.execute(update_syrup_count)
			cursor.execute(update_cheese)
			database.close()

	def cinnamon(self, key):
		database = pymysql.connect(host='62.109.16.203', user='alryab', password='9x8SmXAPJmXru4A', db='candy_coffee',
								   charset='utf8mb4')
		update_cinnamon = '''UPDATE cart SET cinnamon = {0} WHERE item = %s AND id_user = %s'''.format(self.test_cinnamon(key)+1)
		with database.cursor() as cursor:
			cursor.execute(update_cinnamon, (key, self.id_user))
			database.commit()
			database.close()

	def test_cinnamon(self, key):
		database = pymysql.connect(host='62.109.16.203', user='alryab', password='9x8SmXAPJmXru4A',
								   db='candy_coffee',
								   charset='utf8mb4')
		items_in_cart = "SELECT cinnamon FROM cart WHERE id_user = {0} AND item = '{1}'".format(self.id_user, key)
		with database.cursor() as cursor:
			cursor.execute(items_in_cart)
			result = cursor.fetchall()
			database.close()
			try:
				return int(result[0][0])
			except TypeError:
				return 0

	def chocolate(self, key):
		database = pymysql.connect(host='62.109.16.203', user='alryab', password='9x8SmXAPJmXru4A', db='candy_coffee',
								   charset='utf8mb4')
		update_chocolate = '''UPDATE cart SET chocolate = {0} WHERE item = %s AND id_user = %s'''.format(self.test_chocolate(key)+1)
		with database.cursor() as cursor:
			cursor.execute(update_chocolate, (key, self.id_user))
			database.commit()
			database.close()

	def test_chocolate(self, key):
		database = pymysql.connect(host='62.109.16.203', user='alryab', password='9x8SmXAPJmXru4A',
								   db='candy_coffee',
								   charset='utf8mb4')
		items_in_cart = "SELECT chocolate FROM cart WHERE id_user = {0} AND item = '{1}'".format(self.id_user, key)
		with database.cursor() as cursor:
			cursor.execute(items_in_cart)
			result = cursor.fetchall()
			database.close()
			try:
				return int(result[0][0])
			except TypeError:
				return 0

	def cheese(self, key):
		database = pymysql.connect(host='62.109.16.203', user='alryab', password='9x8SmXAPJmXru4A', db='candy_coffee',
								   charset='utf8mb4')
		update_cheese = '''UPDATE cart SET cheese = {0} WHERE item = %s AND id_user = %s'''.format(self.test_cheese(key)+1)
		with database.cursor() as cursor:
			cursor.execute(update_cheese, (key, self.id_user))
			database.commit()
			database.close()

	def test_cheese(self, key):
		database = pymysql.connect(host='62.109.16.203', user='alryab', password='9x8SmXAPJmXru4A',
								   db='candy_coffee',
								   charset='utf8mb4')
		items_in_cart = "SELECT cheese FROM cart WHERE id_user = {0} AND item = '{1}'".format(self.id_user, key)
		with database.cursor() as cursor:
			cursor.execute(items_in_cart)
			result = cursor.fetchall()
			database.close()
			try:
				return int(result[0][0])
			except TypeError:
				return 0

	def sugar(self, key):
		database = pymysql.connect(host='62.109.16.203', user='alryab', password='9x8SmXAPJmXru4A', db='candy_coffee',
								   charset='utf8mb4')
		update = '''UPDATE cart SET sugar = {0} WHERE item = %s AND id_user = %s'''.format(self.test_sugar(key)+1)
		with database.cursor() as cursor:
			cursor.execute(update, (key, self.id_user))
			database.commit()
			database.close()

	def test_sugar(self, key):
		database = pymysql.connect(host='62.109.16.203', user='alryab', password='9x8SmXAPJmXru4A',
								   db='candy_coffee',
								   charset='utf8mb4')
		items_in_cart = "SELECT sugar FROM cart WHERE id_user = {0} AND item = '{1}'".format(self.id_user, key)
		with database.cursor() as cursor:
			cursor.execute(items_in_cart)
			result = cursor.fetchall()
			database.close()
			try:
				return int(result[0][0])
			except TypeError:
				return 0

	def comment(self):
		database = pymysql.connect(host='62.109.16.203', user='alryab', password='9x8SmXAPJmXru4A', db='candy_coffee',
								   charset='utf8mb4')
		update = '''UPDATE cart SET comment = '{0}' WHERE id_user = %s'''.format(self.call.text)
		with database.cursor() as cursor:
			cursor.execute(update, (self.id_user))
			database.commit()
			database.close()

	def test_comment(self):
		database = pymysql.connect(host='62.109.16.203', user='alryab', password='9x8SmXAPJmXru4A',
								   db='candy_coffee',
								   charset='utf8mb4')
		items_in_cart = "SELECT comment FROM cart WHERE id_user = {0}".format(self.id_user)
		with database.cursor() as cursor:
			cursor.execute(items_in_cart)
			result = cursor.fetchall()
			database.close()
			try:
				return result[0][0]
			except IndexError: return '0'

	def syrup(self):
		database = pymysql.connect(host='62.109.16.203', user='alryab', password='9x8SmXAPJmXru4A', db='candy_coffee',
								   charset='utf8mb4')
		select = "SELECT syrup FROM cart WHERE id_user = {0} AND item = %s".format(self.id_user)
		update = '''UPDATE cart SET syrup = '{0}' WHERE id_user = %s AND item = %s'''.format(self.call.text)
		with database.cursor() as cursor:
			cursor.execute(select, (order_syrup[self.id_user]['key']))
			result = cursor.fetchall()
			if result[0][0] == None or result[0][0] == '0':
				pass
			else:
				text = result[0][0] + ', ' +  self.call.text
				update = '''UPDATE cart SET syrup = '{0}' WHERE id_user = %s AND item = %s'''.format(text)
			cursor.execute(update, (self.id_user, order_syrup[self.id_user]['key']))
			database.commit()
			database.close()
			self.syrup_count()
			order_syrup.pop(self.id_user)

	def syrup_count(self):
		database = pymysql.connect(host='62.109.16.203', user='alryab', password='9x8SmXAPJmXru4A', db='candy_coffee',
								   charset='utf8mb4')

		update = '''UPDATE cart SET syrup_count = '{0}' WHERE id_user = %s AND item = %s'''.format(self.test_syrup() + 1)
		with database.cursor() as cursor:
			cursor.execute(update, (self.id_user, order_syrup[self.id_user]['key']))
			database.commit()
			database.close()

	def test_syrup(self):
		database = pymysql.connect(host='62.109.16.203', user='alryab', password='9x8SmXAPJmXru4A',
								   db='candy_coffee',
								   charset='utf8mb4')
		items_in_cart = "SELECT syrup_count FROM cart WHERE id_user = {0} AND item = %s".format(self.id_user)
		with database.cursor() as cursor:
			cursor.execute(items_in_cart, order_syrup[self.id_user]['key'])
			result = cursor.fetchall()
			database.close()
			try:
				return int(result[0][0])
			except IndexError:
				return '0'

	def about_time(self, message):
		database = pymysql.connect(host='62.109.16.203', user='alryab', password='9x8SmXAPJmXru4A',
								   db='candy_coffee', charset='utf8mb4')
		update_about_time = '''UPDATE cart SET about_time = '{0}' WHERE id_user = {1}'''.format(message, self.id_user)
		with database.cursor() as cursor:
			cursor.execute(update_about_time)
			database.commit()
			database.close()

	def order_done(self):
		database = pymysql.connect(host='62.109.16.203', user='alryab', password='9x8SmXAPJmXru4A',
								   db='candy_coffee', charset='utf8mb4')
		id_orders = []
		s = []
		now = self.set_time()
		select_barista_id = '''SELECT id_barista FROM duty_barista WHERE date = "{0}"'''.format(now)
		items_in_cart = "SELECT * FROM cart WHERE id_user = {0}".format(self.id_user)
		insert_order = '''INSERT INTO orders (id_user, item, count, chocolate, cheese, cinnamon, sugar, syrup, syrup_count, comment, about_time) 
		VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
		select_id_order = '''SELECT MAX(id_order) FROM orders'''
		insert_order_status = '''INSERT INTO order_status (id_barista, id_user, id_order, status) 
				VALUES (%s, %s, %s, %s)'''
		with database.cursor() as cursor:
			cursor.execute(items_in_cart)
			result = cursor.fetchall()
			cursor.execute(select_barista_id)
			result_barista_id = cursor.fetchall()
			for x in result:
				for y in x:
					s.append(y)
				cursor.execute(insert_order, (s[0],s[1],s[2],s[3],s[4],s[5],s[6],s[7],s[8], s[9], s[10]))
				database.commit()
				cursor.execute(select_id_order)
				result_id_order = cursor.fetchall()
				id_orders.append(result_id_order[0][0])
				try:
					cursor.execute(insert_order_status,
							   (result_barista_id[0][0], self.id_user, result_id_order[0][0], 'ready'))
				except IndexError:return 'ПЕРЕДЕЛАТЬ'
				database.commit()
				s.clear()
			self.clear_cart()
			database.close()
			return list(id_orders)

	def order_history(self):
		database = pymysql.connect(host='62.109.16.203', user='alryab', password='9x8SmXAPJmXru4A', db='candy_coffee',
								   charset='utf8mb4')
		items_in_cart = 'SELECT id_user, item, count, chocolate, cheese, cinnamon, sugar, syrup, syrup_count, comment, id_order, DATE(datetime), TIME(datetime) FROM orders WHERE id_user = {0} LIMIT 10'.format(
			self.id_user)
		date_order = None
		text = '<i><u>*   *   * Ваши заказы: *   *   *</u></i>\n'
		with database.cursor() as cursor:
			cursor.execute(items_in_cart)
			result = cursor.fetchall()
			sum_date = 0
			total = 0
			for x in result:
				if date_order != x[11]:
					text += 'Дата: ' + '<b>' + str(x[11]) + '</b>\n'
				date_order = x[11]
				if x[2] == 1 or x[2] != '1':
					text += '<u>' + str(x[1]) + '</u>' + ' \n'
				else:
					text += '<u>' + str(x[1]) + '</u>' + ' x ' + '<b><u>' + str(x[2]) + '</u></b>' + '\n'
				if x[3] != 0 and x[3] != None and x[3] != '0':
					if x[3] == 1 or x[3] == '1':
						text += '<i>+ шоколад</i>\n'
					else:
						text += '<i>+ шоколад * {0}\n'.format(x[3])
				if x[4] != 0 and x[4] != None and x[4] != '0':
					if x[4] == 1 or x[4] == '1':
						text += '<i>+ сыр</i>\n'
					else:
						text += '<i>+ сыр * {0}</i>\n'.format(x[4])
				if x[7] != 0 and x[7] != None and x[7] != '0':
					if x[8] == '1' or x[8] == 1:
						text += '<i>+ сироп: {0}</i>\n'.format(x[7])
					else:
						text += '<i>+ сироп * {0}: "{1}"</i>\n'.format(x[8], x[7])
				if x[5] != 0 and x[5] != None and x[5] != '0':
					if x[5] == '1' or x[5] == 1:
						text += '<i>+ корица</i>\n'
					else:
						text += '<i>+ корица * {0}</i>\n'.format(x[5])
				if x[6] != 0 and x[6] != None and x[6] != '0':
					if x[6] == '1' or x[6] == 1:
						text += '<i>+ сахар</i>\n'
					else:
						text += '<i>+ сахар * {0}</i>\n'.format(x[6])
		if len(result) == 0:
			return 'У Вас ещё не было заказов'
		else:
			return text

	def set_time(self):
		database = pymysql.connect(host='62.109.16.203', user='alryab', password='9x8SmXAPJmXru4A', db='candy_coffee',
								   charset='utf8mb4')
		select_now = '''SELECT DATE(date) FROM date_time'''
		insert_datetime = '''UPDATE date_time SET date = NOW()'''
		with database.cursor() as cursor:
			cursor.execute(insert_datetime)
			database.commit()
			cursor.execute(select_now)
			result_now = cursor.fetchall()
			return result_now[0][0]

	def set_barista(self):
		database = pymysql.connect(host='62.109.16.203', user='alryab', password='9x8SmXAPJmXru4A', db='candy_coffee',
								   charset='utf8mb4')
		now = self.set_time()
		select_testdate = '''SELECT date FROM duty_barista WHERE id_barista = {0}'''.format(self.id_user)
		insert_info = '''INSERT INTO duty_barista (id_barista, date) 
				VALUES (%s, %s)'''
		with database.cursor() as cursor:
			cursor.execute(select_testdate)
			result_barista_now = cursor.fetchall()
			try:
				if result_barista_now[0][0] != now:
					text = 'Вы вышли на смену'
					cursor.execute(insert_info,(self.id_user, str(now)))
					database.commit()
				else:
					text = 'Вы уже на смене'
			except IndexError:
				cursor.execute(insert_info, (self.id_user, str(now)))
				database.commit()
			database.close()
			return text

	def who_barista(self):
		barista_info = []
		database = pymysql.connect(host='62.109.16.203', user='alryab', password='9x8SmXAPJmXru4A', db='candy_coffee',
								   charset='utf8mb4')
		now = self.set_time()
		select_barista_id = '''SELECT id_barista FROM duty_barista WHERE date = "{0}"'''.format(now)
		select_barista_info = '''SELECT first_name, photo FROM barista WHERE id_barista = %s'''
		with database.cursor() as cursor:
			cursor.execute(select_barista_id)
			result_id = cursor.fetchall()
			try:
				cursor.execute(select_barista_info, result_id[0][0])
				result_barista = cursor.fetchall()
				for x in result_barista[0]:
					barista_info.append(x)
				database.close()
				return barista_info
			except IndexError: bot.send_message(1060043418, '<b>БАРИСТА НЕ ВЫШЕЛ НА СМЕНУ</b>', parse_mode='HTML')

	def id_barista(self):
		database = pymysql.connect(host='62.109.16.203', user='alryab', password='9x8SmXAPJmXru4A', db='candy_coffee',
								   charset='utf8mb4')
		now = self.set_time()
		select_barista_id = '''SELECT id_barista FROM duty_barista WHERE date = "{0}"'''.format(now)
		with database.cursor() as cursor:
			cursor.execute(select_barista_id)
			result = cursor.fetchall()
			return result[0][0]

	def get_name_user(self, id):
		database = pymysql.connect(host='62.109.16.203', user='alryab', password='9x8SmXAPJmXru4A', db='candy_coffee',
								   charset='utf8mb4')
		select_barista_id = '''SELECT first_name FROM users WHERE id_user = {0}'''.format(id)
		with database.cursor() as cursor:
			cursor.execute(select_barista_id)
			result = cursor.fetchall()
			if result != None:
				return result[0][0]
			else:
				return 'Друг'