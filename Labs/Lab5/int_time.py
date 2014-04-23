import datetime
import time

class Time(object):
	pass

def int_to_time(seconds):
	'''
	This was taken from a previous homework to convert seconds
	into a readable time value.
	'''
	t1 = time.gmtime(seconds)
	return '%2d:%2d:%2d:%2d:%2d:%2d' % (t1.tm_year, t1.tm_mon, t1.tm_mday, t1.tm_hour, t1.tm_min, t1.tm_sec)