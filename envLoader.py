## envLoader.py ################################################################
## the function used to get a list of data lists for a given ###################
## environment file name #######################################################
################################################################################
import csv


## returns a list of lists, where the first three values of each sublist are the
## filename (relative to the data folder), the volume, and the sound type
## ('music', 'short', 'background')

def getFilesList(environmentFileName):
	output = []
	
	##with open('./envfiles/%s' % (environmentFileName), 'rb') as foo:
	with open('%s' % (environmentFileName), 'rb') as foo:
		reader = csv.reader(foo)
		for row in reader:
			output.append([row[0], int(row[1]), row[2]])
			## 0 is filename,
			## 1 is integer volume 0-100,
			## 2 is type (background, short, music...)	
	return output
