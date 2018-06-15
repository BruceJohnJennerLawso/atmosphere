## jukebox.py ##################################################################
## app that plays background noise tracks and music ############################
## in parallel, tries to learn user preferences intelligently ##################
################################################################################
import envLoader
import sound

import random
import time
import pygame


import multiprocessing as mp
## helper function

## isBetween: Num, Num, Num -> Bool

## true if value is between lower and upper, false otherwise

def isBetween(value, lower, upper):
	if((value >= lower)and(value <= upper)):
		return True
	return False



## helper function

## samples a value from a gaussian (normal) distribution, given a mean & stdev
## for that distribution.

## works by sampling 100 values from that normal distribution, and randomly
## choosing one from that selection

## if we want to avoid negative values (for things like time offsets which cant
## be negative), any values beneath valFloor are tossed out 

def getValueFromGaussian(mean, stdev, valFloor = None):
	values = []
	while(len(values) < 100):
		value = random.gauss(mean, stdev)
		if(not valFloor is None):
			if(value > valFloor):
				values.append(value)
		else:
			values.append(value)		
	return random.choice(values)











class Jukebox(object):

	## constructor
	
	## take an environmentFileName, and load everything we need to start playing
	## its described contents

	
	def __init__(self, envFileName, debugInfo=False):
		##self.backgroundSounds = []
		## background sounds, most commonly a 10,20,30 minute long ambient noise
		## track, with a lot of rich, low level variation that playing a handful
		## of short sounds over and over wouldnt be able to provide
		
		## also consumes a crapton of memory unfortunately, so it carries a
		## large ram hit, and a very long load time if we need to pull it up
		## from memory
		##self.shortSounds = []
		## things like a console beeping, birds chirping, etc.
		## anything longer than 15s is probably too long for this category
		##self.musicSounds = []
		## music files, commonly about 4-5 minutes long, but it can be just
		## about any length really
		
		## lists of sound.Sound objects (a wrapper around pygame.mixer.Sound)
		
		
		## ** this is kind of inefficient, doing everything with hardcoded
		##    channel 1, channel 2, channel other type deals, so a better
		##    solution would be to create objects for each type and create them
		##    here, let them do their own things with volume, track selection **
		
		
		
		self.audioFiles = {}
		## listof {"filePath": Str, "decVolume": float, "fileType": Str}
		##
		## note that decVolume is 0.0 to 1.0
		
		## when loaded this looks like
		## listof {"filePath": Str, "decVolume": float, "fileType": Str, "soundObject": sound.Sound}
		
		
		
		self.musicChannel = pygame.mixer.Channel(5)
		
		self.backgroundChannel1 = pygame.mixer.Channel(3)
		self.backgroundChannel2 = pygame.mixer.Channel(4)
		## we allocate 2 channels to the background, since thats really one of
		## the most important parts of the atmosphere, and having two ambient
		## audio tracks gives us more bang for our buck than two musics or
		## shorts playing simultaneously would
		
		self.shortSoundChannel = pygame.mixer.Channel(6)
		## channels which are used to play those sound objects, one at a time in
		## the given channel, but we can play a music file simultaneous with a
		## short sound and so on, which makes things a bit more flexible
		
		
		
		
		self.backgroundVolume = 1.0
		## how loud the background track should be playing at, on a scale of 
		## 0.0 (silent) to 1.0 (full volume)
		self.shortVolume = 1.0
		##
		self.musicVolume = 1.0
		## same idea for the short sounds and the music, allows the end user to
		## throttle them if they want to turn the music up/down, the short
		## sounds end up being too piercing/distracting at a high volume
		
		self.masterVolume = 1.0
		## in addition to the individual parameters, we have a master volume,
		## which is applied to the other sliders, so 0.7 background & 0.7 master
		## gives us 0.7*0.7 = 0.49
		
		
		self.musicPaused = False
		## flag we can toggle in case the end user wants the ambient audio
		## without starting the music playing
		
		
		self.exitSignal = False
		## indicator that we want to end the loop and get out of here
		
		self.loadEnvFile(envFileName, debugInfo)
		## load up the sound objects with all of the info about the sounds, but
		## dont load their file data into memory just yet (ie we have the name &
		## other info about the file, but we havent opened it up just yet
		## because that takes lots of time & memory) 
		
		
		

		self.backgroundLineup = {"A": [], "B": []}
		
		self.musicLineup = []
		
		self.previousMusic = []
		
		self.chooseInitialRandomBackgrounds()
		## pick out a pair of background noise tracks at random and slot them in
		## so they are ready to be played
		self.chooseInitialRandomMusic()
		## randomly select our first music track to play

		##self.randomShortSound = random.choice(self.shortSounds)
		##self.randomShortSound.loadSound()
		##self.randomShortSound.setVolume(0.05)

		self.lastShortSoundTime = time.time()
		## start our recording clock, so the first randomly spaced short sound
		## will play when whatever its dt plus this initial time has passed
		self.waitUntilNextShortSound = getValueFromGaussian(30.0, 10.0, 5.0)
		## that initial wait
		
		

		## once this is all done, the object is just waiting for
		## play() to be called		



	## method
	
	## take a name of an envFile (ie a csv located usually under the project 
	## folder in the envfiles directory), and load up sound objects to wrap
	## each specified track in the sounds list



	def loadEnvFile(self, envFileName, debugInfo=False):

		if(debugInfo):
			print envLoader.getFilesList(envFileName)
	
		for sFile in envLoader.getFilesList(envFileName):
			thisFilePath = sFile[0]
			## where is the file located in this PCs file tree
			decVolume = float(sFile[1]/100.0)
			## volume is stored in the file as a value from 0 to 100, so we
			## adjust it to be correct for a scale from 0.0 to 1.0
			thisFilesType = sFile[2]
			## what type of file is this in ['background', 'short', 'music']


			loadedSoundObject = sound.Sound('./data/%s' % thisFilePath, decVolume, thisFilesType)
			
			self.audioFiles[thisFilePath] = loadedSoundObject
			
	def loadSoundFileIntoMemory(self, byFilePath):			
		self.audioFiles[byFilePath].loadSound()

	def unloadSoundFileFromMemory(self, byFilePath):
		self.audioFiles[byFilePath].clearSound()
		## should purge the object from memory along with its memory footprint
	
	
	def getRandomBackgroundSoundKey(self):
		choice = random.choice([key for key in self.audioFiles if self.audioFiles[key].getSoundType() == 'background'])
		return choice

	def getTotalBackgroundSoundCount(self):
		return len([key for key in self.audioFiles if self.audioFiles[key].getSoundType() == 'background'])
		

	def getTotalMusicFileCount(self):
		return len([key for key in self.audioFiles if self.audioFiles[key].getSoundType() == 'music'])		


	def getRandomShortSoundKey(self):
		choice = random.choice([key for key in self.audioFiles if self.audioFiles[key].getSoundType() == 'short'])
		return choice	

	def getRandomMusicSoundKey(self):
		choice = random.choice([key for key in self.audioFiles if self.audioFiles[key].getSoundType() == 'music'])
		return choice	
	
	
	def soundFileLoaded(self, byFilePath):
		return self.audioFiles[byFilePath].isLoaded()
	
	## method
	
	## make a random selection from the list of background tracks available and
	## load it into memory

	def chooseInitialRandomBackgrounds(self):
		firstChoice = self.getRandomBackgroundSoundKey()
		secondChoice = self.getRandomBackgroundSoundKey()		
		
		while(firstChoice == secondChoice):
			## sometimes we choose the same track twice, especially if the list
			## is small
			
			## ** note this comparison may be slow af, so rewriting this to
			## crosscheck only file names might be a better idea for performance
			## **
			secondChoice = self.getRandomBackgroundSoundKey()
			## keep trying until we get two different sounds

		self.loadSoundFileIntoMemory(firstChoice)
		self.loadSoundFileIntoMemory(secondChoice)
		## these two calls will need to be multithreaded to make the app run
		## smoothly
		##self.backgroundLineup = {"A": [], "B": []}
		
		self.backgroundLineup["A"].append(firstChoice)
		self.backgroundLineup["B"].append(secondChoice)
		


	## method
	
	## same as with background audio tracks, except we only need to pick one
	## music track to play and load it into memory

	def chooseInitialRandomMusic(self):
		
		randomMusicKey = self.getRandomMusicSoundKey()
		self.loadSoundFileIntoMemory(randomMusicKey)
		
		self.musicLineup.append(randomMusicKey)

	## method
	
	## once we're already off and running, choosing the next file to play
	## becomes a lot trickier,

	def chooseRandomBackground(self, channel, andPlay=False):
		newRandomBackground = self.getRandomBackgroundSoundKey()
		
		if(self.getTotalBackgroundSoundCount() > 2):
			while((newRandomBackground == self.getBackgroundSoundByChannelNo(1))and(newRandomBackground == self.getBackgroundSoundByChannelNo(2))):
				newRandomBackground = self.getRandomBackgroundSoundKey()
		
		if(channel == 1):
			##self.firstRandomChoice.stop()
			
			## this would be a good safety feature for the future, but I dont
			## want to gum things up just yet
			
			
			##self.firstRandomChoice.clearSound()
			## weve chosen a new file randomly to play in this slot, so we clear
			## out the old file
			## this was taking way too long with background tracks, makes for a
			## way too noticeable pause where the app goes silent, so Im going
			## to give leaving everything in memory a try
			
			## this should hopefully be possible to implement in the future with
			## multithreading, just have that laggy file loading step done ahead
			## of time in its own thread, while the main app does its own thing
			##self.backgroundLineup = {"A": [], "B": []}
			##self.musicBackground = []
			
			self.backgroundLineup["A"].append(newRandomBackground)
			
			##self.firstRandomChoice = newRandomBackground
			## assign the new file to this slot
			
			if(self.backgroundLineup["A"].index(newRandomBackground) <= 1):
				self.loadSoundFileIntoMemory(newRandomBackground)
			##self.firstRandomChoice.loadSound()	
			## load it up into memory (if necessary
			
			
			if(andPlay):
				## if we specified in the parameters that we wanted the sound
				## to start playing right away, we get it rocking on the correct
				## channel
				self.backgroundChannel1.play(self.audioFiles[newRandomBackground].getSound())
				self.audioFiles[newRandomBackground].incrementPlayCounter()
				## dont forget to increment the play counter for this thing
		elif(channel == 2):
			##self.secondRandomChoice.clearSound()
			self.backgroundLineup["B"].append(newRandomBackground)

			if(self.backgroundLineup["B"].index(newRandomBackground) <= 1):
				self.loadSoundFileIntoMemory(newRandomBackground)

			##self.secondRandomChoice = newRandomBackground
			##self.secondRandomChoice.loadSound()
			## (if necessary)
			if(andPlay):
				self.backgroundChannel2.play(self.audioFiles[newRandomBackground].getSound())
				self.audioFiles[newRandomBackground].incrementPlayCounter()
		else:
			## fuck
			print "Bad call to chooseRandomBackground(self, %i, andPlay)" % channel
			## nonexistent channel provided



	## method

	## check if each of the music/background channels is busy, if they aint,
	## smash that mf play button
	
	## (by which I mean, we tell each of the channels to start playing their
	## assigned sound objects)
	
	## this should only  be called once all of
	## self.randomMusic
	## self.firstRandomChoice
	## self.secondRandomChoice
	##
	## have been assigned 
	## (so only once the initial choose functions have been called)


	def playMusic(self):
		if(not self.musicChannel.get_busy()):
			nextMusicUp = self.musicLineup[0]
			self.musicChannel.play(self.audioFiles[nextMusicUp].getSound())

	def playBackground1(self):
		if(not self.backgroundChannel1.get_busy()):
			nextBackgroundUp = self.backgroundLineup["A"][0]
			self.backgroundChannel1.play(self.audioFiles[nextBackgroundUp].getSound())

	def playBackground2(self):
		if(not self.backgroundChannel2.get_busy()):
			nextBackgroundUp = self.backgroundLineup["B"][0]
			self.backgroundChannel2.play(self.audioFiles[nextBackgroundUp].getSound())


	def play(self):
		self.playMusic()
		self.playBackground1()
		self.playBackground2()
		## check if each channel is busy in sequence, if theyre not playing
		## their shit, we want them to be, so we tell the channel to play using
		## its assigned sound object				








	## our toggle to start and stop the music, which is handy so the end user
	## has more control over what they hear

	## method

	## check if it be
	def isMusicPaused(self):
		return self.musicPaused

	## method
	
	## if it aint, make it be

	def pauseMusic(self):
		self.musicPaused = True
		self.musicChannel.pause()
		
	## method	
		
	## if it so, make it not

	def resumeMusic(self):
		self.musicPaused = False
		self.musicChannel.unpause()

	## method
	
	## if we dont like where its at, make it something else
		
	def togglePauseState(self):
		if(self.isMusicPaused() == True):
			self.resumeMusic()
		else:
			self.pauseMusic()


	## method
	
	## this is primarily for when the current track sucks, so we fade it out and
	## the main loop puts on a new track for us (not handled here though)

	def fadeOutMusicTrack(self, fadetime=False):
		if(fadetime != False):
			self.musicChannel.fadeout(fadetime)
		else:
			self.musicChannel.fadeout()
	
	
	## method
	
	## check and see what our current choices are of sound objects for each
	## channel based on what number of channel we are curious about
	## (first -> 1, second -> 2)
	
	## getBackgroundSoundByChannelNo: Int -> key

	def getBackgroundSoundByChannelNo(self, channel):
		if(channel == 1):
			return self.backgroundLineup["A"][0]
		elif(channel == 2):
			return self.backgroundLineup["B"][0]
		else:
			print "bad call to getBackgroundSoundByChannelNo(%i)" % channel
			
	


	
	## method
	
	## we're off and running, but the current music track has either ended or
	## was nexted by the user, so we need to load up a new one into memory and
	## flush the last one to keep memory consumption under control
	
	## as far as I cant tell this call to loadSound is not holding up the main
	## loop as drastically as background loading was, so loading in oldschool
	## sequential with the main program flow is probably fine for the moment,
	## but it should really be parallelized at some point

	def addRandomSelectionToMusicLineup(self):
		
		
		newRandomMusic = self.getRandomMusicSoundKey()
		
		if(len(self.musicLineup) != 0):
			while(newRandomMusic == self.musicLineup[-1]):
				newRandomMusic = self.getRandomMusicSoundKey()			
			
			## if I want to slice off only a certain length off the end use
			## foo =[1,2,3,4,5,6,7,8]
			## foo[-4:-1]
			## ie fourth last to last
		self.musicLineup.append(newRandomMusic)
	
	def chooseRandomMusic(self,andPlay=False):
		newRandomMusic = self.getRandomMusicSoundKey()
		## make a random selection from the music list for what to put on next
		while(newRandomMusic == self.musicLineup[-1]):
			newRandomMusic = self.getRandomMusicSoundKey()
			## if we get a repeat, try again because repetition is bad
			##
			## make sure that it isnt the same as the last one added (index -1)
		

		
		self.audioFiles[self.musicLineup[0]].clearSound()	
		## clear out the memory occupied by the old sound in memory
		
		self.previousMusic.append(self.musicLineup.pop(0))
		## add the most recently played track (just finished playing) to the
		## "previously played" list and pop it out of the current lineup
		self.addRandomSelectionToMusicLineup()
		## make sure at least one track is in the music lineup
		
		nextRandomMusicUp = self.musicLineup[0]
		## assign the new track as whatevers bubbled to the top (start) of the
		## list
		if(not self.audioFiles[nextRandomMusicUp].isLoaded()):
			self.audioFiles[nextRandomMusicUp].loadSound()
			## check if our file is loaded into memory, and load it up if not
		if(andPlay):
			print "Playing track %s" % self.musicLineup[0]
			self.musicChannel.play(self.audioFiles[nextRandomMusicUp].getSound())			
			self.audioFiles[nextRandomMusicUp].incrementPlayCounter()
			## start playing the song on the music channel
	
	
	## method
	
	## the two main parts of the ambiance besides the music are the (long-term)
	## background and the (short-term) short sounds. A timer counts down
	## random intervals and plays a short sound every time the timer runs out
	
	## this method picks a new one from the list, flushes whatever was on before
	## (again memory usage, although I wonder if it might be overkill not to 
	## load everything into memory with short sounds being so small), loads up
	## the new choice, and starts it playing (if requested andPlay)
			
	##def chooseRandomShortSound(self,andPlay=False):
	##	newRandomShortSound = random.choice(self.shortSounds)
	##	while(newRandomShortSound == self.randomShortSound):
	##		newRandomShortSound = random.choice(self.shortSounds)	
		
	##	self.randomShortSound.clearSound()	
	##	self.randomShortSound = newRandomShortSound
	##	self.randomShortSound.loadSound()
	##	self.randomShortSound.setVolume(0.05)
	##	if(andPlay):
	##		self.shortSoundChannel.play(self.randomShortSound.getSound())			
	##		self.randomShortSound.incrementPlayCounter()			


	## get channel volumes
	
	## gets the value of the slider for the particular channel we have in mind
	## *not* the true output volume, which depends on the master volume as well


	## method
	
	## get the volume for the background channel
	
	def getBackgroundChannelVolume(self):
		return (self.backgroundVolume)


	## method
	
	## get the volume for the background channel

	def getShortSoundChannelVolume(self):
		return (self.shortVolume)


	## method
	
	## get the volume for the background channel

	def getMusicChannelVolume(self):
		return (self.musicVolume)		
		

	## get channel output volumes
	
	## ie how loud should the output for this category *actually* be, once its
	## modified with whatever the master volume is


	## method
	
	## get the volume for the background channels output

	def getBackgroundOutputVolume(self):
		return (self.getBackgroundChannelVolume()*self.masterVolume)


	## method

	## get the volume for the short sound channels output			

	def getShortSoundOutputVolume(self):
		return (self.getShortSoundChannelVolume()*self.masterVolume)


	## method
		
	## get the volume for the music channels output
		
	def getMusicOutputVolume(self):
		return (self.getMusicChannelVolume()*self.masterVolume)				


	## method
	
	## get the master volume modifier, ie if the music channel is set to 0.7,
	## and the master volume is 0.8, the resulting output volume will be 
	## 0.7*0.8 = 0.56
		
	def getMasterVolume(self):
		return self.masterVolume
	



	## method
	
	## update the pygame output channels with the true output volume they should
	## have based on whats stored in this object

	def applyOutputChannelVolumes(self):
		self.backgroundChannel1.set_volume(self.getBackgroundOutputVolume())
		self.backgroundChannel2.set_volume(self.getBackgroundOutputVolume())
		self.shortSoundChannel.set_volume(self.getShortSoundOutputVolume())
		self.musicChannel.set_volume(self.getMusicOutputVolume())	

	## method
	
	## sets a value for the background channels raw volume (before the master
	## adjustment) and updates the actual pygame output channels to match
	
	def setBackgroundVolume(self, newVolume):
		self.backgroundVolume = newVolume
		self.applyOutputChannelVolumes()	

	## method
	
	## moves the raw volume for the background channel upwards by change units
	## (downwards if negative), and caps that change at 0.0 or 1.0 if we exceed
	## our bounds for volume
	
	def incrementBackgroundVolume(self, change):
		newVolume = self.getBackgroundChannelVolume()+change
		
		if(isBetween(newVolume, 0.0, 1.0)):
			self.setBackgroundVolume(newVolume)
		else:
			if(newVolume > 1.0):
				self.setBackgroundVolume(1.0)
			elif(newVolume < 0.0):
				self.setBackgroundVolume(0.0)	
				

	## method
	
	## sets a value for the short sound channels raw volume (before the master
	## adjustment) and updates the actual pygame output channels to match
	
	def setShortSoundVolume(self, newVolume):
		self.shortVolume = newVolume
		self.applyOutputChannelVolumes()


	## method
	
	## moves the raw volume for the short sound channel upwards by change units
	## (downwards if negative), and caps that change at 0.0 or 1.0 if we exceed
	## our bounds for volume
	
	def incrementShortSoundVolume(self, change):
		newVolume = self.getShortSoundChannelVolume()+change
		
		if(isBetween(newVolume, 0.0, 1.0)):
			self.setShortSoundVolume(newVolume)
		else:
			if(newVolume > 1.0):
				self.setShortSoundVolume(1.0)
			elif(newVolume < 0.0):
				self.setShortSoundVolume(0.0)	

	## method
	
	## sets a value for the music channels raw volume (before the master
	## adjustment) and updates the actual pygame output channels to match
		
	def setMusicVolume(self, newVolume):
		self.musicVolume = newVolume
		self.applyOutputChannelVolumes()


	## method
	
	## moves the raw volume for the music channel upwards by change units
	## (downwards if negative), and caps that change at 0.0 or 1.0 if we exceed
	## our bounds for volume

	def incrementMusicVolume(self, change):
		newVolume = self.getMusicChannelVolume()+change
		
		if(isBetween(newVolume, 0.0, 1.0)):
			self.setMusicVolume(newVolume)
		else:
			if(newVolume > 1.0):
				self.setMusicVolume(1.0)
			elif(newVolume < 0.0):
				self.setMusicVolume(0.0)	


	## method
	
	## sets a value for the master channels volume and updates the actual
	## pygame output channels to match
		
	def setMasterVolume(self, newVolume):
		self.masterVolume = newVolume
		self.applyOutputChannelVolumes()

	## method
	
	## moves the volume for the master slider upwards by change units
	## (downwards if negative), and caps that change at 0.0 or 1.0 if we exceed
	## our bounds for volume
			
	def incrementMasterVolume(self, change):
		newVolume = self.getMasterVolume()+change
		
		if(isBetween(newVolume, 0.0, 1.0)):
			self.setMasterVolume(newVolume)
		else:
			if(newVolume > 1.0):
				self.setMasterVolume(1.0)
			elif(newVolume < 0.0):
				self.setMasterVolume(0.0)	


	## method
	
	## loop gets called once per cycle of the main run loop (ie once per
	## rendering frame for pygame), and handles the progression of playing
	## sounds in a logical order, starting up the next sound in line, checking
	## to see if its time to play a short sound
					
	def loop(self):
		if((not self.musicChannel.get_busy())and(self.isMusicPaused() == False)):
			## music has finished, need to put another track on0
			self.chooseRandomMusic(andPlay=True)
			
		if(not self.backgroundChannel1.get_busy()):		
			## background sound on channel 1 has finished,
			## need to put another track on
			self.chooseRandomBackground(1, andPlay=True)
		if(not self.backgroundChannel2.get_busy()):		
			## background sound on channel 2 has finished,
			## need to put another track on
			self.chooseRandomBackground(2, andPlay=True)
		
		if(self.countdownToNextShortSound() <= 0.0):
			## weve passed or reached our target time, and need to play another
			## short sound
			if(not self.shortSoundChannel.get_busy()):
				self.chooseRandomShortSound(andPlay=True)
				## load up the short sound and get it playing
				self.lastShortSoundTime = time.time()
				## note what time we played the sound at to measure the delay to
				## the next by
				self.waitUntilNextShortSound = getValueFromGaussian(30, 10, 5)
				## pick a new value from the gaussian distribution with mean 30s
				## stdev 10s, and a min value of 5s, this will be how long we
				## wait in seconds before playing the next short sound
			
			## in case else, we just keep waiting until the short sound channel
			## is free (presumably we had an oddly long short sound taking up
			## the channel on a really short delay from the gaussian generator,
			## just a one in a million sort of thing)
			
			## technically this does make the delay overlong, but its likely
			## negligible

	## method
	
	## lets us know how long we have to wait until the next short sound should
	## be played

	def countdownToNextShortSound(self):
		return (self.waitUntilNextShortSound - (time.time()-self.lastShortSoundTime))






