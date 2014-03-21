import tftpy
import os
import shutil
import pdb

getVersion = open('version.txt', 'r')
version = getVersion.readlines()
version = version[-1].strip()

def prompt_user():
	'''
	The prompt_user function prompts the user for IP's
	'''
	loop = True
	IPList = []
	while (loop == True):
		IP = raw_input("Enter Management IP (or done): ")
		if IP == 'done':
			loop = False
		else:
			IPList.append(IP)
			continue
	return IPList

def fetch_config(IPList):
	'''
	The fetch_config function pulls the startup config file from
	the specified TFTP client. It takes the IPList as a parameter
	which is of type list.
	'''
	for i in range(len(IPList)):
		connection = tftpy.TftpClient(IPList[i], 69)
		if os.path.exists(IPList[i] + 'startup-configv' + version ):
			connection.download('/startup-config', IPList[i] + 'tmp_startup-configv' + version)
			config_diff(IPList, version)
		else:
			connection.download('/startup-config', IPList[i] + 'startup-configv' + version)		


def parse_config(IPList, i, version):
	'''
	The parse_config function extracts the hostname and version
	from the startup config file. It takes the following paramters:
	IPList of type list, i which is just our iterator from main, 
	and version which is of type character, extracted from our
	version.txt file.
	'''
	nextVersion = int(version) + 1
	nextVersion = str(nextVersion)
	if os.path.exists(IPList[i] + 'startup-configv' + nextVersion):
		f = open(IPList[i] + 'startup-configv' + nextVersion, 'r')
		config = f.readlines()
	elif os.path.exists(IPList[i] + 'startup-configv' + version):
		g = open(IPList[i] + 'startup-configv' + version, 'r')
		config = g.readlines()
	for line in config:
		if 'hostname' in line:
			line = line.strip()
			line = line.split(" ")
			hostname = line[1]
		if 'version' in line:
			line2 = line.strip()
			line2 = line.split(" ")
			version = line2[1]
	hnv = [hostname, version]
	return hnv


def print_results(results, IPList):
	'''
	The function print_results prints the results of the program
	to the user. It takes the parameter 'results' which is a list that
	contains the extracted hostname and version. It also takes the
	IPList which is of type list. 
	'''
	for i in range(len(IPList)):
		print 'Saving new config for ' + IPList[i] + '(' + results[0] + ')' + 'running IOS version ' + results[1]



def config_diff(IPList, version):
	'''
	The function config_diff compares the new file to the latest
	version on record to see if any changes have occurred and reacts
	accordingly. It takes IPList as a parameter which is of type list
	and it takes version which is of type character.
	'''
	i = 1
	for i in range(len(IPList)):
		f = open(IPList[i] + 'startup-configv' + version)
		t = open(IPList[i] + 'tmp_startup-configv' + version)
		previous = f.readlines()
		current = t.readlines()
		f.close()
		t.close()
		j = 0
		while j<len(previous)-1:
			j += 1
			if previous[j] != current[j]:
				nextVersion = int(version) + 1
				nextVersion = str(nextVersion)
				shutil.copyfile(IPList[i] + 'tmp_startup-configv' + version, IPList[i] + 'startup-configv' + nextVersion)
				rmpath = IPList[i] + 'tmp_startup-configv' + version
				os.remove(rmpath)
				v = open('version.txt', 'w')
				v.write(nextVersion)
				break
			else: 
				continue
			j += 1		
	if os.path.exists(IPList[i] + 'tmp_startup-configv' + version):
		rmpath2 = IPList[i] + 'tmp_startup-configv' + version
		os.remove(rmpath2)

def main():
	#connection = tftpy.TftpClient('192.168.0.1', 69)
	#connection.download('/startup-config', 'tmp_startup-config')
	IPs = prompt_user()
	fetch_config(IPs)
	for i in range(len(IPs)):
		result = parse_config(IPs, i, version)
	print_results(result, IPs)
if __name__ == '__main__':
	main()