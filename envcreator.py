## envcreator.py ###############################################################
## use a file selection dialog to pick audio files to be used ##################
## in a playlist saved by this script ##########################################
################################################################################
from Tkinter import Tk
import Tkinter as tk
from Tkinter import *
from tkFileDialog import askopenfilename
import tkFileDialog
import ntpath


import sliders

from sys import argv







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
	##backgroundVolume = sliders.getScaleValue('Background sounds volume', 'Volume')
	backgroundVolume = 30
	for background in backgroundFiles:
		outputCsv[0] += "%s,%s,%s\n" % (ntpath.basename(background), backgroundVolume,'background')
	print outputCsv

def addShortSoundClipsToCsv(outputCsv):
	shortSoundFiles = getListOfFiles('Choose background sounds (short)')	
	##shortSoundVolume = sliders.getScaleValue('Short background volume', 'Volume')
	shortSoundVolume = 25
	for short in shortSoundFiles:
		outputCsv[0] += "%s,%s,%s\n" % (ntpath.basename(short), shortSoundVolume,'short')	
	print outputCsv

def addMusicTrackToCsv(outputCsv):
	##print "Adding Music Track to csv: ", outputCsv
	musicFiles = getListOfFiles('Choose background music')	
	##print "Selected files, ", musicFiles
	##musicVolume = sliders.getScaleValue('Music volume', 'Volume')	
	musicVolume = 55
	##print "Adding line to outputCsv"
	for music in musicFiles:
		outputCsv[0] += "%s,%s,%s\n" % (ntpath.basename(music), 50,'music')	
		##outputCsv[0] += "%s,%s,%s\n" % (ntpath.basename(music), musicVolume,'music')			
	print outputCsv

if(__name__ == "__main__"):
	outputCsv = ""
	output = [outputCsv]
	
	

	
	win = Tk()
	


	def endApp():
		win.destroy()
		
		if(output[0] != ""):
			file_save(output[0])
		

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

	root = tk.Tk()
	main = MainWindow(root)
	main.pack(side="top", fill="both", expand=True)
	root.mainloop()

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
