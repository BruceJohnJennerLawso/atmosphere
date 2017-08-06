## deletableSound.py ###########################################################
## wrap up the pygame sound type in an object so we can get rid ################
## of it and its massive ram hit ###############################################
################################################################################
import pygame


class Sound(object):
	
	## constructor
	
	## take a basic list of properties a sound must have and store them in this
	## object, 
	## the filePath (where to load the sound from), 
	## the volume adjustment (relative to blaring everything at full because not
	## every track is at a similar volume level unfortunately),
	## the soundType, one of ['music', 'short', 'background']
	
	def __init__(self, filePath, volume, soundType):
		self.filePath = filePath
		self.volume = volume
		self.soundType = soundType
		## record the arguments in the object
		
		
		self.playCount = 0
		## ticker for how many times the track has played in this session
		## (ie this lifetime of the sound object)
		self.pygameSound = []
		## storage container for the actual pygame.mixer.Sound object that this
		## class wraps
		self.loaded = False
		## start off with the flag for this sound set to off 
		## (because the sound file has not been loaded into memory yet at
		## construction)
	
	## method
	
	## if the sound object is not loaded up, construct a pygame.mixer.Sound in
	## the container list, otherwise do nothing
	
	def loadSound(self):
		if(not self.pygameSound):
			self.pygameSound.append(pygame.mixer.Sound(self.filePath))
			## takes a decent amount of time, and consumes a much larger RAM
			## footprint than the file size itself (decompressed)
		self.loaded = True
		## flip the state flag so we know the sound has been loaded into memory
		## and is "ready to go"
	
	## method
	
	## empty the list containing the pygame.mixer.Sound object, freeing up the
	## memory it was stored in. Not nearly as slow in terms of cpu ticks as
	## loadSound, but it does appear to take some time on the clock when this
	## runs	
		
	def clearSound(self):
		del self.pygameSound[:]
		## restores self.pygameSound to an empty list
		self.loaded = False
		## flip the state flag so we know the sound is considered "unloaded"

	
	## method
	
	## return the value of our loaded flag, so we can see if this thing is
	## loaded into memory or not
	
	def isLoaded(self):
		return self.loaded

		
	## method
	
	## if the pygame.mixer.Sound object is available, we will want to retrieve
	## it to do stuff with it (play it, mainly), so getSound returns the object
	## that weve worked so hard to store
	
	## note in retrospect Im not terribly fond of this volumeModifier parameter,
	## seems like asking for unexpected behaviours
		
	def getSound(self, volumeModifier=1.0):
		if(not self.isLoaded()):
			##self.loadSound()
			## old behaviour was to force loading a sound, which I am disliking
			## because it encourages halts in the middle of the program
			
			## changing this to none type
			return None
		else:
			self.pygameSound[0].set_volume(volumeModifier*self.volume)
			return self.pygameSound[0]
	
	## method
	
	## increment the play counter for this session (but not for the entire
	## history of this file
	
	def incrementPlayCounter(self):
		self.playCount += 1
	
	## method
	
	## get how many times this sound has been played this session (ie the
	## lifetime of this particular object)
		
	def getPlayCounter(self):
		return self.playCount

	## method
	
	## get the volume for this particular sound object, ie a modifier from 0.0
	## to 1.0 inclusive, which is applied to the sound object when we return it,
	## 0.0 making the sound silent, 1.0 making it full volume

	def getVolume(self):
		return self.volume
	
	## method
	
	## set the volume parameter for this sound to something between 0.0 and 1.0,
	## if we are handed a value outside of those bounds, we force it to the 
	## nearest point on the range 0.0 to 1.0
	
	def setVolume(self, volume):
		if(0.0 <= volume <= 1.0):
			self.volume = volume
		else:
			if(volume > 1.0):
				self.volume = 1.0
			elif(volume < 0.0):
				self.volume = 0.0
	
	## method
	
	## return the type 'tag' of this sound, one of ['music', 'background', 'short']
	
	def getSoundType(self):
		return self.soundType



## test loads up all sounds available in an environment file and demo loading
## them up as a sound object before discarding them again to demo the ability to
## load and clear large chunks of memory

if __name__ == '__main__':

	import envLoader
	## this is only required for our all up test of the sound loading/discard
	## system, no need to weigh down the rest of the app with needless imports
	
	pygame.init()
	pygame.mixer.init()
	
	music = pygame.mixer.Channel(5)
	## I believe this was related to playing simultaneous sounds (each channel
	## can only wait for the sound playing before to finish, whereas the
	## channels can play simultaneous)
	
	musics = []
	for fileNm in envLoader.getFilesList('./envfiles/ebonHawk2.csv'):
		fileName = fileNm[0]	
		fileVolume = fileNm[1]
		fileType = fileNm[2]
		## one of ['music', 'short', 'background']
		print "Loading music file %s" % fileName
		filePath = "./data/%s" % fileName
		musics.append(Sound(filePath, fileVolume, fileType))		

	print "Filenames Loaded...\n"
	raw_input("Press Enter to continue...")
	## hold the app


	print "loading music sound files to memory...\n"
	for snd in musics:
		snd.loadSound()
	print "finished music sound files to memory\n"

	raw_input("Press Enter to continue...")

	print "flushing music sound files from memory...\n"
	for snd in musics:
		if(snd.isLoaded()):
			snd.clearSound()
		
		## drop each sound file out of memory so the huge chunk of memory
		## consumed can be freed
	##print musics
	print "finished clearing music sound files from memory"
	raw_input("Press Enter to continue...")
	
	
	
	
	
	
