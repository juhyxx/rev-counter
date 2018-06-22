#!/usr/bin/env python

from view import *
from model import *

app = App()
app.model = Model()
app.model.connect()
app.mainloop()