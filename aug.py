## aug.py ######################################################################
## aug #########################################################################
################################################################################
import pyglet

if(__name__ == "__main__"):

	pyglet.lib.load_library('avbin')
	pyglet.have_avbin = True

	sound = pyglet.media.load('./data/ebonHawkMainHold.mp3', streaming=True)
	sound.play()
	pyglet.app.run()
