import urllib
import pdb

def is_sorted(list1):
	'''
	This function contains the solution
	to exercise 10.6. It checks to see
	if a list is sorted in ascending order.
	It takes one parameter, which is of type
	'list'
	'''	
	for i in range(len(list1) - 1):
		if list1[i] <= list1[i + 1]:
			continue
		else:
			return False
	return True

def has_duplicates(list2):
	'''
	This function contains the solution
	to exercise 10.8. It checks to see
	if an element appears more than once
	in a list. It takes one parameter, which
	is of type 'list'
	'''
	tempList = list2[:]
	tempList.sort()
	for i in range(len(tempList) - 1):
		if tempList[i] != tempList[i + 1]:
			continue
		else:
			return True
	return False

def has_duplicates2(list3):
	'''
	This function contains the solution
	to exercise 11.9. It is the same as
	the solution to exercise 10.8, but it
	uses a dictionary to make the function
	more efficient and simpler. NOTE: I
	referenced the books solution to help
	me solve this problem.
	'''
	dictionary = { }
	for i in range(len(list3)):
		if list3[i] in dictionary:
			return True
		else:
			dictionary[i] = list3[i]
	return False

def zipcode_info(zipcode):
	'''
	This function contains the solution
	to exercise 14.6. It reaches out to
	an external URL that contains data
	on zip codes. It then prints out the 
	population data and city name. It takes
	one parameter which is provided by the
	user, and is the zip code in questions.
	I am not sure how to parse HTML in Python
	so the information returned is not clean.
	NOTE: I referenced the solution provided 
	by the book for help with this problem.
	'''
	path = 'http://uszip.com/zip/' + zipcode
	conn = urllib.urlopen(path)
	for line in conn.readlines():
		line = line.strip()
		if 'Total population' in line:
			print line
		if 'is the ZIP code for' in line:
			print line


def main():
	print is_sorted([1,2,2])
	print is_sorted(['b', 'a'])
	print has_duplicates(['a', 'b', 'f', 'd', 'q'])
	print has_duplicates([1,2,4,1])
	print has_duplicates2(['a', 'b', 'f', 'd', 'q'])
	print has_duplicates2([1,2,4,1])
	zipcode_info(raw_input("Please enter zip code: "))
main()