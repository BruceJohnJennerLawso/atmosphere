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

import time
import re

def getFillColour(currentFillGreen, loadFinished):
	if(loadFinished):
		if(currentFillGreen > 0):
			currentFillGreen -= 1


def getShutdownDelayFromArgString(argString):
	m = re.search('(?<=--shutdownTime=)\w+', argString)
	return int(m.group(0))

def getEnvFileFromArgString(argString):
	m = re.search('(?<=--envFile=)\w+', argString)
	return str(m.group(0))

if(__name__ == "__main__"):
	
	
	blue=(0,0,255)
	green=(0,200,120)
	red=(170,0,0)
	## define our coloury shit

	
	timedShutdown = False
	## flag for whether we have a countdown to the app killing itself after some
	## number of seconds
	envFilePreselected = False
	
	
	manualArguments = argv[1:]
	
	if("options" in manualArguments):
		print "--shutdownTime=\n--envFile=\n"
		exit()
	
	for arg in manualArguments:
		try:
			shutdownDelay = getShutdownDelayFromArgString(arg)
			## take a shot at pulling an int off the end of some argument string
			## formatted in just the right way
			timedShutdown = True
			break
			## once its found, pop out of the loop and flag that we have one set
		except:
			timedShutdown = False
			## otherwise just do nothing

	for arg in manualArguments:
		try:
			preselectedEnvFileName = getEnvFileFromArgString(arg)
			## take a shot at pulling an int off the end of some argument string
			## formatted in just the right way
			envFilePreselected = True
			break
			## once its found, pop out of the loop and flag that we have one set
		except:
			envFilePreselected = False
			## otherwise just do nothing


	Tk().withdraw()
	## we dont want a full GUI, so keep the root window from appearing
	
	
	if(not envFilePreselected):
		filename = askopenfilename(initialdir='./envfiles')
		## show an "Open" dialog box and return the path to the selected file
		envFileName = filename
	else:
		envFileName = preselectedEnvFileName
	
	
	print(envFileName)
	
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
			filesList = envLoader.getFilesList(envFileName)
			for fileInfo in filesList:
				print fileInfo
		
		atmosphericJukebox = jukebox.Jukebox(envFileName, debugInfo)
	except TypeError:
		print "No env file selected, exiting..."
		exit()
			
	if(debugInfo):
		print "Received %i sounds" % len(envLoader.getFilesList(envFileName))
		print "%i background tracks, %i short sounds, %i music tracks" % (len(atmosphericJukebox.backgroundSounds), len(atmosphericJukebox.shortSounds), len(atmosphericJukebox.musicSounds))
	
	startupTime = time.time()
	atmosphericJukebox.play()
	
		
	clock = pygame.time.Clock()
	clock.tick(10)
	
	
	unpauseTriangle = [[10, 10], [25, 20],[ 10, 30]]
	
	def getUnpauseTriangleBox(horizontalOffset=False):
		if(not horizontalOffset):
			return [[unpauseTriangle[0][0], unpauseTriangle[0][1]],[unpauseTriangle[1][0], unpauseTriangle[2][1]]]
		else:
			return [[unpauseTriangle[0][0]+horizontalOffset, unpauseTriangle[0][1]],[unpauseTriangle[1][0]+horizontalOffset, unpauseTriangle[2][1]]]
	
	while(not atmosphericJukebox.exitSignal):
		screen.fill((0,0,0))
		pygame.draw.rect(screen,blue,(120,0,20,2.0*atmosphericJukebox.countdownToNextShortSound()))		
		pygame.draw.rect(screen,blue,(150,(100-100*atmosphericJukebox.getBackgroundChannelVolume()),50,10))
		pygame.draw.rect(screen,green,(225,(100-100*atmosphericJukebox.getMusicChannelVolume()),50,10))
		pygame.draw.rect(screen,blue,(300,(100-100*atmosphericJukebox.getShortSoundChannelVolume()),50,10))
		pygame.draw.rect(screen,red,(380,(100-100*atmosphericJukebox.getMasterVolume()),20,10))		
		if(atmosphericJukebox.isMusicPaused() == True):
			pygame.draw.polygon(screen,blue,unpauseTriangle, 0)
		else:
			pygame.draw.polygon(screen,blue,[getUnpauseTriangleBox()[0], [getUnpauseTriangleBox()[0][0]+5, getUnpauseTriangleBox()[0][1]], [getUnpauseTriangleBox()[0][0]+5, getUnpauseTriangleBox()[1][1]], [getUnpauseTriangleBox()[0][0], getUnpauseTriangleBox()[1][1]] ], 0)
			pygame.draw.polygon(screen,blue,[getUnpauseTriangleBox(10)[0], [getUnpauseTriangleBox(10)[0][0]+5, getUnpauseTriangleBox(10)[0][1]], [getUnpauseTriangleBox(10)[0][0]+5, getUnpauseTriangleBox(10)[1][1]], [getUnpauseTriangleBox(10)[0][0], getUnpauseTriangleBox(10)[1][1]] ], 0)
		for event in pygame.event.get():
			
			def isBetween(value, lower, upper):
				if((value >= lower)and(value <= upper)):
					return True
				return False	
				
			if event.type == pygame.MOUSEBUTTONDOWN:
				if(event.button == 1):
					## left click
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
					atmosphericJukebox.fadeOutMusicTrack(1000)
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
		if(timedShutdown):
			currentRuntime = time.time() - startupTime
			if(currentRuntime >= shutdownDelay):
				atmosphericJukebox.exitSignal = True		
		pygame.display.update()
	if(timedShutdown):
		print "Successfully exited after %i seconds, target %i s" % ((time.time()-startupTime), shutdownDelay)	

