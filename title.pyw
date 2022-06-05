from tkinter import *
import pyquark, playsound

root = Tk()
root.iconbitmap("images/asteroid.ico")
root.title("Planetoids")
root.geometry("800x600")
root.resizable(False, False)


# Background
bg = PhotoImage(file = "images/title.png")
bg_label = Label(root, image = bg)
bg_label.place(x = -2,y = 0)

settings_img = PhotoImage(file= 'images/settings_button.png')
start_img = PhotoImage(file= 'images/start_button.png')
stats_img = PhotoImage(file= 'images/stats_button.png')
guide_img = PhotoImage(file= 'images/how_to_play.png')

def start_game():
    playsound.playsound('pressed.wav')
    pyquark.filestart("planetoids.pyw")
    root.destroy()

def start_settings():
    playsound.playsound('pressed.wav')
    pyquark.filestart("settings.pyw")
    root.destroy()

def start_guide():
    playsound.playsound('pressed.wav')
    pyquark.filestart('guide.pyw')
    root.destroy()

def start_stats():
    playsound.playsound('pressed.wav')
    pyquark.filestart("stats.pyw")
    root.destroy()

def quit(*args):
    playsound.playsound('pressed.wav')
    root.destroy()

start = Button(root, image= start_img, borderwidth= 0, bg= None, command= start_game)
start.place(x= 160, y= 170)

settings = Button(root, image= settings_img, borderwidth= 0, command= start_settings)
settings.place(x= 160, y= 410)

stats = Button(root, image= stats_img, borderwidth= 0, command= start_stats)
stats.place(x= 390, y= 410)

guide = Button(root, image= guide_img, borderwidth= 3, command= start_guide)
guide.place(x= 650, y= 409)

root.bind("q", quit)
root.protocol("WM_DELETE_WINDOW", quit)
root.mainloop()