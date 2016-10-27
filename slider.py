## tk slider demo ##############################################################
################################################################################
from Tkinter import *
import Tkinter as tk

def getScaleValue(scaleTitle, scaleUnits):

	def setVal(val):
		global outputVal
		outputVal = val
	
	def endControl():
		control.destroy()
	
	control=Tk()

	control.protocol("WM_DELETE_WINDOW",endControl)
	

	control.title(scaleTitle)
	control.geometry("650x100+100+50")
	cline1=Label(text=scaleUnits).pack()
	
	cline3=tk.Scale(control,orient=HORIZONTAL,length=580,width=20,sliderlength=10,from_=0,to=100,tickinterval=5, command=setVal)
	cline3.set(50)
	cline3.pack()

	control.mainloop()
	return outputVal

def internetzExample():
	def show_values():
		 return (w1.get(), w2.get())

	master = Tk()
	w1 = Scale(master, from_=0, to=42)
	w1.set(19)
	w1.pack()
	w2 = Scale(master, from_=0, to=200, orient=HORIZONTAL)
	w2.set(23)
	w2.pack()
	Button(master, text='Show', command=show_values).pack()

	mainloop()



if(__name__ =="__main__"):
	print getScaleValue("Volume Slider", "Volume")
	##internetzExample()
