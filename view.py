from tkinter import *
from tkinter import filedialog

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from matplotlib.figure import Figure
from matplotlib import pyplot


class App:
    title = "Rev counter"
    size = "700x500"
    fileType = (("csv", "*.csv"), ("all files", "*.*"))

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, newModel):
        self._model = newModel
        self.model.onDataChange = self.dataChangeHandler

    @model.deleter
    def model(self):
        self._model.destroy()
        del self._model

    def set_title(self, title = ""):
        self.app.title(self.title + ' ' + title)

    def __init__(self, model):
        app = Tk()
        self.app = app
        self.win = PanedWindow()
        app.protocol("WM_DELETE_WINDOW", self.command_quit)

        pyplot.ion()

        self.model = model
        app.geometry(self.size)
        app.config(menu=self.generate_menu_bar(app))
        app.bind("<Control-q>", self.command_quit)
        app.bind("<Control-w>", self.command_quit)
        self.set_title()
        self.win.pack(fill=BOTH, expand=1)

        figure = Figure(figsize=(4, 4), dpi=100)
        figure.set_facecolor("lightgoldenrodyellow")

        subplot = figure.add_subplot(111)
        subplot.set_ylabel("Revs [rev/min]")

        canvas = FigureCanvasTkAgg(figure, master=self.win)
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

        canvas.draw()
        self.canvas = canvas
        self.figure = figure
        self.subplot = subplot
        self.model.data = "1,3\n1,3\n2,3\n1,1\n"
        self.model.connect()
        app.mainloop()

    def dataChangeHandler(self, data):
        self.draw_data(data)

    def draw_data(self, data):
        print("draw_data", data)
        for val in data:
            plot = self.subplot.plot(data[val]['x'], data[val]['y'], '-o')

        self.figure.canvas.draw_idle()
        #self.canvas.draw()

    def generate_menu_bar(self, win):
        menubar = Menu(win)

        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self.command_open)
        filemenu.add_command(label="Save", command=self.command_save)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.command_quit)
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
            self.model.data = file.read()

    def command_save(self):
        filename = filedialog.asksaveasfilename(title="Save file", filetypes=self.fileType)
        if (filename):
            with open(filename, 'w') as file:
                file.write(self.model.originalData)
            self.set_title(filename + ' Saved')

    def command_connect(self):
        print('Connect')

    def command_quit(self, event=None):
        del self.model
        self.app.destroy()