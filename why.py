## why.py ######################################################################
## why u do dis to me ##########################################################
################################################################################
from pygame import mixer # Load the required library
import pygame
import multiprocessing as mp

def playMusic(musicName):
	pygame.mixer.music.load('./data/%s' % musicName)
	pygame.mixer.music.play(0)	

	clock = pygame.time.Clock()
	clock.tick(10)
	while pygame.mixer.music.get_busy():
		pygame.event.poll()
		clock.tick(10)

def runMultithreaded():

	p1 = mp.Process(target = playMusic, args=("ebonHawkMainHold.mp3",), name = "mainHold")
	p2 = mp.Process(target = playMusic, args=("ebonHawkEngineRoom.mp3",), name = "engineRoom")

	procs = [p1, p2]
	
	for p in procs:
		p.start()

def runLinear():
	p1 = mp.Process(target = playMusic, args=("ebonHawkMainHold.mp3",), name = "mainHold")
	p2 = mp.Process(target = playMusic, args=("ebonHawkEngineRoom.mp3",), name = "engineRoom")

	procs = [p1, p2]
	
	p1.start()
	
	
if(__name__ == "__main__"):
	pygame.init()
	##pygame.display.set_mode((200,100))
	##pygame.mixer.music.load('./data/acousticSunrise.ogg')
	##pygame.mixer.music.play(0)

	##runMultithreaded()
	runLinear()
