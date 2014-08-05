from tkinter import *
from tkinter import ttk

testing = True

def calculate(*args):
    try:
        value = float(feet.get())
        meters.set((0.3048 * value * 10000.0 + 0.5)/10000.0)
    except ValueError:
        pass
    
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
style.configure("TButton", background="#00ffff")
style.configure("TFrame", background="#ff0000")
style.configure("TLabel", background="#00ff00")
style.configure("Title.TLabel", background="#ffff00", font="helvetica 24", padding="10 0 0 0")

rootframe = ttk.Frame(root)
rootframe.grid(row=0, column=0)

rootframe.grid_columnconfigure(0, minsize=320)
rootframe.grid_rowconfigure(0, minsize=40)
rootframe.grid_rowconfigure(1, minsize=200)

titleframe = ttk.Frame(rootframe)
titleframe.grid(column=0, row=0, sticky=(N, E, W))
titleframe.columnconfigure(0, minsize=20)
titleframe.rowconfigure(0, minsize=40)
backimage = PhotoImage(file="back.gif")
ttk.Button(titleframe, image=backimage, command=quit).grid(row=0, column=0, sticky=(N, E, S, W))
ttk.Label(titleframe, text="Menu Title", style="Title.TLabel").grid(row=0, column=1, sticky="news")

mainframe = ttk.Frame(rootframe, padding="0")
mainframe.grid(column=0, row=1, sticky=(N, W, E, S))


feet = StringVar()
meters = StringVar()

feet_entry = ttk.Entry(mainframe, width=7, textvariable=feet)
feet_entry.grid(column=2, row=1, sticky=(W, E))

ttk.Label(mainframe, textvariable=meters).grid(column=2, row=2, sticky=(W, E))
ttk.Button(mainframe, text="Calculate", command=calculate).grid(column=3, row=3, sticky=W)

ttk.Label(mainframe, text="feet").grid(column=3, row=1, sticky=W)
ttk.Label(mainframe, text="is equivalent to").grid(column=1, row=2, sticky=E)
ttk.Label(mainframe, text="meters").grid(column=3, row=2, sticky=W)

for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

root.bind("<Key-Escape>", quit)

root.mainloop()