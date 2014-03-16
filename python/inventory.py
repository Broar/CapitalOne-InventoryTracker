__author__  = 'Steven Briggs'
__version__ = '2014.03.15'

import sqlite3
import logging

DB_NAME = 'inventory.sqlite3'

logging.basicConfig(
     filename='inventory.log',
     level=logging.INFO,
     format='%(levelname)s:%(asctime)s:%(message)s')

class RecordDoesNotExistError(Exception):
    """
    This error should raised when database operations on non-existent 
    records are performed
    """
    def __init__(self, msg):
        """
        Initialize the RecordDoesNotExistError
        
        @param msg:  A message detailing the error
        """
        self.msg = msg
        
    def __str__(self):
        """
        A string representation of the RecordDoesNotExistError
        
        @return:  A message detailing the error
        """
        return repr(self.msg)

class InventoryDatabase(object):
    """
    Creates a SQLite3 database of products and their unique identifiers.
    """
    def __init__(self, __db=None):
        """
        Initialize the InventoryDatabase
        
        @__db:  Database containing products and their IDs
        """
        self.__db = self.establish_connection()
        
    def establish_connection(self):
        """
        Establish a connection with the product database
        
        @return:  Return the Connection to the database of products
        """
        return sqlite3.connect(DB_NAME)
    
    def close_connection(self):
        """
        Close the connection with the product database
        """
        self.__db.close()
    
    def create_inventory(self):
        """
        Create a table in the database called 'inventory' with the columns
        id (primary key), product, and code.
        """
        try:
            self.__db.execute("CREATE TABLE inventory(id INTEGER PRIMARY KEY, product TEXT UNIQUE, code TEXT UNIQUE)")
        except sqlite3.OperationalError as e:
            self.__db.rollback()
            logging.error('OperationalError({0}): Database rolled back'.format(e))
            raise
        else:
            self.__db.commit()
            logging.info('Table "inventory" created')

    def read_product(self, code):
        """
        Read a product from the databased based on a specified code.
        
        @param code: Unique ID of the product to be read
        @return:     Return the latest product selected from the database
                     according to the specified filter.
        """
        cursor = self.__db.cursor()
        cursor.execute("SELECT product FROM inventory WHERE code=?", (code,))
        record = cursor.fetchone()
        if not record:
            msg = "Product with ID {0} non-existent".format(code)
            raise RecordDoesNotExistError(msg)
        return record
    
    def insert_product(self, product):
        """
        Insert a product into the database
        
        @param product:  Product to be inserted into the database
        """
        cursor = self.__db.cursor()
        try:
            cursor.execute("INSERT INTO inventory(product, code) VALUES(?, ?)", product)
        except sqlite3.IntegrityError as e:
            self.__db.rollback()
            logging.error('IntegrityError({0}): Database rolled back'.format(e))
            raise
        else:
            self.__db.commit()
            logging.info('{0} with ID {1} inserted at index {2}'.format(product[0], product[1], cursor.lastrowid))