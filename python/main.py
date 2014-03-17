__author__  = 'Steven Briggs'
__version__ = '2014.03.15'

import inventory
from inventory import InventoryDatabase
import codecs
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
    while not file:
        filename = raw_input(prompt)
        try:
            file = codecs.open(filename, 'rU')
        except FileNotFoundError as e:
            print 'File {0} not found.'.format(file)
        else:
            return file
 
def main():
    print "Welcome to the Inventory Tracker."
    
    productList = findFile("Enter a file with products to track: ")
    theInventory = InventoryDatabase()
    
    for name in productList:
        productNameExists = theInventory.readID(name)
        if productNameExists:
            continue
            
        ID = ''
        productIDExists = True
        while productIDExists:
            ID = generateID()
            productIDExists = theInventory.readProductName(ID)
        
        theInventory.insertProduct((name, ID))
    
    finished = False
    while not finished:
        ID = raw_input('Enter an ID to retrieve the corresponding product: ')
        productName = theInventory.readProductName(ID)
        if productName:
            print productName
        else:
            print 'Invalid ID. A product with ID {0} does not exist.'.format(ID)
    
    theInventory.closeConnection()
            
if __name__ == '__main__':
    main()