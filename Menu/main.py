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

# Set the theme for TTK
style = ttk.Style()
style.theme_use("default")

# Check some colours
bg = style.lookup("TButton", "background")
hv = "gray95"

style.configure('.', font=('Helvetica', 12))
#style.configure("TButton", background=bg)
# style.configure("TFrame", background="#ff0000")
# style.configure("TLabel", background="#00ff00")
style.configure("Title.TLabel", font="Helvetica 24", padding="10 0 0 0")


class Menu(ttk.Frame):
    def __init__(self, master=None, mode=None, *args):
        ttk.Frame.__init__(self, master)
        self.grid(row=0, column=0)
        self.grid_columnconfigure(0, minsize=320)
        self.grid_rowconfigure(0, minsize=40)
        self.grid_rowconfigure(1, minsize=200)
        self.bind("<Key-Escape>", quit)

        if mode == "move":
            self.create_move(*args)
        else:
            self.create(*args)
        self.lower()

    def title(self, title="Menu"):
        # Menu title bar
        titleframe = ttk.Frame(self)
        titleframe.grid(column=0, row=0, sticky=(N, E, W))
        titleframe.columnconfigure(0, minsize=20)
        titleframe.rowconfigure(0, minsize=40)

        self.backimage = PhotoImage(file="back.gif")
        ttk.Button(titleframe, image=self.backimage, command=self.lower).grid(row=0, column=0, sticky=(N, E, S, W))

        ttk.Label(titleframe, text=title, style="Title.TLabel").grid(row=0, column=1, sticky=(N, E, S, W))


    def create(self, title="Menu", names=[], commands=[]):

        self.title(title)

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


    def create_move(self, title="Movment", commands=[]):
        self.title(title)

        # Main Frame
        mainframe = ttk.Frame(self, padding="0")
        mainframe.grid(column=0, row=1, sticky=(N, W, E, S), padx=0, pady=0)

        width = 316
        height = 196
        pad = 3
        edge = 5

        # Canvas for the buttons
        canvas = Canvas(mainframe, width=width, height=height, bd=0, relief=FLAT)
        canvas.grid(column=0, row=0)

        # Middle
        up =   canvas.create_polygon(width*(1/6)+pad, edge,        width*(5/6)-pad, edge,        width/2, height/2-pad, fill=bg, outline="black", activefill=hv)
        down = canvas.create_polygon(width*(1/6)+pad, height-edge, width*(5/6)-pad, height-edge, width/2, height/2+pad, fill=bg, outline="black", activefill=hv)

        # Left Side
        left = canvas.create_polygon(edge, edge,        width*(1/6)-pad, edge,        width/2-pad, height/2-pad/2, edge, height/2-pad/2, fill=bg, outline="black", activefill=hv)
        back = canvas.create_polygon(edge, height-edge, width*(1/6)-pad, height-edge, width/2-pad, height/2+pad/2, edge, height/2+pad/2, fill=bg, outline="black", activefill=hv)

        # Right Side
        forward = canvas.create_polygon(width-edge, edge,        width*(5/6)+pad, edge,        width/2+pad, height/2-pad/2, width-edge, height/2-pad/2, fill=bg, outline="black", activefill=hv)
        right =   canvas.create_polygon(width-edge, height-edge, width*(5/6)+pad, height-edge, width/2+pad, height/2+pad/2, width-edge, height/2+pad/2, fill=bg, outline="black", activefill=hv)

        # Labels
        font = "Helvetica 20"

        canvas.create_text(width*4/5, height*2/3, text="+X", anchor=W, font=font)
        canvas.create_text(width*1/5, height*1/3, text="-X", anchor=E, font=font)

        canvas.create_text(width*4/5, height*1/3, text="+Y", anchor=W, font=font)
        canvas.create_text(width*1/5, height*2/3, text="-Y", anchor=E, font=font)

        canvas.create_text(width*1/2, height*1/4, text="+Z", anchor=S, font=font)
        canvas.create_text(width*1/2, height*3/4, text="-Z", anchor=N, font=font)

        #Canvas(mainframe, width=10, height=10).grid(column=0, row=1)


movemenu = Menu(root, "move", "Move Axes", [])

printmenu = Menu(root, None, "Print", ["From USB", "From Network", "Test Part"])
manualmenu = Menu(root, None, "Manual Control", ["Home", "Move Axes", "Extruders", "Temperatures"], [None, movemenu.lift, None, None])
calibrationmenu = Menu(root, None, "Calibration", ["Level Bed", "Material Selection", "Extruder Offset", "Bed Depth"])
servicingmenu = Menu(root, None, "Servicing", ["Change Filament", "Test Routines", "Software Update", "Shutdown"], [None, None, None, quit])
mainmenu = Menu(root, None, "Main Menu", ["Print", "Manual Control", "Calibration", "Servicing"], [printmenu.lift, manualmenu.lift, calibrationmenu.lift, servicingmenu.lift])



mainmenu.lift()
root.mainloop()