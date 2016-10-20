## atmosphere.py ###############################################################
## play a stack of mp3 files simultaneously ####################################
## to recreate videogame atmosphere ############################################
################################################################################
import pygame
from sys import argv
import csv
import multiprocessing as mp
import random

def getFilesList(environmentFileName):
	output = []
	
	with open('./envfiles/%s' % (environmentFileName), 'rb') as foo:
		reader = csv.reader(foo)
		for row in reader:
			output.append([row[0], int(row[1]), row[2]])
			## 0 is filename, 1 is integer volume		
	return output

def getFillColour(currentFillGreen, loadFinished):
	if(loadFinished):
		if(currentFillGreen > 0):
			currentFillGreen -= 1


if(__name__ == "__main__"):
	
	version = 0.1
	debugInfo = True
	
	envFileName = argv[1]
	
	pygame.init()
	
	pygame.mixer.init()
	
	
	screen = pygame.display.set_mode((400,110))
	pygame.display.set_caption("atmosphere %s" % version)
	
	screen.fill((0,200,0))
	
	
	pygame.mixer.pre_init(44100, -16, 2, 2048)
	pygame.mixer.init()
	
	music = pygame.mixer.Channel(5)
	background1 = pygame.mixer.Channel(3)
	background2 = pygame.mixer.Channel(4)
	
	sounds = []
	musicSounds = []
	
	if(debugInfo):
		print getFilesList(envFileName)
		
	
	for sFile in getFilesList(envFileName):
		newSound = pygame.mixer.Sound('./data/%s' % sFile[0])
		decVolume = float(sFile[1]/100.0)
		print decVolume
		newSound.set_volume(decVolume)
		##newSound.play()
		if(sFile[2] == 'background'):
			sounds.append([newSound, 0])
		elif(sFile[2] == 'music'):
			musicSounds.append([newSound, 0])	
			## in order, the sound object, and how many times its been played
	
	if(debugInfo):
		print "Finished loading %i sounds" % len(getFilesList(envFileName))
	
	
	
	firstRandomChoice = random.choice(sounds)
	secondRandomChoice = random.choice(sounds)
	while(firstRandomChoice == secondRandomChoice):
		secondRandomChoice = random.choice(sounds)
		## keep trying until we get two different sounds
	firstRandomChoice[1] += 1
	secondRandomChoice[1] += 1
	
	background1.play(firstRandomChoice[0])
	background2.play(secondRandomChoice[0])	
	
	randomMusic = random.choice(musicSounds)
	randomMusic[1] += 1 
	music.play(randomMusic[0])
		
	clock = pygame.time.Clock()
	clock.tick(10)
	while(True):
		pygame.event.poll()
		clock.tick(10)	
		if(not music.get_busy()):
			## music has finished, need to put another track on
			randomMusic = random.choice(musicSounds)
			randomMusic[1] += 1 
			music.play(randomMusic[0])









