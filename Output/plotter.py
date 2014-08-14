from decimal import Decimal
from tkinter import *

scale = 40  # 40 for 2cm, 5 for 15cm
margin = 10
window = Decimal(0)


def graph(title="", scale=scale):
    """
    Creates a graph window

    @return:    graph canvas
    """

    root = Tk()
    root.title("Plot: {}".format(title))
    root.attributes('-alpha', 0.8)
    root.geometry('+10+10')

    def close(*args):
        root.destroy()

    root.bind("<Key-Escape>", close)

    canvas = Canvas(root, width=820, height=820, bg="white")
    canvas.pack()

    for i in range(int(800 / scale) + 1):
        canvas.create_line(i * scale + 10, 10, i * scale + 10, 810, width=1, fill="gray85")
        canvas.create_line(10, i * scale + 10, 810, i * scale + 10, width=1, fill="gray85")

        canvas.create_line(5, i * scale + 10, 10, i * scale + 10, width=1, fill="gray")
        canvas.create_line(i * scale + 10, 810, i * scale + 10, 815, width=1, fill="gray")

    canvas.create_line(10, 5, 10, 815, width=1, fill="gray")
    canvas.create_line(5, 810, 815, 810, width=1, fill="gray")

    return canvas


# End of function graph()


def plot(canvas, linelist, trace="black", marker="", radius=0, numbers=False, arrow=none, scale=scale):
    """
    Plot the lines on the specified canvas

    :param numbers:     True/False - print numbers offset by the line normal
    :param arrow:       None/LAST - print arrows pointing toward the last point
    :param scale:
    @param canvas:      canvas to draw on
    @param linelist:    list of lines
    @param radius:      radius of markers
    @param trace:       colour of trace
    @param marker:      colour of marker
    @return:            none
    """

    for i, line in enumerate(linelist):
        x = (scale * line[1][0] + margin + ((window) * 800), scale * line[2][0] + margin + ((window) * 800))
        y = (
            800 - scale * line[1][1] + margin + ((-window) * 800), 800 - scale * line[2][1] + margin + ((-window) * 800))

        fill = ""

        outline = marker
        if i == 0:
            outline = "green"
            fill = "green"

        canvas.create_oval(x[0] - radius, y[0] - radius, x[0] + radius, y[0] + radius, width=1, fill=fill,
                           outline=outline)

        outline = marker
        if line == linelist[-1]:
            outline = "red"

        canvas.create_oval(x[1] - radius, y[1] - radius, x[1] + radius, y[1] + radius, width=1, fill="",
                           outline=outline)
        if trace.startswith("--"):
            fill = trace
            fill = fill.strip("-")
            canvas.create_line(x[0], y[0], x[1], y[1], width=1, fill=fill, dash=1)
        else:
            canvas.create_line(x[0], y[0], x[1], y[1], width=1, fill=trace, arrow=arrow)

        if numbers:
            if not line[0]:
                line[0] = [0, 0]
                pass
            try:
                canvas.create_text((x[0] + x[1]) / 2 + (line[0][0] * 10), (y[0] + y[1]) / 2 - (line[0][1] * 10), text=i,
                                   font="Helvetica 5")
            except:
                # print("Problem with", i)
                pass
    return


# End of function plot()


def points(canvas, linelist, radius=4, marker="blue", scale=scale):
    scale = 40
    margin = 10

    print("Plotting:", [[x, y] for (n, x, y) in linelist])
    for i, line in enumerate(linelist):
        x = (scale * line[1][0] + margin + ((1 - window) * 800), scale * line[2][0] + margin + ((1 - window) * 800))
        y = (800 - scale * line[1][1] + margin + ((window) * 800), 800 - scale * line[2][1] + margin + ((window) * 800))

        canvas.create_oval(x[0] - radius, y[0] - radius, x[0] + radius, y[0] + radius, width=1, fill="",
                           outline=marker)

        canvas.create_oval(x[1] - radius, y[1] - radius, x[1] + radius, y[1] + radius, width=1, fill="",
                           outline=marker)

    return