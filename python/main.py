#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__  = 'Steven Briggs'
__version__ = '2014.03.15'

import inventory
from inventory import InventoryDatabase
import string
import random

CHARS = string.ascii_letters + string.digits
LEN = 6

def generateID():
    """
    Generate a sequence of six alphanumeric characters and return them.
    
    @return:  String of six characters choosen at random
    """
    return ''.join(random.choice(CHARS) for i in xrange(LEN))

def findFile(prompt):
    """
    Open a file by continually prompting the user until a valid filename
    is entered
    
    @param prompt:  Message to prompt the user for input
    @return:  Return a file object once it is successfully opened
    """
    file = None
    # Continue to prompt for a valid file until the user provides one
    while not file:
        filename = raw_input(prompt).strip()
        try:
            file = open(filename, 'rU')
        except IOError:
            print 'File {0} not found.'.format(filename)
        else:
            return file

def insertProducts(productList, theInventory):
    """
    Insert all products (product name, ID) into the database acting as
    an inventory
    
    @param productList:  File containing a list of product names
    @param theInventory: InventoryDatabase where products are stored
    """
    print 'Adding products to the inventory...'
    numAdded = 0
    for productName in productList:
        productNameExists = theInventory.readID(productName)
        # Determine if the product name provided already exists within
        # the specified inventory. If it does, then stop attempting to
        # insert this product and move to the next one.
        if productNameExists:
            continue
            
        ID = ''
        productIDExists = True
        # Since we know the product is not within the inventory, 
        # we must continue generating IDs for it until we find a unique one.
        while productIDExists:
            ID = generateID()
            productIDExists = theInventory.readProductName(ID)
        
        theInventory.insertProduct((productName, ID))
        numAdded = numAdded + 1
    
    print '{0} products added to the inventory'.format(numAdded)
    productList.close()    
            
def main():
    """
    Run the Inventory Tracker program
    """
    print 'Welcome to the Inventory Tracker.'
    
    theInventory = InventoryDatabase()
    numProducts = theInventory.getNumProducts()
    
    if numProducts > 0:
        print '{0} products in the inventory.'.format(numProducts)
    else:
        print '0 products in the inventory.'
    
    prompt = 'Provide a file to add products to the inventory? (Y/N) '
    getFile = raw_input(prompt).strip().lower()
    
    if getFile == 'y':
        # Prompt the user for a file of products and then open it
        productList = findFile('Enter a file to add products to the inventory: ')
        # Insert all the products found in productList into the inventory
        insertProducts(productList, theInventory)
    
    # Continually prompt the user to enter an ID for a product.
    # If the ID is valid, then print the corresponding product name.
    finished = False
    while not finished:
        ID = raw_input('Enter an ID to retrieve a product: ').strip()
        productName = theInventory.readProductName(ID)
        if productName:
            productName = productName[0].rstrip('\n')
            print productName
        else:
            print 'Invalid ID. A product with ID {0} does not exist'.format(ID)
        # Check if the user is ready to exit or not
        decision = raw_input('Exit? (Y/N) ').strip().lower()
        if decision == 'y':
            finished = True
            
    theInventory.closeConnection()
    exit(0)
            
if __name__ == '__main__':
    main()