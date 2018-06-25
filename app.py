#!/usr/bin/env python

from view import App
from model import Model

app = App()
app.model = Model()
app.model.connect()
#app.mainloop()
