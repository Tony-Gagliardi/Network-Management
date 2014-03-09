# Exercise 8.1
def reverse_str(string):
	i = len(string) - 1
	while i >= 0:
		letter = string[i]
		print letter
		i -= 1

# Exercise 8.12	
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