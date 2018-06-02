## uiTools.py ##################################################################
## wrapping some of the more complex pieces of UI code to make it a ############
## bit more robust #############################################################
################################################################################


from Tkinter import Tk
import pygame

def isBetween(value, lower, upper):
	if(upper < lower):
		return isBetween(value, upper, lower)
	
	if((value >= lower)and(value <= upper)):
		return True
	return False

## note that all y coordinates are measured from top of screen downwards, and
## all x coordinates are measured from the


blue=(0,0,255)
green=(0,200,120)
red=(170,0,0)

	##unpauseTriangle = [[10, 10], [25, 20],[ 10, 30]]

	
def getUnpauseTriangleBox(horizontalOffset=False):
	if(not horizontalOffset):
		return [[unpauseTriangle[0][0], unpauseTriangle[0][1]],[unpauseTriangle[1][0], unpauseTriangle[2][1]]]
	else:
		return [[unpauseTriangle[0][0]+horizontalOffset, unpauseTriangle[0][1]],[unpauseTriangle[1][0]+horizontalOffset, unpauseTriangle[2][1]]]
	

class uiButton(object):
	def __init__(self):
		pass
		
	
	## getButtonPosition: None -> Dict{"x": Num, "y": Num}
		
	def getButtonPosition(self):
		return self.position
		
	def getButtonHeight(self):
		return self.height
		
	def getButtonWidth(self):
		return self.width

		
	def getEffectiveButtonHeight(self):
		if hasattr(self, 'effectiveHeight'):
			return self.effectiveHeight
		else:
			return self.height

	def getEffectiveButtonWidth(self):
		if hasattr(self, 'effectiveWidth'):
			return self.effectiveWidth
		else:
			return self.width

	## the difference between height and effective height is 
	##
	## -height is the literal height covered by the visible button onscreen
	## -effective height is the height of the buttons interaction box on the
	## screen, ie so a sliderBar might only be 5 pixels tall, but its track runs
	## 100 pixels, and the user can use a scrollwheel event anywhere in that
	## track to adjust the sliders state
					
					
					
	## positionInButtonArea: Dict{"x": Num, "y": Num} -> Bool
	
	def positionInButtonArea(self, somePosition):
		if(isBetween(somePosition["x"], self.getButtonPosition()["x"], self.getButtonPosition()["x"]+self.getButtonWidth())):
			if(isBetween(somePosition["y"], self.getButtonPosition()["y"], self.getButtonPosition()["y"]+self.getButtonHeight())):
				return True
		return False

		
	def positionInButtonEffectiveArea(self, somePosition):
		if(isBetween(somePosition["x"], self.getButtonPosition()["x"], self.getButtonPosition()["x"]+self.getEffectiveButtonWidth())):
			if(isBetween(somePosition["y"], self.getButtonPosition()["y"], self.getButtonPosition()["y"]+self.getEffectiveButtonHeight())):
				return True
		return False		

class pausePlayButton(uiButton):
	def __init__(self, buttonPosition, buttonHeight, buttonWidth, buttonPlaying=False):
		self.position = buttonPosition
		self.height = buttonHeight
		self.width = buttonWidth
		if(buttonPlaying):
			self.state = "playing"
		else:
			self.state = "paused"
		##unpauseTriangle = [[10, 10], [25, 20],[ 10, 30]]
		self.unpauseTriangleCoordinates = [ [self.position["x"], self.position["y"]], [self.position["x"]+self.width, self.position["y"]+(0.5*self.height)], [self.position["x"], self.position["y"]+self.height] ]


	
	def getBoxCoordinates(self):
		return [[self.position["x"], self.position["y"]], [self.position["x"]+self.width, self.position["y"]], [self.position["x"]+self.width, self.position["y"]+self.height], [self.position["x"], self.position["y"]+self.height]]
	
	def renderButton(self, screen):
		if(self.state == "paused"):
			pygame.draw.polygon(screen,blue,self.unpauseTriangleCoordinates, 0)
			## the render call for the unpause triangle
		elif(self.state == "playing"):
			
			pauseBoxFraction = 0.34
			## whatever this is it has to be below a half, or youll just get a
			## box
			
			pauseBoxOffset = int(self.width*pauseBoxFraction)
			## has to be rounded to int, or floats get passed to pygames 
			## rendering call and nothing comes out looking right
			
			pauseBoxA = [[self.position["x"], self.position["y"]], [self.position["x"]+pauseBoxOffset, self.position["y"]], [self.position["x"]+pauseBoxOffset, self.position["y"]+self.height], [self.position["x"], self.position["y"]+self.height]]
			pauseBoxB = [[(self.position["x"]+self.width)-pauseBoxOffset, self.position["y"]], [self.position["x"]+self.width, self.position["y"]], [self.position["x"]+self.width, self.position["y"]+self.height], [(self.position["x"]+self.width)-pauseBoxOffset, self.position["y"]+self.height]]


			pygame.draw.polygon(screen,blue,pauseBoxA, 0)
			pygame.draw.polygon(screen,blue,pauseBoxB, 0)

		elif(self.state == "stopped"):
			pygame.draw.polygon(screen,blue,self.getBoxCoordinates(), 0)

	def flipState(self):
		if(self.state == "playing"):
			self.state = "paused"
		elif(self.state == "paused"):
			self.state = "playing"

	def click(self, someFunc=None, *args):
		self.flipState()
		if(someFunc != None):
			someFunc(self.state, *args)


class sliderBar(uiButton):
	## trackPosition is a Dict{"x": Num, "y": Num}
	## paramRange is a Dict{"min": Num, "max": Num}
	def __init__(self, trackPosition, trackHeight, paramRange, buttonHeight, buttonWidth, buttonColour, startValue="max"):
		self.paramRange = paramRange
		self.value = startValue
		
		self.position = trackPosition
		self.trackHeight = trackHeight
		
		self.buttonHeight = buttonHeight
		self.buttonWidth = buttonWidth
		## just for reference for later
		
		self.height = self.buttonHeight
		## height of the button rendered onscreen
		self.effectiveHeight = self.trackHeight
		## height of the track the button can move in
		self.width = self.buttonWidth
		## these specially set parameters will need to be reset if trackHeight
		## or buttonWidth is manually changed after construction
		
		self.buttonColour = buttonColour
		
	def getSliderValue(self):
		if(value == "max"):
			return self.paramRange["max"]
		elif(value == "min"):
			return self.paramRange["max"]
		else:
			return self.value
			## return numeric value
	
	
	def renderButton(self, screen):
			sliderBox = [[self.position["x"], self.position["y"]], [self.position["x"]+pauseBoxOffset, self.position["y"]], [self.position["x"]+pauseBoxOffset, self.position["y"]+self.height], [self.position["x"], self.position["y"]+self.height]]

			pygame.draw.polygon(screen,self.buttonColour,sliderBox, 0)
			
			

if(__name__ == "__main__"):
	unpauseTriangle = [[10, 10], [25, 20],[ 10, 30]]
	print getUnpauseTriangleBox(horizontalOffset=False)

