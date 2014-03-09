import copy
import pdb

class Point(object):
	'''
	This init method contains the solution to Exercise
	17.2. It has two optional parameters, an x and a y 
	coordinate, if not given they are initialized to zero
	'''
	def __init__(self, x = 0, y = 0):
		self.x = x
		self.y = y

	def __str__(self):
		'''
		Method for Exercise 17.3, returns a string
		representation of my point object
		'''
		return '(%.2d, %.2d)' % (self.x, self.y)

	def __add__(self, other):
		'''
		Method for Exercise 17.4, returns a new point
		containing the sum of two points' respective
		coordinates. Also method for Exercise 17.5,
		allows two points to be added together, as well
		as a point and a tuple.
		'''
		if isinstance(other, Point):
			newPoint = copy.deepcopy(self)
			newX = newPoint.x + other.x
			newY = newPoint.y + other.y
			newPoint.x = newX
			newPoint.y = newY
			return newPoint
		else:
			newPoint2 = copy.deepcopy(self)
			xtuple = newPoint2.x + other[0]
			ytuple = newPoint2.y + other[1]
			newPoint2.x = xtuple
			newPoint2.y = ytuple
			return newPoint2

	def print_point(self):
		'''
		Helper method for printing out Point objects
		for Exercise for 17.2.
		'''
		print '(%.2d, %.2d)' % (self.x, self.y)

class Kangaroo(object):
	'''
	The following methods contain the solution
	to Exercise 17.7. I reviewed the code provided
	by Downey to discover the bug, which has to do with
	assigning mutable types as default values for attributes
	'''
	def __init__(self, pouch_contents = None):
		'''
		The init method has one optional paramter,
		which is the pouch contents. If the contents
		are not provided, an empty list is 
		initialized
		'''
		if pouch_contents == None:
			pouch_contents = []
		self.pouch_contents = pouch_contents

	def __str__(self):
		'''
		The str method takes a Kangaroo object and
		prints its location in memory, as well
		as any objects that its pouch contains. I
		used Downey's solution to help complete this
		method
		'''
		string = [object.__str__(self) + 'has: ']
		for obj in self.pouch_contents:
			s = ' ' + object.__str__(obj)
			string.append(s)
		return '\n'.join(string)

	def put_in_pouch(self, other):
		'''
		The put_in_pouch method adds any object
		to the pouch_contents list
		'''
		return self.pouch_contents.append(other)

def print_attributes(obj):
	'''
	Useful function provided by Downey for 
	debugging purposes.
	'''
	for attr in obj.__dict__:
		print attr, getattr(obj, attr)

def main():
	# Exercise 17.2
	pointA = Point(1)
	pointB = Point(3, 5)
	pointA.print_point()
	pointB.print_point()
	# Exercise 17.3
	pointC = Point(8, 13)
	print pointC
	#Exercise 17.4
	print pointB + pointC
	#Exercise 17.5
	print pointB + pointC
	print pointB + (2, 6)
	#Exercise 17.7
	kanga = Kangaroo()
	roo = Kangaroo()
	kanga.put_in_pouch('minikanga')
	kanga.put_in_pouch('baseball')
	kanga.put_in_pouch(roo)
	roo.put_in_pouch('bottle')
	print kanga
	print roo
main()