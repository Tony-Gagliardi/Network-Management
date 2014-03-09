import ch6
import ch7
import ch8
import ch10
import ch14

def main():
	while (True):
		select = raw_input('Please enter which exercise you would like to run, or type exit to finish: ')
		if select == '6.2':
			print 'This exercise calculates the hypotenuse of a triangle'
			legA = int(raw_input('Please enter the first leg: '))
			legB = int(raw_input('Please enter the second leg: '))
			ch6.hypotenuse(legA, legB)
		elif select == '7.4':
			print 'This exercise evalutes expressions using the eval function'
			ch7.eval_loop()
		elif select == '8.1':
			print 'This exercise reverses a string'
			string = raw_input('Please enter a word to be reversed: ')
			ch8.reverse_str(string)
		elif select == '8.12':
			print 'This exercise simulates ROT encryption'
			word = raw_input('Please enter a word to be diffused: ')
			shift = int(raw_input('Please enter a numeric value to shift by: '))
			ch8.rotate_word(word, shift)
		elif select == '9.1':
			print 'Exercise not completed this semester, please try again'
		elif select == '10.6':
			print 'This exercise checks to see if a list is sorted'
			usr_list = []
			loop = True
			while (loop == True):
				list_element = (raw_input("Please enter a list element, type exit to finish: "))
				if list_element == 'exit':
					loop = False
				else: 
					usr_list.append(list_element)
			result = ch10.is_sorted(usr_list)
			if result == True:
				print 'The list is sorted'
			else:
				print 'The list is NOT sorted'
		elif select == '14.6':
			print 'This exercise provides additional info about a zipcode'
			zipcode = raw_input('Please enter a zipcode: ')
			ch14.zipcode_info(zipcode)
		elif select == 'exit':
			return False
		else:
			print 'Selection not found, please try again'
if __name__ == '__main__':
	main()
