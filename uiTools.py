## uiTools.py ##################################################################
## wrapping some of the more complex pieces of UI code to make it a ############
## bit more robust #############################################################
################################################################################


from Tkinter import Tk


def isBetween(value, lower, upper):
	if(upper < lower):
		return isBetween(value, upper, lower)
	
	if((value >= lower)and(value <= upper)):
		return True
	return False

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
		
	## positionInButtonArea: Dict{"x": Num, "y": Num} -> Bool
	
	
	
	def positionInButtonArea(self, somePosition):
		if(isBetween(somePosition["x"], self.getButtonPosition()["x"], self.getButtonPosition()["x"]+self.getButtonWidth())):
			if(isBetween(somePosition["y"], self.getButtonPosition()["y"], self.getButtonPosition()["y"]+self.getButtonHeight())):
				return True
		return False

if(__name__ == "__main__"):
	

