## envLoader.py ################################################################
## the function used to get a list of data lists for a given ###################
## environment file name #######################################################
################################################################################
import csv


def getFilesList(environmentFileName):
	output = []
	
	##with open('./envfiles/%s' % (environmentFileName), 'rb') as foo:
	with open('%s' % (environmentFileName), 'rb') as foo:
		reader = csv.reader(foo)
		for row in reader:
			output.append([row[0], int(row[1]), row[2]])
			## 0 is filename, 1 is integer volume		
	return output
