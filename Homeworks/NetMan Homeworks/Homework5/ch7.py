import string

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
