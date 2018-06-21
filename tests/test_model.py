from unittest import TestCase

from model import *


class TestModel(TestCase):

    def test_convert_data(self):
        model = Model()
        data = model.convert_data('1,1\n2,2')
        self.assertEquals(data, {1: {'y': [1.0], 'x': [0]}, 2: {'y': [2.0], 'x': [1]}})

        data = model.convert_data('1,1')
        self.assertEquals(data, {1: {'x': [0], 'y': [1.0]}})

        data = model.convert_data('1,1\n')
        self.assertEquals(data, {1: {'x': [0], 'y': [1.0]}})