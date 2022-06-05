from tkinter import *
import playsound, pyquark

root = Tk()
root.iconbitmap("images/asteroid.ico")
root.title("Planetoids - Guide")
root.geometry("800x600")
root.resizable(False, False)

# Background
bg = PhotoImage(file = "images/title.png")
bg_label = Label(root, image = bg)
bg_label.place(x = -2,y = 0)

def quit():
	playsound.playsound('pressed.wav')
	pyquark.filestart("title.pyw")
	root.destroy()

guide = """
- Move with arrow keys
- Avoid the asteroids
- Collect hearts to boost your live (You can't have more than three)
- Get to the other side to beat the level

- There are infinite levels
- Boss fights coming soon!
"""



text = Text(root)
text.insert(END, guide)
text.config(state=DISABLED)
text.place(x= 100, y= 200)

root.protocol("WM_DELETE_WINDOW", quit)
root.mainloop()