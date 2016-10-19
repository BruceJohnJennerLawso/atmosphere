## atmosphere.py ###############################################################
## play a stack of mp3 files simultaneously ####################################
## to recreate videogame atmosphere ############################################
################################################################################
import pygame
from sys import argv


def getFilesList(environmentFileName):
	output = []
	
	with open('./envfiles/%s' % (environmentFileName), 'rb') as foo:
		reader = csv.reader(foo)
		for row in reader:
			output.append([row[0], int(row[1])])
			## 0 is filename, 1 is integer volume		
	return output


if(__name__ == "__main__"):
	envFileName = argv[1]
	
	pygame.mixer.init()
	pygame.mixer.pre_init(44100, -16, 2, 2048)
	pygame.init()
	
	sounds = []
	for sFile in getFilesList(envFileName):
		newSound = pygame.mixer.Sound('./data/%s' % sFile[0])
		newSound.set_volume(float(sFile[1]/100.0))
		sounds.append(newSound)
		
	for sound in sounds:
		sound.play()
