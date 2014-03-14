__author__  = 'Steven Briggs'
__version__ = '2014.03.13'

import sqlite3
import logging

DB_NAME = 'inventory.sqlite3'
logging.basicConfig(level=logging.INFO)
log = logging.getLogger('inventory_log')

class RecordDoesNotExistError(RuntimeError):
	"""
	This error should raised and subsequently caught if a database 
	operation on a non-existent record is performed
	"""
	def __init__(self, arg):
		"""
		Initialize the RecordDoesNotExistError
		
		@param arg:  An argument to include in the error, typically a 
		             message about the error
		"""
		self.args = arg


class InventoryDatabase(object):
	"""
	Creates a SQLite3 database of products and their unique identifiers.
	"""
	def __init__(self):
		"""
		Initialize the InventoryDatabase
		"""
		self.db = self.establish_connection()
		self.cursor = db.cursor()
		
	def establish_connection(self):
		"""
		Establish a connection with the specified database
		"""
		return sqlite3.connect(DB_NAME)
	
	def create_inventory(self):
		"""
		Create a table in the database called 'inventory' with the columns
		id (primary key), product, and code.
		"""
		try:
			self.cursor.execute("CREATE TABLE inventory(id INTEGER PRIMARY KEY, product TEXT UNIQUE, code TEXT UNIQUE)")
		except sqlite3.OperationalError as e:
			self.db.rollback()
			log.error('OperationalError({0}): Databased rolled back'.format(e))
		else:
			self.db.commit()
			log.info('Table "inventory" created')
	
	def insert_item(self, product):
		"""
		Insert a product into the database
		
		@param product:  Product to be inserted into the database
		"""
		try:
			self.cursor.execute("INSERT INTO inventory(product, code) VALUES(?, ?)", product)
		except sqlite3.IntegrityError as e:
			self.db.rollback()
			log.error('IntegrityError({0}): Database rolled back'.format(e))
		else:
			self.db.commit()
			log.info('{0} | {1} to index {2}'.format(product[0], product[1], cursor.lastrowid))
		
	def read_product(self, code):
		"""
		Read a product from the databased based on a specified code.
		
		@param code: Unique ID of the product to be read
		@return:     Return the latest product selected from the database
		             according to the specified filter.
		"""
		self.cursor.execute("SELECT product FROM inventory WHERE code=?", (code,))
		record = cursor.fetchone()
		if not record:
			msg = "Product with ID {0} non-existent".format(code)
			raise RecordDoesNotExistError(msg)
		return record
		
	def update_item(self, product, code):
		"""
		Update the identifier of a product in the database

		@param product:  Product whose ID is to be updated
		@param code:  ID that is to be updated
		"""
		try:
			record = self.read_item(code)
		except RecordDoesNotExistError as e:
			log.error("RecordDoesNotExistError({0})".format(e)
		else:
			self.db.execute("UPDATE inventory SET code=? WHERE product=?", (code, product))
			self.db.commit()
			log.info("Updated {0} to ID {1}".format(product, code))
		
	def delete_item(self, code):
		"""
		Delete a product from the database based on a specified id

		@param code:  ID of the product to be deleted
		"""
		try:
			record = self.read_item(code)
		except RecordDoesNotExistError as e:
			log.error("RecordDoesNotExistError({0})".format(e)
		else:
			self.db.execute("DELETE FROM inventory WHERE code=?", (code))
			self.db.commit()
			log.info("Deleted {0} with ID {1}".format(product, code))