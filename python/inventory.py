#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__  = 'Steven Briggs'
__version__ = '2014.03.15'

import sqlite3
import logging

DB_NAME = 'inventory.sqlite3'

# Create a file to log information about database operations
logging.basicConfig(
     filename='inventory.log',
     level=logging.INFO,
     format='%(levelname)s:%(asctime)s:%(message)s')

class InventoryDatabase(object):
    """
    Creates a SQLite3 database of products and their unique identifiers.
    """
    def __init__(self, __db=None):
        """
        Initialize the InventoryDatabase
        
        @__db:  Database containing products and their IDs
        """
        self.__db = self.openConnection()
        self.__db.text_factory = str
        self.createInventory()
        
    def openConnection(self):
        """
        Establish a connection with the product database
        
        @return:  Return the Connection to the database of products
        """
        return sqlite3.connect(DB_NAME)
    
    def closeConnection(self):
        """
        Close the connection with the product database
        """
        self.__db.close()
    
    def createInventory(self):
        """
        Create a table in the database called 'inventory' with the columns
        id (primary key), name, and code.
        """
        query = 'CREATE TABLE inventory(id INTEGER PRIMARY KEY, \
            name TEXT UNIQUE, code TEXT UNIQUE)'
        try:
            self.__db.execute(query)
        except sqlite3.OperationalError as e:
            self.__db.rollback()
            logging.error('OperationalError({0}): Rolled back'.format(e))
        else:
            self.__db.commit()
            logging.info('Table "inventory" created')
    
    def __readFromInventory(self, col, filter, value):
        """
        Read a row from the inventory database by building a query 
        according to specified values
        AQ
        @param col:    Column to read from
        @param filter: Column to filter results by
        @param value:  Actual value to filter by
        @return:       Returns the row that meets the specified query
        """
        cursor = self.__db.cursor()
        query = 'SELECT {0} FROM inventory WHERE {1}=?'.format(col, filter)
        cursor.execute(query, (value,))
        row = cursor.fetchone()
        return row

    def readProductName(self, ID):
        """
        Read a product name from the database based on a specified ID.
        
        @param ID: Unique ID of the product to be read
        @return:   Return the latest product name selected from the database
                   according to the specified filter.
        """
        return self.__readFromInventory('name', 'code', ID)
        
    def readID(self, name):
        """
        Read an ID from the database based on a specified product name.
        
        @param product: Name of the product whose ID is to be read
        @return:        Return the latest ID selected from the database
                        according to the specified filter.
        """
        return self.__readFromInventory('code', 'name', name)
    
    def insertProduct(self, product):
        """
        Insert a product (tuple of name and ID) into the database
        
        @param product:  The product to be inserted in the inventory
        """
        cursor = self.__db.cursor()
        query = 'INSERT INTO inventory(name, code) VALUES(?, ?)'
        try:
            cursor.execute(query, product)
        except sqlite3.IntegrityError as e:
            self.__db.rollback()
            logging.error('IntegrityError({0}): Rolled back'.format(e))
            raise
        else:
            self.__db.commit()
            logging.info('{0} with ID {1} inserted at \
                index {2}'.format(product[0], product[1], cursor.lastrowid))
    
    def getNumProducts(self):
        """
        Return the number of products currently in the inventory.
        
        @return:  Number of products currently in the inventory.
        """
        cursor = self.__db.cursor()
        cursor.execute('SELECT max(id) FROM inventory')
        return cursor.fetchone()[0]