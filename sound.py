## deletableSound.py ###########################################################
## wrap up the pygame sound type in an object so we can get rid ################
## of it and its massive ram hit ###############################################
################################################################################
import pygame


class Sound(object):
	
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
		## 
		self.playCount = 0
		
		self.pygameSound = []
		
		self.loaded = False
	
	def loadSound(self):
		if(not self.pygameSound):
			self.pygameSound.append(pygame.mixer.Sound(self.filePath))
		self.loaded = True
		
	def clearSound(self):
		del self.pygameSound[:]
		self.loaded = False
		
	def getSound(self, volumeModifier=1.0):
		if(not self.loaded):
			self.loadSound()
		for snd in self.pygameSound:
			snd.set_volume(volumeModifier*self.volume)
		return self.pygameSound[0]
	
	def incrementPlayCounter(self):
		self.playCount += 1
		
	def getPlayCounter(self):
		return self.playCount

	def getVolume(self):
		return self.volume
	
	def setVolume(self, volume):
		self.volume = volume
		
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
		snd.clearSound()
		## drop each sound file out of memory so the huge chunk of memory
		## consumed can be freed
	##print musics
	print "finished clearing music sound files from memory"
	raw_input("Press Enter to continue...")
	
	
	
	
	
	
