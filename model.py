import serial
import re

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
        if  re.match("\d+,\d+", newData):
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

    def updateUI(self):
        print('free for update')

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
                except Exception as e:
                    print('Ouups:', value)
                    print(e)
        return result

    def readSerial(self):
        while(self.serial.isOpen()):
            if (self.serial.inWaiting() > 0):
                line = self.serial.readline()
                print(line)
                try:
                    self.dataAppend(line.decode('utf-8').rstrip())
                except:
                    pass
            self.updateUI()

    def connect(self):
        self.serial = serial.Serial(self.port, self.baudrate, timeout=0)
        self.readSerial()

    def destroy(self):
        self.serial.close()