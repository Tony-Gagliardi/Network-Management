import netsnmp as snmp
import time

def main():
	output = open('/tmp/traps', 'a')
	running = True
	while running:
		try:
			input = raw_input()
			output.write(input + "\n")
		except EOFError:
			running = False
	output.close()

if __name__ == '__main__':
	main()

