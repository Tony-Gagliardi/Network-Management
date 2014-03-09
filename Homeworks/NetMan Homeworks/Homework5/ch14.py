import urllib

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