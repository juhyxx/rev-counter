import serial
from multiprocessing import Pool
from multiprocessing import Process

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
        self.inputData = self.inputData + newData
        self._data = self.convert_data(self.inputData)
        print(self._data)
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
                key = int(val[0])
                item = result.get(key)
                if (item is None):
                    result[key] = {"x": [], "y": []}
                    item = result.get(key)
                item['y'].append(float(val[1]))
                item['x'].append(index)
                index += 1
        return result

    def readSerial(self):
        with serial.Serial(self.port, self.baudrate, timeout=1) as ser:
            while(1):
                line = ser.readline()
                self.dataAppend(line.decode('utf-8').replace(r"\r\n", r"\n"))

    def connect(self):
        self.process = Process(target=self.readSerial)
        self.process.start()

    def destroy(self):
        self.process.terminate()