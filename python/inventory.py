import sqlite3

class InventoryDB(Object):
	"""
	Creates a SQLite3 database of products and their unique identifiers.
	"""
	def __init__(self, name, db=None):
		"""
		Initialize the Database
		
		@param name:  Database's name
		@param db:  SQLite3 connection to the database
		"""
		self.name = name
		self.db = self.establish_connection()
		
	def establish_connection(self):
		"""
		Establish a connection with the specified database
		"""
		return sqlite3.connect(self.name)
	
	def create_inventory(self):
		"""
		Create a table in the database called 'inventory' with the columns
		id (primary key), code, and item.
		
		@return:  Return true if the database was able to create the table;
		          otherwise, return false.
		"""
		self.db.execute('''CREATE TABLE inventory(id INTEGER PRIMARY KEY, code TEXT, item TEXT)''')
		self.db.commit()
		return True
	
	def insert_item(self, item):
		"""
		Insert an item into the database
		
		@param item:  A tuple of an item's code and the item itself
		@return:  Return true if the database was able to insert the item;
		          otherwise, return false.
		"""
		self.db.execute('''INSERT INTO inventory(code, item) VALUES(?,?)''', item)
		self.db.commit()
		return True
		
	def read_item(self, code):
		"""
		Read an item from the databased based on a specified code.

		@param code: Unique identifier of an item
		@return:  Return true if the database was able to read the item;
		          otherwise, return false.
		"""
		self.db.execute('''SELECT item FROM inventory where code=?''', code)
                return True
                
	def update_item(self, item, code):
		"""
                Update the code of an item in the database

                @param item:  The item
                @param code:  Code of the item to be updated
                @return:  Return true if the database was able to udate the code;
		          otherwise, return false.
		"""
		self.db.execute('''UPDATE inventory SET code = ? WHERE item = ?''', (code, item))
		self.db.commit()
		return True
		
	def delete_item(self, code):
		"""
		Delete an item from the database based on a specified code

		@param code:  Code of the item to be deleted
		@return:  Return true if the database was able to delete the item;
		          otherwise, return false.
		"""
		self.db.execute('''DELETE FROM inventory WHERE code = ?''', (code))
		self.db.commit()
		return True
	
