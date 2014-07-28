from tkinter import *


def graph(title=""):
    """
    Creates a graph window

    @return:    graph canvas
    """
    scale = 40

    root = Tk()
    root.title("Plot: {}".format(title))
    root.attributes('-alpha', 0.8)
    root.geometry('+10+10')

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


def plot(canvas, linelist, radius=4, trace="black", marker="blue"):
    """
    Plot the lines on the specified canvas

    @param canvas:      canvas to draw on
    @param linelist:    list of lines
    @param radius:      radius of markers
    @param trace:       colour of trace
    @param marker:      colour of marker
    @return:            none
    """
    scale = 40
    margin = 10

    for i, line in enumerate(linelist):
        x = (scale * line[1][0] + margin, scale * line[2][0] + margin)
        y = (800 - scale * line[1][1] + margin, 800 - scale * line[2][1] + margin)

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

        canvas.create_line(x[0], y[0], x[1], y[1], width=1, fill=trace, dash=1)
    return
# End of function plot()


def points(canvas, linelist, radius=4, marker="blue"):
    scale = 40
    margin = 10

    print("Plotting:", [[x, y] for (n, x, y) in linelist])
    for i, line in enumerate(linelist):
        x = (scale * line[1][0] + margin, scale * line[2][0] + margin)
        y = (800 - scale * line[1][1] + margin, 800 - scale * line[2][1] + margin)

        canvas.create_oval(x[0] - radius, y[0] - radius, x[0] + radius, y[0] + radius, width=1, fill="",
                           outline=marker)

        canvas.create_oval(x[1] - radius, y[1] - radius, x[1] + radius, y[1] + radius, width=1, fill="",
                           outline=marker)

    return