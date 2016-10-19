## atmosphere.py ###############################################################
## play a stack of mp3 files simultaneously ####################################
## to recreate videogame atmosphere ############################################
################################################################################
import pygame
from sys import argv
import csv

def getFilesList(environmentFileName):
	output = []
	
	with open('./envfiles/%s' % (environmentFileName), 'rb') as foo:
		reader = csv.reader(foo)
		for row in reader:
			output.append([row[0], int(row[1])])
			## 0 is filename, 1 is integer volume		
	return output


if(__name__ == "__main__"):
	debugInfo = True
	
	envFileName = argv[1]
	
	pygame.init()
	
	pygame.display.set_mode((400,110))
	
	pygame.mixer.init()
	pygame.mixer.pre_init(44100, -16, 2, 2048)
	
	sounds = []
	
	if(debugInfo):
		print getFilesList(envFileName)
	for sFile in getFilesList(envFileName):
		newSound = pygame.mixer.Sound('./data/%s' % sFile[0])
		decVolume = float(sFile[1]/100.0)
		print decVolume
		newSound.set_volume(decVolume)
		newSound.play()
		sounds.append(newSound)
	if(debugInfo):
		print "Finished loading %i sounds" % len(getFilesList(envFileName))
		
	for sound in sounds:
		sound.play()
		
	clock = pygame.time.Clock()
	clock.tick(10)
	while(True):
		pygame.event.poll()
		clock.tick(10)	
		
