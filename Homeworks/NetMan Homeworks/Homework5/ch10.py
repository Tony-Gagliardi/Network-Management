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