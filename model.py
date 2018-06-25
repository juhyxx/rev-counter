import serial
from multiprocessing import Pool
from multiprocessing import Process
import threading
import time


# python -m serial.tools.miniterm <port_name>

class Model:
    inputData = ''
    port = '/dev/ttyACM0'
    baudrate = 9600

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, newData):
        self.inputData = newData
        self._data = self.convert_data(self.inputData)
        self.onDataChange(self._data)

    def dataAppend(self, newData):
        self.inputData = self.inputData + newData + '\n'
        self._data = self.convert_data(self.inputData)
        self.onDataChange(self._data)

    @property
    def originalData(self):
        return self._originalData

    @originalData.setter
    def originalData(self, data):
        self._originalData = data;

    def onDataChange(self, data):
        print('Data changed, implement me')

    @staticmethod
    def convert_data(data):
        result = {}
        index = 0
        for value in data.split("\n"):
            if (value):
                val = value.split(",")
                try:
                    key = int(val[0])
                    item = result.get(key)
                    if (item is None):
                        result[key] = {"x": [], "y": []}
                        item = result.get(key)
                    item['y'].append(float(val[1]))
                    item['x'].append(index)
                    index += 1
                except:
                    print('Ouups:', value)
        return result

    def readSerial(self):
        t = threading.currentThread()
        while getattr(t, "do_run", True):
            with serial.Serial(self.port, self.baudrate, timeout=1) as ser:
                while(True):
                    line = ser.readline()
                    self.dataAppend(line.decode('utf-8').rstrip())

    def connect(self):
        self.t = threading.Thread(target=self.readSerial, name="SerialReader")
        self.t.do_run = True
        self.t.start()

    def destroy(self):
        self.t.do_run = False
        #time.sleep(5)
        self.t.join()
