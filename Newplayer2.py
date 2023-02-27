#The better version of the mp3 player, Finds every single mp3 and wav file in the comp
import tkinter
import os
from audioplayer import AudioPlayer
import multiprocessing as mp
import numpy as np

#list of all the songs in the computer
stuf = []
n = 0
#Searching these two folders for audio files
listofitems = os.walk(".")
listofitems = list(listofitems)
listofitems = np.array(listofitems)
#searching through for audio files.
for dirc,useless,item in listofitems:
	for item2 in item:
		if ".mp3" in item2 or ".wav" in item2 in item2:
			stuf.append(dirc + "\\" + item2)

#This checks to see if there is a musiclist file and if there isn't, creates it
#utf-8 encoding is used because it raises an encoding error otherwise
musiclist = open("musiclist.txt", "a", encoding = "utf-8")
musiclist.close()

#This code is used to compare the songs inside the songs within the text file with
#the songs in the list to make sure repeat songs do not appear
musiclist = open("musiclist.txt", "r", encoding = "utf-8")
lines = musiclist.readlines()

for item in lines:
	for item2 in stuf:
		if item2 in item:
			stuf.remove(item2)
musiclist.close()

#Now the songs in the list stuf are added to the text file musiclist.txt
musiclist = open("musiclist.txt", "a", encoding = "utf-8")

for item in stuf:
	musiclist.write(item + "\n")
musiclist.close()

musiclist = open("musiclist.txt", "r", encoding = "utf-8")
lines = musiclist.readlines()

stuf = []
for item in lines:
	addedsong = ''
	for item2 in item:
		
		if item2 == '\\':
			addedsong = ''
			continue
		
		if item2 == "\n":
			break

		addedsong = addedsong + item2

	stuf.append(addedsong)

#A window is made in tkinter to be used in the program
mainwindow = tkinter.Tk()

#A listbox widget is added for the music and a scrollbar widget to scroll through the listbox
scroller = tkinter.Scrollbar(mainwindow)
tracklist = tkinter.Listbox(mainwindow,bd = 5, width = 100, yscrollcommand = scroller.set)

#songs are added to the listbox
for item in stuf:
	tracklist.insert(n,item)
	n = n+1

#a volume control widget is added in the form of a scale
listofmusic = []
listofprocesses = []

#This function is bound to the listbox to decide which song is played and to make sure two songs dont play at the same time
def musicselection(placeholder = 0):
	global loopvalue
	file = ''
	curser = tracklist.curselection()[0]
	for item in lines[curser]:
		if item == '\n':
			break
		file = file + item

	listofmusic.append(AudioPlayer(file))
	listofmusic[-1].volume = Volumecontrol.get()
	try:
		listofmusic[-1].play(loopvalue)
	except FileNotFoundError:
		tracklist.delete(curser)
	if len(listofmusic) > 1:
		remover = listofmusic.pop(0)
		remover.stop()
		remover.close()

#This function handles the volume of the audio
def Volumechange(Volume1):
	if len(listofmusic) >= 1:
		listofmusic[-1].volume = int(Volume1)
	else:
		pass

#This function handles pausing and playing the songs
Pauseval = 0
def Pauseplay():
	#Simple way of making sure if the song is paused or playing
	global Pauseval
	if len(listofmusic) >= 1 and Pauseval == 0:
		listofmusic[-1].pause()
		Pauseval = 1
	elif len(listofmusic) >= 1 and Pauseval == 1:
		listofmusic[-1].resume()
		Pauseval = 0
	else:
		pass

#this function plays the next song in the list
def nexta():
	if len(listofmusic) >= 1:
		#this is the next index after the current one
		selc = tracklist.curselection()[0] + 1
		#this clears the selection of the previous index so it doesn't cause problems with the player
		tracklist.selection_clear(tracklist.curselection()[0])
		tracklist.selection_set(selc)
		musicselection()

#This function plays the previous song in the list
def previa():
	if len(listofmusic) >= 1 and (tracklist.curselection()[0] - 1) != -1:
		#this is the previous index after the current one
		selc = tracklist.curselection()[0] -1
		#this clears the selection of the previous index so it doesn't cause problems with the player
		tracklist.selection_clear(tracklist.curselection()[0])
		tracklist.selection_set(selc)
		musicselection()

#This function handles looping. All it does is make a value true or false
loopvalue = False
def loopfunc():
	global loopvalue
	
	if loopvalue == False:
		loopvalue = True

	elif loopvalue == True:
		loopvalue = False
#the main loop of the tkinter box is given below as well as the packing and binding of functions
if __name__ == "__main__":

	tracklist.bind("<<ListboxSelect>>",musicselection)
	tracklist.pack(side = "left", fill = 'both')
	
	scroller.pack(side = "right", fill = "y")
	scroller.config(command = tracklist.yview)
	
	Volumecontrol = tkinter.Scale(mainwindow, from_ = 0, to = 100, label = "Volume", command = Volumechange)
	Volumecontrol.pack()
	
	Pausecontrol = tkinter.Button(mainwindow, text = 'Pause', command = Pauseplay, width = 5)
	Pausecontrol.pack()

	Loopcontrol = tkinter.Button(mainwindow, text = 'Loop',command = loopfunc, width = 5)
	Loopcontrol.pack()

	Nextcontrol = tkinter.Button(mainwindow, text = 'Next', command = nexta, width = 5)
	Nextcontrol.pack()

	Prevcontrol = tkinter.Button(mainwindow, text = 'Previous', command = previa, width = 5)
	Prevcontrol.pack()

	#Delcontrol = tkinter.Button(mainwindow, text = 'Delete', command = deletes, width = 5)
	#Delcontrol.pack()

	mainwindow.mainloop()