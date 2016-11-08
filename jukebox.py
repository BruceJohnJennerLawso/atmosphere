## jukebox.py ##################################################################
## app that plays background noise tracks and music ############################
## in parallel, tries to learn user preferences intelligently ##################
################################################################################
import envLoader
import sound

import random
import pygame

class Jukebox(object):
	
	def __init__(self, envFileName, debugInfo=False):
		self.sounds = []
		self.shortSounds = []
		self.musicSounds = []
		
		self.musicChannel = pygame.mixer.Channel(5)
		self.background1Channel = pygame.mixer.Channel(3)
		self.background2Channel = pygame.mixer.Channel(4)
		self.shortSoundChannel = pygame.mixer.Channel(6)
		
		self.loadEnvFile(envFileName, debugInfo)
		self.chooseInitialRandomBackgrounds()
		self.chooseInitialRandomMusic()

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
		while((newRandomBackground == getBackgroundSoundByChannelNo(1))and(newRandomBackground == getBackgroundSoundByChannelNo(2))):
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











