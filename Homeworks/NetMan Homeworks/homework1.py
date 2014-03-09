# Note to Grader: The end of each exercise has commented
# out test cases that can be used for code validation.

import math
import string

# Exercise 6.2
# Stage 1 I developed the function skeleton
# Then I imported the math library
# Then I wrote out the calculation for the hypotenuse
# Then I tested to make sure my logic was correct
# Finally, I made sure it was working correctly with calls
# to the function

def hypotenuse(legA, legB):
	hyp = math.sqrt((legA*legA) + (legB*legB))
	return hyp

#print hypotenuse(3,4)
#print hypotenuse(6,8)
# end Exercise 6.2

# Exercise 7.4
def eval_loop():
	loop = True
	while(loop == True):
		string = eval(str(raw_input("Enter statement here, type 'done' when finished: ")))
		if (string == 'done'):
			loop = False
			print string2
		else:
			loop = True
			print string
			string2 = string

#eval_loop()
# end Exercise 7.4

# Exercise 8.1
def reverse_str(string):
	i = len(string) - 1
	while i >= 0:
		letter = string[i]
		print letter
		i -= 1

#reverse_str("tails")
#reverse_str("colorado")
# end Exercise 8.1

# Exercise 8.3
# Given that fruit is a string, fruit[:] means the entire string. This syntax
# is called string slicing, but since a slice range has not been given
# it will just print out the entire string.

# Exercise 8.10
def is_palindrome(word):
	print "Yes" if (word[::-1] == word) else "No"

# is_palindrome("hannah")
# is_palindrome("Colorado")
# end Exercise 8.10

# Exercise 8.12
# NOTE: I referenced the solution provided by the author to solve this problem
# at http://www.greenteapress.com/thinkpython/code/rotate.py	
def rotate_word(word, shift):
	# make the input lowercase
	word = word.lower()
	shifted_string = ''
	for letter in word:
		# set the start to the numeric code of 'a'
		baseline = ord('a')
		# find the position in the alphabet of the letter
		position = ord(letter) - baseline
		# find the appropriate replacemet letter based on shift
		shifter = (position + shift) % 26 + baseline
		# convert the numeric code back to the character
		shifted_string += chr(shifter)
	print shifted_string

#rotate_word('cheer', 7)
#rotate_word('melon', -10)
#rotate_word('PYTHON', 17)
# end Exercise 8.12
	


