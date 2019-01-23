from tkinter import *
from os import system
from os.path import basename
from sys import exit, executable
from platform import system as platform_system

GUI_FONT = ('Arial', 32)
GUI_BOX_SIZE = 100
GUI_BOX_SPACING = 10
GUI_BOX_BORDER_WIDTH = 3
GUI_FRAME_INDEX = 0
GUI_DELAY = 200
GUI_COLOR_1 = '#f5f5dc'
GUI_COLOR_2 = '#e9e9af'
GUI_COLOR_3 = '#dddd88'
GUI_OUTLINE_1 = '#ff0000'
GUI_OUTLINE_2 = '#00ff00'
GUI_OUTLINE_3 = '#0000ff'
GUI_COLOR_GREEN = '#00bb00'
GUI_COLOR_RED = '#bb0000'
GUI_COLOR_BLACK = '#000000'
GUI_DASH = (5,4,5,3)

def gui_replay(master, canvas, item_matrix, solution, puzzle_size):
    global GUI_FRAME_INDEX

    numbers = solution[GUI_FRAME_INDEX]
    next_zero = None
    color_this = None
    if GUI_FRAME_INDEX + 1 < len(solution):
        next_zero = solution[GUI_FRAME_INDEX + 1].index(0)
        color_this = solution[GUI_FRAME_INDEX][next_zero]
    for y in range(puzzle_size):
        for x in range(puzzle_size):
            n = numbers[y+puzzle_size*x]
            BORDER_COLOR = None
            if n == solution[-1][y+puzzle_size*x]:
                BORDER_COLOR = GUI_COLOR_GREEN    #if number is in place, show green cell border
            else:
                BORDER_COLOR = GUI_COLOR_RED    #else red cell border

            if n == 0:
                canvas.itemconfig(item_matrix[y][x][0],
                        fill=GUI_COLOR_2,
                        outline=GUI_COLOR_2,
                        width=GUI_BOX_BORDER_WIDTH)
            elif n == color_this:
                canvas.itemconfig(item_matrix[y][x][0],
                        fill=GUI_COLOR_1,
                        outline=BORDER_COLOR,
                        width=GUI_BOX_BORDER_WIDTH)
            else:
                canvas.itemconfig(item_matrix[y][x][0],
                        fill=GUI_COLOR_1,
                        outline=BORDER_COLOR,
                        width=GUI_BOX_BORDER_WIDTH)

            s = str(n)
            if not n:
                s = ''
            canvas.itemconfig(item_matrix[y][x][1], text=s)

    GUI_FRAME_INDEX += 1
    if GUI_FRAME_INDEX >= len(solution):
        GUI_FRAME_INDEX = 0
    canvas.update()

    if GUI_FRAME_INDEX != 0:
        master.after(GUI_DELAY, gui_replay, master, canvas, item_matrix, solution, puzzle_size)

def gui_close(event):
    exit(0)

def gui_item_matrix(canvas, puzzle_size):
    item_matrix = [[[None, None] for x in range(puzzle_size)] for y in range(puzzle_size)]
    for y in range(puzzle_size):
        for x in range(puzzle_size):

            y0 = y * GUI_BOX_SIZE + GUI_BOX_SPACING
            x0 = x * GUI_BOX_SIZE + GUI_BOX_SPACING
            y1 = y0 + GUI_BOX_SIZE - GUI_BOX_SPACING
            x1 = x0 + GUI_BOX_SIZE - GUI_BOX_SPACING
            item_matrix[y][x][0] = canvas.create_rectangle(y0, x0, y1, x1, dash=GUI_DASH, fill=GUI_COLOR_1)

            yt = y0 + ((GUI_BOX_SIZE - GUI_BOX_SPACING) / 2)
            xt = x0 + ((GUI_BOX_SIZE - GUI_BOX_SPACING) / 2)
            item_matrix[y][x][1] = canvas.create_text((yt, xt), font=GUI_FONT, text='')

    return item_matrix

def visualizer(solution, puzzle_size):
    master = Tk()
    canvas_width = (GUI_BOX_SIZE * puzzle_size) + GUI_BOX_SPACING
    canvas_height = (GUI_BOX_SIZE * puzzle_size) + GUI_BOX_SPACING
    canvas = Canvas(master, width=canvas_width+1, height=canvas_height+1, bg=GUI_COLOR_2, borderwidth=0, highlightthickness=0)
    canvas.pack()
    item_matrix = gui_item_matrix(canvas, puzzle_size)
    master.bind('<Escape>', gui_close)
    master.bind('<Q>', gui_close)
    master.bind('<q>', gui_close)
    master.after(0, gui_replay, master, canvas, item_matrix, solution, puzzle_size)
    if platform_system() is 'Darwin':
        system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "''' + basename(executable)  + '''" to true' ''')
    master.mainloop()
