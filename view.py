import tkinter as tk
from tkinter import filedialog

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


class App(tk.Frame):
    title = "Rev counter"
    size = "700x500"
    fileType = (("csv", "*.csv"), ("all files", "*.*"))
    lines = {}

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, new_model):
        self._model = new_model
        self.model.onDataChange = self.draw_data
        self.model.updateUI = self.updateUI

    def updateUI(self):
        try:
            self.win.update()
        except:
            pass

    def set_title(self, title = ""):
        self.win.title(self.title + ' ' + title)

    def __init__(self,  *args, **kwargs):
        win = tk.Tk()
        tk.Frame.__init__(self, win, *args, **kwargs)

        self.win = win
        win.geometry(self.size)
        win.config(menu=self.generate_menu_bar(win))
        win.protocol("WM_DELETE_WINDOW", self.command_quit)
        win.bind("<Control-q>", self.command_quit)
        win.bind("<Control-w>", self.command_quit)
        self.set_title()
        self.generate_chart()

    def generate_chart(self):
        plt.ion()
        figure = Figure(figsize=(4, 4), dpi=100)
        figure.set_facecolor("lightgoldenrodyellow")

        axis = figure.add_subplot(111)
        axis.set_ylabel("Revs [rev/min]")

        canvas = FigureCanvasTkAgg(figure, master=self.win)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        canvas.draw()
        self.axis = axis
        self.canvas = canvas

    def draw_data(self, data):
        axis = self.axis
        range = {
            'xmin': 0,
            'xmax': 0,
            'ymin': 0,
            'ymax': 0
        }

        for sensor in data:
            try:
                line = self.lines[sensor]
            except:
                line, = axis.plot([],[], label=sensor)
                self.lines[sensor] = line
            x = data[sensor]['x']
            y = data[sensor]['y']
            line.set_data(x, y)
            try:
                range['xmin'] = min(min(x), range['xmin'])
                range['ymin'] = min(min(y), range['ymin'])
                range['xmax'] = max(max(x), range['xmax'])
                range['ymax'] = max(max(y), range['ymax'])
            except:
                range['xmin'] = 0
                range['ymin'] = 0
                range['xmax'] = 0
                range['ymax'] = 0
        axis.legend()

        axis.set_xlim(range['xmin'], range['xmax'])
        axis.set_ylim(range['ymin'], range['ymax'])

        try:
            self.canvas.draw()
        except:
            print('Bum')


    def generate_menu_bar(self, win):
        menubar = tk.Menu(win)

        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self.command_open)
        filemenu.add_command(label="Save", command=self.command_save)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.command_quit)
        menubar.add_cascade(label="File", menu=filemenu)

        serialmenu = tk.Menu(menubar, tearoff=0)
        serialmenu.add_command(label="Connect", command=self.command_connect)
        serialmenu.add_command(label="Disconnect",
                               command=self.command_disconnect)
        serialmenu.add_command(label="Show log", command=self.command_save)
        menubar.add_cascade(label="Serial", menu=serialmenu)
        return menubar

    def command_open(self):
        filename = filedialog.askopenfilename(title="Open file",
                                              filetypes=self.fileType)
        if filename:
            file = open(filename, 'r')
            self.set_title(filename)
            self.model.data = file.read()

    def command_save(self):
        filename = filedialog.asksaveasfilename(title="Save file",
                                                filetypes=self.fileType)
        if filename:
            with open(filename, 'w') as file:
                file.write(self.model.originalData)
            self.set_title(filename + ' Saved')

    def command_connect(self):
        print('Connect')

    def command_disconnect(self):
        self.model.disconnect()

    def command_quit(self, event=None):
        self.model.destroy()
        self.win.destroy()
