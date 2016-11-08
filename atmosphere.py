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
import jukebox

def getFillColour(currentFillGreen, loadFinished):
	if(loadFinished):
		if(currentFillGreen > 0):
			currentFillGreen -= 1


if(__name__ == "__main__"):
	

	Tk().withdraw()
	## we don't want a full GUI, so keep the root window from appearing
	filename = askopenfilename(initialdir='./envfiles')
	## show an "Open" dialog box and return the path to the selected file
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
		
	try:
		if(debugInfo):
			print envLoader.getFilesList(envFileName)
		
		atmosphericJukebox = jukebox.Jukebox(envFileName, debugInfo)
	except TypeError:
		print "No env file selected, exiting..."
		exit()		
			
	if(debugInfo):
		print "Received %i sounds" % len(envLoader.getFilesList(envFileName))
		print "%i background tracks, %i short sounds, %i music tracks" % (len(atmosphericJukebox.sounds), len(atmosphericJukebox.shortSounds), len(atmosphericJukebox.musicSounds))
	
	atmosphericJukebox.play()
	
		
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
					atmosphericJukebox.nextMusicTrack(1000)
					## this is much simpler, just fadeout the current track,
					## and the main loop will put on a new track
					
		pygame.event.poll()
		clock.tick(10)	
		atmosphericJukebox.loop()

