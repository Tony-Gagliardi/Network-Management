from math import sqrt
from copy import deepcopy
import datetime


class Point(object):
	'''
	object for representing a point in 2-d space
	attributes: x-coordinate and y-coordinate
    '''

class Rectangle(object):
	'''
	object for representing a rectangle
	attributes: height, width and point of corner.
	'''
class Time(object):
	'''
	object for representing Time
	attributes: hour, minutes, seconds
	'''

def time_to_int(time):
	'''
	Function provided to us by the book
	'''
	minutes = time.hour * 60 + time.minutes
	seconds = minutes * 60 + time.seconds
	return seconds

def int_to_time(seconds):
	'''
	Function provided to us by the book
	'''
	time = Time()
	minutes, time.seconds = divmod(seconds, 60)
	time.hour, time.minutes = divmod(minutes, 60)
	return time

def distance_between_points(PointA, PointB):
	'''
	The distance_between_points function calculates the distance
	between two points using the standard distance formula. It takes
	two parameters, both of which are of type 'Point'. Solution to 
	Exercise 15.1
	'''
	distance = sqrt((PointA.x - PointB.x) ** 2 + (PointA.y - PointB.y) **2)
	print distance
def move_rectangle(rect, dx, dy):
	'''
	The move_rectangle function contains the solution to Exercise 15.2
	by moving the corner of the rectangle by the specified amounts. It
	takes three parameters which are 'rect' which is of type Rectange,
	dx which is of type int, and dy which is of type int. dx modifies
	the x-coordinate of the corner and dy modifies the y-coordinate
	of the corner
	'''
	rect.corner.x += dx
	rect.corner.y += dy
	print rect.corner.x, rect.corner.y

def print_time(time):
	'''
	The print_time function contains the solution to Exercise 16.1
	by printing out the time in the specified format. It takes one parameter
	which is of type 'Time'.
	'''
	print '%2d:%2d:%2d' % (time.hour, time.minutes, time.seconds)

def is_after(t1, t2):
	'''
	The is_after function contains the solution to Exercise 16.2
	by checking to see if t1 is chronologically after t2. It takes 
	two parameters, both of type 'Time'.
	'''
	print (t1.hour, t1.minutes, t1.seconds) > (t2.hour, t2.minutes, t2.seconds)

def increment(time, seconds):
	'''
	The increment function contains the solution to Exercise 16.3
	by using modular arithmetic to increase each attribute of time. It
	takes two parameters, time is of type 'Time' and seconds is of 
	type 'Int'.
	'''
	time.seconds += seconds
	time.minutes += time.seconds / 60
	time.hour += time.minutes / 60
	
	if time.seconds >= 60:
		time.seconds %= 60
		time.minutes += time.seconds / 60

	if time.minutes >= 60:
		time.minutes %= 60
		time.hour += time.minutes / 60
		time.hour %= 24

	print_time(time)

def increment2(time, seconds):
	'''
	The increment2 function contains the solution to Exercise 16.4
	by using the same arithmetic from the original increment function,
	except this time we are not modifying the time parameter passed in
	by using deepcopy. It takes two paramters, time is of type 'Time'
	and seconds is of type 'Int'.
	'''
	newTime = deepcopy(time)

	newTime.seconds += seconds
	newTime.minutes += newTime.seconds / 60
	newTime.hour += newTime.minutes / 60
	
	if newTime.seconds >= 60:
		newTime.seconds %= 60
		newTime.minutes += newTime.seconds / 60

	if newTime.minutes >= 60:
		newTime.minutes %= 60
		newTime.hour += newTime.minutes / 60
		newTime.hour %= 24

	print_time(newTime)

def increment3(time, seconds):
	'''
	The increment3 function contains the solution to Exercise 16.5
	by using two functions provided to us by the book to increment
	the time. It takes two parameters, time is of type 'Time'
	and seconds is of type 'Int'.
	'''
	newTime = deepcopy(time)

	newTime2 = time_to_int(newTime)
	newTime2 += seconds
	finalTime = int_to_time(newTime2)

	print_time(finalTime)

def mul_time(time, number):
	'''
	The mul_time function contains the solution to part A of 
	Exercise 16.6. It takes two parameters, time is of type 'Time'
	and number can be any number.
	'''
	newTime = deepcopy(time)

	newTime2 = time_to_int(newTime)
	newTime2 *= number
	finalTime = int_to_time(newTime2)

	print_time(finalTime)

def average_pace(time, distance):
	'''
	The average_pace function contains the solution to Part B of
	Exercise 16.6. It takes two parameters, time is of type 'Time',
	and distance is in miles. The book said to use mul_time 
	for this function, but that would only make sense if '1/distance'
	was passed in as the parameter 'distance'. Prof. Dehus gave me permission
	to write the function this way.
	'''
	finishTime = deepcopy(time)

	finishTime1 = time_to_int(finishTime)
	finishTime1 /= distance
	paceTime = int_to_time(finishTime1)

	print_time(paceTime)

def current_day():
	'''
	The current_day function contains the solution to Part 1 of 
	Exercise 16.7. It prints out the current day of the week.
	'''
	weekdays = {0 : 'Monday', 1 : 'Tuesday', 2 : 'Wednesday', 3 : 'Thursday'
				, 4 : 'Friday', 5 : 'Saturday', 6 : 'Sunday'}
	day = datetime.date.today()
	day = day.weekday()
	print 'Today is ' + weekdays[day]

def birthday_wait():
	'''
	The birthday_wait function contains the solution to Part 2 of
	Exercise 16.7. It prints out my age and the time left until
	my birthday. If you replace the attributes of 'birthday' with
	your own, you can find out yours!
	'''
	today = datetime.datetime.today()
	birthday = datetime.datetime(1993, 4, 1, 20, 40, 10)
	age = today - birthday
	years = age.days
	years /= 365.242
	years = int(years)
	print 'I am ' + str(years) + ' ' + 'years old' 

	upcomingBirthday = datetime.datetime(today.year, birthday.month, 
		                birthday.day, birthday.hour, birthday.minute
		                , birthday.second)
	timeLeft =  upcomingBirthday - today
	print ('There are ' + str(timeLeft) + ' ' + 'until my birthday!')


def main():
	point0 = Point()
	point0.x = 3
	point0.y = 5

	point1 = Point()
	point1.x = 9
	point1.y = 10
	distance_between_points(point0, point1)

	rect = Rectangle()
	rect.width = 25.0
	rect.heigth = 17.0
	rect.corner = Point()
	rect.corner.x = 1
	rect.corner.y = 1
	move_rectangle(rect, 6, 8)

	time0 = Time()
	time0.hour = 17
	time0.minutes = 25
	time0.seconds = 51
	print_time(time0)
	time1 = Time()
	time1.hour = 11
	time1.minutes = 27
	time1.seconds = 33
	is_after(time0, time1)

	increment(time0, 3000)
	increment2(time1, 3600)

	increment3(time1, 3601)
	mul_time(time1, 2)
	average_pace(time1, 60)

	current_day()
	birthday_wait()

main()