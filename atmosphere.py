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

import uiTools

def getFillColour(currentFillGreen, loadFinished):
	if(loadFinished):
		if(currentFillGreen > 0):
			currentFillGreen -= 1


def getShutdownDelayFromArgString(argString):
	m = re.search('(?<=--shutdownTime=)\w+', argString)
	return int(m.group(0))

def getIntegerValueFromArgString(argString, targetFlagString):
	m = re.search('(?<=%s=)\w+' % targetFlagString, argString)
	return int(m.group(0))

def getEnvFileFromArgString(argString):
	m = re.search('(?<=--envFile=)\w+\.(csv|env)', argString)
	return str(m.group(0))

## foldFileExtensionsIntoString: Listof(Str) -> Str

def foldFileExtensionsIntoString(fileExtensionList):
	output = ""
	for ext in fileExtensionList:
		if(output != ""):
			output += "|"
		output += ext
	return output
		

def getFilenameFromArgString(argString, targetFlagString, availableFileExtensions):
	##m = re.search('(?<=%s=)\w+\.(csv|env)', argString)
	m = re.search('(?<=%s=)\w+\.(%s)' % (targetFlagString, foldFileExtensionsIntoString(availableFileExtensions)), argString)
	return str(m.group(0))

def stringToBoolean(someStr):
	if(someStr.lower() in ["true", "yes", "yea", "1"]):
		return True
	elif(someStr.lower() in ["false", "no", "nah", "0"]):
		return False
	else:
		return None
		## lets get explicit about sending everything to hell


def getBooleanSwitchOptionFromArgString(argString, targetFlagString):
	m = re.search('(?<=%s=)\w+' % targetFlagString , argString)
	return m.group(0)



def searchForIntegerArgument(manualArguments, targetFlagString):
	argumentFound = False
	integerValue = -1
	for arg in manualArguments:
		try:
			##shutdownDelay = getShutdownDelayFromArgString(arg)
			integerValue = getIntegerValueFromArgString(arg, targetFlagString)
			## take a shot at pulling an int off the end of some argument string
			## formatted in just the right way
			argumentFound = True
			break
			## once its found, pop out of the loop and flag that we have one set
		except:
			argumentFound = False
			## otherwise just do nothing
	return integerValue, argumentFound


	

def searchForFilenameArgument(manualArguments, targetFlagString, availableFileExtensions):
	argumentFound = False
	filenameOutput = ""
	for arg in manualArguments:
		try:
			##shutdownDelay = getShutdownDelayFromArgString(arg)
			##integerValue = getIntegerValueFromArgString(arg, targetFlagString)
			filenameOutput = getFilenameFromArgString(arg, targetFlagString, availableFileExtensions)
			## take a shot at pulling an int off the end of some argument string
			## formatted in just the right way
			argumentFound = True
			break
			## once its found, pop out of the loop and flag that we have one set
		except:
			argumentFound = False
			## otherwise just do nothing
	return filenameOutput, argumentFound
	
	
	
def searchForBooleanArgument(manualArguments, targetFlagString):
	argumentFound = False
	booleanOutput = False
	for arg in manualArguments:
		try:
			##shutdownDelay = getShutdownDelayFromArgString(arg)
			##integerValue = getIntegerValueFromArgString(arg, targetFlagString)
			rawBooleanString = getBooleanSwitchOptionFromArgString(arg, targetFlagString)
			print rawBooleanString
			## take a shot at pulling an int off the end of some argument string
			## formatted in just the right way
			if(stringToBoolean(rawBooleanString) != None):
				print "'%s' has a booelean argument %r as '%s'" % (arg, stringToBoolean(rawBooleanString), rawBooleanString)
				booleanOutput = stringToBoolean(rawBooleanString)
				argumentFound = True
				break
			else:
				print "'%s' does not have a booelean argument" % (arg)
				argumentFound = False
			## once its found, pop out of the loop and flag that we have one set
		except:
			argumentFound = False
			## otherwise just do nothing
	return booleanOutput, argumentFound	

def getUnpauseTriangleBox(horizontalOffset=False):
	if(not horizontalOffset):
		return [[unpauseTriangle[0][0], unpauseTriangle[0][1]],[unpauseTriangle[1][0], unpauseTriangle[2][1]]]
	else:
		return [[unpauseTriangle[0][0]+horizontalOffset, unpauseTriangle[0][1]],[unpauseTriangle[1][0]+horizontalOffset, unpauseTriangle[2][1]]]
	
	
if(__name__ == "__main__"):
	
	
	blue=(0,0,255)
	green=(0,200,120)
	red=(170,0,0)
	## define our coloury shit

	
	timedShutdown = False
	## flag for whether we have a countdown to the app killing itself after some
	## number of seconds
	envFilePreselected = False


	musicStartStateSpecified = False
	startWithMusicPaused = False
	
	
	manualArguments = argv[1:]
	
	if(manualArguments == ["options"]):
		print "--shutdownTime=\n--envFile=\n--startWithMusicPaused=\n"
		exit()
		## print the basic command line options for this 
	elif(manualArguments == ["tests"]):
		for op in ["yea", "Yea", "Nope", "NAH", "True", "FALSE", "true", "False"]:
			print repr(op), " -> ", repr(stringToBoolean(op))
		valueFound, wasFoundFlag = searchForBooleanArgument(["--shutdownTime=nah"], "--shutdownTime")
		print "wasFoundFlag ", repr(wasFoundFlag)
		print "valueFound ", repr(valueFound)
		exit()
		
	shutdownDelay, timedShutdown = searchForIntegerArgument(manualArguments, "--shutdownTime")
	preselectedEnvFileName, envFilePreselected = searchForFilenameArgument(manualArguments, "--envFile", ['csv', 'env'])
	startWithMusicPaused, musicStartStateSpecified = searchForBooleanArgument(manualArguments, "--startWithMusicPaused")	
	## retrieve any and all command line arguments





	Tk().withdraw()
	## we dont want a full GUI through TkInter, so keep the root window from 
	## appearing (main gui here will be done through pygame
	
	
	if(not envFilePreselected):
		filename = askopenfilename(initialdir='./envfiles')
		## show an "Open" dialog box and return the path to the selected file
		envFileName = filename
	else:
		envFileName = "./envfiles/%s" % preselectedEnvFileName
	## determine which envfile should be loaded and store it as a string under
	## envFileName
	print(envFileName)
	
	
	version = 0.21
	## program version
	##
	## version history goes like this:
	## 0.0x basic testing to figure out how to make the app workable
	## 0.1x was the first stable version, developed around late 2016, early 2017
	## and used as a good copy for about a year
	## 0.2x is the new and improved version which will see the code get
	## commented and refactored to a much cleaner level, and the memory usage
	## reduced significantly
	## 0.3x will be a complete overhaul of what the app does, finally adding
	## support for simulated objects under the hood, such as moving people,
	## doors, and other spatial related upgrades
	
	
	debugInfo = True
	## by default show debug output
	
	
	pygame.init()
	pygame.mixer.init()
	## pygame setup
	
	screen = pygame.display.set_mode((440,120))
	## define a basic window size of 120 high, 440 wide
	pygame.display.set_caption("atmosphere %s" % version)
	
	
	pygame.mixer.pre_init(44100, -16, 2, 2048)
	## need to look up what this actually meant
	pygame.mixer.init()
	## also why is mixer.init() called twice...
		
	try:
		if(debugInfo):
			filesList = envLoader.getFilesList(envFileName)
			## get a list of audio files to be used
			## returns a 2-list, contains length 3 lists with info about each
			## file
			for fileInfo in filesList:
				print fileInfo
		
		atmosphericJukebox = jukebox.Jukebox(envFileName, debugInfo)
		## object wrapping all of the loaded sound files and their behaviour
	except TypeError:
		print "No env file selected, exiting..."
		exit()
			
	if(debugInfo):
		print "Received %i sounds" % len(envLoader.getFilesList(envFileName))
		print "%i background tracks, %i short sounds, %i music tracks" % (len(atmosphericJukebox.backgroundSounds), len(atmosphericJukebox.shortSounds), len(atmosphericJukebox.musicSounds))
	
	startupTime = time.time()
	atmosphericJukebox.play()
	
	
	if(debugInfo):
		print "musicStartStateSpecified = ", musicStartStateSpecified
		print "envFilePreselected = ", envFilePreselected
		print "timedShutdown = ", timedShutdown
		
		
		
	if(musicStartStateSpecified and startWithMusicPaused):
		atmosphericJukebox.togglePauseState()	
		musicPausePlayButton = uiTools.pausePlayButton({"x": 10, "y": 10}, 20, 15, False)
	else:
		musicPausePlayButton = uiTools.pausePlayButton({"x": 10, "y": 10}, 20, 15, True)
	
	masterVolumeSlider = uiTools.sliderBar({"x": 380, "y": 0}, 110, {"min": 0,"max": 100}, 10, 20, red)	
	backgroundVolumeSlider = uiTools.sliderBar({"x": 150, "y": 0}, 110, {"min": 0,"max": 100}, 10, 50, blue)		
	musicVolumeSlider = uiTools.sliderBar({"x": 225, "y": 0}, 110, {"min": 0,"max": 100}, 10, 50, green)		
	shortSoundVolumeSlider = uiTools.sliderBar({"x": 300, "y": 0}, 110, {"min": 0,"max": 100}, 10, 50, blue)		
	## define all of the buttons	
	uiParts = {"musicPausePlayButton": musicPausePlayButton, \
	 "masterVolumeSlider": masterVolumeSlider, \
	 "backgroundVolumeSlider": backgroundVolumeSlider, \
	 "musicVolumeSlider": musicVolumeSlider, \
	 "shortSoundVolumeSlider": shortSoundVolumeSlider, \
	 }	
	## add all buttons to a dict so we can loop through
	clock = pygame.time.Clock()
	clock.tick(10)
	
	
	##unpauseTriangle = [[10, 10], [25, 20],[ 10, 30]]
	## [x, y] coordinates, y is measured downwards from top of window
	## x is measured across from left hand side of window
	
	while(not atmosphericJukebox.exitSignal):
		screen.fill((0,0,0))
		
		countdownUiHeight = 2.0*atmosphericJukebox.countdownToNextShortSound()
		pygame.draw.rect(screen,blue,(120,0,20,countdownUiHeight))	
		## render the countdown timer as a rectangle wiping upwards as the time
		## to the next short sound being played hits zero
		
		for component in uiParts:
			uiParts[component].renderButton(screen)
		## render the four volume sliders for the app, positioned on the canvas
		## depending on volume, 100% at the top, 0% at the bottom

		for event in pygame.event.get():
			
			def isBetween(value, lower, upper):
				if((value >= lower)and(value <= upper)):
					return True
				return False	
				
			if event.type == pygame.MOUSEBUTTONDOWN:
				if(event.button == 1):
					## left click
					if(musicPausePlayButton.positionInButtonArea( {"x": pygame.mouse.get_pos()[0], "y": pygame.mouse.get_pos()[1]})):
						musicPausePlayButton.click(atmosphericJukebox.togglePauseState())		
							
				elif(event.button == 4):
					## scroll wheel up 
					if(backgroundVolumeSlider.positionInButtonEffectiveArea({"x": pygame.mouse.get_pos()[0], "y": pygame.mouse.get_pos()[1]})):	
						backgroundVolumeSlider.incrementState(10)
						atmosphericJukebox.setBackgroundVolume(backgroundVolumeSlider.getSliderFractionalValue())

					if(musicVolumeSlider.positionInButtonEffectiveArea({"x": pygame.mouse.get_pos()[0], "y": pygame.mouse.get_pos()[1]})):	
						musicVolumeSlider.incrementState(10)
						atmosphericJukebox.setMusicVolume(musicVolumeSlider.getSliderFractionalValue())
					
					if(shortSoundVolumeSlider.positionInButtonEffectiveArea({"x": pygame.mouse.get_pos()[0], "y": pygame.mouse.get_pos()[1]})):	
						shortSoundVolumeSlider.incrementState(10)
						atmosphericJukebox.setShortSoundVolume(shortSoundVolumeSlider.getSliderFractionalValue())
					
					if(masterVolumeSlider.positionInButtonEffectiveArea({"x": pygame.mouse.get_pos()[0], "y": pygame.mouse.get_pos()[1]})):	
						masterVolumeSlider.incrementState(10)
						atmosphericJukebox.setMasterVolume(masterVolumeSlider.getSliderFractionalValue())
				
				if(event.button == 5):
					## scroll wheel down
					if(backgroundVolumeSlider.positionInButtonEffectiveArea({"x": pygame.mouse.get_pos()[0], "y": pygame.mouse.get_pos()[1]})):	
						backgroundVolumeSlider.incrementState(-10)
						atmosphericJukebox.setBackgroundVolume(backgroundVolumeSlider.getSliderFractionalValue())

					if(musicVolumeSlider.positionInButtonEffectiveArea({"x": pygame.mouse.get_pos()[0], "y": pygame.mouse.get_pos()[1]})):	
						musicVolumeSlider.incrementState(-10)
						atmosphericJukebox.setMusicVolume(musicVolumeSlider.getSliderFractionalValue())
					
					if(shortSoundVolumeSlider.positionInButtonEffectiveArea({"x": pygame.mouse.get_pos()[0], "y": pygame.mouse.get_pos()[1]})):	
						shortSoundVolumeSlider.incrementState(-10)
						atmosphericJukebox.setShortSoundVolume(shortSoundVolumeSlider.getSliderFractionalValue())
					
					if(masterVolumeSlider.positionInButtonEffectiveArea({"x": pygame.mouse.get_pos()[0], "y": pygame.mouse.get_pos()[1]})):	
						masterVolumeSlider.incrementState(-10)
						atmosphericJukebox.setMasterVolume(masterVolumeSlider.getSliderFractionalValue())
			if(event.type == pygame.QUIT):
				atmosphericJukebox.exitSignal = True
			
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					pass
				if event.key == pygame.K_RIGHT:
					atmosphericJukebox.fadeOutMusicTrack(1000)
					## fade forward to the next track if the current one sucks
				
				## background sounds
				if(event.key == pygame.K_q):
					backgroundVolumeSlider.incrementState(10)
					atmosphericJukebox.setBackgroundVolume(backgroundVolumeSlider.getSliderFractionalValue())	
				if(event.key == pygame.K_a):
					backgroundVolumeSlider.incrementState(-10)
					atmosphericJukebox.setBackgroundVolume(backgroundVolumeSlider.getSliderFractionalValue())	
				
				## music
				if(event.key == pygame.K_w):
					musicVolumeSlider.incrementState(10)
					atmosphericJukebox.setMusicVolume(musicVolumeSlider.getSliderFractionalValue())	
				if(event.key == pygame.K_s):
					musicVolumeSlider.incrementState(-10)
					atmosphericJukebox.setMusicVolume(musicVolumeSlider.getSliderFractionalValue())
				
				## short sounds
				if(event.key == pygame.K_e):
					shortSoundVolumeSlider.incrementState(10)
					atmosphericJukebox.setShortSoundVolume(shortSoundVolumeSlider.getSliderFractionalValue())
				if(event.key == pygame.K_d):
					shortSoundVolumeSlider.incrementState(-10)
					atmosphericJukebox.setShortSoundVolume(shortSoundVolumeSlider.getSliderFractionalValue())
				
				## master volume
				if(event.key == pygame.K_EQUALS):
					## plus and up	
					masterVolumeSlider.incrementState(10)
					atmosphericJukebox.setMasterVolume(masterVolumeSlider.getSliderFractionalValue())
				if(event.key == pygame.K_MINUS):
					## minus and down
					masterVolumeSlider.incrementState(-10)
					atmosphericJukebox.setMasterVolume(masterVolumeSlider.getSliderFractionalValue())
				
				## pause/play music
				if(event.key == pygame.K_SPACE):
					atmosphericJukebox.togglePauseState()				
				
				## check info
				if(event.key == pygame.K_i):
					if(debugInfo):
						print "Channel 1: %r, Channel 2: %r" % (atmosphericJukebox.background1Channel.get_busy(), atmosphericJukebox.background1Channel.get_busy())
		
		pygame.event.poll()
		## check for events
		clock.tick(10)	
		## tick 10 milliseconds
		atmosphericJukebox.loop()
		## update the jukebox object
		
		if(timedShutdown):
			currentRuntime = time.time() - startupTime
			if(currentRuntime >= shutdownDelay):
				atmosphericJukebox.exitSignal = True		
		## if a timedShutdown was requested, keep running down the timer until
		## we hit zero
		
		pygame.display.update()
		## pygame internal stuff
		
	if(timedShutdown):
		if(debugInfo):
			print "Successfully exited after %i seconds, targeted shutdown was set for %i s" % ((time.time()-startupTime), shutdownDelay)	

