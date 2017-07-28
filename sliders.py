## sliders.py ##################################################################
## all manner of useful widgets to get yo sliding needs done ###################
## looks like this was just a testbed I had for learning how the tkinter #######
## sliders work ################################################################
################################################################################
from Tkinter import Tk
import Tkinter as tk

from sys import argv

def getScaleValue(scaleTitle, scaleUnits):

	def setVal(val):
		global outputVal
		outputVal = val
	
	def endControl():
		control.destroy()
	
	control=tk.Tk()

	control.protocol("WM_DELETE_WINDOW",endControl)

	control.title()
	control.geometry("650x100+100+250")
	cline1=tk.Label(control, text=scaleUnits).pack()
	
	cline3=tk.Scale(control,orient=tk.HORIZONTAL,length=580,width=20,sliderlength=10,from_=0,to=100,tickinterval=5, command=setVal)
	cline3.set(50)
	cline3.pack()
	control.mainloop()
	print "Slider widget outputting ", outputVal
	return outputVal
	
if(__name__ == "__main__"):
	print getScaleValue("Test Scale", "Units")
