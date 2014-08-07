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

ttk.Button(root, text="Quit", command=quit).grid(row=0, column=0, sticky=(N, E, S, W))

style = ttk.Style()
style.theme_use("default")
# style.configure("TButton", background="#00ffff")
# style.configure("TFrame", background="#ff0000")
#style.configure("TLabel", background="#00ff00")
style.configure("Title.TLabel", font="Helvetica 24", padding="10 0 0 0")


class Menu(ttk.Frame):
    def __init__(self, master=None, *args):
        ttk.Frame.__init__(self, master)
        self.grid(row=0, column=0)
        self.grid_columnconfigure(0, minsize=320)
        self.grid_rowconfigure(0, minsize=40)
        self.grid_rowconfigure(1, minsize=200)
        self.bind("<Key-Escape>", quit)

        self.create(*args)

    def create(self, title="Menu", names=[], commands=[]):
        # Menu title bar
        titleframe = ttk.Frame(self)
        titleframe.grid(column=0, row=0, sticky=(N, E, W))
        titleframe.columnconfigure(0, minsize=20)
        titleframe.rowconfigure(0, minsize=40)

        self.backimage = PhotoImage(file="back.gif")
        ttk.Button(titleframe, image=self.backimage, command=self.lower).grid(row=0, column=0, sticky=(N, E, S, W))

        ttk.Label(titleframe, text=title, style="Title.TLabel").grid(row=0, column=1, sticky=(N, E, S, W))

        # Menu content
        mainframe = ttk.Frame(self, padding="0")
        mainframe.grid(column=0, row=1, sticky=(N, W, E, S))

        if len(names) == 0:
            names = list("Button " + str(x + 1) for x in range(4))

        while len(commands) < len(names):
            commands.append(None)

        items = len(names)

        if items == 1:
            layouts = [(0, 0, 1, 1)]
            mainframe.grid_rowconfigure(0, minsize=200)
            mainframe.grid_columnconfigure(0, minsize=320)

        elif items == 2:
            layouts = [(0, 0, 1, 1), (1, 0, 1, 1)]
            mainframe.grid_rowconfigure(0, minsize=100)
            mainframe.grid_rowconfigure(1, minsize=100)
            mainframe.grid_columnconfigure(0, minsize=320)

        elif items == 3:
            layouts = [(0, 0, 1, 2), (1, 0, 1, 1), (1, 1, 1, 1)]
            mainframe.grid_rowconfigure(0, minsize=100)
            mainframe.grid_rowconfigure(1, minsize=100)
            mainframe.grid_columnconfigure(0, minsize=160)
            mainframe.grid_columnconfigure(1, minsize=160)

        elif items == 4:
            layouts = [(0, 0, 1, 1), (0, 1, 1, 1), (1, 0, 1, 1), (1, 1, 1, 1)]
            mainframe.grid_rowconfigure(0, minsize=100)
            mainframe.grid_rowconfigure(1, minsize=100)
            mainframe.grid_columnconfigure(0, minsize=160)
            mainframe.grid_columnconfigure(1, minsize=160)

        elif items == 5:
            layouts = [(0, 0, 1, 2), (0, 2, 1, 1), (1, 0, 1, 1), (1, 1, 1, 1), (1, 2, 1, 1)]
            mainframe.grid_rowconfigure(0, minsize=100)
            mainframe.grid_rowconfigure(1, minsize=100)
            mainframe.grid_columnconfigure(0, minsize=107)
            mainframe.grid_columnconfigure(1, minsize=106)
            mainframe.grid_columnconfigure(2, minsize=107)

        elif items == 6:
            layouts = [(0, 0, 1, 1), (0, 1, 1, 1), (0, 2, 1, 1), (1, 0, 1, 1), (1, 1, 1, 1), (1, 2, 1, 1)]
            mainframe.grid_rowconfigure(0, minsize=100)
            mainframe.grid_rowconfigure(1, minsize=100)
            mainframe.grid_columnconfigure(0, minsize=107)
            mainframe.grid_columnconfigure(1, minsize=106)
            mainframe.grid_columnconfigure(2, minsize=107)

        else:
            layouts = [(0, 0, 1, 1) for x in names]

        for i, (name, command, layout) in enumerate(zip(names, commands, layouts)):
            ttk.Button(mainframe, text=name, command=command) \
                .grid(row=layout[0], column=layout[1], rowspan=layout[2], columnspan=layout[3], sticky=(N, E, S, W))


menu = Menu(root, "Test Menu", ["Button 1", "Button 2"])


root.mainloop()