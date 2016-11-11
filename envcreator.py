## envcreator.py ###############################################################
## use a file selection dialog to pick audio files to be used ##################
## in a playlist saved by this script ##########################################
################################################################################
from Tkinter import Tk
from Tkinter import *
from tkFileDialog import askopenfilename
import tkFileDialog
import ntpath


import sliders

from sys import argv

def getScaleValue(scaleTitle, scaleUnits):

	def setVal(val):
		global outputVal
		outputVal = val
	
	def endControl():
		control.destroy()
	##Tk().withdraw()
	control=Tk()
	control.withdraw()
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
	dialog.withdraw()
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


def addBackgroundTracksToCsv(outputCsv):
	backgroundFiles = getListOfFiles('Choose background sounds')
	backgroundVolume = sliders.getScaleValue('Background sounds volume', 'Volume')
	for background in backgroundFiles:
		outputCsv[0] += "%s,%s,%s\n" % (ntpath.basename(background), backgroundVolume,'background')


def addShortSoundClipsToCsv(outputCsv):
	shortSoundFiles = getListOfFiles('Choose background sounds (short)')	
	shortSoundVolume = sliders.getScaleValue('Short background volume', 'Volume')
	for short in shortSoundFiles:
		outputCsv[0] += "%s,%s,%s\n" % (ntpath.basename(short), shortSoundVolume,'short')	

def addMusicTrackToCsv(outputCsv):
	musicFiles = getListOfFiles('Choose background music')	
	musicVolume = sliders.getScaleValue('Music volume', 'Volume')	
	for music in musicFiles:
		outputCsv[0] += "%s,%s,%s\n" % (ntpath.basename(music), musicVolume,'music')	

if(__name__ == "__main__"):
	outputCsv = ""
	output = [outputCsv]
	def fuckup(output):
		output[0] = "foobar"
		print outputCsv
	
	win = Tk()
	


	def endApp():
		win.destroy()
		
		if(output[0] != ""):
			file_save(output[0])
		

		fuckup(output)
		print "outputCsv: ", output[0]
		exit()
		
	win.protocol("WM_DELETE_WINDOW",endApp)
	
	
	button1 = Button(win, text="Add Background Track (Long)", command=lambda: addBackgroundTracksToCsv(output))
	button2 = Button(win, text="Add Background Sound (Short)", command=lambda: addShortSoundClipsToCsv(output))	
	button3 = Button(win, text="Add Music Track", command=lambda: addMusicTrackToCsv(output))	
	button4 = Button(win, text="Exit", command=lambda: endApp())		

	buttons = [button1, button2, button3, button4]
	for button in buttons:
		button.pack()
		
	def after(self, ms, func=None, *args):
		print output
		
	win.mainloop()


def originalStuff():
	outputCsv = ""

	backgroundFiles = getListOfFiles('Choose background sounds')
	backgroundVolume = getScaleValue('Background sounds volume', 'Volume')
	musicFiles = getListOfFiles('Choose background music')	
	musicVolume = getScaleValue('Music volume', 'Volume')
	shortSoundFiles = getListOfFiles('Choose background sounds (short)')	
	shortSoundVolume = getScaleValue('Short background volume', 'Volume')

	for background in backgroundFiles:
		outputCsv += "%s,%s,%s\n" % (ntpath.basename(background), backgroundVolume,'background')
	for music in musicFiles:
		outputCsv += "%s,%s,%s\n" % (ntpath.basename(music), musicVolume,'music')		
	for short in shortSoundFiles:
		outputCsv += "%s,%s,%s\n" % (ntpath.basename(short), shortSoundVolume,'short')		
	print outputCsv
	
	if(outputCsv != ""):
		file_save(outputCsv)
