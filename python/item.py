import random
import string

LEN = 6
CHARS = list(string.ascii_letters)
CHARS.append(list(string.ascii_digits))

class IDGenerator(object):
	
	"""
	A generator that constructs a six character ID for items.
	"""
	
	def generate_ID(self, item):
		"""
		Create an ID for the specified item.
		
		The ID consists of six alpha-numeric characters that can be both 
		upper and lowercase. Repetition of characters is allowed.
		
		@param item:  Item whose ID is being generated
		@return:  An alpha-numeric string that is six characters long
		"""
		
		return ''.join(random.choice(CHARS) for x in xrange(LEN))

class Item(object):

	"""
	An item with a unique name and product ID from a store's inventory.
	"""
	
	def __init__(self, name, ID=None, IDGenerator=IDGenerator()):
		"""
		Initializes the item
		
		@param name:  Actual name of the item
		@param ID:  Identifier that represents the item
		"""
		self.name = name
		self.ID = IDGenerator.generate_ID()