from tkinter import *
from configparser import ConfigParser
import pyquark, playsound

root = Tk()
root.geometry("800x600")
root.title("Planetoids - Stats")
root.iconbitmap("images/asteroid.ico")
root.resizable(False, False)

# Background
bg = PhotoImage(file = "images/title.png")
bg_label = Label( root, image = bg)
bg_label.place(x = -2,y = 0)

back_img = PhotoImage(file= "images/back_button.png")

config_object = ConfigParser()
config_object.read("config.ini")

scores = config_object["SCORES"]

def quit():
	playsound.playsound('pressed.wav')
	pyquark.filestart("title.pyw")
	root.destroy()

def refresh():
	config_object.read("config.ini")
	scores = config_object["SCORES"]
	score_label.config(text= scores["highscore"] + "\t\t" + scores["latest"])

def reset():
	scores["HIGHSCORE"] = "0"
	scores["LATEST"] = "0"
	with open('config.ini', 'w') as conf:
		config_object.write(conf)
	refresh()

Label(root, text= "HIGHSCORE:\tLATEST:", font= (("helvetica"), 40), bg= "black", fg= "white")
score_label = Label(root, text= scores["highscore"] + "\t\t" + scores["latest"], font= (("courier new"), 40), bg= "black", fg= "white")
score_label.place(x= 150, y= 240)

Button(root, text= "Reset", command= reset, bg= "white").place(x= 600, y= 500)
Button(root, image= back_img, command=quit).place(x= 270, y= 450)

root.protocol("WM_DELETE_WINDOW", quit)
root.mainloop()