## atmosphere.py ###############################################################
## play a stack of mp3 files simultaneously ####################################
## to recreate videogame atmosphere ############################################
################################################################################
import pygame
from sys import argv
import multiprocessing as mp
import random

from Tkinter import Tk
from tkFileDialog import askopenfilename

import sound
import envLoader


def getFillColour(currentFillGreen, loadFinished):
	if(loadFinished):
		if(currentFillGreen > 0):
			currentFillGreen -= 1


if(__name__ == "__main__"):
	

	Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
	filename = askopenfilename(initialdir='./envfiles') # show an "Open" dialog box and return the path to the selected file
	print(filename)
	envFileName = filename
	
	version = 0.1
	debugInfo = True
	
	
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
	shortSounds = []
	musicSounds = []
	
	
	try:
		if(debugInfo):
			print envLoader.getFilesList(envFileName)
		
		for sFile in envLoader.getFilesList(envFileName):
			decVolume = float(sFile[1]/100.0)

			if(sFile[2] == 'background'):
				sounds.append(sound.Sound('./data/%s' % sFile[0], decVolume, sFile[2]))
			elif(sFile[2] == 'short'):
				shortSounds.append(sound.Sound('./data/%s' % sFile[0], decVolume, sFile[2]))				
			elif(sFile[2] == 'music'):
				musicSounds.append(sound.Sound('./data/%s' % sFile[0], decVolume, sFile[2]))	
				## in order, the sound object, and how many times its been played
	except TypeError:
		print "No env file selected, exiting..."
		exit()		
			
	if(debugInfo):
		print "Finished loading %i sounds" % len(envLoader.getFilesList(envFileName))
	
	
	
	firstRandomChoice = random.choice(sounds)
	secondRandomChoice = random.choice(sounds)
	while(firstRandomChoice == secondRandomChoice):
		secondRandomChoice = random.choice(sounds)
		## keep trying until we get two different sounds
	
	firstRandomChoice.loadSound()
	secondRandomChoice.loadSound()
	
	background1.play(firstRandomChoice.getSound())
	background2.play(secondRandomChoice.getSound())	
	
	firstRandomChoice.incrementPlayCounter()
	secondRandomChoice.incrementPlayCounter()
	
	randomMusic = random.choice(musicSounds)
	## small thing that could be changed here, a quick check to make sure
	## the same sound isnt playing back to back.
	
	## its not very likely, but on a small playlist it would be annoying
	randomMusic.loadSound()
	music.play(randomMusic.getSound())
		
	clock = pygame.time.Clock()
	clock.tick(10)
	while(True):
		
		for event in pygame.event.get():
			if(event.type == pygame.QUIT):
				print "pygame.QUIT event heard"
				break
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					pass
				if event.key == pygame.K_RIGHT:
					print "pygame.K_RIGHT event heard"
					music.fadeout(1000)
					## this is much simpler, just fadeout the current track,
					## and the main loop will put on a new track
					
		pygame.event.poll()
		clock.tick(10)	
		if(not music.get_busy()):
			## music has finished, need to put another track on
			randomMusic.clearSound()
			## clear the current music track from memory so we dont bleed all
			## over the ram
			randomMusic = random.choice(musicSounds)
			## randomly choose a new music track
			randomMusic.loadSound()
			music.play(randomMusic.getSound())
			randomMusic.incrementPlayCounter()
		if(not background1.get_busy()):		
			## background sound on channel 1 has finished,
			## need to put another track on
			firstRandomChoice.clearSound()
			firstRandomChoice = random.choice(sounds)
			while(firstRandomChoice == secondRandomChoice):
				firstRandomChoice = random.choice(sounds)
			## pick something randomly out of the list and make sure it isnt
			## the same track already playing on the other background noise
			## channel
			firstRandomChoice.loadSound()
			background1.play(firstRandomChoice.getSound())
			firstRandomChoice.incrementPlayCounter()			
		if(not background2.get_busy()):		
			## background sound on channel 2 has finished,
			## need to put another track on
			
			secondRandomChoice = random.choice(sounds)
			while(secondRandomChoice == firstRandomChoice):
				secondRandomChoice = random.choice(sounds)
			## pick something randomly out of the list and make sure it isnt
			## the same track already playing on the other background noise
			## channel
			secondRandomChoice.loadSound()
			background2.play(secondRandomChoice.getSound())	
			secondRandomChoice.incrementPlayCounter()




