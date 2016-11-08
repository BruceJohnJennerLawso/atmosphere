## jukebox.py ##################################################################
## app that plays background noise tracks and music ############################
## in parallel, tries to learn user preferences intelligently ##################
################################################################################
import envLoader
import sound

import random
import time
import pygame

def isBetween(value, lower, upper):
	if((value >= lower)and(value <= upper)):
		return True
	return False



def getValueFromGaussian(mean, stdev, valFloor = 0):
	values = []
	while(len(values) < 100):
		value = random.gauss(mean, stdev)
		if(value > valFloor):
			values.append(value)
	return random.choice(values)

class Jukebox(object):
	
	def __init__(self, envFileName, debugInfo=False):
		self.sounds = []
		self.shortSounds = []
		self.musicSounds = []
		## lists of sound.Sound objects (a wrapper around pygame.mixer.Sound)
		
		self.musicChannel = pygame.mixer.Channel(5)
		self.background1Channel = pygame.mixer.Channel(3)
		self.background2Channel = pygame.mixer.Channel(4)
		self.shortSoundChannel = pygame.mixer.Channel(6)
		## channels which are used to play those sound objects, one at a time
		
		
		
		self.masterVolume = 1.0
		self.backgroundVolume = 1.0
		self.shortVolume = 1.0
		self.musicVolume = 1.0
		
		self.exitSignal = False
		## indicator that we want to end the loop and get out of here
		
		self.loadEnvFile(envFileName, debugInfo)
		## load up the objects with all of the info about the sounds, but
		## without loading them into memory just yet
		
		
		self.lastShortSoundTime = time.time()
		self.waitUntilNextShortSound = getValueFromGaussian(30.0, 10.0, 5.0)
		
		self.randomShortSound = random.choice(self.shortSounds)
		self.randomShortSound.loadSound()
		self.randomShortSound.setVolume(0.05)
		
		self.chooseInitialRandomBackgrounds()
		## pick out a pair of background noise tracks at random
		self.chooseInitialRandomMusic()
		## randomly select our first music track to play
		
		## once this is all done, the object is just waiting for
		## play() to be called

	def loadEnvFile(self, envFileName, debugInfo=False):

		if(debugInfo):
			print envLoader.getFilesList(envFileName)
	
		for sFile in envLoader.getFilesList(envFileName):
			decVolume = float(sFile[1]/100.0)
			if(sFile[2] == 'background'):
				self.sounds.append(sound.Sound('./data/%s' % sFile[0], decVolume, sFile[2]))
			elif(sFile[2] == 'short'):
				self.shortSounds.append(sound.Sound('./data/%s' % sFile[0], decVolume, sFile[2]))				
			elif(sFile[2] == 'music'):
				self.musicSounds.append(sound.Sound('./data/%s' % sFile[0], decVolume, sFile[2]))	
		## hoping if theres an exception here it gets thrown out to the main loop		

	def chooseInitialRandomBackgrounds(self):
		self.firstRandomChoice = random.choice(self.sounds)
		self.secondRandomChoice = random.choice(self.sounds)
		while(self.firstRandomChoice == self.secondRandomChoice):
			self.secondRandomChoice = random.choice(self.sounds)
			## keep trying until we get two different sounds
	
		self.firstRandomChoice.loadSound()
		self.secondRandomChoice.loadSound()

	def chooseInitialRandomMusic(self):
		
		self.randomMusic = random.choice(self.musicSounds)
		self.randomMusic.loadSound()

	def play(self):
		if(not self.musicChannel.get_busy()):
			self.musicChannel.play(self.randomMusic.getSound())
		if(not self.background1Channel.get_busy()):
			self.background1Channel.play(self.firstRandomChoice.getSound())	
		if(not self.background2Channel.get_busy()):
			self.background2Channel.play(self.secondRandomChoice.getSound())				

	def nextMusicTrack(self, fadetime=False):
		if(fadetime != False):
			self.musicChannel.fadeout(fadetime)
		else:
			self.musicChannel.fadeout()

	def getBackgroundSoundByChannelNo(self, channel):
		if(channel == 1):
			return self.firstRandomChoice
		elif(channel == 2):
			return self.secondRandomChoice
		else:
			print "bad call to getBackgroundSoundByChannelNo(%i)" % channel
			return []
			
	

	def chooseRandomBackground(self, channel, andPlay=False):
		newRandomBackground = random.choice(self.sounds)
		while((newRandomBackground == self.getBackgroundSoundByChannelNo(1))and(newRandomBackground == self.getBackgroundSoundByChannelNo(2))):
			newRandomBackground = random.choice(self.sounds)
		
		if(channel == 1):
			##self.firstRandomChoice.stop()
			
			## this would be a good safety feature for the future, but I dont
			## want to gum things up just yet
			self.firstRandomChoice.clearSound()
			## weve chosen a new file randomly to play in this slot, so we clear
			## out the old file
			self.firstRandomChoice = newRandomBackground
			## assign the new file to this slot
			self.firstRandomChoice.loadSound()	
			## load it up into memory
			if(andPlay):
				## if we specified in the parameters that we wanted the sound
				## to start playing right away, we get it rocking on the correct
				## channel
				self.background1Channel.play(self.firstRandomChoice.getSound())
				self.firstRandomChoice.incrementPlayCounter()
				## dont forget to increment the play counter for this thing
		elif(channel == 2):
			self.secondRandomChoice.clearSound()
			self.secondRandomChoice = newRandomBackground
			self.secondRandomChoice.loadSound()
			if(andPlay):
				self.background2Channel.play(self.secondRandomChoice.getSound())
				self.secondRandomChoice.incrementPlayCounter()
		else:
			## fuck
			print "Bad call to chooseRandomBackground(self, %i, andPlay)" % channel
	
	def chooseRandomMusic(self,andPlay=False):
		newRandomMusic = random.choice(self.musicSounds)
		while(newRandomMusic == self.randomMusic):
			newRandomMusic = random.choice(self.musicSounds)	
		
		self.randomMusic.clearSound()	
		self.randomMusic = newRandomMusic
		self.randomMusic.loadSound()
		if(andPlay):
			self.musicChannel.play(self.randomMusic.getSound())			
			self.randomMusic.incrementPlayCounter()
			
	def chooseRandomShortSound(self,andPlay=False):
		newRandomShortSound = random.choice(self.shortSounds)
		while(newRandomShortSound == self.randomShortSound):
			newRandomShortSound = random.choice(self.shortSounds)	
		
		self.randomShortSound.clearSound()	
		self.randomShortSound = newRandomShortSound
		self.randomShortSound.loadSound()
		self.randomShortSound.setVolume(0.05)
		if(andPlay):
			self.shortSoundChannel.play(self.randomShortSound.getSound())			
			self.randomShortSound.incrementPlayCounter()			
	
	def getBackgroundVolume(self):
		return (self.backgroundVolume*self.masterVolume)
		
	def getShortSoundVolume(self):
		return (self.shortVolume*self.masterVolume)
	
	def getMusicVolume(self):
		return (self.musicVolume*self.masterVolume)		
	
	def getMasterVolume(self):
		return self.masterVolume
	
	
	def setBackgroundVolume(self, newVolume):
		self.backgroundVolume = newVolume
		self.background1Channel.set_volume(self.getBackgroundVolume())
		self.background2Channel.set_volume(self.getBackgroundVolume())		
	
	def incrementBackgroundVolume(self, change):
		if(isBetween(self.getBackgroundVolume()+change, 0.0, 1.0)):
			self.setBackgroundVolume(self.getBackgroundVolume()+change)
		else:
			if(self.getBackgroundVolume()+change > 1.0):
				self.setBackgroundVolume(1.0)
			elif(self.getBackgroundVolume()+change < 0.0):
				self.setBackgroundVolume(0.0)	
				
	
	def setShortSoundVolume(self, newVolume):
		self.shortVolume = newVolume
		self.shortSoundChannel.set_volume(self.getShortSoundVolume())

	def incrementShortSoundVolume(self, change):
		if(isBetween(self.getShortSoundVolume()+change, 0.0, 1.0)):
			self.setShortSoundVolume(self.getShortSoundVolume()+change)
		else:
			if(self.getShortSoundVolume()+change > 1.0):
				self.setShortSoundVolume(1.0)
			elif(self.getShortSoundVolume()+change < 0.0):
				self.setShortSoundVolume(0.0)	
		
	def setMusicVolume(self, newVolume):
		self.musicVolume = newVolume
		self.musicChannel.set_volume(self.getMusicVolume())		

	def incrementMusicVolume(self, change):
		if(isBetween(self.getMusicVolume()+change, 0.0, 1.0)):
			self.setMusicVolume(self.getMusicVolume()+change)
		else:
			if(self.getMusicVolume()+change > 1.0):
				self.setMusicVolume(1.0)
			elif(self.getMusicVolume()+change < 0.0):
				self.setMusicVolume(0.0)	
		
	def setMasterVolume(self, newVolume):
		self.masterVolume = newVolume
		self.background1Channel.set_volume(self.getBackgroundVolume())
		self.background2Channel.set_volume(self.getBackgroundVolume())		
		self.shortSoundChannel.set_volume(self.getShortSoundVolume())			
		self.musicChannel.set_volume(self.getMusicVolume())	
		
	def incrementMasterVolume(self, change):
		if(isBetween(self.getMasterVolume()+change, 0.0, 1.0)):
			self.setMasterVolume(self.getMasterVolume()+change)
		else:
			if(self.getMasterVolume()+change > 1.0):
				self.setMasterVolume(1.0)
			elif(self.getMasterVolume()+change < 0.0):
				self.setMasterVolume(0.0)	

					
	def loop(self):
		if(not self.musicChannel.get_busy()):
			## music has finished, need to put another track on
			self.chooseRandomMusic(andPlay=True)
		if(not self.background1Channel.get_busy()):		
			## background sound on channel 1 has finished,
			## need to put another track on
			self.chooseRandomBackground(1, andPlay=True)
		if(not self.background2Channel.get_busy()):		
			## background sound on channel 2 has finished,
			## need to put another track on
			self.chooseRandomBackground(2, andPlay=True)
		
		if((time.time()-self.lastShortSoundTime) >= self.waitUntilNextShortSound):
			## weve passed or reached our target time, and need to play the
			if(not self.shortSoundChannel.get_busy()):
				self.chooseRandomShortSound(andPlay=True)
			self.lastShortSoundTime = time.time()
			self.waitUntilNextShortSound = getValueFromGaussian(30, 10, 5)

	def countdownToNextShortSound(self):
		return (self.waitUntilNextShortSound - (time.time()-self.lastShortSoundTime))






