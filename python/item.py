import random
import string

LEN = 6
CHARS = list(string.ascii_letters)
CHARS.append(list(string.ascii_digits))

class CodeGenerator(object):
	
	"""
	A generator that constructs a six character code for items.
	"""
		
	def generate_code(self):
		"""
		Create an item's code.
		
		The code consists of six alphanumeric characters that can be both 
		upper and lowercase. Repetition of characters is allowed.
		
		@return:  An alphanumeric string that is six characters long
		"""
		
		return ''.join(random.choice(CHARS) for x in xrange(LEN))