from tkinter import *

# Defaults
scale = 40              # 40 for 2cm, 5 for 15cm
margin = 10             # Margin between plot and window border


def graph(title="", scale=scale):
    """
    Creates a graph window

    @return:    graph canvas
    """

    # Create TK environment
    root = Tk()
    root.title("Plot: {}".format(title))
    root.attributes('-alpha', 0.8)
    root.geometry('+10+10')

    # Bind escape to close window
    def close(*args):
        root.destroy()
    root.bind("<Key-Escape>", close)

    # Create canvas for drawing on
    canvas = Canvas(root, width=820, height=820, bg="white")
    canvas.pack()

    # Create the grid and axes ticks
    for i in range(int(800 / scale) + 1):
        # Grid
        canvas.create_line(i * scale + 10, 10, i * scale + 10, 810, width=1, fill="gray85")
        canvas.create_line(10, i * scale + 10, 810, i * scale + 10, width=1, fill="gray85")

        # Ticks
        canvas.create_line(5, i * scale + 10, 10, i * scale + 10, width=1, fill="gray")
        canvas.create_line(i * scale + 10, 810, i * scale + 10, 815, width=1, fill="gray")

    # Create axes lines
    canvas.create_line(10, 5, 10, 815, width=1, fill="gray")
    canvas.create_line(5, 810, 815, 810, width=1, fill="gray")

    return canvas
# End of function graph()


def plot(canvas, linelist, trace="black", marker="", radius=0, numbers=False, arrow=None, scale=scale):
    """
    Plot the lines on the specified canvas

    :param numbers:     True/False - print numbers offset by the line normal
    :param arrow:       None/LAST - print arrows pointing toward the last point
    :param scale:       800/limits
    @param canvas:      canvas to draw on
    @param linelist:    list of lines
    @param radius:      radius of markers
    @param trace:       colour of trace
    @param marker:      colour of marker
    @return:            none
    """

    # Plot each line
    for i, line in enumerate(linelist):
        # Scale the coordinates
        x = (scale * line[1][0] + margin, scale * line[2][0] + margin)
        y = (800 - scale * line[1][1] + margin, 800 - scale * line[2][1] + margin)

        # Start markers
        fill = ""
        outline = marker
        # If at first point, fill marker in green and outline in green
        if i == 0:
            outline = "green"
            fill = "green"
        # Draw the marker
        canvas.create_oval(x[0] - radius, y[0] - radius, x[0] + radius, y[0] + radius, width=1, fill=fill,
                           outline=outline)

        # End marker
        outline = marker
        # If at last point, outline in red
        if line == linelist[-1]:
            outline = "red"
        # Draw the marker
        canvas.create_oval(x[1] - radius, y[1] - radius, x[1] + radius, y[1] + radius, width=1, fill="",
                           outline=outline)

        # Traces
        # If trace colour starts with -- make trace dashed
        if trace.startswith("--"):
            fill = trace
            fill = fill.strip("-")
            # Create a dashed trace
            canvas.create_line(x[0], y[0], x[1], y[1], width=1, fill=fill, dash=1)
        else:
            # Create solid trace
            canvas.create_line(x[0], y[0], x[1], y[1], width=1, fill=trace, arrow=arrow)

        # If numbers are to be drawn
        if numbers:
            # Generate default coordinates for lines with no normal
            if not line[0]:
                line[0] = [0, 0]
                pass
            try:
                # Try to draw number at normal position
                canvas.create_text((x[0] + x[1]) / 2 + (line[0][0] * 10), (y[0] + y[1]) / 2 - (line[0][1] * 10), text=i,
                                   font="Helvetica 8")
            except:
                # The normal coordinates were not right
                # print("Problem with", i)
                pass
    return
# End of function plot()


def points(canvas, linelist, radius=4, marker="blue", scale=scale):
    """
    Draw points at the start and end point of each line

    :param canvas:      canvas to draw on
    :param linelist:    list of lines to draw
    :param radius:      radius of vertex markers
    :param marker:      colour of vertex markers
    :param scale:       scale of graph
    :return:            none
    """

    # Plot markers for each line
    for i, line in enumerate(linelist):
        # Scale the coordinates
        x = (scale * line[1][0] + margin, scale * line[2][0] + margin)
        y = (800 - scale * line[1][1] + margin, 800 - scale * line[2][1] + margin)

        # Draw the start marker
        canvas.create_oval(x[0] - radius, y[0] - radius, x[0] + radius, y[0] + radius, width=1, fill="",
                           outline=marker)
        # Draw the end marker
        canvas.create_oval(x[1] - radius, y[1] - radius, x[1] + radius, y[1] + radius, width=1, fill="",
                           outline=marker)
    return
# End of function points()