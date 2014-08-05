from tkinter import *
from tkinter import ttk

def calculate(*args):
    try:
        value = float(feet.get())
        meters.set((0.3048 * value * 10000.0 + 0.5)/10000.0)
    except ValueError:
        pass
    
root = Tk()
#root.overrideredirect(True)

style = ttk.Style()
style.theme_use("clam")
style.configure('TButton', foreground='#334353')
style.configure('TFrame', background='#334353')

root.title("Feet to Meters")
root.geometry("320x240+450+350")
root.grid_columnconfigure(0, minsize=320)
root.grid_rowconfigure(0, minsize=40)
root.grid_rowconfigure(1, minsize=200)

titleframe = ttk.Frame(root)
titleframe.grid(column=0, row=0, sticky=(N, E, W))
titleframe.columnconfigure(0, minsize=20)
titleframe.rowconfigure(0, minsize=40)
backimage = PhotoImage(file="back.png")
ttk.Button(titleframe, image=backimage, command=quit).grid(row=0, column=0)
ttk.Label(titleframe, text="Menu Title").grid(row=0, column=1, sticky=(N, E, S, W))

mainframe = ttk.Frame(root, padding="0")
mainframe.grid(column=0, row=1, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

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

root.bind('<Key-Escape>', quit)

root.mainloop()