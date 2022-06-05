from tkinter import *
from configparser import ConfigParser
import pyquark, playsound

root = Tk()
root.geometry("800x600")
root.title("Planetoids - Settings")
root.iconbitmap("images/asteroid.ico")
root.resizable(False, False)

# Background
bg = PhotoImage(file = "images/title.png")
bg_label = Label( root, image = bg)
bg_label.place(x = -2,y = 0)

back_img = PhotoImage(file= "images/back_button.png")

config_object = ConfigParser()
config_object.read("config.ini")

sound_volume = config_object["SOUNDVOLUME"]

def save():
	sound_volume["music"] = str(music.get())
	sound_volume["sfx"] = str(sound.get())
	with open('config.ini', 'w') as conf:
		config_object.write(conf)

def quit():
	save()
	playsound.playsound('pressed.wav')
	pyquark.filestart("title.pyw")
	root.destroy()

def scalesfx(value = None):
	playsound.playsound('pressed.wav')

music = Scale(root, from_=0, to=9, orient= HORIZONTAL, bg= "black", fg= "white", command= scalesfx)
music.set(sound_volume["music"])
Label(root, text= "Music", bg= "black", fg= "white", font= ("helvetica", 30)).place(x= 220, y= 150)
music.place(x= 220, y= 200)

sound = Scale(root, from_=0, to=9, orient= HORIZONTAL, bg= "black", fg= "white", command= scalesfx)
sound.set(sound_volume["sfx"])
Label(root, text= "SFX", bg= "black", fg = "white", font = ("helvetica", 30)).place(x= 430, y= 150)
sound.place(x= 420, y= 200)

Button(root, image= back_img, command=quit).place(x= 270, y= 450)

root.protocol("WM_DELETE_WINDOW", quit)
root.mainloop()