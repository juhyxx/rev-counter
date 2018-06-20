from tkinter import *
from tkinter import filedialog

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from matplotlib.figure import Figure


class App:
    title = "Rev counter"
    size = "700x500"
    fileType = (("csv", "*.csv"), ("all files", "*.*"))

    def set_title(self, title = ""):
        self.app.title(self.title + ' ' + title)

    def __init__(self, model):
        app = Tk()
        self.app = app
        self.win = PanedWindow()

        self._model = model
        self._model.onDataChange = self.dataChangeHandler;

        app.geometry(self.size)
        app.config(menu=self.generate_menu_bar(app))
        app.bind("<Control-q>", self.commandQuit)
        app.bind("<Control-w>", self.commandQuit)
        self.set_title()
        self.win.pack(fill=BOTH, expand=1)
        self.subplot = self.generate_chart(self.win)
        self._model.data = "1,289\n1,268\n2,300\n1,287"
        app.mainloop()

    def dataChangeHandler(self, data):
        self.draw_data(data)

    def draw_data(self, data):
        for val in data:
            self.subplot.plot(data[val]['x'], data[val]['y'], '-o')
        self.figure.canvas.draw_idle()

    def generate_chart(self, parent):
        figure = Figure(figsize=(4, 4), dpi=100)
        figure.set_facecolor("lightgoldenrodyellow")
        self.figure = figure

        subplot = figure.add_subplot(111)
        subplot.set_ylabel("Revs [rev/min]")

        canvas = FigureCanvasTkAgg(figure, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

        return subplot

    def generate_menu_bar(self, win):
        menubar = Menu(win)

        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self.command_open)
        filemenu.add_command(label="Save", command=self.command_save)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.commandQuit)
        menubar.add_cascade(label="File", menu=filemenu)

        serialmenu = Menu(menubar, tearoff=0)
        serialmenu.add_command(label="Connect", command=self.command_connect)
        serialmenu.add_command(label="Disconnect", command=self.command_save)
        serialmenu.add_command(label="Show log", command=self.command_save)
        menubar.add_cascade(label="Serial", menu=serialmenu)
        return menubar

    def command_open(self):
        filename = filedialog.askopenfilename(title="Open file", filetypes=self.fileType)
        if (filename):
            file = open(filename, 'r')
            self.set_title(filename)
            self._model.data = file.read()

    def command_save(self):
        filename = filedialog.asksaveasfilename(title="Save file", filetypes=self.fileType)
        if (filename):
            with open(filename, 'w') as file:
                file.write(self._model.originalData)
            self.set_title(filename + ' Saved')

    def command_connect(self):
        print('Connect')

    def commandQuit(self, event=None):
        self.app.destroy()