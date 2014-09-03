import platform
from tkinter import *
from tkinter import ttk

# Check if running on linux (Raspberry Pi) or otherwise just testing
if platform.system() == "Linux":
    testing = False
else:
    testing = True

# Create TK object
root = Tk()
# Hide window decorations
root.overrideredirect(True)

# Set window size and position
if testing:
    # Testing machine - window in middle of screen
    root.geometry("320x240+450+350")
else:
    # Pi - window in top left (fills screen)
    root.geometry("320x240+0+0")
    # Hide cursor on touchscreen
    root.config(cursor="none")

# Create full screen quit button
ttk.Button(root, text="Quit", command=quit).grid(row=0, column=0, sticky=(N, E, S, W))

# Set the theme for TTK
style = ttk.Style()
style.theme_use("default")

# Set some colours
bg = style.lookup("TButton", "background")  # Background
hv = "gray95"  # Hover
pr = "white"  # Press

# Set styles
style.configure('.', font=('Helvetica', 12))
style.configure("Title.TLabel", font="Helvetica 24", padding="10 0 0 0")  # Title font


class Menu(ttk.Frame):
    def __init__(self, master=None, mode=None, *args):
        """
        Create a menu object.

        Modes:  None - button grid menu
                move - six button movement menu

        :param master:  TK root object
        :param mode:    type of menu to create
        :param args:
        """
        # Create the master frame for layout
        ttk.Frame.__init__(self, master)
        self.grid(row=0, column=0)
        # Split into two rows
        self.grid_columnconfigure(0, minsize=320)
        # Title row is 40px high
        self.grid_rowconfigure(0, minsize=40)
        # Main row is 200px high
        self.grid_rowconfigure(1, minsize=200)
        # Bind escape key to quit program
        self.bind("<Key-Escape>", quit)

        # Generate the menu contents
        if mode == "move":
            self.create_move(*args)
        else:
            self.create(*args)

        # Hide the menu
        self.lower()
    # End of function __init__()


    def title(self, title="Menu"):
        # Menu title bar
        """
        Create title bar

        :param title:   title of menu
        """
        # Create frame for title contents
        titleframe = ttk.Frame(self)
        titleframe.grid(column=0, row=0, sticky=(N, E, W))
        titleframe.columnconfigure(0, minsize=20)
        titleframe.rowconfigure(0, minsize=40)

        # Create back button
        self.backimage = PhotoImage(file="back.gif")
        ttk.Button(titleframe, image=self.backimage, command=self.lower).grid(row=0, column=0, sticky=(N, E, S, W))

        # Create title
        ttk.Label(titleframe, text=title, style="Title.TLabel").grid(row=0, column=1, sticky=(N, E, S, W))
    # End of function title()


    def create(self, title="Menu", names=[], commands=[]):
        """
        Generate button grid menu contents

        :param title:       title of menu
        :param names:       names of buttons
        :param commands:    commands to execute on each button press
        """

        # Create title bar
        self.title(title)

        # Menu content
        mainframe = ttk.Frame(self, padding="0")
        mainframe.grid(column=0, row=1, sticky=(N, W, E, S))

        # If there are no button names specified, make 4 numbered buttons
        if len(names) == 0:
            names = list("Button " + str(x + 1) for x in range(4))

        # If there are less commands than names, pad them out with None
        while len(commands) < len(names):
            commands.append(None)

        # Generate layout according to number of items in menu
        items = len(names)
        # One large button
        if items == 1:
            layouts = [(0, 0, 1, 1)]
            mainframe.grid_rowconfigure(0, minsize=200)
            mainframe.grid_columnconfigure(0, minsize=320)
        # Two buttons, on top of each other
        elif items == 2:
            layouts = [(0, 0, 1, 1), (1, 0, 1, 1)]
            mainframe.grid_rowconfigure(0, minsize=100)
            mainframe.grid_rowconfigure(1, minsize=100)
            mainframe.grid_columnconfigure(0, minsize=320)
        # Three buttons, one large on top with two underneath
        elif items == 3:
            layouts = [(0, 0, 1, 2), (1, 0, 1, 1), (1, 1, 1, 1)]
            mainframe.grid_rowconfigure(0, minsize=100)
            mainframe.grid_rowconfigure(1, minsize=100)
            mainframe.grid_columnconfigure(0, minsize=160)
            mainframe.grid_columnconfigure(1, minsize=160)
        # Four buttons, in 2x2 grid
        elif items == 4:
            layouts = [(0, 0, 1, 1), (0, 1, 1, 1), (1, 0, 1, 1), (1, 1, 1, 1)]
            mainframe.grid_rowconfigure(0, minsize=100)
            mainframe.grid_rowconfigure(1, minsize=100)
            mainframe.grid_columnconfigure(0, minsize=160)
            mainframe.grid_columnconfigure(1, minsize=160)
        # Five buttons, first double width, on 3x2 grid
        elif items == 5:
            layouts = [(0, 0, 1, 2), (0, 2, 1, 1), (1, 0, 1, 1), (1, 1, 1, 1), (1, 2, 1, 1)]
            mainframe.grid_rowconfigure(0, minsize=100)
            mainframe.grid_rowconfigure(1, minsize=100)
            mainframe.grid_columnconfigure(0, minsize=107)
            mainframe.grid_columnconfigure(1, minsize=106)
            mainframe.grid_columnconfigure(2, minsize=107)
        # Six buttons, on 3x2 grid
        elif items == 6:
            layouts = [(0, 0, 1, 1), (0, 1, 1, 1), (0, 2, 1, 1), (1, 0, 1, 1), (1, 1, 1, 1), (1, 2, 1, 1)]
            mainframe.grid_rowconfigure(0, minsize=100)
            mainframe.grid_rowconfigure(1, minsize=100)
            mainframe.grid_columnconfigure(0, minsize=107)
            mainframe.grid_columnconfigure(1, minsize=106)
            mainframe.grid_columnconfigure(2, minsize=107)
        # Otherwise, all in one grid space
        else:
            layouts = [(0, 0, 1, 1) for x in names]

        # Create buttons according to layout
        for i, (name, command, layout) in enumerate(zip(names, commands, layouts)):
            ttk.Button(mainframe, text=name, command=command) \
                .grid(row=layout[0], column=layout[1], rowspan=layout[2], columnspan=layout[3], sticky=(N, E, S, W))
    # End of function create()


    def create_move(self, title="Movment", commands=[]):
        """
        Create six button movement menu

        :param title:       menu title
        :param commands:    commands for each button
        """

        # Create menu bar
        self.title(title)

        # Main Frame
        mainframe = ttk.Frame(self, padding="0")
        mainframe.grid(column=0, row=1, sticky=(N, W, E, S), padx=0, pady=0)

        # Dimensions of canvas
        width = 316
        height = 196
        pad = 3
        edge = 5

        # Canvas for the buttons
        canvas = Canvas(mainframe, width=width, height=height, bd=0, relief=FLAT)
        canvas.grid(column=0, row=0)

        # Lists of buttons
        button = [0, 0, 0, 0, 0, 0]
        tag = ["+X", "-X", "+Y", "-Y", "+Z", "-Z"]

        # Middle
        button[4] = canvas.create_polygon(width * (1 / 6) + pad, edge, width * (5 / 6) - pad, edge, width / 2,
                                          height / 2 - pad)  # +Z
        button[5] = canvas.create_polygon(width * (1 / 6) + pad, height - edge, width * (5 / 6) - pad, height - edge,
                                          width / 2, height / 2 + pad)  # -Z

        # Left Side
        button[1] = canvas.create_polygon(edge, edge, width * (1 / 6) - pad, edge, width / 2 - pad,
                                          height / 2 - pad / 2, edge, height / 2 - pad / 2)  # -X
        button[3] = canvas.create_polygon(edge, height - edge, width * (1 / 6) - pad, height - edge, width / 2 - pad,
                                          height / 2 + pad / 2, edge, height / 2 + pad / 2)  # -Y

        # Right Side
        button[2] = canvas.create_polygon(width - edge, edge, width * (5 / 6) + pad, edge, width / 2 + pad,
                                          height / 2 - pad / 2, width - edge, height / 2 - pad / 2)  # +Y
        button[0] = canvas.create_polygon(width - edge, height - edge, width * (5 / 6) + pad, height - edge,
                                          width / 2 + pad, height / 2 + pad / 2, width - edge,
                                          height / 2 + pad / 2)  # +X

        # Set properties of buttons
        for i, b in enumerate(button):
            canvas.itemconfig(b, fill=bg, outline="black", activefill=hv, tags=tag[i])

        # Create labels
        font = "Helvetica 20"
        # X labels
        canvas.create_text(width * 4 / 5, height * 2 / 3, text="+X", anchor=W, font=font)
        canvas.create_text(width * 1 / 5, height * 1 / 3, text="-X", anchor=E, font=font)
        # Y labels
        canvas.create_text(width * 4 / 5, height * 1 / 3, text="+Y", anchor=W, font=font)
        canvas.create_text(width * 1 / 5, height * 2 / 3, text="-Y", anchor=E, font=font)
        # Z labels
        canvas.create_text(width * 1 / 2, height * 1 / 4, text="+Z", anchor=S, font=font)
        canvas.create_text(width * 1 / 2, height * 3 / 4, text="-Z", anchor=N, font=font)

        # Pressed effects
        def press(item, name, command):
            # Change the colour
            canvas.itemconfig(item, activefill=pr)
            # Execute the action
            command()

        # Unpress effects
        def unpress(item, name, command):
            # Change the colour
            canvas.itemconfig(item, activefill=hv)

        # Add press functionality to each button
        for t, b, c in zip(tag, button, commands):
            # Bind the press effects
            canvas.tag_bind(t, "<ButtonPress-1>", lambda event, item=b, name=t, command=c: press(item, name, command))
            # Bind the unpress effects
            canvas.tag_bind(t, "<ButtonRelease-1>",
                            lambda event, item=b, name=t, command=c: unpress(item, name, command))
    # End of function create_move()


# Create all the menus:
# Movement menu
movemenu = Menu(root, "move", "Move Axes",
                [lambda: print("0"), lambda: print("1"), lambda: print("2"), lambda: print("3"), lambda: print("4"),
                 lambda: print("5")])
# Printing menu
printmenu = Menu(root, None, "Print", ["From USB", "From Network", "Test Part"])
# Manual control menu
manualmenu = Menu(root, None, "Manual Control", ["Home", "Move Axes", "Extruders", "Temperatures"],
                  [None, movemenu.lift, None, None])
# Calibration menu
calibrationmenu = Menu(root, None, "Calibration", ["Level Bed", "Material Selection", "Extruder Offset", "Bed Depth"])
# Servicing menu
servicingmenu = Menu(root, None, "Servicing", ["Change Filament", "Test Routines", "Software Update", "Shutdown"],
                     [None, None, None, quit])
# Main menu
mainmenu = Menu(root, None, "Main Menu", ["Print", "Manual Control", "Calibration", "Servicing"],
                [printmenu.lift, manualmenu.lift, calibrationmenu.lift, servicingmenu.lift])

# Raise the main menu
mainmenu.lift()
# Run the main loop
root.mainloop()