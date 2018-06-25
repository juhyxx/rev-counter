from serial import Serial, SerialException
import re
from tkinter import messagebox



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
        self.on_data_change(self._data)

    def data_append(self, newData):
        if  re.match("\d+,\d+", newData):
            self.inputData = self.inputData + newData + '\n'
            self._data = self.convert_data(self.inputData)
            self.on_data_change(self._data)

    @property
    def original_data(self):
        return self._originalData

    @original_data.setter
    def original_data(self, data):
        self._originalData = data;

    def on_data_change(self, data):
        print('Data changed, implement me')

    def update_ui(self):
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

    def read_serial(self):
        while(self.serial and self.serial.isOpen()):
            if (self.serial.inWaiting() > 0):
                line = self.serial.readline()
                print(line)
                try:
                    self.data_append(line.decode('utf-8').rstrip())
                except:
                    pass
            self.update_ui()

    def connect(self):
        try:
            self.serial = Serial(self.port, self.baudrate, timeout=0)
            self.read_serial()
        except SerialException as e:
            print(e)
            messagebox.showerror("Port /dev/ttyACM0 not found", "Connect Arduino first")

    def destroy(self):
        self.serial.close()