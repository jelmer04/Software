import platform
from tkinter import *
from tkinter import ttk

if platform.system() == "Linux":
    testing = False
else:
    testing = True

root = Tk()
root.overrideredirect(True)
root.title("Feet to Meters")

if testing:
    root.geometry("320x240+450+350")
else:
    root.geometry("320x240+0+0")
    root.config(cursor="none")


style = ttk.Style()
style.theme_use("default")
#style.configure("TButton", background="#00ffff")
#style.configure("TFrame", background="#ff0000")
#style.configure("TLabel", background="#00ff00")
style.configure("Title.TLabel", background="#ffff00", font="Helvetica 24", padding="10 0 0 0")


class Menu(ttk.Frame):
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)
        self.grid(row=0, column=0)
        self.grid_columnconfigure(0, minsize=320)
        self.grid_rowconfigure(0, minsize=40)
        self.grid_rowconfigure(1, minsize=200)
        self.bind("<Key-Escape>", quit)

        self.create()

    def create(self):
        # Menu title bar
        titleframe = ttk.Frame(self)
        titleframe.grid(column=0, row=0, sticky=(N, E, W))
        titleframe.columnconfigure(0, minsize=20)
        titleframe.rowconfigure(0, minsize=40)

        self.backimage = PhotoImage(file="back.gif")
        ttk.Button(titleframe, image=self.backimage, command=self.destroy).grid(row=0, column=0, sticky=(N, E, S, W))

        ttk.Label(titleframe, text="Menu Title", style="Title.TLabel").grid(row=0, column=1, sticky=(N, E, S, W))

        # Menu content
        mainframe = ttk.Frame(self, padding="0")
        mainframe.grid(column=0, row=1, sticky=(N, W, E, S))
        mainframe.grid_rowconfigure(0, minsize=100)
        mainframe.grid_rowconfigure(1, minsize=100)
        mainframe.grid_columnconfigure(0, minsize=160)
        mainframe.grid_columnconfigure(1, minsize=160)

        ttk.Button(mainframe, text="Button 1").grid(row=0, column=0, sticky=(N, E, S, W))
        ttk.Button(mainframe, text="Button 2").grid(row=0, column=1, sticky=(N, E, S, W))
        ttk.Button(mainframe, text="Button 3").grid(row=1, column=0, sticky=(N, E, S, W))
        ttk.Button(mainframe, text="Button 4", command=quit).grid(row=1, column=1, sticky=(N, E, S, W))


menu = Menu(master=root)
root.mainloop()