## deletableSound.py ###########################################################
## wrap up the pygame sound type in an object so we can get rid ################
## of it and its massive ram hit ###############################################
################################################################################
import pygame
import envLoader


class Sound(object):
	
	def __init__(self, filePath, volume, soundType):
		self.filePath = filePath
		self.volume = volume
		self.soundType = soundType
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
		
	def getSoundType(self):
		return self.soundType



if __name__ == '__main__':

	
	pygame.init()
	
	pygame.mixer.init()
	
	music = pygame.mixer.Channel(5)
	
	
	##[('./data/swtor%i.ogg' % i) for i in range(1,40)]
	
	musics = []
	for fileNm in envLoader.getFilesList('./envfiles/swtorHawk.csv'):
		print "Loading music file %s" % fileNm[0]
		##musics.append(pygame.mixer.Sound("./data/%s" % fileNm[0]))
		musics.append(Sound("./data/%s" % fileNm[0], fileNm[1], fileNm[2]))		

	raw_input("Press Enter to continue...")
	print "loading music list"
	for snd in musics:
		snd.loadSound()


	raw_input("Press Enter to continue...")
	print "flushing music list"
	for snd in musics:
		snd.clearSound()
	print musics
	raw_input("Press Enter to continue...")
	
	
	
	
	
	
