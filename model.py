import serial

class Model:
    inputData = ''

    @property
    def data(self, data):
        return self._data

    @data.setter
    def data(self, newData):
        self.inputData = newData;
        self._data = self.convert_data(newData)
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

    def connect(self ):
        # python -m serial.tools.miniterm <port_name>
        with serial.Serial('/dev/ttyS4', 9600, timeout=1) as ser:
            line = ser.readline()  # read a '\n' terminated line
            print(line)
