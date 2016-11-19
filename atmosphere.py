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
	
	
	blue=(0,0,255)
	green=(0,200,120)
	red=(170,0,0)


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
	
	
	screen = pygame.display.set_mode((440,120))
	pygame.display.set_caption("atmosphere %s" % version)
	
	##screen.fill((0,200,0))
	
	
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
	
	
	unpauseTriangle = [[10, 10], [25, 20],[ 10, 30]]
	
	while(not atmosphericJukebox.exitSignal):
		screen.fill((0,0,0))
		pygame.draw.rect(screen,blue,(120,0,20,2.0*atmosphericJukebox.countdownToNextShortSound()))		
		pygame.draw.rect(screen,blue,(150,(100-100*atmosphericJukebox.getBackgroundVolume()),50,10))
		pygame.draw.rect(screen,green,(225,(100-100*atmosphericJukebox.getMusicVolume()),50,10))
		pygame.draw.rect(screen,blue,(300,(100-100*atmosphericJukebox.getShortSoundVolume()),50,10))
		pygame.draw.rect(screen,red,(380,(100-100*atmosphericJukebox.getMasterVolume()),20,10))		
		if(atmosphericJukebox.isMusicPaused() == True):
			pygame.draw.polygon(screen,blue,unpauseTriangle, 0)
		for event in pygame.event.get():
			
			def isBetween(value, lower, upper):
				if((value >= lower)and(value <= upper)):
					return True
				return False	
				
			if event.type == pygame.MOUSEBUTTONDOWN:
				if(event.button == 1):
					if(atmosphericJukebox.isMusicPaused() == True):
						if(isBetween(pygame.mouse.get_pos()[0], unpauseTriangle[0][0],unpauseTriangle[1][0])):
							if(isBetween(pygame.mouse.get_pos()[1], unpauseTriangle[0][1],unpauseTriangle[2][1])):
								## Yes this is a box, but it wont be too far off
								atmosphericJukebox.togglePauseState()
				elif(event.button == 4):
					## scroll wheel up
					if(isBetween(pygame.mouse.get_pos()[0], 150,200)):
						atmosphericJukebox.incrementBackgroundVolume(0.1)
					elif(isBetween(pygame.mouse.get_pos()[0], 225,275)):
						atmosphericJukebox.incrementMusicVolume(0.1)
					elif(isBetween(pygame.mouse.get_pos()[0], 300,350)):	
						atmosphericJukebox.incrementShortSoundVolume(0.1)
					elif(isBetween(pygame.mouse.get_pos()[0], 380,400)):	
						atmosphericJukebox.incrementMasterVolume(0.1)	
				if(event.button == 5):
					## scroll wheel down
					if(isBetween(pygame.mouse.get_pos()[0], 150,200)):
						atmosphericJukebox.incrementBackgroundVolume(-0.1)
					elif(isBetween(pygame.mouse.get_pos()[0], 225,275)):
						atmosphericJukebox.incrementMusicVolume(-0.1)
					elif(isBetween(pygame.mouse.get_pos()[0], 300,350)):	
						atmosphericJukebox.incrementShortSoundVolume(-0.1)
					elif(isBetween(pygame.mouse.get_pos()[0], 380,400)):	
						atmosphericJukebox.incrementMasterVolume(-0.1)	
			if(event.type == pygame.QUIT):
				atmosphericJukebox.exitSignal = True
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					pass
				if event.key == pygame.K_RIGHT:
					atmosphericJukebox.nextMusicTrack(1000)
					## this is much simpler, just fadeout the current track,
					## and the main loop will put on a new track
				if(event.key == pygame.K_q):
					atmosphericJukebox.incrementBackgroundVolume(0.1)	
				if(event.key == pygame.K_a):
					atmosphericJukebox.incrementBackgroundVolume(-0.1)
				if(event.key == pygame.K_w):
					atmosphericJukebox.incrementMusicVolume(0.1)	
				if(event.key == pygame.K_s):
					atmosphericJukebox.incrementMusicVolume(-0.1)
				if(event.key == pygame.K_e):
					atmosphericJukebox.incrementShortSoundVolume(0.1)	
				if(event.key == pygame.K_d):
					atmosphericJukebox.incrementShortSoundVolume(-0.1)	
				if(event.key == pygame.K_EQUALS):
					atmosphericJukebox.incrementMasterVolume(0.1)	
				if(event.key == pygame.K_MINUS):
					atmosphericJukebox.incrementMasterVolume(-0.1)	
				if(event.key == pygame.K_SPACE):
					atmosphericJukebox.togglePauseState()				
				if(event.key == pygame.K_i):
					print "Channel 1: %r, Channel 2: %r" % (atmosphericJukebox.background1Channel.get_busy(), atmosphericJukebox.background1Channel.get_busy())
		
		pygame.event.poll()
		clock.tick(10)	
		atmosphericJukebox.loop()
		pygame.display.update()

