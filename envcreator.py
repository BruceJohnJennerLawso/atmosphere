## envcreator.py ###############################################################
## use a file selection dialog to pick audio files to be used ##################
## in a playlist saved by this script ##########################################
################################################################################
from Tkinter import Tk
from Tkinter import *
from tkFileDialog import askopenfilename
import tkFileDialog
import ntpath

from sys import argv

def getScaleValue(scaleTitle, scaleUnits):

	def setVal(val):
		global outputVal
		outputVal = val
	
	def endControl():
		control.destroy()
	
	control=Tk()

	control.protocol("WM_DELETE_WINDOW",endControl)
	

	control.title(scaleTitle)
	control.geometry("650x100+100+250")
	cline1=Label(text=scaleUnits).pack()
	
	cline3=Scale(control,orient=HORIZONTAL,length=580,width=20,sliderlength=10,from_=0,to=100,tickinterval=5, command=setVal)
	cline3.set(50)
	cline3.pack()

	control.mainloop()
	return outputVal


def getListOfFiles(dialogPrompt):
	dialog = Tk()
	filez = tkFileDialog.askopenfilenames(parent=dialog,title=dialogPrompt,initialdir='./data')
	files = [nm for nm in filez]
	return files

def file_save(text2save):
	f = tkFileDialog.asksaveasfile(mode='w', defaultextension=".csv", initialdir='./envfiles')
	if f is None:
		return True
		## hit cancel button, didnt save anything
	f.write(text2save)
	f.close()

if(__name__ == "__main__"):


	outputCsv = ""

	backgroundFiles = getListOfFiles('Choose background sounds')
	backgroundVolume = getScaleValue('Background sounds volume', 'Volume')
	musicFiles = getListOfFiles('Choose background music')	
	musicVolume = getScaleValue('Music volume', 'Volume')

	for background in backgroundFiles:
		outputCsv += "%s,%s,%s\n" % (ntpath.basename(background), backgroundVolume,'background')
	for music in musicFiles:
		outputCsv += "%s,%s,%s\n" % (ntpath.basename(music), musicVolume,'music')		
	print outputCsv
	
	file_save(outputCsv)

