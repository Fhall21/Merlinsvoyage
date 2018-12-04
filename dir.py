import os


def ensure_dir(directory):
	if not os.path.exists(directory):
		os.makedirs(directory)

#setup
month_num = 10
ensure_dir('C:/Users/VicFel/Documents/Programming/merlinsvoyage/10/')
print ('done')